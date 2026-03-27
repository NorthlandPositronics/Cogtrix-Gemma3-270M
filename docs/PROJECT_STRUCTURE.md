# Gemma 3 270M Minimal Container - Project Structure

```
.
├── README.md              # Main documentation
├── BUILD.md               # Build instructions and architecture support
├── LICENSE                # MIT License with Gemma terms notice
├── docker/Dockerfile              # Multi-stage Dockerfile for PyTorch image
├── docker/Dockerfile.llamacpp     # Ultra-fast llama.cpp (GGUF) CPU-only image (Unsloth QAT by default)
├── scripts/build.sh               # Build script for PyTorch image (multi-arch)
├── scripts/build-llamacpp.sh      # Build script for llama.cpp image
├── src/inference.py               # Python inference script
├── src/api_server.py              # OpenAI-compatible FastAPI server
├── requirements.txt               # Python dependencies (PyTorch path)
├── .dockerignore                  # Files to exclude from Docker build
└── .gitignore                     # Git ignore file
```

## File Descriptions

### Core Files
- **Dockerfile**: Multi-stage build for minimal image size
- **inference.py**: Main inference script with CPU/GPU support
- **scripts/build.sh**: Automated build script for single or multi-arch builds

### Documentation
- **README.md**: Project overview, quick start, and usage examples
- **BUILD.md**: Detailed build instructions and troubleshooting
- **LICENSE**: MIT license with Gemma terms compliance notice

### Configuration
- **requirements.txt**: Pinned Python dependencies
- **.dockerignore**: Exclude unnecessary files from Docker context
- **.gitignore**: Standard Python/Git ignore patterns

## Key Features

✅ Minimal image size (~900MB - 1GB)  
✅ Multi-architecture support (x86_64, aarch64)  
✅ CPU-only inference (PyTorch or llama.cpp)  
✅ Model weights baked into image (safetensors or GGUF; default GGUF from Unsloth QAT)  
✅ OpenAI-compatible API endpoints  
✅ Security-focused (non-root user)  
✅ Production-ready  
