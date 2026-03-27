# Gemma 3 270M Minimal Container

A minimal Docker container for running the Gemma 3 270M LLM model with OpenAI-compatible API support.

## 🚀 Quick Start

### Build the Image

```bash
# PyTorch-based image (current default)
./scripts/build.sh

# Ultra-fast startup (llama.cpp + GGUF, CPU-only, OpenAI-compatible)
# Defaults to Unsloth QAT GGUF (unsloth/gemma-3-270m-it-qat-GGUF, Q4_K_M)
./scripts/build-container-image.sh
# Override GGUF repo/variant if needed:
# GGUF_REPO=some/other-repo GGUF_VARIANT=Q4_K_S ./scripts/build-container-image.sh
# Build a host-optimized native llama.cpp binary if you control the CPU target:
# GGML_NATIVE=ON ./scripts/build-container-image.sh
```

### Run the Container

```bash
# CPU-only mode
docker run -it cogtrix-gemma3-270m python src/inference.py --prompt "Hello"

# llama.cpp OpenAI server (fast startup, CPU-only, Unsloth QAT GGUF baked in)
docker run -p 8080:8080 cogtrix-gemma3-270m
# Override context window if needed (default 4096):
#   docker run -e LLAMA_ARG_CTX_SIZE=8192 -p 8080:8080 cogtrix-gemma3-270m
# Useful runtime overrides:
#   docker run -e LLAMA_ARG_PARALLEL=1 -e LLAMA_ARG_NO_WARMUP=1 -p 8080:8080 cogtrix-gemma3-270m

# Interactive mode
docker run -it cogtrix-gemma3-270m python src/inference.py --interactive

# API server mode
docker run -p 8080:8080 cogtrix-gemma3-270m python src/api_server.py
```

### Test the API

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-270m",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7
  }'
```

## 📁 Project Structure

```
.
├── scripts/                 # Build helpers
│   ├── build.sh             # PyTorch image build script (tags :latest)
│   └── build-container-image.sh    # llama.cpp image build script
├── requirements.txt         # Python dependencies
├── .github/               # GitHub Actions workflows
├── .gitignore            # Git ignore rules
├── .dockerignore         # Docker ignore rules
├── docker/               # Docker-related files
│   ├── Dockerfile        # Multi-stage PyTorch Dockerfile
│   ├── Dockerfile.llamacpp # Fast-start llama.cpp image
│   └── download_gguf.py  # Build-time GGUF fetch helper
├── src/                  # Source code
│   ├── inference.py      # Direct inference script
│   ├── api_server.py     # OpenAI-compatible API server
│   ├── api_server_mock.py # Mock API for testing
│   ├── test_inference.py # Inference tests
│   └── setup-permissions.sh # Permission setup script
├── docs/                 # Documentation
│   ├── README.md         # This file
│   ├── API_REFERENCE.md  # API documentation
│   ├── API_SERVER.md     # API server guide
│   ├── ARCHITECTURE.md   # System architecture
│   ├── BUILD.md          # Build instructions
│   ├── CONTRIBUTING.md   # Contribution guidelines
│   ├── DEPLOYMENT.md     # Deployment guide
│   ├── PROJECT_STRUCTURE.md # Project structure
│   ├── PROJECT_SUMMARY.md # Project summary
│   ├── QUICK_REFERENCE.md # Quick reference
│   └── TESTING_RESULTS.md # Test results
├── examples/             # Example usage
```

## 🔧 Features

- **Minimal Image Size**: optimized fast-start llama.cpp image for CI validation
- **Fast-Start Variant**: llama.cpp + GGUF image starts in about a second on 2 vCPU runners
- **Tuned Defaults**: llama.cpp path defaults to `threads-batch=2`, `batch=64`, `ubatch=64`, `parallel=1`, `no-warmup=1`
- **Multi-Architecture**: Supports x86_64 and aarch64
- **CPU Only**: no CUDA, ROCm, or MPS runtime path in the optimized image
- **OpenAI-Compatible API**: drop-in replacement for OpenAI API
- **Streaming Support**: Server-Sent Events (SSE) for streaming responses
- **Model Embedded**: Gemma 3 270M weights baked into the image

## 📊 Image Size Breakdown

| Component | Size |
|-----------|------|
| Runtime base + llama.cpp | lean Debian runtime |
| GGUF weights (Q4_K_M) | ~235 MB class |
| **Total** | significantly smaller than the PyTorch image |

## llama.cpp Tuning

The fast-start image is tuned for small CPU runners:

- `LLAMA_ARG_CTX_SIZE=4096`
- `LLAMA_ARG_THREADS=2`
- `LLAMA_ARG_THREADS_BATCH=2`
- `LLAMA_ARG_BATCH=64`
- `LLAMA_ARG_UBATCH=64`
- `LLAMA_ARG_PARALLEL=1`
- `LLAMA_ARG_FLASH_ATTN=auto`
- `LLAMA_ARG_NO_WARMUP=1`

If you control the deployment CPU target, you can also build a host-optimized binary:

```bash
GGML_NATIVE=ON ./scripts/build-container-image.sh
```

That build is CPU-specific and should be treated as an optimization variant, not a universally portable image.

## 📖 Documentation

- [API Reference](docs/API_REFERENCE.md) - Complete API documentation
- [API Server Guide](docs/API_SERVER.md) - API server setup and usage
- [Build Instructions](docs/BUILD.md) - Detailed build guide
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Architecture Overview](docs/ARCHITECTURE.md) - System design

## 🧪 Testing

```bash
# Run inference tests
docker run -it cogtrix-gemma3-270m python src/test_inference.py

# Test API endpoints
curl http://localhost:8080/health
curl http://localhost:8080/v1/models
```

## 🛠️ Development

```bash
# Build development image
docker build -t gemma-3-270m-dev -f docker/Dockerfile.dev .

# Run with model volume
docker run -it \
  -v /path/to/model:/app/data/model \
  gemma-3-270m-dev python src/inference.py
```

## 📄 License

MIT License - See [LICENSE](docs/LICENSE) for details.

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.
