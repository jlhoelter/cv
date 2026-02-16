#!/bin/bash
#
# Publish CV to GitHub Pages
# Pushes the cv/ directory to github.com/jlhoelter/cv
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
CV_SUBTREE="tracks/jobsuche/cv"
REMOTE_REPO="git@github.com:jlhoelter/cv.git"
BRANCH="main"

echo "📤 Publishing CV to GitHub Pages..."
echo "   Workspace: $WORKSPACE_ROOT"
echo "   Subtree:   $CV_SUBTREE"
echo "   Remote:    $REMOTE_REPO"
echo ""

cd "$WORKSPACE_ROOT"

# Check if there are uncommitted changes in cv/
if ! git diff --quiet HEAD -- "$CV_SUBTREE" 2>/dev/null; then
    echo "⚠️  Warning: You have uncommitted changes in cv/"
    echo "   Commit them first or they won't be published."
    echo ""
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted."
        exit 1
    fi
fi

# Push subtree
echo "🚀 Pushing to GitHub Pages..."
git subtree push --prefix="$CV_SUBTREE" "$REMOTE_REPO" "$BRANCH"

echo ""
echo "✅ CV published successfully!"
echo "🔗 https://jlhoelter.github.io/cv/"
echo ""
echo "Note: GitHub Pages may take 1-2 minutes to update."
