#!/bin/bash

# CV HTML Generator
# Wrapper script for generate-html.py

set -e

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKDOWN_FILE="${MARKDOWN_FILE:-$SCRIPT_DIR/CV_Jan_Hoelter_final.md}"
OUTPUT_FILE="${OUTPUT_FILE:-$SCRIPT_DIR/index.html}"
PHOTO_FILE="${PHOTO_FILE:-$SCRIPT_DIR/Jan_Hoelter_Foto.jpeg}"
LANG="${LANG:-de}"

# Run Python generator
python3 "$SCRIPT_DIR/generate-html.py" \
  "$MARKDOWN_FILE" \
  --output "$OUTPUT_FILE" \
  --photo "$PHOTO_FILE" \
  --lang "$LANG"

echo "✓ HTML CV generated successfully"
echo "  Open: file://$OUTPUT_FILE"
