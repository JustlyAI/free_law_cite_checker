# Extract Citations Command

Extract all legal citations and their surrounding context from a document and create a condensed version.

## Usage

/extract_cites '<input_file>' '<output_file>'

## Instructions

You are extracting legal citations from the file: $ARGUMENTS

Parse the arguments to get input and output file paths, then:

1. **Read the Input File**

   - Verify the input file exists and is readable
   - Use the Read tool to examine the document

2. **Identify Citations**
   Look for legal citation patterns including:

   - Federal Reporter citations (e.g., "123 F.3d 456")
   - Federal Supplement citations (e.g., "456 F. Supp. 3d 789")
   - Westlaw citations (e.g., "2020 WL 1234567")
   - Federal Appendix citations (e.g., "21 F.4th 216")
   - State court citations
   - Docket numbers (e.g., "No. 2020-02558")

3. **Extract Context**
   For each citation found:

   - Capture the case name
   - Include brief surrounding context explaining the case's relevance
   - Note the court and year if available

4. **Create Output File**

   If no output file is specified in arguments:

   - Import datetime: `from datetime import datetime`
   - Extract base filename from input path (without extension)
   - Create timestamp: `datetime.now().strftime("%Y%m%d_%H%M%S")`
   - Create output directory: `data/outputs/{base_filename}/citecheck_result_{timestamp}/`
   - Save extracted citations as `extracted_cites.md` in that directory

   Write a markdown file with:

   - Name the source and output filenames at the top
   - Organized sections by topic/issue
   - Each citation with its case name and brief context
   - Do NOT use any markdown formatting (no italics, bold, or underscores) in case names or citations.

5. **Format Guidelines**

   ```markdown
   # Legal Citations Extract

   **Source File:** [full path to input file]  
   **Extract File:** [full path to output file]

   ## [Topic/Section Name]

   ### [Subsection if needed]

   [Case Name], [Citation] - [Brief description of holding/relevance]
   ```

6. **Output File Naming**

   - **Important**: If output file is not specified, create organized output structure:
     - Create folder: `data/outputs/{input_filename}/citecheck_result_{timestamp}/`
     - Save as: `extracted_cites.md` in that folder
   - Example: For "memo.md" input, output goes to:
     `data/outputs/memo/citecheck_result_20250729_150000/extracted_cites.md`

7. **Success Message**
   Display: "✅ Successfully extracted [X] citations to [output_file]"
