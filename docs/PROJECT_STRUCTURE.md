# Gemma 3 270M Minimal Container - Project Structure

```
.
├── README.md              # Main documentation
├── BUILD.md               # Build instructions and architecture support
├── LICENSE                # MIT License with Gemma terms notice
├── docker/Dockerfile              # Multi-stage Dockerfile for PyTorch image
├── docker/Dockerfile.llamacpp     # Ultra-fast llama.cpp (GGUF) CPU-only image (Unsloth QAT by default)
├── scripts/build.sh               # Build script for PyTorch image (tags :latest)
├── scripts/build-container-image.sh      # Build script for llama.cpp image
├── src/inference.py               # Python inference script
├── src/api_server.py              # OpenAI-compatible FastAPI server
├── requirements.txt               # Python dependencies (PyTorch path)
├── .dockerignore                  # Files to exclude from Docker build
└── .gitignore                     # Git ignore file
```

## File Descriptions

### Core Files
- **docker/Dockerfile**: Legacy PyTorch-based build
- **docker/Dockerfile.llamacpp**: Primary fast-start CPU-only build
- **src/inference.py**: Python inference script for the PyTorch path
- **scripts/build.sh**: Legacy PyTorch build script tagged as `latest`
- **scripts/build-container-image.sh**: Primary llama.cpp build script

### Documentation
- **README.md**: Project overview, quick start, and usage examples
- **BUILD.md**: Detailed build instructions and troubleshooting
- **LICENSE**: MIT license with Gemma terms compliance notice

### Configuration
- **requirements.txt**: Pinned Python dependencies
- **.dockerignore**: Exclude unnecessary files from Docker context
- **.gitignore**: Standard Python/Git ignore patterns

## Key Features

✅ Fast-start CPU-only image for CI validation
✅ Multi-architecture support (x86_64, aarch64)
✅ OpenAI-compatible API endpoints
✅ Baked-in GGUF model (default: Unsloth QAT)
✅ Security-focused runtime (non-root user)
