# Free Law Cite Checker

A Python-based tool for validating legal citations using the CourtListener API. This tool can be used standalone or integrated with Claude Code as a custom command for enhanced productivity.

## NOT CONFIDENTIAL

This tool is intended for legal research and citation verification only. Please note that both Claude Code and the CourtListener API are external services. As such, they are not suitable for handling privileged or confidential information without enterprise-grade configuration—do not submit any sensitive or confidential data when using this tool or its integrations.

## About Eyecite and Free Law Project

This tool leverages the power of **Eyecite**, an open-source, high-performance tool for extracting, parsing, and normalizing legal citations from free-form text. Developed by Free Law Project in collaboration with the Harvard Library Innovation Lab, Eyecite has been battle-tested on over fifty million citations across CourtListener and the Caselaw Access Project.

### Eyecite Key Capabilities

- **Extraction**: Recognizes hundreds of citation patterns (full case, short form, statutory, journal, supra, id.)
- **Aggregation**: Links shorthand ("supra," "id.") citations back to their antecedents
- **Annotation**: Wraps citations in custom markup for downstream processing
- **Normalization**: Converts citations into a consistent reporter format and exposes metadata (volume, page, court, year, pincite, parties)
- **Cleaning**: Pre-processes text (e.g. removing noise) to improve parsing accuracy

Eyecite powers CourtListener's Citation Lookup and Verification APIs and can be used standalone via its Python library or command-line interface. It's the backbone of any system needing robust, scalable legal citation handling.

### Free Law Project APIs

The CourtListener API, provided by Free Law Project, offers comprehensive access to legal data including:

- Citation lookup and verification endpoints powered by Eyecite
- Access to millions of legal opinions and documents
- Court data and docket information
- Judge biographical information

