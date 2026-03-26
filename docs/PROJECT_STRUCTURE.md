# Gemma 3 270M Minimal Container - Project Structure

```
.
├── README.md              # Main documentation
├── BUILD.md               # Build instructions and architecture support
├── LICENSE                # MIT License with Gemma terms notice
├── Dockerfile             # Multi-stage Dockerfile for minimal image
├── scripts/build.sh               # Build script with multi-arch support
├── inference.py           # Python inference script
├── requirements.txt       # Python dependencies
├── .dockerignore          # Files to exclude from Docker build
└── .gitignore             # Git ignore file
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
✅ CPU and GPU inference  
✅ Model weights baked into image  
✅ No external dependencies (Ollama, llama.cpp)  
✅ Security-focused (non-root user)  
✅ Production-ready  
