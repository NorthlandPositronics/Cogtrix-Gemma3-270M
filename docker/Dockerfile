# syntax=docker/dockerfile:1
# ============================================
# Gemma 3 270M Minimal Container (CPU-Only)
# 4-stage build optimised for minimal image size
# ============================================

# ── Stage 1: builder ─────────────────────────────────────────
# Install Python dependencies, then strip unused torch modules.
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

# --no-compile skips .pyc generation at install time (~200 MB saved)
RUN pip install --no-cache-dir --user --no-compile -r requirements.txt

# Remove files not needed at inference time.
# Only strips items that are NOT imported by torch.__init__ at module level.
# torch>=2.4 imports many subpackages unconditionally (ao, distributed, _dynamo,
# _inductor, onnx, ...) so stripping them causes an ImportError on 'import torch'.
# Safe to remove:
#   torch/test/         77 MB  pure test suite (never imported at runtime)
#   torch/include/      51 MB  C++ headers (only needed for building extensions)
#   test *.so           ~1 MB  test-only shared libraries
#   accelerate           4 MB  not used by this project
#   *.dist-info         15 MB  pip metadata (unused at runtime)
RUN SITE=/root/.local/lib/python3.11/site-packages && \
    rm -rf  "$SITE/torch/test" \
            "$SITE/torch/include" \
            "$SITE/torch/lib/libtorchbind_test.so" \
            "$SITE/torch/lib/libjitbackend_test.so" \
            "$SITE/accelerate" && \
    find /root/.local -name "*.dist-info" -type d -exec rm -rf {} + 2>/dev/null || true

# ── Stage 2: downloader ──────────────────────────────────────
# Fetch model weights via HF token (secret never stored in any image layer).
FROM python:3.11-slim AS downloader

RUN pip install --no-cache-dir "huggingface-hub>=0.28.0"

COPY docker/download_model.py /tmp/download_model.py
RUN --mount=type=secret,id=hf_token python3 /tmp/download_model.py

# ── Stage 3: quantizer ───────────────────────────────────────
# Apply dynamic INT8 quantization to halve the on-disk model size.
# Reuses the already-slimmed builder environment (torch + transformers present).
FROM builder AS quantizer

COPY --from=downloader /model /model
COPY docker/quantize_model.py /tmp/quantize_model.py
RUN python3 /tmp/quantize_model.py

# ── Stage 4: runtime ─────────────────────────────────────────
# Assemble the final image from slimmed packages and quantized model.
FROM python:3.11-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --create-home --shell /bin/bash appuser

WORKDIR /app

# --chown on COPY eliminates the separate RUN chown layer that previously
# duplicated ~575 MB of model data as a new image layer.
COPY --from=builder  --chown=appuser:appgroup /root/.local /home/appuser/.local
COPY                 --chown=appuser:appgroup src/         ./src/
COPY --from=quantizer --chown=appuser:appgroup /model      ./data/model/

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app/src
ENV MODEL_PATH=/app/data/model
ENV OMP_NUM_THREADS=4
ENV MKL_NUM_THREADS=4
# Prevent Python from writing .pyc files into the container filesystem at runtime
ENV PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8080

CMD ["python", "src/api_server.py"]
