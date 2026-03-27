# Changelog

## 1.0.0 (2026-03-27)


### Features

* BuildKit secret download of Gemma 3 weights + CI publish ([6cb2a31](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/6cb2a31e01d5da45bc73baab348d21882904ec95))
* BuildKit secret download of Gemma 3 weights + CI publish ([6cb2a31](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/6cb2a31e01d5da45bc73baab348d21882904ec95))
* bump default llama.cpp context to 4096 and document override ([c7ccb2f](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/c7ccb2f9441595fa129cf36094fc8e9e78814495))
* **docker:** cut image size by ~50% via INT8 quantization + torch cleanup ([2cb7589](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/2cb7589ca8f815aefa73ecc260ec7503a4623784))
* download model weights at build time via BuildKit secret ([69a995d](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/69a995dc031f297ad1342cd1849c2ef389a4b4a8))
* fast-start llama.cpp image with Unsloth QAT GGUF ([c84db4a](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/c84db4a6bba428f70e0c1072fd9d9ca2ffdd2515))
* initial release — Gemma 3 270M OpenAI-compatible container ([772b643](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/772b643728bf54f7318e41dcf66bef2d2cb8b58d))


### Bug Fixes

* **api:** add trust_remote_code to from_config and error logging for inference ([ee5a7c9](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/ee5a7c9a9d0dcd4f4f2165259cc88a8684c5d07a))
* **api:** cast model to float32 before quantize_dynamic at load time ([41896a8](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/41896a8dde7e7cbce938e27628685f059c2f8833))
* **ci:** use buildx imagetools create for multi-arch manifest ([c899bc9](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/c899bc9b239ccdd3ecf6e73f3a5d410a2a3180c9))
* **deps:** use torch&gt;=2.4.0 for arm64 compatibility ([5867bce](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/5867bce92231532f102a7cd64d78f3dede468226))
* **dockerfile:** unblock download_model.py from .dockerignore; fix PYTHONPATH ([c7d4f10](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/c7d4f10ce893a4b2a5e189f328aeecd6d8cbfd73))
* **dockerfile:** use COPY script for model download to fix -c multiline issue ([723e0e5](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/723e0e5ce6d32d9abeacaf032f1755a8d8013da4))
* **dockerfile:** use Python API for model download instead of huggingface-cli ([4e01c39](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/4e01c39e1331d0fb3b8759fa064b5c667e148e88))
* **docker:** final image build fix — minimal safe stripping ([d0bf5d3](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/d0bf5d3ab50c825f07aec5d8dbd1e61fc398fa15))
* **docker:** final image build fix — minimal safe stripping ([d0bf5d3](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/d0bf5d3ab50c825f07aec5d8dbd1e61fc398fa15))
* **docker:** keep torch/distributed — breaks import torch on &gt;=2.4 ([5302eeb](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/5302eeba8c555bd2055304d6abc81e9207ed2c68))
* **docker:** keep torch/distributed — breaks import torch on &gt;=2.4 ([5302eeb](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/5302eeba8c555bd2055304d6abc81e9207ed2c68))
* **docker:** keep torch/distributed — required by torch&gt;=2.4 import chain ([91ed659](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/91ed659bae49107ffce9206a7ead44e22b593103))
* **docker:** minimal safe torch stripping only ([8c3eea0](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/8c3eea0daa0e3eeec1a8303f3ec03bf598dcbc59))
* **docker:** minimal safe torch stripping only ([8c3eea0](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/8c3eea0daa0e3eeec1a8303f3ec03bf598dcbc59))
* **docker:** minimal safe torch stripping only ([eef69d8](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/eef69d8e0a0993a1d08e25a58b870ee8a659c03b))
* **docker:** only strip torch items safe to remove in torch&gt;=2.4 ([2acec70](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/2acec70521c013f3ea5fb3d37b7bd2dd26088e37))
* **docker:** only strip torch items safe to remove in torch&gt;=2.4 ([2acec70](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/2acec70521c013f3ea5fb3d37b7bd2dd26088e37))
* **docker:** only strip torch items safe to remove in torch&gt;=2.4 ([64edbc8](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/64edbc8118af5b455505b1ec4d4bd11f87568c21))
* **docker:** quantize_model.py device_map removal — fixes image build ([dcdb033](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/dcdb0338226df81bb44dfb8209c272983ce04c4c))
* **docker:** quantize_model.py device_map removal — fixes image build ([dcdb033](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/dcdb0338226df81bb44dfb8209c272983ce04c4c))
* **docker:** remove device_map from quantize_model.py ([328a00a](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/328a00aea79da5a92ca8001e6406713d24f67200))
* **docker:** remove device_map from quantize_model.py ([328a00a](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/328a00aea79da5a92ca8001e6406713d24f67200))
* **docker:** remove device_map from quantize_model.py ([ec898fa](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/ec898fa34376e22c3105bcff505cf3c362add94a))
* **docker:** safe torch stripping — unblocks image build ([500196e](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/500196ef2069c9335f02874af2ab6cbcdb03c724))
* **docker:** safe torch stripping — unblocks image build ([500196e](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/500196ef2069c9335f02874af2ab6cbcdb03c724))
* **docker:** use qnnpack backend for INT8 quantization on ARM64 ([7bcf69c](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/commit/7bcf69c9e501a06c4614e7287ac192fa463e2bcf))

## [1.1.0](https://github.com/NorthlandPositronics/Cogtrix-Gemma3-270M/compare/v1.0.0...v1.1.0) (unreleased)

- add llama.cpp CPU-only image with Unsloth QAT GGUF default
- faster startup (~1s) and docs update
- version bump
