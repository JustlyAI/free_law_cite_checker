# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based legal citation validation tool that uses the CourtListener API to check legal citations in documents. The tool can be used standalone or integrated with Claude Code as a custom command.

## Key Commands

### Running the Citation Checker
```bash
# Check citations with console output only
python cite_check.py <file_path>

# Check citations and save report to specific directory
python cite_check.py <file_path> <output_directory>

# Default output directory when using custom command
python cite_check.py <file_path> data/outputs/citecheck_results
```

### Development Commands
```bash
# Install dependencies with uv (if available) or pip
uv sync  # or pip install -r pyproject.toml

# Run tests (if pytest is available)
pytest

# Format code
black cite_check.py
```

## Architecture

### Core Components

1. **cite_check.py** - Main module containing:
   - `CitationLookupClient`: API client for CourtListener
   - `Citation`: Data class for citation results
   - `check_citations()`: Main function that processes files and returns structured results
   - Path validation functions for security

2. **Custom Command Integration** (.claude/commands/cite_check.md):
   - Slash command `/cite_check` for Claude Code integration
   - Handles formatting and presentation of results with colors and emojis

### Key Design Decisions

- **Security**: Path validation prevents directory traversal attacks and writing to system directories
- **Error Handling**: Returns structured `{success: bool, error?: str, data?: dict}` responses
- **API Integration**: Uses CourtListener's citation lookup API with proper rate limiting
- **File Support**: Processes .md, .txt, and .markdown files only

## Important Configuration

### Environment Setup
The CourtListener API token must be set via:
```bash
export COURTLISTENER_API_TOKEN="your-token-here"
```
Or create a `.env` file with:
```
COURTLISTENER_API_TOKEN=your-token-here
```

### API Limits
- Free tier: 5,000 requests/day
- Rate limit: 10 requests/second
- Max text length: 64,000 characters per request

## Citation Status Codes
- 200 (FOUND): Citation found in database
- 404 (NOT_FOUND): Citation not in database
- 400 (INVALID): Invalid citation format
- 300 (MULTIPLE_MATCHES): Multiple potential matches
- 429 (TOO_MANY_CITATIONS): Rate limit exceeded

## Output Structure
Reports are saved as JSON with:
- Metadata (file path, timestamp, summary counts)
- Detailed citation array with status, case names, and positions
- Example: `data/outputs/citecheck_results/filename_report_YYYYMMDD_HHMMSS.json`