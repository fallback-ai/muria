# Cactus Export Handoff — For Suleiman

## Background (quick summary)

We're exporting our finetuned model (AfriqueGemma-4B + Muria LoRA) to a `.cact` binary for on-device inference using the Cactus Flutter SDK.

I merged the LoRA adapter into the base model, stripped the vision tower (text-only), and remapped the weights to the correct format. The clean checkpoint is already uploaded to HuggingFace.

The final step — compiling it to `.cact` — requires Cactus running on **macOS**. That's where you come in.

---

## Why I couldn't finish on Kaggle

Cactus's build system compiles C++ kernels with ARM NEON flags (`-march=armv8.2-a+...`).
Kaggle runs on Intel x86_64 — that compiler flag is invalid there, so the build fails.
The PyPI wheel also ships no pre-built binary for Linux.
Cactus is designed to be run from a **Mac dev machine**. You're up.

---

## What you need to do

### 1. Install Cactus on your Mac

```bash
brew install cactus-compute/cactus/cactus
cactus --version   # confirm it works
```

### 2. Download the clean checkpoint from HuggingFace

```bash
pip install huggingface_hub
```

```python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="fallback-ai/Muria-Afrique-Gemma-4B",
    allow_patterns="clean-checkpoint/*",
    local_dir="./muria_clean_lm",
    token="<HF_TOKEN>",
)
```

This downloads ~8.5 GB into `./muria_clean_lm/clean-checkpoint/`.

### 3. Run the conversion

```bash
cactus convert ./muria_clean_lm/clean-checkpoint ./muria_cact_output --bits 4
```

- Output will be a `.cact` file inside `./muria_cact_output/`
- Should be ~2–2.5 GB after 4-bit quantization
- The LOAD REPORT should show **no MISSING keys** — if it does, ping me

### 4. Upload the `.cact` back to HuggingFace

```python
from huggingface_hub import HfApi
import glob

api = HfApi(token="<HF_TOKEN>")
cact_file = glob.glob("./muria_cact_output/**/*.cact", recursive=True)[0]

api.upload_file(
    path_or_fileobj=cact_file,
    path_in_repo="muria-afriquegemma-4b-faw.cact",
    repo_id="fallback-ai/Muria-Afrique-Gemma-4B",
    repo_type="model",
)
print("Done!")
```

---

## HuggingFace repo

```
https://huggingface.co/fallback-ai/Muria-Afrique-Gemma-4B
```

Clean checkpoint lives at: `clean-checkpoint/` folder in that repo (private).
Ask for the HF token if you don't have it.

---

## The export notebook

The full Kaggle notebook is at `muria-export-quantize-v1.ipynb` in this repo if you need context.
