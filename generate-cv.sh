#!/bin/bash
#
# CV Generator - Erstellt Word-Dokument aus Markdown
# Usage: ./generate-cv.sh <markdown-file>
# Example: ./generate-cv.sh CV_Jan_Hoelter_TIMOCOM_DE.md
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if markdown file is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: No markdown file specified${NC}"
    echo "Usage: $0 <markdown-file>"
    echo "Example: $0 CV_Jan_Hoelter_TIMOCOM_DE.md"
    exit 1
fi

MARKDOWN_FILE="$1"
PHOTO_FILE="Jan_Hoelter_Foto.jpeg"

# Check if markdown file exists
if [ ! -f "$MARKDOWN_FILE" ]; then
    echo -e "${RED}Error: File '$MARKDOWN_FILE' not found${NC}"
    exit 1
fi

# Check if photo exists
if [ ! -f "$PHOTO_FILE" ]; then
    echo -e "${YELLOW}Warning: Photo '$PHOTO_FILE' not found. CV will be generated without photo.${NC}"
    HAS_PHOTO=false
else
    HAS_PHOTO=true
fi

# Generate output filename (replace .md with .docx)
OUTPUT_FILE="${MARKDOWN_FILE%.md}.docx"

echo -e "${GREEN}Generating CV...${NC}"
echo "  Input:  $MARKDOWN_FILE"
echo "  Output: $OUTPUT_FILE"
if [ "$HAS_PHOTO" = true ]; then
    echo "  Photo:  $PHOTO_FILE"
fi
echo ""

# Export variables for Python script
export MARKDOWN_FILE
export OUTPUT_FILE
export PHOTO_FILE
export HAS_PHOTO

# Generate Word document using Python
python3 << 'PYTHON_SCRIPT'
import sys
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Read environment variables
markdown_file = os.environ['MARKDOWN_FILE']
output_file = os.environ['OUTPUT_FILE']
photo_file = os.environ['PHOTO_FILE']
has_photo = os.environ['HAS_PHOTO'] == 'true'

# Read markdown
with open(markdown_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Create document
doc = Document()

# Set page margins (narrow margins for professional CV)
sections = doc.sections
for section in sections:
    section.top_margin = Cm(1.27)
    section.bottom_margin = Cm(1.27)
    section.left_margin = Cm(1.91)
    section.right_margin = Cm(1.91)

# Configure default styles
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Parse content line by line
lines = content.split('\n')
i = 0
first_heading = True

while i < len(lines):
    line = lines[i].strip()

    # Skip empty lines
    if not line:
        i += 1
        continue

    # Main heading (Name) with optional photo
    if line.startswith('# ') and first_heading:
        first_heading = False

        if has_photo and os.path.exists(photo_file):
            # Create table for name + photo layout
            table = doc.add_table(rows=1, cols=2)
            table.autofit = False
            table.allow_autofit = False

            # Left cell: Name
            left_cell = table.rows[0].cells[0]
            left_cell.width = Inches(5)
            p = left_cell.paragraphs[0]
            run = p.add_run(line[2:].strip())
            run.font.size = Pt(24)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 51, 102)

            # Right cell: Photo
            right_cell = table.rows[0].cells[1]
            right_cell.width = Inches(1.5)
            p = right_cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            run = p.add_run()
            run.add_picture(photo_file, width=Inches(1.2))

            # Remove borders
            for row in table.rows:
                for cell in row.cells:
                    cell._element.get_or_add_tcPr().append(
                        doc._element.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tcBorders',
                        {'val': 'none'})
                    )
        else:
            # No photo: just name as heading
            p = doc.add_heading(line[2:].strip(), level=1)
            p.runs[0].font.size = Pt(24)
            p.runs[0].font.color.rgb = RGBColor(0, 51, 102)

    # Subtitle line with bold + markdown italic
    elif line.startswith('**') and line.endswith('**') and not line.startswith('###'):
        p = doc.add_paragraph()
        run = p.add_run(line.strip('*'))
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)

    # Italic subtitle
    elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
        p = doc.add_paragraph()
        run = p.add_run(line.strip('*'))
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = RGBColor(96, 96, 96)

    # Horizontal rule (section separator)
    elif line == '---':
        doc.add_paragraph()

    # Section heading (## )
    elif line.startswith('## '):
        doc.add_paragraph()
        p = doc.add_heading(line[3:], level=2)
        p.runs[0].font.size = Pt(14)
        p.runs[0].font.color.rgb = RGBColor(0, 51, 102)
        p.runs[0].font.bold = True

    # Company/Position heading (### )
    elif line.startswith('### '):
        doc.add_paragraph()
        p = doc.add_paragraph()
        run = p.add_run(line[4:].strip('*'))
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)

    # Bullet points
    elif line.startswith('- '):
        p = doc.add_paragraph(line[2:], style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(3)

    # Contact info or regular paragraph
    else:
        # Check for emoji/icon contact info
        if any(emoji in line for emoji in ['📧', '🔗', '☎️', 'E-Mail:', 'Mobil:', 'LinkedIn:']):
            p = doc.add_paragraph(line)
            p.runs[0].font.size = Pt(10)
            p.runs[0].font.color.rgb = RGBColor(64, 64, 64)
            p.paragraph_format.space_after = Pt(2)
        else:
            p = doc.add_paragraph(line)

    i += 1

# Save document
doc.save(output_file)
print(f"✓ Word document created: {output_file}")
PYTHON_SCRIPT

# Check if Python script succeeded
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ CV successfully generated!${NC}"
    echo ""
    ls -lh "$OUTPUT_FILE"
else
    echo -e "${RED}✗ Error generating CV${NC}"
    exit 1
fi
