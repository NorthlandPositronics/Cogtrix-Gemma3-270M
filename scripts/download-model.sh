#!/bin/bash
# Download Gemma 3 270M model weights for local development (outside Docker).
#
# NOTE: The Docker image downloads its own weights at build time via BuildKit
# secret — you do NOT need to run this script before `make build`.
# Use this only if you want to run inference.py or api_server.py directly
# on the host (without Docker).

set -e

echo "=========================================="
echo "  Downloading Gemma 3 270M Model Weights"
echo "=========================================="

if [ -z "$HF_TOKEN" ]; then
    echo "ERROR: HF_TOKEN environment variable is not set."
    echo ""
    echo "To download the model:"
    echo "  1. Accept the Gemma license: https://huggingface.co/google/gemma-3-270m-it"
    echo "  2. Generate a token: https://huggingface.co/settings/tokens"
    echo "  3. export HF_TOKEN='hf_...'"
    echo "  4. Re-run this script"
    echo ""
    exit 1
fi

mkdir -p data/model

echo "Downloading to data/model/ ..."
export PATH="$PATH:$HOME/.local/bin"
huggingface-cli download google/gemma-3-270m-it --local-dir data/model --token "$HF_TOKEN" --quiet

echo ""
echo "Model downloaded successfully to data/model/"
echo ""
echo "Files:"
ls -lh data/model/
