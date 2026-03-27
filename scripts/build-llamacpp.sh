#!/bin/bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-gemma-3-270m-llamacpp}"
TAG="${TAG:-latest}"

if [ -z "${HF_TOKEN:-}" ]; then
  echo "ERROR: HF_TOKEN is required to download GGUF weights."
  echo "export HF_TOKEN=hf_..."
  exit 1
fi

echo "Building ${IMAGE_NAME}:${TAG} (llama.cpp, CPU-only)…"
docker build \
  -f docker/Dockerfile.llamacpp \
  --secret id=hf_token,env=HF_TOKEN \
  -t "${IMAGE_NAME}:${TAG}" \
  .

echo "Done. Run with:"
echo "  docker run -p 8080:8080 ${IMAGE_NAME}:${TAG}"
