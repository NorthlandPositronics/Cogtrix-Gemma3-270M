# Gemma 3 270M Minimal Container - Quick Reference

## One-Liner Commands

### Build
```bash
# Quick build for current architecture
docker build -t cogtrix-gemma3-270m .

# Build for specific architecture
docker build --platform linux/amd64 -t cogtrix-gemma3-270m .

# Multi-arch build
docker buildx build --platform linux/amd64,linux/arm64 -t cogtrix-gemma3-270m --load .

# Ultra-fast llama.cpp build (GGUF, CPU-only)
./scripts/build-container-image.sh
# (defaults to unsloth/gemma-3-270m-it-qat-GGUF, variant Q4_K_M)
```

### Run
```bash
# Quick test
docker run --rm cogtrix-gemma3-270m python inference.py --prompt "Hello"

# Interactive mode
docker run -it cogtrix-gemma3-270m python inference.py --interactive

# OpenAI-compatible llama.cpp server (fast start)
docker run -p 8080:8080 cogtrix-gemma3-270m
# Increase context (default 4096):
#   docker run -e LLAMA_ARG_CTX_SIZE=8192 -p 8080:8080 cogtrix-gemma3-270m
# Override GGUF at runtime if built that way:
#   GGUF_REPO=... GGUF_VARIANT=Q4_K_S ./scripts/build-container-image.sh
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
| llama.cpp runtime | lean native binary |
| GGUF model (Q4_K_M) | ~235 MB class |
| **Total** | much smaller than the PyTorch image |

## Troubleshooting Quick Fixes

**Issue**: Model not found
```bash
# Ensure you've accepted the Gemma license on Hugging Face
# and have valid credentials
```

**Issue**: Out of memory
```bash
# Reduce context or generation size
docker run -e LLAMA_ARG_CTX_SIZE=2048 -p 8080:8080 cogtrix-gemma3-270m
```

## File Reference

| File | Purpose |
|------|---------|
| `docker/Dockerfile` | Legacy PyTorch Dockerfile |
| `docker/Dockerfile.llamacpp` | Primary fast-start Dockerfile |
| `scripts/build.sh` | Legacy PyTorch build script |
| `scripts/build-container-image.sh` | Primary llama.cpp build script |
| `requirements.txt` | Python dependencies |
| `README.md` | Main documentation |
| `BUILD.md` | Build instructions |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLAMA_ARG_CTX_SIZE` | Runtime context window | 4096 |
| `GGUF_REPO` | Build-time GGUF repository override | unsloth/gemma-3-270m-it-qat-GGUF |
| `GGUF_VARIANT` | Build-time GGUF quantization override | Q4_K_M |

## Performance Tips

1. **Context**: Lower `LLAMA_ARG_CTX_SIZE` if you need less RAM or faster cold start.
2. **Threads**: Keep `LLAMA_ARG_THREADS=2` on GitHub-hosted 2 vCPU runners.
3. **Quantization**: Keep `Q4_K_M` unless you have measured a better tradeoff.
4. **Batch size**: Reduce `LLAMA_ARG_BATCH` if you see memory pressure.

## Security Notes

- Container runs as non-root user (`appuser:appgroup`)
- No external network access needed at runtime (model baked in)
- Minimal runtime surface