Learn more at [CourtListener API documentation](https://www.courtlistener.com/help/api/rest/v4/citation-lookup/)

## Features

- **Citation Validation**: Validates legal citations against CourtListener's comprehensive database
- **Batch Processing**: Process entire documents to find and validate multiple citations
- **Multiple Formats**: Supports `.md`, `.txt`, and `.markdown` files
- **Detailed Reports**: Generates JSON reports with citation status, case names, and metadata
- **Claude Code Integration**: Custom slash command for seamless AI-assisted workflows with formatted output

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Getting a CourtListener API Token](#getting-a-courtlistener-api-token)
- [Usage](#usage)
  - [Using the Python Script Directly](#using-the-python-script-directly)
  - [Using with Claude Code](#using-with-claude-code)
    - [What is Claude Code?](#what-is-claude-code)
    - [Installing Claude Code](#installing-claude-code)
    - [Setting Up Custom Commands](#setting-up-custom-commands)
    - [How Custom Commands Work](#how-custom-commands-work)
- [Output Format](#output-format)
- [Examples](#examples)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.8 or higher
- CourtListener API token (free tier available)
- (Optional) Claude Code for enhanced workflow integration (requires Claude Pro/Max subscription)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/justlyai/free_law_cite_checker.git
cd free_law_cite_checker
```

2. Set up environment with uv:

```bash
# Create virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
uv sync
```

3. Set up your environment (see [Configuration](#configuration))

## Getting a CourtListener API Token

1. **Get a CourtListener API token**:

   - Visit [CourtListener.com](https://www.courtlistener.com)
   - Create an account or sign in
   - Navigate to your profile settings
   - Generate an API token

2. **Add your API token to the project**:

   - Set it as an environment variable:
     ```bash
     export COURTLISTENER_API_TOKEN="your-token-here"
     ```
   - Or create a `.env` file in the project root:
     ```
     COURTLISTENER_API_TOKEN=your-token-here
     ```

3. **API Limits**:
   - Free tier: 5,000 requests per day
   - Rate limit: 10 requests per second
   - See [CourtListener API documentation](https://www.courtlistener.com/api/) for details

## Usage

### Using the Python Script Directly

1. **Set your API token** (choose one method):

   Environment variable:

   ```bash
   export COURTLISTENER_API_TOKEN="your-token-here"
   ```

   Or create a `.env` file:

   ```
   COURTLISTENER_API_TOKEN=your-token-here
   ```

2. **Run the script**:

   ```bash
   # Check citations in a file (output to console)
   python cite_check.py data/inputs/citecheck_test.md

   # Save report to a specific directory
   python cite_check.py data/inputs/citecheck_test.md /path/to/output/directory
   ```

### Using with Claude Code

#### What is Claude Code?

Claude Code is Anthropic's AI-powered coding assistant that runs in your terminal. It can understand your entire codebase, execute commands, and help you code faster with deep contextual awareness.

#### Installing Claude Code

1. **Install via npm** (requires Node.js 16+):

   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Verify installation**:

   ```bash
   claude --version
   ```

3. **Authenticate** (requires Claude Pro or Max subscription):
   ```bash
   claude login
   ```
   This will open your browser for authentication. Your credentials are securely stored.

#### Available Custom Commands

This project includes three custom commands for different citation workflows:

##### 1. `/cite_check` - Direct Citation Validation

Checks all citations in your document against the CourtListener database.

**Usage**:

```bash
/cite_check my-legal-document.md
```

**What it does**:

- Sends your entire document to the CourtListener API
- Validates each citation found
- Generates a detailed report with validation status
- Saves results to `data/outputs/<filename>/citecheck_result_<timestamp>/citations_report.json`

##### 2. `/cite_extract` - Extract Citations Only

Extracts citations and their context WITHOUT sending data to external APIs.

**Usage**:

```bash
/cite_extract input-document.md output-file.md
# Or without output file (auto-generates in data/outputs/)
/cite_extract input-document.md
```

**What it does**:

- Reads your document locally
- Identifies legal citations using pattern recognition
- Extracts case names and surrounding context
- Creates a condensed file with just the citations
- **Privacy benefit**: Your full document gets sent to the LLM but not to the CourtListener API

**Output format**:

```markdown
# Legal Citations Extract

**Source File:** /path/to/input.md
**Extract File:** /path/to/output.md

## Citations Found

Smith v. Jones, 123 F.3d 456 (2d Cir. 2020) - Established the standard for...
Doe v. Roe, 789 U.S. 123 (2019) - Held that privileged communications...
```

##### 3. `/cite_extract_and_check` - Two-Step Workflow

Combines extraction and validation for maximum privacy and functionality.

**Usage**:

```bash
/cite_extract_and_check my-confidential-brief.md
```

**What it does**:

1. First extracts citations locally (like `/cite_extract`)
2. Then checks ONLY the extracted citations against CourtListener
3. Saves both the extraction and validation results together

**Benefits**:

- Your full document stays private
- Only citation text is sent to the API
- You get full validation results
- Both files saved in the same result folder

#### Privacy Considerations

When working with sensitive legal documents, consider:

- **`/cite_check`**: Sends your ENTIRE document to CourtListener API
- **`/cite_extract`**: Processed by LLM only (can be local), no CourtListener API call
- **`/cite_extract_and_check`**: Only sends extracted citations to API

For privileged or confidential documents, use `/cite_extract` to create a citations-only file first, review it, then run `/cite_check` on the extracted file if comfortable.

#### Setting Up Custom Commands

The custom commands are already included in `.claude/commands/`. To use them:

1. Start Claude Code in your project directory:

   ```bash
   cd /path/to/free_law_cite_checker
   claude
   ```

2. Use any of the commands:
   ```bash
   /cite_check data/inputs/citecheck_test.md
   /cite_extract brief.md
   /cite_extract_and_check memo.md
   ```

#### How Custom Commands Work

- Commands are Markdown files in `.claude/commands/`
- The filename becomes the command name (e.g., `cite_check.md` → `/cite_check`)
- `$ARGUMENTS` is replaced with any text after the command
- Commands provide detailed instructions for Claude to follow

#### Benefits of Claude Code Integration

1. **Enhanced Output Formatting**: Claude Code can display results with colors, emojis, and structured formatting
2. **Error Handling**: Better error messages and guidance when issues occur
3. **Workflow Automation**: Combine citation checking with other development tasks
4. **Context Awareness**: Claude understands your project structure and can suggest improvements
5. **Interactive Assistance**: Get help interpreting results or fixing citation issues

## Output Format

### Console Output (Direct Script Usage)

When run directly, the script outputs a summary to the console:

```
Citation Check Summary:
- Total: 9 citations
- Valid: 5
- Not found: 4
- Invalid: 0

Report saved: /path/to/output/document/citecheck_result_20240326_103000/citations_report.json
```

### Output Directory Structure

When an output directory is specified, the tool creates a nested folder structure.

For example:

```bash
python cite_check.py legal_memo.md data/outputs
```

Creates:

```
data/outputs/
  └── legal_memo/
      └── citecheck_result_20240326_103000/
          └── citations_report.json
```

### JSON Report Format

The detailed JSON report saved to disk contains comprehensive information:

```json
{
  "metadata": {
    "file": "/absolute/path/to/document.md",
    "checked_at": "2024-03-26T10:30:00.123456",
    "total_citations": 5,
    "summary": {
      "found": 3,
      "not_found": 1,
      "invalid": 0,
      "multiple_matches": 1
    }
  },
  "citations": [
    {
      "citation_text": "347 U.S. 483",
      "normalized": ["347 U.S. 483"],
      "status": 200,
      "status_name": "FOUND",
      "valid": true,
      "position": {
        "start": 156,
        "end": 203
      },
      "case_info": {
        "case_name": "Brown v. Board of Education",
        "clusters": [...]
      }
    }
  ]
}
```

## Examples

### Example 1: Simple Citation Check

Use the provided test file and run the script:

```bash
python cite_check.py data/inputs/test.md
```

## Configuration

### Environment Variables

- `COURTLISTENER_API_TOKEN`: Your CourtListener API token (required)

### Security Notes

- When working with confidential information, only use Claude Code with a secure, enterprise-grade configuration.
- The CourtListener API is an external service; it should not be used for privileged or confidential information.
- The script validates file paths to prevent directory traversal attacks.
- Output directories are validated to prevent writing to system directories.
- API tokens (such as your CourtListener API token) should never be committed to version control.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CourtListener](https://www.courtlistener.com) for providing the comprehensive legal citation API
- [Free Law Project](https://free.law/) for maintaining open legal data
- [Eyecite](https://github.com/freelawproject/eyecite) - The powerful citation extraction engine behind CourtListener's citation APIs
- [Harvard Library Innovation Lab](https://lil.law.harvard.edu/) for collaboration on Eyecite development
