# Gemma 3 270M Minimal Container Image

## Multi-Architecture Docker Build Configuration

This project builds a minimal container image for running the Gemma 3 270M LLM model on both x86_64 and aarch64 architectures.

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
./scripts/build-llamacpp.sh
# Override (optional):
# GGUF_REPO=your/repo GGUF_VARIANT=Q4_K_S ./scripts/build-llamacpp.sh
```

### Build for Specific Architecture

```bash
# x86_64 (AMD64)
./scripts/build.sh --platform linux/amd64

# aarch64 (ARM64)
./scripts/build.sh --platform linux/arm64
```

### Build Multi-Architecture Image

```bash
# Enable Buildx
docker buildx create --name multiarch --use --bootstrap

# Build for both architectures
./scripts/build.sh --multiarch
```

### Build and Push to Registry

```bash
# Push multi-arch image
./scripts/build.sh --multiarch --push

# Or with specific registry
IMAGE_NAME=your-registry/gemma-3-270m-minimal ./scripts/build.sh --multiarch --push
```

## Usage

### Run Container

```bash
# Basic inference
docker run -it gemma-3-270m-minimal python inference.py --prompt "Hello, how are you?"

# With GPU support
docker run --gpus all -it gemma-3-270m-minimal python inference.py --prompt "Hello"

# Interactive mode
docker run -it gemma-3-270m-minimal python inference.py --interactive
```

### Custom Parameters

```bash
docker run --rm gemma-3-270m-minimal python inference.py \
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

- **Base Image**: python:3.11-alpine
- **Estimated Size**: ~900MB - 1GB
- **Model**: Gemma 3 270M (Instruction-Tuned)
- **Model Size**: ~536MB (safetensors format)
- **PyTorch**: 2.4.0 (CPU + CUDA support)
- **Python**: 3.11

## Build Options

| Option | Description | Default |
|--------|-------------|---------|
| `--name` | Image name | gemma-3-270m-minimal |
| `--tag` | Image tag | latest |
| `--platform` | Target platform | local |
| `--multiarch` | Build for multiple architectures | false |
| `--push` | Push to registry | false |

## Troubleshooting

### Common Issues

**Issue**: Build fails on ARM Mac (M1/M2)
- **Solution**: Use `--platform linux/arm64` explicitly

**Issue**: CUDA not available
- **Solution**: Expected on CPU-only systems. Container auto-detects hardware.

**Issue**: Model not found
- **Solution**: Ensure you have accepted the Gemma license on Hugging Face and have valid credentials.

### Debug Build

```bash
# Build with debug output
docker build --progress=plain -t gemma-3-270m-minimal .
```

## Performance

Expected inference speeds:

| Hardware | Architecture | Tokens/Second |
|----------|-------------|---------------|
| CPU (4 cores) | x86_64 | 5-10 |
| CPU (8 cores) | x86_64 | 10-15 |
| GPU (RTX 3060) | x86_64 | 50-80 |
| Apple M1/M2 | aarch64 | 15-25 |

## Security

- Non-root user (appuser:appgroup)
- Minimal base image (Alpine)
- No unnecessary packages
- Model weights baked into image (no runtime downloads)

## License

MIT License. Model weights subject to Google's Gemma Terms of Use.
