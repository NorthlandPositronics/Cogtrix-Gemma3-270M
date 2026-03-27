# Gemma 3 270M Minimal Container Image

## Multi-Architecture Docker Build Configuration

This project ships two build paths:
- a legacy PyTorch image
- a primary fast-start llama.cpp image for CI validation

## Quick Start

### Prerequisites

- Docker 20.10+ with Buildx support
- At least 15GB free disk space
- 8GB+ RAM recommended

### Build for Current Architecture

```bash
./scripts/build.sh

# Faster-start llama.cpp variant (CPU-only, GGUF, OpenAI API)
# Defaults: GGUF_REPO=unsloth/gemma-3-270m-it-qat-GGUF, GGUF_VARIANT=Q4_K_M
./scripts/build-container-image.sh
# Override (optional):
# GGUF_REPO=your/repo GGUF_VARIANT=Q4_K_S ./scripts/build-container-image.sh
# Context window (default 4096) can be overridden at run time:
# docker run -e LLAMA_ARG_CTX_SIZE=8192 -p 8080:8080 cogtrix-gemma3-270m
```

### Build and Push Multi-Architecture Images

Use CI for tagged release images. For manual multi-arch publishing, use `docker buildx` directly.

## Usage

### Run Container

```bash
# Basic inference
docker run -it cogtrix-gemma3-270m python inference.py --prompt "Hello, how are you?"

# Interactive mode
docker run -it cogtrix-gemma3-270m python inference.py --interactive

# Fast-start OpenAI-compatible server
docker run -p 8080:8080 cogtrix-gemma3-270m

# Override context window (default 4096)
docker run -e LLAMA_ARG_CTX_SIZE=8192 -p 8080:8080 cogtrix-gemma3-270m
```

### Custom Parameters

```bash
docker run --rm cogtrix-gemma3-270m python inference.py \
  --prompt "Explain quantum computing" \
  --max-tokens 100 \
  --temperature 0.8
```

## Architecture Support

| Architecture | Platform Flag | Status |
|--------------|---------------|--------|
| x86_64 | linux/amd64 | ✅ Supported |
| aarch64 | linux/arm64 | ✅ Supported |

## Image Specifications

- **Primary runtime**: `llama.cpp` + GGUF
- **Default model source**: `unsloth/gemma-3-270m-it-qat-GGUF`
- **Default quantization**: `Q4_K_M`
- **Default context**: `4096`
- **Legacy path**: PyTorch-based image remains available

## Build Options

| Option | Description | Default |
|--------|-------------|---------|
| `IMAGE_NAME` | Output image name | `cogtrix-gemma3-270m` |
| `TAG` | Output tag | `latest` |
| `GGUF_REPO` | Build-time GGUF source repo | `unsloth/gemma-3-270m-it-qat-GGUF` |
| `GGUF_VARIANT` | Build-time GGUF quantization | `Q4_K_M` |
| `LLAMA_ARG_CTX_SIZE` | Runtime default context window | `4096` |

## Troubleshooting

### Common Issues

**Issue**: Build fails on ARM Mac (M1/M2)
- **Solution**: Use `--platform linux/arm64` explicitly

**Issue**: Model not found
- **Solution**: Ensure you have accepted the Gemma license on Hugging Face and have valid credentials.

### Debug Build

```bash
# Build with debug output
docker build --progress=plain -t cogtrix-gemma3-270m .
```

## Performance

Measured fast-start image on a 2 vCPU runner-class host:

| Metric | Value |
|--------|-------|
| Startup to `/v1/models` ready | ~1.06 s |
| 64-token completion latency | ~0.87 s |
| Throughput | ~73 tok/s |

## Security

- Non-root user (`appuser:appgroup`)
- Lean runtime image
- Model weights baked into image (no runtime downloads)

## License

MIT License. Model weights subject to Google's Gemma Terms of Use.
