# Changelog

## 1.1.1 (2026-03-27)

### Features

- add the fast-start CPU-only `llama.cpp` image with baked-in Unsloth QAT GGUF weights
- align CI/CD and image publishing around the `cogtrix-gemma3-270m` image name

### Improvements

- raise the default context window to 4096 and document `LLAMA_ARG_CTX_SIZE`
- rename the primary image build script to `scripts/build-container-image.sh`
- move the release-please config under `.github/` and point the workflow at the new path
