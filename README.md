# Free Law Cite Checker

A Python-based tool for validating legal citations using the CourtListener API. This tool can be used standalone or integrated with Claude Code as a custom command for enhanced productivity.

## NOT CONFIDENTIAL

This tool is intended for legal research and citation verification only. Please note that both Claude Code and the CourtListener API are external services. As such, they are not suitable for handling privileged or confidential information—do not submit any sensitive or confidential data when using this tool or its integrations.

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
git clone https://github.com/[your-username]/free_law_cite_checker.git
cd free_law_cite_checker
```

2. Install dependencies:

```bash
pip install requests python-dotenv
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
   python cite_check.py document.md

   # Save report to a specific directory
   python cite_check.py document.md /path/to/output/directory
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

#### Setting Up Custom Commands

Claude Code supports custom slash commands - reusable prompts stored as Markdown files that execute specific workflows.

1. **Create the commands directory**:

   ```bash
   mkdir -p .claude/commands
   ```

2. **Create a custom command file** `.claude/commands/cite_check.md`:

   ```markdown
   # Citation Check Command

   Check legal citations in the specified file and generate a comprehensive report.

   ## Usage

   /cite_check <file_path>

   ## Instructions

   Execute the citation check using the following steps:

   1. Validate the input file exists and is readable
   2. Run: python cite_check.py "$ARGUMENTS" "data/outputs/citecheck_results"
   3. Display formatted results with color coding
   4. Show the report save location
   ```

3. **Use the custom command**:

   ```bash
   # Start Claude Code in your project directory
   cd /path/to/free_law_cite_checker
   claude

   # Use the custom command
   /cite_check my-legal-document.md
   ```

#### How Custom Commands Work

- Commands are Markdown files in `.claude/commands/`
- The filename becomes the command name (e.g., `cite_check.md` → `/cite_check`)
- `$ARGUMENTS` is replaced with any text after the command
- Commands can include detailed instructions for Claude to follow
- Commands are project-specific and can be committed to version control

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

Report saved: /path/to/output/document_report_20240326_103000.json
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

Create a test file `test.md`:

```markdown
The landmark case Brown v. Board of Education, 347 U.S. 483 (1954) established...
See also Miranda v. Arizona, 384 U.S. 436 (1966) for related precedent.
```

Run:

```bash
python cite_check.py test.md
```

### Example 2: Checking a Legal Brief

```bash
# Direct usage
python cite_check.py legal-briefs/motion-to-dismiss.md reports/

# With Claude Code
claude
/cite_check legal-briefs/motion-to-dismiss.md
```

### Example 3: Batch Processing

Create a simple wrapper script:

```python
import os
from cite_check import check_citations

for filename in os.listdir('documents'):
    if filename.endswith(('.md', '.txt')):
        result = check_citations(f'documents/{filename}', 'reports')
        print(f"Processed {filename}: {result['success']}")
```

## Configuration

### Environment Variables

- `COURTLISTENER_API_TOKEN`: Your CourtListener API token (required)

### Security Notes

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
- The legal technology community for feedback and suggestions
