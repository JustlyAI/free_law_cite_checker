#!/usr/bin/env python3
"""
CourtListener Citation Check - Core functionality

A minimal script that checks legal citations using the CourtListener API.
Returns structured data for the command to format and present.
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import IntEnum

# Try to load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Constants
COURTLISTENER_BASE_URL = "https://www.courtlistener.com/api/rest/v4/citation-lookup/"
MAX_TEXT_LENGTH = 64000
REQUEST_TIMEOUT = (5, 30)  # (connection, read) timeouts in seconds


class CitationStatus(IntEnum):
    """HTTP-style status codes for citation lookup results."""

    FOUND = 200
    NOT_FOUND = 404
    INVALID = 400
    MULTIPLE_MATCHES = 300
    TOO_MANY_CITATIONS = 429


@dataclass
class Citation:
    """Represents a parsed citation result."""

    citation: str
    normalized_citations: List[str]
    start_index: Optional[int] = None
    end_index: Optional[int] = None
    status: int = CitationStatus.FOUND
    error_message: Optional[str] = None
    clusters: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.status == CitationStatus.FOUND

    @property
    def case_name(self) -> Optional[str]:
        if self.clusters:
            return self.clusters[0].get("case_name")
        return None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Citation":
        return cls(
            citation=data.get("citation", ""),
            normalized_citations=data.get("normalized_citations", []),
            start_index=data.get("start_index"),
            end_index=data.get("end_index"),
            status=data.get("status", CitationStatus.FOUND),
            error_message=data.get("error_message"),
            clusters=data.get("clusters", []),
        )


class CitationLookupClient:
    """Client for the CourtListener Citation Lookup API."""

    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.environ.get("COURTLISTENER_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "API token required. Set COURTLISTENER_API_TOKEN environment variable."
            )

        self.headers = {"Authorization": f"Token {self.api_token}"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _handle_response(self, response: requests.Response) -> List[Dict[str, Any]]:
        if response.status_code == 401:
            raise Exception("Invalid API token")
        if response.status_code == 429:
            raise Exception("API rate limit exceeded")

        response.raise_for_status()
        return response.json()

    def lookup_text(self, text: str) -> List[Citation]:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        if len(text) > MAX_TEXT_LENGTH:
            raise ValueError(
                f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters"
            )

        response = self.session.post(
            COURTLISTENER_BASE_URL, data={"text": text}, timeout=REQUEST_TIMEOUT
        )
        results = self._handle_response(response)
        return [Citation.from_dict(result) for result in results]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


def validate_file_path(file_path: str) -> Path:
    """
    Validate file path to prevent directory traversal attacks.

    Args:
        file_path: The file path to validate

    Returns:
        Resolved Path object

    Raises:
        ValueError: If path is invalid or contains traversal attempts
    """
    try:
        # Resolve to absolute path
        path = Path(file_path).resolve()

        # Check for directory traversal attempts
        if ".." in file_path:
            raise ValueError("Path traversal detected")

        # Ensure file exists
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")

        # Ensure it's a file, not a directory
        if not path.is_file():
            raise ValueError(f"Not a file: {file_path}")

        # Check file extension
        if path.suffix.lower() not in [".md", ".txt", ".markdown"]:
            raise ValueError("File must be .md, .txt, or .markdown")

        return path

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Invalid file path: {str(e)}")


def validate_output_directory(output_dir: str) -> Path:
    """
    Validate output directory to prevent malicious file writes.

    Args:
        output_dir: The output directory path

    Returns:
        Resolved Path object

    Raises:
        ValueError: If path is invalid or potentially dangerous
    """
    try:
        # Resolve to absolute path
        path = Path(output_dir).resolve()

        # Check for directory traversal attempts
        if ".." in output_dir:
            raise ValueError("Path traversal detected in output directory")

        # Don't allow writing to system directories
        forbidden_prefixes = ["/etc", "/usr", "/bin", "/sbin", "/System", "/Windows"]
        path_str = str(path)
        for prefix in forbidden_prefixes:
            if path_str.startswith(prefix):
                raise ValueError(f"Cannot write to system directory: {prefix}")

        return path

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Invalid output directory: {str(e)}")


def check_citations(file_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Check citations in a file and return structured results.

    Args:
        file_path: Path to the file to check
        output_dir: Optional directory to save the report (if None, no file is saved)

    Returns:
        Dictionary containing:
        - success: bool
        - error: Optional error message
        - data: Citation check results (if successful)
    """
    try:
        # Validate and read file
        path = validate_file_path(file_path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Initialize client and lookup citations
        with CitationLookupClient() as client:
            citations = client.lookup_text(content)

        # Process results
        status_counts = {
            "found": 0,
            "not_found": 0,
            "invalid": 0,
            "multiple_matches": 0,
        }

        citation_data = []

        for citation in citations:
            # Count statuses
            if citation.status == CitationStatus.FOUND:
                status_counts["found"] += 1
            elif citation.status == CitationStatus.NOT_FOUND:
                status_counts["not_found"] += 1
            elif citation.status == CitationStatus.INVALID:
                status_counts["invalid"] += 1
            elif citation.status == CitationStatus.MULTIPLE_MATCHES:
                status_counts["multiple_matches"] += 1

            # Build citation info
            citation_info = {
                "citation_text": citation.citation,
                "normalized": citation.normalized_citations,
                "status": citation.status,
                "status_name": CitationStatus(citation.status).name,
                "valid": citation.is_valid,
                "position": {"start": citation.start_index, "end": citation.end_index},
            }

            if citation.clusters:
                citation_info["case_info"] = {
                    "case_name": citation.case_name,
                    "clusters": citation.clusters,
                }

            citation_data.append(citation_info)

        # Build report
        report = {
            "metadata": {
                "file": str(path.absolute()),
                "checked_at": datetime.now().isoformat(),
                "total_citations": len(citations),
                "summary": status_counts,
            },
            "citations": citation_data,
        }

        # Save report if output directory specified
        saved_to = None
        result_folder = None
        if output_dir:
            # Validate output directory
            output_path = validate_output_directory(output_dir)
            
            # Create nested folder structure: output_dir/filename/citecheck_result_timestamp/
            base_filename = path.stem
            # Remove '_extracted_cites' suffix if present
            if base_filename.endswith("_extracted_cites"):
                base_filename = base_filename[:-16]  # Remove the last 16 characters
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create the nested directory structure
            result_folder = output_path / base_filename / f"citecheck_result_{timestamp}"
            result_folder.mkdir(parents=True, exist_ok=True)
            
            # Save report with consistent name in the timestamped folder
            output_file = result_folder / "citations_report.json"

            # Ensure we're not overwriting system files
            if output_file.exists() and output_file.stat().st_uid == 0:
                raise ValueError("Cannot overwrite system file")

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            saved_to = str(output_file)

        # Prepare return data
        return_data = {"report": report, "saved_to": saved_to}
        
        # If we saved to a folder, also return the folder path for other commands to use
        if result_folder:
            return_data["result_folder"] = str(result_folder)
            
        return {"success": True, "data": return_data}

    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"An error occurred: {e.__class__.__name__}"}


def main():
    """Simple CLI interface for testing."""
    if len(sys.argv) < 2:
        print("Usage: python citecheck.py <file_path> [output_dir]")
        sys.exit(1)

    file_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = check_citations(file_path, output_dir)

    if result["success"]:
        report = result["data"]["report"]
        summary = report["metadata"]["summary"]
        
        print("Citation Check Summary:")
        print(f"- Total: {report['metadata']['total_citations']} citations")
        print(f"- Valid: {summary['found']}")
        print(f"- Not found: {summary['not_found']}")
        print(f"- Invalid: {summary['invalid']}")
        
        if result["data"]["saved_to"]:
            print(f"\nReport saved: {result['data']['saved_to']}")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
