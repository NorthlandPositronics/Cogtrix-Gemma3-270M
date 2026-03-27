#!/bin/bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-cogtrix-gemma3-270m}"
TAG="${TAG:-latest}"
GGUF_REPO="${GGUF_REPO:-unsloth/gemma-3-270m-it-qat-GGUF}"
GGUF_VARIANT="${GGUF_VARIANT:-Q4_K_M}"
LLAMA_ARG_CTX_SIZE="${LLAMA_ARG_CTX_SIZE:-4096}"
GGML_NATIVE="${GGML_NATIVE:-OFF}"

if [ -z "${HF_TOKEN:-}" ]; then
  echo "ERROR: HF_TOKEN is required to download GGUF weights."
  echo "export HF_TOKEN=hf_..."
  exit 1
fi

echo "Building ${IMAGE_NAME}:${TAG} (llama.cpp, CPU-only)…"
echo "  GGUF_REPO=${GGUF_REPO}"
echo "  GGUF_VARIANT=${GGUF_VARIANT}"
echo "  LLAMA_ARG_CTX_SIZE=${LLAMA_ARG_CTX_SIZE}"
echo "  GGML_NATIVE=${GGML_NATIVE}"
docker build \
  -f docker/Dockerfile.llamacpp \
  --build-arg GGUF_REPO="${GGUF_REPO}" \
  --build-arg GGUF_VARIANT="${GGUF_VARIANT}" \
  --build-arg LLAMA_ARG_CTX_SIZE="${LLAMA_ARG_CTX_SIZE}" \
  --build-arg GGML_NATIVE="${GGML_NATIVE}" \
  --secret id=hf_token,env=HF_TOKEN \
  -t "${IMAGE_NAME}:${TAG}" \
  .

echo "Done. Run with:"
echo "  docker run -p 8080:8080 ${IMAGE_NAME}:${TAG}"
