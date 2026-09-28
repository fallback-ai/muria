# Muria: Fall Armyworm Agronomic Assistant — Complete Architecture & Staged Roadmap
**An Offline-First, Multilingual Mobile AI System for Nigerian Smallholder Farmers**

---

## 1. Executive Summary & Positioning

Project Muria is an offline-first agronomic assistant designed to run on resource-constrained Android smartphones (4GB–8GB RAM) owned by smallholder maize farmers across Nigeria. It provides real-time crop diagnosis, safety-critical treatment protocols, and conversational agricultural extension in **Hausa, Yoruba, Igbo, Nigerian Pidgin, and English**, with **zero dependency on cellular data or cloud backends**.

### Dual Strategic Framing
1. **Direct Human & Economic Impact:** Delivers immediate, trusted Fall Armyworm (*Spodoptera frugiperda*) identification and non-hallucinated integrated pest management (IPM) guidelines to smallholders who lack access to agricultural extension workers.
2. **Open Research Contribution:** Delivers the first verifiable benchmark evaluating on-device micro-vision models (LiteRT YOLO) and continued pre-trained African language models (AfriqueGemma-4B) under *real, noisy Nigerian field conditions* (glare, leaf dust, motion blur, early vs. late whorl damage, multiple instars) rather than sanitized laboratory datasets.

---

## 2. Recent Architectural Shifts & Why We Adopted a 4-Stage Roadmap

Following deeper technical profiling of low-cost Android hardware constraints (specifically entry-level octa-core Cortex-A53/A55 chipsets, slow eMMC 5.1 flash storage, and strict Android Low Memory Killer policies), we identified several operational bottlenecks in our earlier monolithic designs. We have restructured the architecture into a **4-Stage Rollout Roadmap**.

### The Core Architectural Shifts:

1. **Speech-to-Text (STT) Footprint Reality & Deferral:**
   * *Previous Plan:* Assumed Meta MMS ASR could run in ~25MB–35MB RAM alongside the reasoning engine.
   * *Analysis & Correction:* The full Meta MMS ASR model (`mms-1b-all`) contains roughly 1 Billion parameters (~700MB–1GB INT8 quantized). Paging and running a 1GB ASR model on an entry-level 4GB phone creates severe memory contention and risks immediate termination by the Android OS Low Memory Killer (LMK). Additionally, acoustic coverage for Nigerian Pidgin (`pcm`) in multilingual ASR remains brittle.
   * *Decision:* **Defer voice input (STT) to Stage 4.** In Stages 1 and 2, voice input is replaced by high-accuracy visual diagnosis coupled with guided Yes/No visual disambiguation cards.

2. **CPU Throughput & Flash Paging Bottleneck (The 4B Model Reality):**
   * *Previous Plan:* Assumed that because AfriqueGemma-4B fits in 4-bit quantization (~2.1GB RAM), it should handle all interactions end-to-end.
   * *Analysis & Correction:* On budget processors (e.g., MediaTek Helio G-series, Unisoc SC9863A with Cortex-A53/A55 cores), CPU inference throughput for a 4B parameter model is approximately **1.5 to 3 tokens per second**, and hardware NPU delegates are absent. Furthermore, cold-paging 2.1GB of weights off slow eMMC 5.1 flash memory takes 4 to 8 seconds. Forcing every crop scan through the 4B model would force the farmer to wait 40+ seconds for an answer while draining battery and inducing thermal throttling.
   * *Decision:* **Re-instate the Two-Tier Cascade.** High-confidence vision detections bypass the LLM entirely, triggering instant deterministic advice cards. The 4B LLM is activated exclusively for conversational follow-ups.

3. **Restoring the Deterministic Advice Cascade (Safety-Critical Grounding):**
   * *Previous Plan:* Relied on the 4B LLM + RAG to synthesize chemical dosages and treatment instructions on every query.
   * *Analysis & Correction:* Relying on parametric memory or dynamic text generation for chemical pesticides in low-resource African languages carries hallucination risk. Even a minor misinterpretation of dilution ratios (e.g., knapsack sprayer volume vs. chemical concentration) can poison crops or endanger farmers.
   * *Decision:* Hard-code verified FAO, CABI, and extension service economic thresholds into **instant, deterministic Advice Cards** linked directly to vision classes. The LLM handles dialogue, translation nuance, and situational reasoning, but does not invent pesticide recipes.

4. **Cross-Lingual Retrieval Grounding:**
   * *Previous Plan:* Planned to use English-centric dense embeddings (e.g., Nomic-Embed) for cross-lingual vector search.
   * *Analysis & Correction:* Standard English embedding spaces perform poorly when matching vernacular Hausa or Pidgin farmer queries against English scientific PDFs.
   * *Decision:* Primary retrieval is **keyed directly on the detected vision class and agronomic growth stage metadata tags** (e.g., `pest: fall_armyworm`, `damage_type: whorl_feeding`, `economic_threshold: >20%`). Semantic search is reserved for open follow-ups.

