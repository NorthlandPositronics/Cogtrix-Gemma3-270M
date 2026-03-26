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
docker run -it gemma-3-270m-minimal python src/inference.py --prompt "Hello"

# Interactive mode
docker run -it gemma-3-270m-minimal python src/inference.py --interactive

# API server mode
docker run -p 8080:8080 gemma-3-270m-minimal python src/api_server.py
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
├── build.sh                 # Build script for multi-architecture images
├── requirements.txt         # Python dependencies
├── Makefile               # Build automation
├── VERSION                # Project version
├── .github/               # GitHub Actions workflows
├── .gitignore            # Git ignore rules
├── .dockerignore         # Docker ignore rules
├── docker/               # Docker-related files
│   └── Dockerfile        # Multi-stage Dockerfile
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
└── data/                 # Data files and model weights
```

## 🔧 Features

- **Minimal Image Size**: ~900MB - 1GB optimized container
- **Multi-Architecture**: Supports x86_64 and aarch64
- **CPU & GPU**: Runs on both CPU and GPU (CUDA)
- **OpenAI-Compatible API**: Drop-in replacement for OpenAI API
- **Streaming Support**: Server-Sent Events (SSE) for streaming responses
- **Model Embedded**: Gemma 3 270M weights baked into the image

## 📊 Image Size Breakdown

| Component | Size |
|-----------|------|
| Base (python:3.11-alpine) | ~45 MB |
| PyTorch (CPU+GPU) | ~200-300 MB |
| Transformers | ~100 MB |
| Gemma 3 270M Weights | ~536 MB |
| **Total** | **~900 MB - 1 GB** |

## 📖 Documentation

- [API Reference](docs/API_REFERENCE.md) - Complete API documentation
- [API Server Guide](docs/API_SERVER.md) - API server setup and usage
- [Build Instructions](docs/BUILD.md) - Detailed build guide
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Architecture Overview](docs/ARCHITECTURE.md) - System design

## 🧪 Testing

```bash
# Run inference tests
docker run -it gemma-3-270m-minimal python src/test_inference.py

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
