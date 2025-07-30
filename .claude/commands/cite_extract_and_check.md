# Extract and Check Citations Command

Extract legal citations from a document and immediately check them against the CourtListener database.

## Usage

/cite_extract_and_check $ARGUMENTS

## Instructions

You are extracting and checking legal citations from the file: $ARGUMENTS

Execute the following steps:

1. **Validate Input**

   - Verify the file exists and is readable
   - Ensure it's a .md, .txt, or .markdown file
   - If invalid, provide clear error message

2. **Extract Citations**
   
   Read the document and identify all legal citations using your understanding of citation formats:

   - Federal Reporter citations (e.g., "123 F.3d 456")
   - Federal Supplement citations (e.g., "456 F. Supp. 3d 789")
   - Westlaw citations (e.g., "2020 WL 1234567")
   - Federal Appendix citations (e.g., "21 F.4th 216")
   - State court citations
   - Docket numbers (e.g., "No. 2020-02558")

   For each citation found:
   - Capture the case name
   - Include brief surrounding context explaining the case's relevance
   - Note the court and year if available

3. **Create Extraction Output**

   Create output directory structure and save extracted citations:
   
   ```python
   from datetime import datetime
   from pathlib import Path
   
   # Extract base filename from input path (without extension)
   input_path = Path(input_file)
   base_filename = input_path.stem
   
   # Create timestamp
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   
   # Create output directory
   output_dir = Path(f"data/outputs/{base_filename}/citecheck_result_{timestamp}")
   output_dir.mkdir(parents=True, exist_ok=True)
   
   # Save extracted citations
   extract_path = output_dir / "extracted_cites.md"
   ```
   
   Format the extracted citations file:
   
   ```markdown
   # Legal Citations Extract

   **Source File:** [full path to input file]  
   **Extract File:** [full path to output file]

   ## Citations Found

   [Case Name], [Citation] - [Brief description of holding/relevance]
   ```
   
   Important: Do NOT use any markdown formatting (no italics, bold, or underscores) in case names or citations.

4. **Check Citations with CourtListener**

   Run citation check on the extracted citations file and save the results:

   ```python
   import sys
   import json
   sys.path.append('.')
   from cite_check import check_citations
   
   # Check the extracted citations file WITHOUT specifying output_dir
   # This returns the results without creating any folders
   result = check_citations(str(extract_path))
   
   # Save the results ourselves in the same folder as extracted_cites.md
   if result['success']:
       report_path = output_dir / 'citations_report.json'
       with open(report_path, 'w') as f:
           json.dump(result['data']['report'], f, indent=2)
   ```

5. **Display Combined Results**

   Show both extraction and validation results:

   ```
   📋 Citation Extraction & Check Complete
   
   ✂️  Extraction Results:
     • Citations found: X
     • Extract saved to: [path]
   
   📊 Validation Results:
     Total citations checked: X
       ✅ Valid & found: X
       ⚠️  Not in database: X
       ❌ Invalid format: X
       🔄 Multiple matches: X
   
   Citation Details:
     ✓ [citation] - [case name] (for found)
     ✗ [citation] - NOT FOUND (for not found)
   
   💾 Full report saved to: [output_dir]/citations_report.json
   ```

6. **Error Handling**
   
   Handle errors appropriately:
   - File not found: "❌ Error: File 'X' not found"
   - Invalid format: "❌ Error: File must be .md, .txt, or .markdown"
   - Missing API token: "❌ Error: COURTLISTENER_API_TOKEN not set"
   - No citations found: "⚠️  No legal citations found in the document"

The command combines extraction and validation to provide a complete citation analysis workflow in a single step.