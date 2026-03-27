# Changelog

## [1.2.1](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/compare/v1.2.0...v1.2.1) (2026-03-27)


### Bug Fixes

* **ci:** publish release images from release workflow ([e8b29e8](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/e8b29e866d7c9be5139c2de481d81f9b1997fa87))

## [1.2.0](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/compare/v1.1.1...v1.2.0) (2026-03-27)


### Features

* tune llama.cpp runtime defaults ([bc4bf1a](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/bc4bf1a3e120fc0f766473f82af30273c236793e))

## 1.1.1 (2026-03-27)

### Features

- add the fast-start CPU-only `llama.cpp` image with baked-in Unsloth QAT GGUF weights
- align CI/CD and image publishing around the `cogtrix-gemma3-270m` image name

### Improvements

- raise the default context window to 4096 and document `LLAMA_ARG_CTX_SIZE`
- rename the primary image build script to `scripts/build-container-image.sh`
- move the release-please config under `.github/` and point the workflow at the new path
