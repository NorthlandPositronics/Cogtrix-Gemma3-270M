"""Download Gemma 3 270M GGUF weights (Q4_K_M) at Docker build time using a BuildKit secret."""

import sys, os
from huggingface_hub import snapshot_download

try:
    token = open("/run/secrets/hf_token").read().strip()
except FileNotFoundError:
    print(
        "ERROR: /run/secrets/hf_token not found — "
        "pass --secret id=hf_token,env=HF_TOKEN to docker build",
        file=sys.stderr,
    )
    sys.exit(1)

if not token:
    print("ERROR: HF_TOKEN secret is empty", file=sys.stderr)
    sys.exit(1)

repo = os.environ.get("GGUF_REPO", "unsloth/gemma-3-270m-it-qat-GGUF")
variant = os.environ.get("GGUF_VARIANT", "Q4_K_M")
pattern = f"*{variant}.gguf"

print(f"Downloading GGUF ({variant}) from {repo} …", flush=True)
local_dir = snapshot_download(
    repo_id=repo,
    local_dir="/model",
    token=token,
    allow_patterns=[pattern, "*.tokenizer*", "*.tiktoken*"],
    ignore_patterns=["*.safetensors", "*.bin", "*.pt", "*.h5", "*.msgpack"],
)
from pathlib import Path

ggufs = list(Path("/model").rglob(pattern))
if not ggufs:
    print("ERROR: No GGUF file found after download.", file=sys.stderr)
    sys.exit(1)

target = Path(f"/model/gemma-3-270m-{variant.lower()}.gguf")
ggufs[0].rename(target)
print(f"GGUF ready at {target}", flush=True)
print("Download complete.", flush=True)
