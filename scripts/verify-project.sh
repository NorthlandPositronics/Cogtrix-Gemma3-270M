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
    "docker/Dockerfile"
    "docker/Dockerfile.llamacpp"
    "scripts/build.sh"
    "scripts/build-container-image.sh"
    "requirements.txt"
    ".dockerignore"
    ".gitignore"
    ".github/workflows/ci.yml"
    ".github/workflows/release-please.yml"
    ".github/ISSUE_TEMPLATE/bug_report.md"
    ".github/ISSUE_TEMPLATE/feature_request.md"
    ".github/release-please-config.json"
    ".release-please-manifest.json"
    "src/inference.py"
    "src/api_server.py"
    "src/api_server_mock.py"
    "src/test_inference.py"
    "docs/PROJECT_STRUCTURE.md"
    "docs/QUICK_REFERENCE.md"
    "docs/BUILD.md"
    "docs/PROJECT_SUMMARY.md"
)

# Check files
MISSING=0
FOUND=0

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
        FOUND=$((FOUND + 1))
    else
        echo "✗ $file (MISSING)"
        MISSING=$((MISSING + 1))
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
    echo "  2. Run ./scripts/build-container-image.sh to build the fast-start image"
    echo "  3. Test with: docker run -p 8080:8080 cogtrix-gemma3-270m"
    exit 0
else
    echo "✗ Some files are missing. Please review the project structure."
    exit 1
fi
