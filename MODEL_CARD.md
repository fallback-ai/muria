---
language:
- en
- ha
- yo
- ig
- pcm
license: cc-by-4.0
base_model: McGill-NLP/AfriqueGemma-4B
tags:
- text-generation
- transformers
- gguf
- conversational
- agriculture
- fall-armyworm
- lora
- sft
- trl
- 5 languages
pipeline_tag: text-generation
---

# Muria — Afrique-Gemma-4B (Fine-tuned)

Muria is an assistant fine-tuned for Nigerian smallholder maize farmers, providing diagnostic, scouting, and integrated pest management (IPM) guidance for the **Fall Armyworm (*Spodoptera frugiperda*)** in **English, Hausa, Igbo, Yoruba, and Nigerian Pidgin**. It is a LoRA fine-tune of **McGill-NLP/AfriqueGemma-4B**, merged and quantized to GGUF (`Q4_K_M`) for local/edge inference on 4–8GB RAM Android devices.

> *"License: CC BY 4.0, per McGill-NLP/AfriqueGemma-4B's official repository (license: cc-by-4.0, stated explicitly in its model card). Note for transparency: while distributed under CC BY 4.0, the base weights are a continued-pretraining adaptation of google/gemma-3-4b-pt."*

---

## Model Details

* **Base model:** `McGill-NLP/AfriqueGemma-4B` — continued-pretrain (CPT) on the `gemma-3-4b-pt` base lineage (not `-it`/instruct). It has **no inherited chat template or instruction-following behavior; all of that was introduced during this fine-tune from zero.**
* **Architecture:** Gemma-3, 4B parameters
* **Fine-tuning method:** LoRA ($r=32, \alpha=64$), targeting attention (`q/k/v/o_proj`) and MLP (`gate/up/down_proj`) modules, then merged into the base weights.
* **Training framework:** TRL `SFTTrainer`, cosine LR schedule (peak 2e-4, ~3% warmup), early stopping on `eval_loss`.
* **Quantization & Format:** Merged 16-bit weights quantized to GGUF `Q4_K_M` (~2.5GB active memory footprint) via `llama.cpp` for on-device mobile runtimes.
* **Languages Covered:**
  * English (`en`)
  * Hausa (`ha`)
  * Igbo (`ig`)
  * Yoruba (`yo`)
  * Nigerian Pidgin (`pcm`)

---

## Domain Grounding & Authoritative Knowledge

All diagnostic responses, scouting instructions, and biological markers are strictly grounded in peer-reviewed and institutional fall armyworm agronomy guidance:
* **FAO FAW Guidance Note 2 — Scouting (2018):** Systematic W-pattern scouting, 10-plant stations, current infestation defined by recent damage/fresh frass, natural-enemy observation and record keeping.
* **FAO Integrated Management of the Fall Armyworm on Maize (2018):** Integrated, ecological management, manual destruction of egg masses/young larvae, crop diversification, avoidance of late planting, and conservation of natural enemies.
* **CABI Fall Armyworm Field Handbook:** Larval diagnostic markings (pale inverted "Y" on the head, 4 dark spots arranged in a square on the 8th abdominal segment, and whorl frass).
* **Jibril & Ahmed (2025, FAO AGRIS):** Nigeria field evidence on maize–soybean intercropping and FAW incidence/damage suppression.

---

## Safety Guardrails & Model Alignment

1. **Strict Exclusion of Pesticide Dosage Guessing:**
   * Universal chemical dosage figures are intentionally omitted. The model will **never** guess or recommend unverified chemical concentrations or knapsack sprayer volumes. Instead, it instructs the farmer to consult the registered local product label and extension agents.
2. **Built-in Citation Attribution:**
   * Every response embeds its source authority directly (e.g., `Source: FAO FAW Guidance Note 2 (2018)`).
3. **Clarifying Diagnostics on Low-Confidence Vision:**
   * When prompted with ambiguous observations or low-confidence vision signals (e.g., Tier-1 classifier outputs like *55% fall armyworm, 40% other*), the model asks targeted diagnostic follow-up questions rather than forcing a diagnosis.

---

## Dataset Breakdown

The fine-tuning dataset comprises 145 instruction-response pairs:
* **Train split:** 125 pairs (25 each for `en`, `ha`, `ig`, `yo`, `pcm`).
* **Eval split:** 20 pairs (4 each for `en`, `ha`, `ig`, `yo`, `pcm`).
* **Format:**
  * 19 single-turn agronomic QA pairs per language.
  * 5 multi-turn context preservation dialogues per language.
  * 5 low-confidence Tier-1 clarification pairs per language.

---

## Prompt Template (Gemma-3 Turn Format)

```text
<start_of_turn>user
{instruction}<end_of_turn>
<start_of_turn>model
{response}<end_of_turn>
```

---

## Usage

### llama.cpp / Mobile Runtime (GGUF)

```bash
./llama-cli -m Muria-Afrique-Gemma-4B.Q4_K_M.gguf \
    -p "<start_of_turn>user\nTa yaya zan bambanta kwaron soja da wata tsutsa?<end_of_turn>\n<start_of_turn>model\n" \
    -n 150 --temp 0.2
```

### Python (Transformers + PEFT)

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "McGill-NLP/AfriqueGemma-4B"
ADAPTER_ID = "fallback-ai/Muria-Afrique-Gemma-4B-LoRA"

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float16, device_map="auto")
model = PeftModel.from_pretrained(base_model, ADAPTER_ID)

prompt = "How often I suppose check my maize for fall armyworm?"
formatted = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"

inputs = tokenizer(formatted, return_tensors="pt").to(model.device)
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=150, temperature=0.2)

print(tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True))
```

---

## Multi-Format Mobile Conversion (.CACT, INT4, GGUF)

To support flexible on-device deployment across diverse Android runtimes without retraining, raw LoRA adapters are distributed alongside the quantized GGUF:
* **Dedicated Adapter Repo:** [`fallback-ai/Muria-Afrique-Gemma-4B-LoRA`](https://huggingface.co/fallback-ai/Muria-Afrique-Gemma-4B-LoRA)
* **Main Repo Subfolder:** [`fallback-ai/Muria-Afrique-Gemma-4B/adapters`](https://huggingface.co/fallback-ai/Muria-Afrique-Gemma-4B)

### Converting to Target Mobile Formats

Use the provided conversion utility `scripts/merge_and_convert.py`:

```bash
# 1. Merge LoRA with McGill-NLP/AfriqueGemma-4B to produce 16-bit weights
python scripts/merge_and_convert.py --action merge --output-dir ./muria-merged-fp16

# 2. Build Cactus (.cact) format for ultra-compact mobile deployment
python scripts/merge_and_convert.py --action cact --output-file muria.cact

# 3. Quantize to GGUF (Q4_K_M or Q4_0) for llama.cpp
python scripts/merge_and_convert.py --action gguf --quant-type Q4_K_M --llama-cpp-dir /path/to/llama.cpp
```

