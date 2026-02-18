#!/bin/bash

# CV HTML Generator
# Wrapper script for generate-html.py

set -e

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKDOWN_FILE="${MARKDOWN_FILE:-$SCRIPT_DIR/CV_Jan_Hoelter_final.md}"
OUTPUT_FILE="${OUTPUT_FILE:-$SCRIPT_DIR/index.html}"
PHOTO_FILE="${PHOTO_FILE:-assets/Jan_Hoelter_Foto.jpeg}"
LANG="${LANG:-de}"

# Run Python generator
python3 "$SCRIPT_DIR/generate-html.py" \
  "$MARKDOWN_FILE" \
  -o "$OUTPUT_FILE" \
  -p "$PHOTO_FILE" \
  -l "$LANG"

echo "✓ HTML CV generated successfully"
echo "  Open: file://$OUTPUT_FILE"