5. **SambaGuard Vision Dataset Calibration:**
   * *Previous Plan:* Hypothetical outputs referenced mixed classes like "stem borer".
   * *Analysis & Correction:* The target SambaGuard dataset labels are strictly: `egg`, `frass`, `larva`, and `larval_damage` (overall $\text{mAP}_{50} \approx 0.347$).
   * *Decision:* Align detection classes strictly to real life stages, and implement confidence threshold gating ($C \ge 0.60$ for direct advice; $C < 0.60$ triggers guided disambiguation).

---

## 3. The 4-Stage Rollout Roadmap

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: THE BULLETPROOF FIELD MVP (Immediate Production Target)                 │
├──────────────────────────────────────────────────────────────────────────────────┤
│ • Input: Live camera view via CameraX                                            │
│ • Vision: YOLOv11n / YOLOv8n running on Google LiteRT (~6MB binary, w8a32)       │
│ • Reasoning: Deterministic FAO/CABI Advice Card (Linked to detection class)      │
│ • Output: Natural Voice synthesis via Soro-TTS / VITS (~28MB ONNX per language)   │
│ • Specs: < 150 MB RAM | < 300 ms Latency | Zero Hallucination Risk | 100% Offline│
└──────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: GUIDED VISUAL DISAMBIGUATION (No STT Required)                          │
├──────────────────────────────────────────────────────────────────────────────────┤
│ • Triggered when YOLO confidence is ambiguous (e.g., C < 0.60)                   │
│ • Farmer is presented with intuitive icon/tap questions:                        │
│   - "Do you see moist sawdust-like frass inside the top whorl?" [Yes] [No]       │
│   - "Are leaf pinholes localized or widespread across >3 out of 10 plants?"      │
│ • Rules engine refines diagnosis without demanding high-overhead speech models.  │
└──────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 3: AFRIQUEGEMMA-4B CONVERSATIONAL REASONING & EXTENSION                    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ • Activated on-demand when the farmer taps "Ask Muria a complex question"        │
│ • AfriqueGemma-4B loaded via memory-mapped Cactus (.cact) or llama.cpp (.gguf)   │
│ • Local Auto-RAG retrieves verified FAO context chunks for grounding             │
│ • Enables interactive agronomic troubleshooting, weather contingency, and nuance │
└──────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 4: NATIVE VOICE INPUT (STT / SPEECH RECOGNITION)                           │
├──────────────────────────────────────────────────────────────────────────────────┤
│ • Introduce lightweight, quantized Nigerian speech-to-text models once validated │
│ • Complete full hands-free speech-in / speech-out loop across all 4 languages    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Selections, Engine Architecture & Research Evidence

### A. Vision Engine: YOLO on Google LiteRT
* **Model:** YOLOv11n (or YOLOv8n) fine-tuned on SambaGuard Fall Armyworm classes (`egg`, `frass`, `larva`, `larval_damage`).
* **Runtime:** **Google LiteRT** (`w8a32` dynamic INT8 quantization).
* **Client Implementation:** The official Flutter package `ultralytics_yolo: ^0.6.15`.
* **Technical Justification:**
  * As documented in [`docs_research/ultralytics_litert.md`](../docs_research/ultralytics_litert.md), LiteRT traces PyTorch graphs directly and delegates execution to ARM GPU/OpenCL and XNNPACK on CPU.
  * In [`docs_research/yolo_flutter_app_readme.md`](../docs_research/yolo_flutter_app_readme.md), `YOLOView` integrates CameraX frame acquisition, planar NCHW letterboxing, and Non-Maximum Suppression (NMS) natively in C++, avoiding hundreds of lines of error-prone manual image buffer transposition in Kotlin.
  * Footprint is exceptional: **~6MB model size**, **$<20\text{MB}$ active RAM**, and **$<35\text{ms}$ latency**.

### B. Voice Engine (TTS): Soro-TTS / VITS on sherpa-onnx
* **Model:** Meta MMS VITS fine-tuned on Nigerian speech datasets (Soro-TTS suite).
  * Hausa: `Shinzmann/soro-tts-hau` (see [`docs_research/soro_tts_hau.md`](../docs_research/soro_tts_hau.md))
  * Yoruba: `Shinzmann/soro-tts-yor`
  * Igbo: `Shinzmann/soro-tts-ibo`
  * Nigerian Pidgin: Meta MMS `pcm` / WAXAL (see [`docs_research/renpiper_mms_onnx.md`](../docs_research/renpiper_mms_onnx.md))
* **Runtime:** **`sherpa-onnx`** via `sherpa_onnx: ^1.13.8` (see [`docs_research/sherpa_pub_dev.md`](../docs_research/sherpa_pub_dev.md) and [`docs_research/sherpa_tts_overview.md`](../docs_research/sherpa_tts_overview.md)).
* **Technical Justification:**
  * **Modular RAM Allocation:** As verified in [`docs_research/renpiper_mms_onnx.md`](../docs_research/renpiper_mms_onnx.md), an INT8 quantized VITS model is **only ~28MB on disk** and takes **$<45\text{MB}$ RAM** during generation.
  * The app only loads the active language voice pack into RAM; the remaining three languages remain inert on flash storage.
  * Soro-TTS models are trained on native speakers, providing natural prosody and phonetics that Nigerian farmers trust.

