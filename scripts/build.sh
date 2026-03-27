#!/bin/bash
set -e

# Gemma 3 270M Minimal Container Build Script
# Supports x86_64 and aarch64 architectures
# Requires HF_TOKEN env var to download model weights at build time.

IMAGE_NAME="gemma-3-270m-minimal"
VERSION="latest"
ARCH=$(uname -m)

case $ARCH in
    x86_64)   PLATFORM="linux/amd64" ;;
    aarch64|arm64) PLATFORM="linux/arm64" ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

if [ -z "$HF_TOKEN" ]; then
    echo "ERROR: HF_TOKEN is not set."
    echo ""
    echo "The model weights are downloaded at build time using your Hugging Face token."
    echo "To get a token:"
    echo "  1. Accept the Gemma license: https://huggingface.co/google/gemma-3-270m-it"
    echo "  2. Generate a token: https://huggingface.co/settings/tokens"
    echo "  3. Export it: export HF_TOKEN='hf_...'"
    echo ""
    exit 1
fi

echo "=========================================="
echo "Gemma 3 270M Minimal Container Builder"
echo "=========================================="
echo "Architecture: $ARCH ($PLATFORM)"
echo "Image: $IMAGE_NAME:$VERSION"
echo "=========================================="

if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

export DOCKER_BUILDKIT=1

echo "Building Docker image (downloading model weights — this may take a few minutes)..."
docker build \
    --platform "$PLATFORM" \
    --secret id=hf_token,env=HF_TOKEN \
    -t "$IMAGE_NAME:$VERSION" \
    -f docker/Dockerfile \
    .

echo ""
echo "Build complete!"
echo "Image: $IMAGE_NAME:$VERSION"
echo ""
echo "To run inference:"
echo "  docker run -it $IMAGE_NAME:$VERSION python src/inference.py --interactive"
echo ""
echo "To start the API server:"
echo "  docker run -p 8080:8080 $IMAGE_NAME:$VERSION python src/api_server.py"
