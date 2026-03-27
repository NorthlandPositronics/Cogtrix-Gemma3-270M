# Architecture Support Documentation

## Supported Architectures

This project supports the following CPU architectures for the fast-start CPU-only image:

### 1. x86_64 (AMD64)
- **Platform**: `linux/amd64`
- **Status**: Fully supported
- **Use Cases**: Desktops, laptops, servers, cloud instances
- **Performance**: Excellent CPU support

### 2. aarch64 (ARM64)
- **Platform**: `linux/arm64`
- **Status**: Fully supported
- **Use Cases**: Apple Silicon Macs, ARM servers, Raspberry Pi 4/5, AWS Graviton
- **Performance**: Good CPU support

## Building for Each Architecture

### x86_64 (AMD64)

```bash
# Direct build
docker build --platform linux/amd64 -t gemma-3-270m:amd64 .

# Using build script
./scripts/build.sh
```

### aarch64 (ARM64)

```bash
# Direct build
docker build --platform linux/arm64 -t gemma-3-270m:arm64 .

# Using build script
./scripts/build.sh
```

### Multi-Architecture Build

```bash
# Manual Docker Buildx
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t cogtrix-gemma3-270m:latest \
  --push \
  .
```

## Platform-Specific Considerations

### x86_64 (Linux/Windows/macOS)

**CPU Inference**:
- Uses AVX2/AVX-512 instructions when available
- Good performance on modern CPUs
- Memory: ~4-6 GB RAM recommended

### aarch64 (Linux/macOS)

**CPU Inference**:
- Optimized ARM NEON instructions
- Excellent performance on Apple M1/M2/M3
- Good performance on ARM servers
- Memory: ~4-6 GB RAM recommended

## Performance Comparison

| Platform | Architecture | Inference Speed | Notes |
|----------|-------------|-----------------|-------|
| 2 vCPU runner-class host | x86_64 | ~73 tok/s | llama.cpp Q4_K_M, 64-token sample |
| Apple M1 Pro | aarch64 | workload-dependent | expected good CPU support |
| AWS Graviton3 | aarch64 | workload-dependent | expected good CPU support |

## Multi-Arch Image Distribution

### Using Docker Hub

```bash
# Build and push multi-arch manifest
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t your-dockerhub-username/cogtrix-gemma3-270m:latest \
  --push \
  .
```

### Using GitHub Container Registry

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/username/cogtrix-gemma3-270m:latest \
  --push \
  .
```

## Verification

### Check Image Architecture

```bash
# List image details
docker inspect cogtrix-gemma3-270m | grep Architecture

# Run and check inside container
docker run --rm cogtrix-gemma3-270m python -c "import platform; print(platform.machine())"
```

### Verify Multi-Arch Manifest

```bash
# Inspect manifest
docker manifest inspect your-registry/cogtrix-gemma3-270m:latest

# Should show both amd64 and arm64 variants
```

## Troubleshooting Architecture Issues

### Issue: Wrong architecture image pulled

**Symptoms**: Container fails to start with "exec format error"

**Solution**:
```bash
# Pull specific architecture
docker pull --platform linux/amd64 cogtrix-gemma3-270m

# Or build locally for your architecture
docker build --platform linux/$(uname -m) -t cogtrix-gemma3-270m .
```

### Issue: Slow performance on ARM

**Possible causes**:
1. Using x86_64 image on ARM (emulation)
2. Not using hardware acceleration

**Solutions**:
```bash
# Ensure correct architecture image
docker pull --platform linux/arm64 cogtrix-gemma3-270m

# Enable Metal on Apple Silicon
docker run --rm -e METAL_DEVICE_WRAPPER_TYPE=1 cogtrix-gemma3-270m
```

## Future Architecture Support

Potential future architectures:
- riscv64 (RISC-V)
- ppc64le (PowerPC)
- s390x (IBM Z)

These would require:
1. PyTorch support for the architecture
2. Testing and validation
3. CI/CD pipeline updates

## Resources

- [Docker Multi-Platform Builds](https://docs.docker.com/build/building/multi-platform/)
- [PyTorch Architecture Support](https://pytorch.org/docs/stable/notes/cpu.html)
- [Hugging Face Transformers Architecture Notes](https://huggingface.co/docs/transformers/installation)
