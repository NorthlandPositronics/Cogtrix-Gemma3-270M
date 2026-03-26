# syntax=docker/dockerfile:1
# ============================================
# Gemma 3 270M Minimal Container (CPU-Only)
# Optimized for minimal image size - CPU inference only
# ============================================

# Stage 1: Builder — install Python deps
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Model downloader — fetch weights using HF token (never baked into final image)
FROM python:3.11-slim AS downloader

RUN pip install --no-cache-dir "huggingface-hub>=0.28.0"

# HF_TOKEN is injected as a BuildKit secret — never stored in any image layer.
COPY docker/download_model.py /tmp/download_model.py
RUN --mount=type=secret,id=hf_token python3 /tmp/download_model.py

# Stage 3: Runtime — assemble the final image
FROM python:3.11-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy source code
COPY src/ ./src/

# Copy model weights from downloader stage
COPY --from=downloader /model ./data/model/

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app/src:$PYTHONPATH
ENV MODEL_PATH=/app/data/model
ENV OMP_NUM_THREADS=4
ENV MKL_NUM_THREADS=4

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

CMD ["python", "src/inference.py"]
