# Gemma 3 270M Minimal Container

A minimal Docker container for running the Gemma 3 270M LLM model with OpenAI-compatible API support.

## 🚀 Quick Start

### Build the Image

```bash
./scripts/build.sh
```

### Run the Container

```bash
# CPU-only mode
docker run -it cogtrix-gemma3-270m python src/inference.py --prompt "Hello"

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
│   ├── build.sh             # PyTorch image build script
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
└── examples/             # Example usage
```

## 🔧 Features

- **Minimal Image Size**: optimized fast-start llama.cpp image for CI validation
- **Multi-Architecture**: Supports x86_64 and aarch64
- **CPU Only**: optimized image has no GPU runtime path
- **OpenAI-Compatible API**: Drop-in replacement for OpenAI API
- **Streaming Support**: Server-Sent Events (SSE) for streaming responses
- **Model Embedded**: Gemma 3 270M weights baked into the image

## 📊 Image Size Breakdown

| Component | Size |
|-----------|------|
| llama.cpp runtime | lean native binary |
| GGUF model (Q4_K_M) | ~235 MB class |
| **Total** | much smaller than the legacy PyTorch image |

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
