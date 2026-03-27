"""
Quantize Gemma 3 270M weights to dynamic INT8 at Docker build time.

Reduces on-disk model size from ~512 MB (bfloat16 safetensors) to ~260 MB
(INT8 linear-layer weights saved via torch.save).  Runs inside the builder
stage — no HF token is needed here, the model files come from the downloader
stage via COPY.

The inference code (inference.py / api_server.py) automatically detects
model_quantized.pt and loads the quantized model at runtime.
"""

import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM

MODEL_DIR = Path("/model")
ORIGINAL = MODEL_DIR / "model.safetensors"
QUANTIZED = MODEL_DIR / "model_quantized.pt"


def main() -> None:
    if not ORIGINAL.exists():
        print(f"ERROR: {ORIGINAL} not found", file=sys.stderr)
        sys.exit(1)

    original_mb = ORIGINAL.stat().st_size / 1024 / 1024
    print(f"Loading model ({original_mb:.0f} MB, bfloat16) for quantization…", flush=True)

    # float32 is required by torch.quantization.quantize_dynamic.
    # device_map and low_cpu_mem_usage are omitted intentionally: both require
    # accelerate / torch.distributed which are stripped from the builder stage
    # to reduce image size.  The quantizer stage inherits from builder, so CPU
    # is the only available device anyway.
    model = AutoModelForCausalLM.from_pretrained(
        str(MODEL_DIR),
        torch_dtype=torch.float32,
        trust_remote_code=True,
    )

    print("Applying dynamic INT8 quantization to nn.Linear layers…", flush=True)
    model = torch.quantization.quantize_dynamic(
        model,
        {torch.nn.Linear},
        dtype=torch.qint8,
    )

    print(f"Saving quantized model to {QUANTIZED}…", flush=True)
    torch.save(model.state_dict(), str(QUANTIZED))

    quantized_mb = QUANTIZED.stat().st_size / 1024 / 1024
    saved_mb = original_mb - quantized_mb
    print(
        f"Quantized: {quantized_mb:.0f} MB  "
        f"(was {original_mb:.0f} MB — saved {saved_mb:.0f} MB / {saved_mb / original_mb * 100:.0f}%)",
        flush=True,
    )

    ORIGINAL.unlink()
    print(f"Removed {ORIGINAL.name}", flush=True)
    print("Quantization complete.", flush=True)


if __name__ == "__main__":
    main()
