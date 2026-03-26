#!/bin/bash
#
# verify-project.sh - Verify all project files are present
#

set -e

echo "========================================"
echo "  Gemma 3 270M Project Verification"
echo "========================================"
echo ""

# Define required files
REQUIRED_FILES=(
    "README.md"
    "Dockerfile"
    "build.sh"
    "inference.py"
    "requirements.txt"
    ".dockerignore"
    ".gitignore"
    "LICENSE"
    "Makefile"
    "test_inference.py"
    "CONTRIBUTING.md"
    "PROJECT_STRUCTURE.md"
    "QUICK_REFERENCE.md"
    "BUILD.md"
    "VERSION"
    ".github/workflows/docker-build.yml"
    ".github/ISSUE_TEMPLATE/bug_report.md"
    ".github/ISSUE_TEMPLATE/feature_request.md"
)

# Check files
MISSING=0
FOUND=0

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
        ((FOUND++))
    else
        echo "✗ $file (MISSING)"
        ((MISSING++))
    fi
done

echo ""
echo "========================================"
echo "  Summary"
echo "========================================"
echo "Found: $FOUND files"
echo "Missing: $MISSING files"
echo ""

if [ $MISSING -eq 0 ]; then
    echo "✓ All required files are present!"
    echo ""
    echo "Next steps:"
    echo "  1. Review README.md for quick start"
    echo "  2. Run ./build.sh to build the image"
    echo "  3. Test with: docker run -it gemma-3-270m-minimal python inference.py --interactive"
    exit 0
else
    echo "✗ Some files are missing. Please review the project structure."
    exit 1
fi
