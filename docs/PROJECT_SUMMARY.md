# Project Summary - Gemma 3 270M Minimal Container

## Overview

This project provides a container image optimized for CI validation runs with Gemma 3 270M. The primary path is a CPU-only, OpenAI-compatible llama.cpp image using a baked-in GGUF model for fast startup, low memory use, and predictable inference on small GitHub runners.

## Key Features

✅ **Fast Start**: About a second to readiness on a 2 vCPU runner
✅ **Multi-Architecture**: Supports x86_64 and aarch64
✅ **CPU Only**: No GPU runtime path in the optimized image
✅ **Baked Model**: GGUF weights included in the image
✅ **Production Ready**: Complete with tests, docs, and CI/CD
✅ **Lean Runtime**: llama.cpp path avoids heavy PyTorch startup costs

## Project Files

### Core Files
- `docker/Dockerfile` - Legacy PyTorch-based Docker build
- `docker/Dockerfile.llamacpp` - Primary fast-start llama.cpp GGUF build
- `src/inference.py` - Python inference script for the PyTorch path
- `scripts/build.sh` - Legacy PyTorch image build script (`:latest`)
- `scripts/build-container-image.sh` - Build the llama.cpp image (CPU-only, OpenAI API)
- `requirements.txt` - Python dependencies for the PyTorch path

### Documentation
- `README.md` - Main project documentation
- `BUILD.md` - Build instructions and troubleshooting
- `DEPLOYMENT.md` - Deployment guide for various platforms
- `ARCHITECTURE.md` - Architecture support details
- `QUICK_REFERENCE.md` - Quick command reference
- `PROJECT_STRUCTURE.md` - File organization guide
- `CONTRIBUTING.md` - Contribution guidelines

### Configuration
- `.dockerignore` - Docker build exclusions
- `.gitignore` - Git ignore patterns
- `LICENSE` - MIT License with Gemma terms

### Testing
- `test_inference.py` - Verification test suite

### GitHub Integration
- `.github/workflows/ci.yml` - CI and image publishing pipeline
- `.github/workflows/release-please.yml` - release-please automation
- `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report template
- `.github/ISSUE_TEMPLATE/feature_request.md` - Feature request template

### Utilities
- `verify-project.sh` - Project verification script
- `.release-please-manifest.json` - Release version manifest

## Quick Start

### Build
```bash
# For current architecture
./scripts/build.sh

# For specific architecture
./scripts/build.sh --platform linux/amd64  # x86_64
./scripts/build.sh --platform linux/arm64  # aarch64

# Multi-architecture
./scripts/build.sh --multiarch
```

### Run
```bash
# Basic inference
docker run -it cogtrix-gemma3-270m python inference.py --prompt "Hello"

# Interactive mode
docker run -it cogtrix-gemma3-270m python inference.py --interactive

# Fast-start OpenAI-compatible server
docker run -p 8080:8080 cogtrix-gemma3-270m
```

## Technical Specifications

### Image Composition
| Component | Size |
|-----------|------|
| llama.cpp runtime | lean native binary |
| GGUF model (Q4_K_M) | ~235 MB class |
| **Total** | much smaller than the legacy PyTorch image |

### Supported Platforms
- **x86_64**: Linux, Windows (WSL2), macOS (Intel)
- **aarch64**: Linux (ARM), macOS (Apple Silicon), AWS Graviton

### Dependencies
- llama.cpp
- GGUF model weights
- OpenBLAS runtime
- Python 3.11 only for helper tooling / legacy path

## Performance

| Platform | Architecture | Tokens/Second |
|----------|-------------|---------------|
| 2 vCPU runner-class host | x86_64 | ~73 |
| Apple M1/M2 | aarch64 | workload-dependent |

## Usage Examples

### Simple Inference
```bash
docker run --rm cogtrix-gemma3-270m \
  python inference.py \
  --prompt "Explain quantum computing" \
  --max-tokens 100 \
  --temperature 0.7
```

### Interactive Mode
```bash
docker run -it cogtrix-gemma3-270m \
  python inference.py --interactive
```

## Deployment Options

1. **Local**: Docker Desktop, Docker Engine
2. **Cloud**: AWS EC2, GCP, Azure
3. **Kubernetes**: GKE, EKS, AKS
4. **Edge**: Raspberry Pi and other ARM edge devices
5. **Serverless**: Cloud Run, AWS Lambda (with limitations)

## Security

- Non-root user (appuser:appgroup)
- Minimal base image (Alpine Linux)
- No external dependencies at runtime
- Model weights baked into image
- No unnecessary packages

## Testing

```bash
# Run test suite inside container
docker run --rm cogtrix-gemma3-270m python test_inference.py

# Verify project structure
./verify-project.sh
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License (see LICENSE file). Note: Gemma model weights are subject to Google's Gemma Terms of Use.

## Resources

- [Gemma 3 Technical Report](https://arxiv.org/abs/2503.19786)
- [Hugging Face Model](https://huggingface.co/google/gemma-3-270m-it)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)

## Acknowledgments

- Google DeepMind for Gemma model
- Hugging Face for Transformers library
- PyTorch community
- Docker community for Buildx

---

**Ready to deploy!** Follow the Quick Start section above to get started.
