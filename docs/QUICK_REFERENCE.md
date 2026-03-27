# Gemma 3 270M Minimal Container - Quick Reference

## One-Liner Commands

### Build
```bash
# Quick build for current architecture
docker build -t gemma-3-270m-minimal .

# Build for specific architecture
docker build --platform linux/amd64 -t gemma-3-270m-minimal .

# Multi-arch build
docker buildx build --platform linux/amd64,linux/arm64 -t gemma-3-270m-minimal --load .

# Ultra-fast llama.cpp build (GGUF, CPU-only)
./scripts/build-llamacpp.sh
# (defaults to unsloth/gemma-3-270m-it-qat-GGUF, variant Q4_K_M)
```

### Run
```bash
# Quick test
docker run --rm gemma-3-270m-minimal python inference.py --prompt "Hello"

# Interactive mode
docker run -it gemma-3-270m-minimal python inference.py --interactive

# With GPU
docker run --gpus all -it gemma-3-270m-minimal python inference.py --prompt "Hello"

# OpenAI-compatible llama.cpp server (fast start)
docker run -p 8080:8080 gemma-3-270m-llamacpp
# Increase context (default 4096):
#   docker run -e LLAMA_ARG_CTX_SIZE=8192 -p 8080:8080 gemma-3-270m-llamacpp
# Override GGUF at runtime if built that way:
#   GGUF_REPO=... GGUF_VARIANT=Q4_K_S ./scripts/build-llamacpp.sh
```

## Common Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--prompt` | Input text | "Hello, how can I assist you today?" |
| `--max-tokens` | Max tokens to generate | 256 |
| `--temperature` | Sampling temperature (0.0-2.0) | 0.7 |
| `--top-k` | Top-k sampling | 50 |
| `--top-p` | Top-p sampling | 0.95 |
| `--do-sample` | Enable sampling | False |
| `--interactive` | Interactive mode | False |

## Architecture Support

| Architecture | Platform Flag | Tested |
|--------------|---------------|--------|
| x86_64 | linux/amd64 | ✓ |
| aarch64 | linux/arm64 | ✓ |

## Image Size Reference

| Component | Size |
|-----------|------|
| Base (python:3.11-alpine) | ~45 MB |
| PyTorch | ~200-300 MB |
| Transformers | ~100 MB |
| Model Weights | ~536 MB |
| **Total** | **~900 MB - 1 GB** |

## Troubleshooting Quick Fixes

**Issue**: Model not found
```bash
# Ensure you've accepted the Gemma license on Hugging Face
# and have valid credentials
```

**Issue**: CUDA not available
```bash
# Expected on CPU-only systems. Container auto-detects hardware.
```

**Issue**: Out of memory
```bash
# Reduce --max-tokens parameter
docker run --rm gemma-3-270m-minimal python inference.py --prompt "Hello" --max-tokens 50
```

## File Reference

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage build definition |
| `build.sh` | Build script with multi-arch support |
| `inference.py` | Main inference script |
| `test_inference.py` | Verification tests |
| `requirements.txt` | Python dependencies |
| `Makefile` | Build automation |
| `README.md` | Main documentation |
| `BUILD.md` | Build instructions |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Path to model directory | /app/model |
| `HF_HOME` | Hugging Face cache directory | /app/.cache/huggingface |
| `TORCH_HOME` | PyTorch cache directory | /app/.cache/torch |

## Performance Tips

1. **GPU**: Use `--gpus all` flag for GPU acceleration
2. **Sampling**: Use `--do-sample` for more diverse outputs
3. **Temperature**: Lower values (0.3-0.5) for more deterministic outputs
4. **Max tokens**: Adjust based on your needs to save memory

## Security Notes

- Container runs as non-root user (appuser:appgroup)
- No external network access needed (model baked in)
- Minimal attack surface (Alpine base)
