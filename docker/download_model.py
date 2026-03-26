"""Download Gemma 3 270M weights at Docker build time using a BuildKit secret."""
import sys
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

print(f"Downloading google/gemma-3-270m-it ...", flush=True)
snapshot_download(
    "google/gemma-3-270m-it",
    local_dir="/model",
    token=token,
    ignore_patterns=["*.msgpack", "*.h5", "*.ot", "flax_*", "tf_*", "rust_*"],
)
print("Download complete.", flush=True)
