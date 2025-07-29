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

   First, create a temporary extraction file, then run the citation check to get the result folder:
   
   - Save initially to a temporary location in the same directory as input file
   - Use filename: input filename + "_extracted_cites.md"
   - Format with clear structure:
   
   ```markdown
   # Legal Citations Extract

   **Source File:** [full path to input file]  
   **Extract File:** [full path to output file]

   ## Citations Found

   [Case Name], [Citation] - [Brief description of holding/relevance]
   ```
   
   Important: Do NOT use any markdown formatting (no italics, bold, or underscores) in case names or citations.

4. **Check Citations with CourtListener**

   Check citations and then move the extracted file to the result folder:

   ```python
   import sys
   import shutil
   from pathlib import Path
   sys.path.append('.')
   from cite_check import check_citations
   
   # Check the extracted citations file
   result = check_citations(str(extract_path), "data/outputs")
   
   # If successful and we have a result folder, move the extracted file there
   if result['success'] and 'result_folder' in result['data']:
       result_folder = Path(result['data']['result_folder'])
       final_extract_path = result_folder / 'extracted_cites.md'
       shutil.move(str(extract_path), str(final_extract_path))
       # Update the extract_path for display
       extract_path = final_extract_path
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
   
   💾 Full report saved to: [path]
   ```

6. **Error Handling**
   
   Handle errors appropriately:
   - File not found: "❌ Error: File 'X' not found"
   - Invalid format: "❌ Error: File must be .md, .txt, or .markdown"
   - Missing API token: "❌ Error: COURTLISTENER_API_TOKEN not set"
   - No citations found: "⚠️  No legal citations found in the document"

The command combines extraction and validation to provide a complete citation analysis workflow in a single step.