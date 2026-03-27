# Changelog

## [1.0.1](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/compare/v1.0.0...v1.0.1) (2026-03-27)


### Bug Fixes

* **release:** restore release-please baseline to 1.1.1 ([3b67bba](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/3b67bbac0e5e180848e6a454ac7fc6a0970564af))

## 1.1.1 (2026-03-27)

### Features

- add the fast-start CPU-only `llama.cpp` image with baked-in Unsloth QAT GGUF weights
- align CI/CD and image publishing around the `cogtrix-gemma3-270m` image name

### Improvements

- raise the default context window to 4096 and document `LLAMA_ARG_CTX_SIZE`
- rename the primary image build script to `scripts/build-container-image.sh`
- move the release-please config under `.github/` and point the workflow at the new path
