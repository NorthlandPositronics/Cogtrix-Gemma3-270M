# ============================================
# Gemma 3 270M Minimal Container (CPU-Only)
# Optimized for minimal image size - CPU inference only
# ============================================

# Stage 1: Builder
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (CPU-only PyTorch)
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Install minimal runtime dependencies (no CUDA libs needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy source code
COPY src/ ./src/

# Copy model weights (embedded in image)
COPY data/model/ ./data/model/

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app/src:$PYTHONPATH
ENV MODEL_PATH=/app/data/model
ENV OMP_NUM_THREADS=4
ENV MKL_NUM_THREADS=4

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose API port
EXPOSE 8080

# Default command (can be overridden)
CMD ["python", "src/inference.py"]
