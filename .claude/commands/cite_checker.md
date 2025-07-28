# Citation Check Command

Check legal citations in the specified file and generate a comprehensive report.

## Usage

/citecheck $ARGUMENTS

## Instructions

You are performing a citation check on the file: $ARGUMENTS

Execute the citation check using the following steps:

1. **Validate Input**

   - Verify the file exists and is readable
   - Ensure it's a .md, .txt, or .markdown file
   - If invalid, provide clear error message

2. **Run Citation Check**
   Use Python to import and run the citation checker:

   ```python
   import sys
   sys.path.append('.')
   from src.run.citecheck import check_citations

   result = check_citations("$ARGUMENTS", "data/outputs/citecheck_results")
   ```

3. **Handle Results**
   If successful, display:

   - Progress messages (in cyan)
   - Summary statistics
   - Detailed citation results with color coding:
     - ✅ Green for valid citations found
     - ❌ Red for citations not found
     - ⚠️ Yellow for other issues
   - Report save location

4. **Format Output**

   ```
   📊 Citation Check Complete

   Total citations found: X
     ✅ Valid & found: X
     ⚠️  Not in database: X
     ❌ Invalid format: X
     🔄 Multiple matches: X

   Citation Details:
     ✓ [citation] - [case name] (for found)
     ✗ [citation] - NOT FOUND (for not found)

   💾 Report saved to: [path]
   ```

5. **Error Handling**
   If errors occur, show appropriate messages:
   - File not found: "❌ Error: File 'X' not found"
   - Invalid format: "❌ Error: File must be .md, .txt, or .markdown"
   - Missing API token: "❌ Error: COURTLISTENER_API_TOKEN not set"