### C. Reasoning Engine (LLM): AfriqueGemma-4B
* **Model:** `McGill-NLP/AfriqueGemma-4B` fine-tuned with LoRA on verified Nigerian agronomic data (`faw_finetune_train.jsonl`).
* **Runtime Container:** **`.cact` (CQ4 4-bit)** on Cactus Engine (fallback: **`.gguf` (Q4_K_M)** on `llama.cpp`).
* **Technical Justification:**
  * As documented in [`docs_research/cact-format.md`](../docs_research/cact-format.md), `.cact` uses a 196-byte geometry header and zero-copy memory mapping (`mmap`). The Android kernel maps model weights directly from storage pages without copying the entire 2.1GB binary into the JVM heap.
  * AfriqueGemma-4B retains the critical multilingual tokenizers and continued pre-training for African languages that generic Western models lack.
  * By restricting LLM execution to **Stage 3**, we completely shield daily diagnosis workflows from slow token-generation bottlenecks.

### D. Grounding & Local Knowledge Base (RAG)
* **Engine:** **Cactus Auto-RAG** via `corpusDir` (see [`docs_research/rag.md`](../docs_research/rag.md) and [`docs_research/api-reference.md`](../docs_research/api-reference.md)).
* **Embedding Model:** `Nomic-Embed-Text-v1.5` (see [`docs_research/quickstart.md`](../docs_research/quickstart.md)).
* **Technical Justification:**
  * Cactus natively indexes markdown and text documents in a designated local directory (`corpusDir`) and retrieves relevant chunks into the prompt context via `model.ragQuery()`.
  * **Deterministic Metadata Layer:** All FAO/CABI economic thresholds (e.g., "Spray only if $>20\%$ of plants show fresh feeding; do not mix chemicals without reading manufacturer labels") are stored with explicit document IDs to guarantee verifiable citations.

### E. Client Application Framework: Flutter (Dart)
* **Framework:** **Flutter** targeting Android API 24+ (`arm64-v8a`).
* **Technical Justification:**
  * Unifies all three native C++ runtimes (`ultralytics_yolo`, `sherpa_onnx`, and `cactus.dart`) through official, tested Dart FFI bindings.
  * Completely bypasses writing hundreds of lines of complex JNI/C++ glue code and manual Android CameraX YUV-to-RGB image processors in Kotlin.

---

## 5. Memory & Performance Budget (Target: 4GB RAM Android)

### Theoretical Worst-Case vs. Actual Muria Staged Reality

| Phase | Active Engine | Active Models in Memory | Peak RAM | Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1: Field Scouting** | LiteRT + Flutter UI | YOLOv11n (~6MB) | **~120 MB** | $<35\text{ms}$ |
| **Stage 1: Advice Audio** | sherpa-onnx + Flutter UI | Active VITS voice pack (~28MB) | **~135 MB** | $<300\text{ms}$ |
| **Stage 2: Disambiguation** | Rules Engine + Flutter UI| None (Static UI logic) | **~90 MB** | Instant |
| **Stage 3: LLM Reasoning** | Cactus Engine + Auto-RAG | AfriqueGemma-4B + Nomic-Embed | **~1,920 MB** | 1.5–3 tok/sec |

*Android Low Memory Killer (LMK) triggers around 2,400MB on a 4GB device. Stages 1 and 2 operate well under 150MB, and Stage 3 peaks at ~1,920MB, leaving a safe **~480MB headroom buffer**.*

---

## 6. Engineering Implementation Checklist

- [x] **Fine-Tuning Notebook Cleaned:** `muria-afriquegemma-faw-finetune-v1.ipynb` outputs verified LoRA adapters to Hugging Face Hub (`fallback-ai/Muria-Afrique-Gemma-4B-LoRA`).
- [x] **Export Pipeline Modularized:** `muria-export-quantize-v1.ipynb` merges 16-bit weights and builds standalone GGUF `Q4_K_M` binaries.
- [ ] **Stage 1 Flutter App Shell:**
  - [ ] Add `ultralytics_yolo: ^0.6.15` and bundle `faw_yolo_w8a32.tflite`.
  - [ ] Add `sherpa_onnx: ^1.13.8` and bundle Soro-TTS VITS models (`hau`, `yor`, `ibo`, `pcm`).
  - [ ] Create deterministic FAO Advice Card dictionary linked to YOLO output classes.
- [ ] **Stage 2 Visual Decision Tree:**
  - [ ] Design icon-based disambiguation prompts for borderline YOLO predictions.
- [ ] **Stage 3 LLM Bridge:**
  - [ ] Integrate `cactus.dart` with compiled `.cact` weights and local FAO corpus folder.
- [ ] **Stage 4 ASR Benchmarking:**
  - [ ] Profile quantized Meta MMS ASR on real entry-level Android devices before enabling mic input.
