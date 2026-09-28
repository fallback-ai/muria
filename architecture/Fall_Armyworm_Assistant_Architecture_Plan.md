# Muria: Fall Armyworm Agronomic Assistant — Complete Architecture & Staged Roadmap
**An Offline-First, Multilingual Mobile AI System for Nigerian Smallholder Farmers**

---

## 1. Executive Summary & Strategic Positioning

Project Muria is an offline-first agronomic assistant engineered to run entirely on-device on resource-constrained Android smartphones (4GB–8GB RAM) owned by smallholder maize farmers, lead farmers, and local extension workers across Nigeria. It delivers real-time crop diagnosis, safety-critical integrated pest management (IPM) treatment protocols, and conversational agricultural extension in **Hausa, Yoruba, Igbo, Nigerian Pidgin, and English**, with **zero dependency on cellular data connectivity or cloud servers**.

### Dual Strategic Framing (Direct Human Benefit + Open Research Contribution)
1. **Direct Human & Economic Impact:** Delivers immediate, trusted Fall Armyworm (*Spodoptera frugiperda*) identification and non-hallucinated IPM guidelines directly to smallholders who lack access to agricultural extension agents (Nigeria currently has an extension agent-to-farmer ratio worse than 1:5,000).
2. **Open Research Contribution:** Produces an open, verifiable benchmark evaluating on-device micro-vision models (LiteRT YOLO) and continued pre-trained African language models (AfriqueGemma-4B) under *real, noisy Nigerian field conditions* (tropical glare, leaf dust, motion blur, early vs. late whorl damage, overlapping instars) rather than sanitized laboratory datasets (e.g., PlantVillage).

---

## 2. Recent Architectural Shifts: Why We Adopted a 4-Stage Rollout Roadmap

Following in-depth technical analysis and empirical profiling of low-cost Android hardware constraints (specifically entry-level octa-core ARM Cortex-A53/A55 chipsets, slow eMMC 5.1 flash storage, and strict Android Low Memory Killer policies), we identified several operational bottlenecks in our earlier monolithic designs. After this analysis, we decided to come up with a **4-Stage Rollout Roadmap**.

Here is why the architecture was shifted from the previous plan:

### A. Speech-to-Text (STT) Footprint Reality & Deferral to Stage 4
* **Previous Plan:** Assumed Meta MMS ASR could run within ~25MB–35MB RAM concurrently with the vision and reasoning engines.
* **Analysis & Finding:** The 25MB–35MB figure belongs to the VITS Text-to-Speech (TTS) voice packs, not Speech Recognition (ASR). The Meta MMS Multilingual ASR model (`mms-1b-all`) contains roughly 1 Billion parameters (~700MB–1GB in INT8 quantization). Cold-paging a 1GB ASR model on an entry-level 4GB phone creates severe memory contention and risks instant process termination by the Android Low Memory Killer (LMK). Furthermore, acoustic coverage for Nigerian Pidgin (`pcm`) in multilingual ASR remains unverified and brittle in noisy field acoustics.
* **Architectural Shift:** **Voice input (STT) is deferred to Stage 4.** In Stages 1, 2, and 3, user interaction relies on the live camera viewfinder, guided tap cards, and pre-written quick question chips / typed text. This validates the entire vision, advice, fast-path FAQ, and LLM reasoning pipeline without being blocked by speech recognition overhead.

### B. The 4B Model on Budget CPUs: Speed & Flash Paging Bottleneck, Not Just RAM
* **Previous Plan:** Assumed that because AfriqueGemma-4B fits in 4-bit quantization (~2.1GB RAM), it should handle all farmer queries end-to-end.
* **Analysis & Finding:** While a 2.1GB model technically fits in the free RAM of a 4GB device (which provides ~2.4GB usable before LMK intervention), CPU inference throughput on budget processors (e.g., MediaTek Helio G25/G35, Unisoc SC9863A with Cortex-A53/A55 cores) is only **1.5 to 3 tokens per second**. Furthermore, cold-paging 2.1GB of weights off slow eMMC 5.1 flash storage requires **5 to 8 seconds**. Forcing every crop scan through the 4B model would force the farmer to wait 40+ seconds for a simple diagnostic verdict, rapidly draining battery and inducing thermal throttling.
* **Architectural Shift:** **Re-instate the Two-Tier Cascade.** High-confidence vision detections bypass the LLM entirely, triggering instant deterministic advice cards. The 4B LLM is loaded exclusively on-demand in **Stage 3B** when a query cannot be answered by the fast-path FAQ cache.

### C. Restoring the Deterministic FAO Advice Cascade (Safety-Critical Grounding)
* **Previous Plan:** Relied on the 4B LLM + RAG to synthesize chemical dosages and treatment instructions on every query.
* **Analysis & Finding:** Relying on parametric memory or dynamic LLM text generation for chemical pesticides in low-resource African languages carries an unacceptable hallucination risk. A minor misinterpretation of dilution ratios (e.g., mixing rates per 15L knapsack sprayer vs. per-hectare concentrations) can poison crops, waste scarce capital, or endanger farmer health.
* **Architectural Shift:** Hard-code verified FAO, CABI, and Nigerian agricultural extension economic thresholds into **instant, deterministic Advice Cards** linked directly to vision classes. The LLM handles open-ended agronomic dialogue and situational reasoning, but never invents pesticide recipes.

### D. Guided Visual / Icon Disambiguation in Stage 2
* **Previous Plan:** Any ambiguous detection was escalated directly to conversational reasoning.
* **Analysis & Finding:** In the field, wind motion, blur, and lighting often yield intermediate confidence scores ($C < 0.60$). Invoking a 2.1GB LLM to resolve a blurry camera frame is inefficient and slow.
* **Architectural Shift:** Introduce **Stage 2: Guided Visual Disambiguation**. When YOLO confidence is borderline, the UI presents 1–2 intuitive visual/icon tap cards (e.g., "Do you see fresh sawdust-like frass inside the deep whorl?", "Are pinholes found on >3 out of 10 adjacent plants?"). This resolves ambiguity within 100ms with zero RAM surge.

### E. Semantic Fast-Path FAQ Cache (Pre-LLM Shortcut)
* **Previous Plan:** Any follow-up question required cold-loading AfriqueGemma-4B from flash memory.
* **Analysis & Finding:** Post-diagnosis farmer questions are overwhelmingly common variants of a small set of frequent practical concerns (*"Is it too late to spray?"*, *"What if I don't have that chemical?"*, *"Can I spray before rain?"*, *"How much water per knapsack?"*). Paging 2.1GB to answer standard questions creates unnecessary latency and battery drain.
* **Architectural Shift:** Introduce an **On-Device Semantic FAQ Fast-Path** using a lightweight, resident multilingual embedding model (`multilingual-e5-small`, ~120MB RAM). Questions are matched against a curated, cited FAQ store. High-similarity matches return instant cited answers read aloud via Soro-TTS (**zero LLM tokens, zero cold-load latency**). Only unindexed or complex queries fall through to AfriqueGemma-4B.

### F. Dual Knowledge Store Architecture
* **Previous Plan:** Attempted to use a single corpus of raw technical agronomy PDFs for both fast answers and LLM retrieval.
* **Analysis & Finding:** Raw PDF text chunks do not read naturally as direct spoken vernacular answers, and semantic search over dense technical documents frequently misidentifies farmer intent.
* **Architectural Shift:** Separate knowledge into two distinct stores:
  1. **Store A (Curated Vernacular FAQ Store):** Short, pre-written, verified, and cited Q&A pairs designed specifically for direct spoken synthesis via Soro-TTS.
  2. **Store B (Raw FAO/CABI Agronomy Corpus):** Comprehensive technical agronomy documentation used as reference grounding for AfriqueGemma-4B during Stage 3B open reasoning.

### G. SambaGuard Vision Dataset Calibration
* **Previous Plan:** Conceptual documentation referenced mixed pest classes like "stem borer".
* **Analysis & Finding:** The target SambaGuard dataset labels are strictly: `egg`, `frass`, `larva`, and `larval_damage` (overall $\text{mAP}_{50} \approx 0.347$).
* **Architectural Shift:** Detection outputs are aligned strictly to real SambaGuard life stages, with confidence threshold gating ($C \ge 0.60$ for direct advice; $C < 0.60$ triggers guided disambiguation).

---

## 3. The 4-Stage Rollout Roadmap & Staged Build Order

### Strategic Target Architecture vs. Staged Build Order
To prevent development from being blocked by unverified components (e.g. STT models), we distinguish between the **Target Architecture** (the finished system) and the **Staged Build Order** (how we build and validate components sequentially):

1. **Build Step 1 (Stage 1):** Vision (LiteRT YOLO) $\rightarrow$ Deterministic FAO Advice Card $\rightarrow$ Vernacular Voice Output (Soro-TTS). *Zero speech recognition, zero typed questions.*
2. **Build Step 2 (Stage 2):** Guided Yes/No Visual Disambiguation cards (Tappable UI, *still no speech recognition*).
3. **Build Step 3 (Stage 3):** Question Input via **Tappable Quick-Question Chips or Typed Text** $\rightarrow$ Semantic FAQ Matching (`multilingual-e5-small`) $\rightarrow$ AfriqueGemma-4B Fallback. *Validates the entire reasoning and retrieval pipeline with zero STT risk.*
4. **Build Step 4 (Stage 4):** Swap typed/chip input for **Native Hands-Free Speech Recognition (STT)** once acoustic models are profiled and verified on Hausa, Yoruba, Igbo, and Pidgin.

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: THE BULLETPROOF FIELD MVP (Immediate Target)                                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Input: Live camera viewfinder via CameraX                                            │
│ • Vision: YOLOv11n / YOLOv8n running on Google LiteRT (~6MB binary, w8a32 INT8)        │
│ • Reasoning: Deterministic FAO/CABI Advice Card (Linked directly to detection class)   │
│ • Output: Natural Voice synthesis via Soro-TTS / VITS (~28MB ONNX per active language) │
│ • Performance: < 150 MB Peak RAM | < 300 ms Total Latency | 0% Hallucination Risk      │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: GUIDED VISUAL DISAMBIGUATION (Zero Speech Overhead)                           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Triggered when YOLO confidence is ambiguous (e.g., C < 0.60)                         │
│ • Farmer is presented with high-contrast icon / visual cards:                          │
│   - "Do you see moist sawdust-like frass inside the top whorl?" [Yes] [No]             │
│   - "Are leaf pinholes localized or widespread across >3 out of 10 plants?" [Yes] [No] │
│ • Rules engine refines diagnosis without demanding high-overhead speech models.        │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 3: AGRONOMIC Q&A & REASONING (Dual-Track Fast-Path + LLM Fallback)              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Input: Quick-question chips or typed text (v1); hands-free STT (Stage 4)             │
│ • Fast-Path (Semantic FAQ Match):                                                      │
│   - Embedded with multilingual-e5-small (~120MB resident) against Curated FAQ Store   │
│   - High Similarity (cosine >= 0.82) -> Instant verified cited answer spoken via TTS   │
│   - Zero LLM tokens | Zero cold-load cost | Instant response                           │
│ • Deep Reasoning Fallback (AfriqueGemma-4B):                                           │
│   - If no confident FAQ match -> Cold-load AfriqueGemma-4B via Cactus (.cact mmap)    │
│   - Auto-RAG pulls verified FAO context chunks for grounded conversational reasoning   │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 4: NATIVE VOICE INPUT (STT / SPEECH RECOGNITION)                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Introduce lightweight, quantized Nigerian speech-to-text models once validated       │
│ • Complete full hands-free speech-in / speech-out loop across all 4 languages          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Selections, Engine Architecture & Research Evidence

### A. Vision Engine: YOLO on Google LiteRT
* **Model:** YOLOv11n (or YOLOv8n) fine-tuned on SambaGuard Fall Armyworm classes (`egg`, `frass`, `larva`, `larval_damage`).
* **Runtime:** **Google LiteRT** (`w8a32` dynamic INT8 quantization).
* **Client Implementation:** The official Flutter package `ultralytics_yolo: ^0.6.15`.
* **Technical Justification & Documentation Cross-References:**
  * As detailed in [`docs_research/ultralytics_litert.md`](../docs_research/ultralytics_litert.md), LiteRT traces PyTorch graphs directly and delegates execution to ARM GPU/OpenCL and XNNPACK on CPU, avoiding standard TFLite runtime overhead.
  * In [`docs_research/yolo_flutter_app_readme.md`](../docs_research/yolo_flutter_app_readme.md), `YOLOView` integrates CameraX frame acquisition, planar NCHW letterboxing, and Non-Maximum Suppression (NMS) natively in C++, avoiding hundreds of lines of error-prone manual image buffer transposition in Kotlin.
  * Footprint is exceptional: **~6MB model size**, **$<20\text{MB}$ active RAM**, and **$<35\text{ms}$ inference latency** on ARM Cortex-A53/A55 cores (see [`docs_research/google_litert_android.md`](../docs_research/google_litert_android.md) and [`docs_research/ultralytics_tflite.md`](../docs_research/ultralytics_tflite.md)).

### B. Voice Engine (TTS): Soro-TTS / VITS on sherpa-onnx
* **Model:** Meta MMS VITS fine-tuned on Nigerian speech datasets (Soro-TTS suite).
  * **Hausa:** `Shinzmann/soro-tts-hau` (see [`docs_research/soro_tts_hau.md`](../docs_research/soro_tts_hau.md))
  * **Yoruba:** `Shinzmann/soro-tts-yor`
  * **Igbo:** `Shinzmann/soro-tts-ibo`
  * **Nigerian Pidgin:** Meta MMS `pcm` / WAXAL (see [`docs_research/renpiper_mms_onnx.md`](../docs_research/renpiper_mms_onnx.md))
* **Runtime:** **`sherpa-onnx`** via `sherpa_onnx: ^1.13.8` (see [`docs_research/sherpa_pub_dev.md`](../docs_research/sherpa_pub_dev.md) and [`docs_research/sherpa_tts_overview.md`](../docs_research/sherpa_tts_overview.md)).
* **Technical Justification & Documentation Cross-References:**
  * **Modular RAM Allocation:** As verified in [`docs_research/renpiper_mms_onnx.md`](../docs_research/renpiper_mms_onnx.md), an INT8 quantized VITS model is **only ~28MB on disk** and takes **$<45\text{MB}$ RAM** during generation.
  * The application loads only the active language voice pack into RAM; the remaining three language models remain inert on flash storage (see [`docs_research/sherpa_vits_models.md`](../docs_research/sherpa_vits_models.md)).
  * Soro-TTS models are trained on native Nigerian speakers, providing natural tonal inflection and phonetic accuracy that Nigerian farmers understand and trust.

### C. Fast-Path Semantic FAQ Engine: Four Rules for Success
To make the fast-path semantic shortcut reliable in production without compromising agronomic safety, four architectural rules are enforced:

#### Rule 1: Two Separate Corpora, Not One
* **Store A (Curated Vernacular FAQ Store):** Contains short, pre-written, verified Q&A pairs formatted specifically for spoken speech output via Soro-TTS. Raw technical PDF chunks are unreadable when spoken aloud.
* **Store B (Raw FAO/CABI Literature):** Comprehensive technical agronomy documentation used exclusively for Stage 3B open LLM reasoning.

**Curated Vernacular FAQ Entry Schema:**
```json
{
  "id": "faq_faw_spray_timing_01",
  "category": "treatment_timing",
  "language": "hau",
  "question_variants": [
    "Shin ya yi latti in fesa magani?",
    "Idan tsutsotsi sun girma yana da amfani a fesa magani?",
    "Yaushe ne lokacin da ya dace a fesa masara?"
  ],
  "spoken_answer": "Idan tsutsa ta riga ta kai girman santimita biyu ko ta shiga zurfin kwanya, feshin magani ba zai yi aiki sosai ba domin tana kariya. Zai fi kyau a zuba yashi mai tsabta ko toka a cikin kwanyar, ko a cire su da hannu.",
  "citation": "FAO Fall Armyworm IPM Guide (2018), Section 4.2"
}
```

#### Rule 2: Strict Threshold Discipline
* Vision confidence ($C \ge 0.60$) and embedding cosine similarity operate on completely different scales.
* The cosine similarity threshold for the FAQ fast-path is set conservatively at **$\text{sim} \ge 0.82–0.85$**.
* **Failure Fallthrough Guarantee:** Any borderline or near-miss query must fall through to Stage 3B (LLM reasoning). A near-miss must *never* return a plausible-but-wrong cached answer.

#### Rule 3: Cross-Lingual Embedding Verification
* English-centric embeddings (such as Nomic-Embed-Text) fail on African vernacular queries.
* `intfloat/multilingual-e5-small` (~120MB INT8 quantized) must be empirically benchmarked against genuine Hausa, Yoruba, Igbo, and Pidgin farmer phrasing before production deployment to verify it can distinguish between closely related questions (e.g., *"Is it too late to spray?"* vs. *"What if I spray too much?"*).

#### Rule 4: Keep Embedding Model Resident & Warm
* Because `multilingual-e5-small` is compact (~120MB) and serves both fast-path FAQ lookup and Stage 3B RAG retrieval, it is loaded once on app startup and kept resident in memory.
* It does *not* participate in the aggressive load/unload lifecycle reserved for the 4B parameter LLM.

### D. Deep Reasoning Engine (LLM): AfriqueGemma-4B
* **Model:** `McGill-NLP/AfriqueGemma-4B` fine-tuned with QLoRA on verified Nigerian agronomic data (`faw_finetune_train.jsonl`).
* **Runtime Container:** **`.cact` (CQ4 4-bit)** on Cactus Engine (fallback: **`.gguf` (Q4_K_M)** on `llama.cpp`).
* **Technical Justification & Documentation Cross-References:**
  * As documented in [`docs_research/cact-format.md`](../docs_research/cact-format.md), `.cact` uses a 196-byte geometry header and zero-copy memory mapping (`mmap`). The Android kernel maps model weights directly from storage pages without copying the entire 2.1GB binary into the JVM heap.
  * In [`docs_research/llm.md`](../docs_research/llm.md) and [`docs_research/v1.6_overview.md`](../docs_research/v1.6_overview.md), Cactus manages prompt cache rolling, context windows, and execution delegates on mobile devices.
  * AfriqueGemma-4B retains the critical multilingual tokenizers and continued pre-training for African languages that generic Western models lack.
  * Restricting LLM execution to **Stage 3B fallback** completely shields daily diagnosis workflows from slow token-generation bottlenecks on entry-level CPUs.

### E. Grounding & Local Knowledge Base (RAG)
* **Engine:** **Cactus Auto-RAG** via `corpusDir` (see [`docs_research/rag.md`](../docs_research/rag.md) and [`docs_research/api-reference.md`](../docs_research/api-reference.md)).
* **Embedding Model:** `multilingual-e5-small` (see [`docs_research/quickstart.md`](../docs_research/quickstart.md)).
* **Technical Justification & Documentation Cross-References:**
  * Cactus natively indexes markdown and text documents in a designated local directory (`corpusDir`) and retrieves relevant chunks into the prompt context via `model.ragQuery()`.
  * **Deterministic Metadata Layer:** All FAO/CABI economic thresholds (e.g., "Spray only if $>20\%$ of plants show fresh feeding; do not mix chemicals without reading manufacturer labels") are stored with explicit document IDs to guarantee verifiable citations.

### F. Client Application Framework: Flutter (Dart)
* **Framework:** **Flutter** targeting Android API 24+ (`arm64-v8a`).
* **Comparison: Flutter vs. Native Kotlin:**
  * *Unified Native Interop:* Flutter binds to all native C++ runtimes (`ultralytics_yolo`, `sherpa_onnx`, and `cactus.dart`) via mature Dart FFI bindings (see [`docs_research/sherpa_flutter_app.md`](../docs_research/sherpa_flutter_app.md) and [`docs_research/cli.md`](../docs_research/cli.md)).
  * *Camera Pipeline:* `ultralytics_yolo` exposes a turnkey `YOLOView` widget that handles CameraX image streams and NMS natively in C++, completely avoiding manual YUV-to-RGB conversion in Kotlin.
  * *Development Velocity:* Single reactive UI codebase for multi-screen navigation, audio streaming, and localized UI components across Hausa, Yoruba, Igbo, and English.

---

## 5. End-to-End System Execution Flow

```text
                     [ Farmer Opens Muria Camera View ]
                                     │
                                     ▼
                [ Google LiteRT YOLOv11n Runs on Camera Stream ]
                (Inference: ~30ms | Active RAM: ~18MB | w8a32)
                                     │
                                     ▼
                   [ Confidence Score Assessment ]
                     ╱                             ╲
      High Confidence (C >= 0.60)           Ambiguous (C < 0.60)
                   │                                       │
                   ▼                                       ▼
    [ Instant FAO Advice Card Lookup ]     [ Stage 2 Visual Disambiguation ]
    - Matched against verified IPM store   - "Do you see fresh frass in whorl?"
    - Zero LLM tokens | Zero latency       - "Are pinholes on >3 out of 10 plants?"
                   │                                       │
                   ▼                                       ▼
     [ sherpa-onnx Soro-TTS Speaks ]          [ Refined Class Selected ]
     - Synthesizes vernacular audio                        │
     - ~28MB VITS active RAM                               ▼
                   │                          [ Instant FAO Advice Card ]
                   │
                   ▼
     [ "Ask Muria a Question" Tapped? ]
          ╱                      ╲
        [No]                    [Yes]
         │                        │
         ▼                        ▼
    [Flow Ends]         [ Question Input: Tappable Chip or Typed Text (v1) ]
                        [ (Note: Replaced by sherpa-onnx STT Voice in Stage 4) ]
                                  │
                                  ▼
                        [ multilingual-e5-small Embeds Query ]
                        (~120MB, kept resident in memory)
                                  │
                                  ▼
                        [ Semantic Match vs. Curated FAQ Store ]
                         ╱                                    ╲
         High Similarity (sim >= 0.82)              Low Similarity / No Match
                   │                                            │
                   ▼                                            ▼
    [ Instant Cited Answer from FAQ ]          [ Stage 3B: Cactus Loads AfriqueGemma-4B ]
    - Spoken immediately via Soro-TTS          - Zero-copy mmap from storage (~2.1GB)
    - Zero LLM tokens | Zero cold-load         - Auto-RAG pulls verified FAO context
                                               - Streams conversational answer in vernacular
                                               - Auto-unloads / drops cache on return to camera
```

---

## 6. Memory & Performance Budget (Target: 4GB RAM Android Phone)

### Target Device Hardware Constraints
* **Operating System:** Android 11–14 (API 30–34)
* **Chipset:** MediaTek Helio G25/G35 or Unisoc SC9863A (8x ARM Cortex-A53 @ 1.6–2.0 GHz)
* **Total Physical RAM:** 4,000 MB
* **Usable RAM (after OS & system services):** ~2,400 MB
* **Storage:** 64GB eMMC 5.1 (Sequential Read: ~250 MB/s; Random Read: ~30 MB/s)

### Staged Memory Allocation Table

| Runtime Phase | Active Engine(s) | Active Models in RAM | Peak RAM Usage | Latency / Throughput |
| :--- | :--- | :--- | :--- | :--- |
| **Idle / App Launch** | Flutter Engine | None | **~75 MB** | Instant |
| **Stage 1: Field Scouting** | LiteRT + CameraX | YOLOv11n (~6MB) | **~120 MB** | $< 35\text{ms}$ per frame |
| **Stage 1: Advice Audio** | `sherpa-onnx` + AudioSink | Active VITS voice pack (~28MB) | **~135 MB** | $< 300\text{ms}$ to first audio |
| **Stage 2: Disambiguation** | Flutter Rules Engine | None (Static visual assets) | **~90 MB** | Instant |
| **Stage 3A: Fast-Path FAQ** | Vector Engine + Soro-TTS | `multilingual-e5-small` + VITS | **~185 MB** | $< 150\text{ms}$ response |
| **Stage 3B: LLM Reasoning** | Cactus Engine + Auto-RAG | AfriqueGemma-4B + Embedding | **~1,920 MB** | 1.5–3.0 tokens/second |

> [!NOTE]
> Android's Low Memory Killer (LMK) triggers around **2,400 MB** of application memory consumption on a 4GB device. Stages 1, 2, and 3A operate well under **200 MB**, and Stage 3B peaks at **~1,920 MB**, maintaining a safe **~480 MB headroom buffer** that prevents OS task kills.

---

## 7. Verifiability, IPM Safety & Anti-Hallucination Guardrails

1. **Strict Class Isolation:** The vision engine detects strictly four SambaGuard life stages: `egg`, `frass`, `larva`, and `larval_damage`.
2. **Economic Threshold Hardcoding:**
   * Whorl damage $< 20\%$ during vegetative stage: Advise manual crushing of egg masses, application of clean sand/ash in whorls, or neem extract; **no chemical spray recommended**.
   * Whorl damage $\ge 20\%$ with active larvae present: Recommend registered local insecticides (e.g., Emamectin benzoate, Chlorantraniliprole) with strict dilution ratios (e.g., milliliters per 15L knapsack) sourced directly from FAO/IITA extension bulletins.
3. **Parametric Memory Lockdown:** AfriqueGemma-4B is explicitly prompted via system instructions to refuse dosage calculations not present in the retrieved RAG context, eliminating dangerous unit-conversion errors.

---

## 8. Engineering Implementation Checklist

- [x] **Fine-Tuning Notebook Cleaned:** `muria-afriquegemma-faw-finetune-v1.ipynb` outputs verified LoRA adapters to Hugging Face Hub (`fallback-ai/Muria-Afrique-Gemma-4B-LoRA`).
- [x] **Export Pipeline Modularized:** `muria-export-quantize-v1.ipynb` merges 16-bit weights and builds standalone GGUF `Q4_K_M` binaries.
- [ ] **Stage 1 Flutter Application Shell:**
  - [ ] Initialize Flutter project with `ultralytics_yolo: ^0.6.15` and bundle `faw_yolo_w8a32.tflite` (see [`docs_research/ultralytics_litert.md`](../docs_research/ultralytics_litert.md) and [`docs_research/yolo_flutter_app_readme.md`](../docs_research/yolo_flutter_app_readme.md)).
  - [ ] Add `sherpa_onnx: ^1.13.8` and bundle Soro-TTS VITS models (`hau`, `yor`, `ibo`, `pcm`) (see [`docs_research/sherpa_pub_dev.md`](../docs_research/sherpa_pub_dev.md) and [`docs_research/soro_tts_hau.md`](../docs_research/soro_tts_hau.md)).
  - [ ] Implement deterministic FAO Advice Card lookup dictionary linked to YOLO output classes.
- [ ] **Stage 2 Visual Decision Tree:**
  - [ ] Implement guided icon/visual disambiguation prompts for borderline YOLO predictions ($C < 0.60$).
- [ ] **Stage 3 Fast-Path FAQ & LLM Bridge:**
  - [ ] Populate Curated Vernacular FAQ Store with verified, cited agronomy Q&A pairs (JSON schema with question variants, vernacular answer, citation).
  - [ ] Implement quick-question chips / typed text UI for Stage 3 input.
  - [ ] Integrate resident `multilingual-e5-small` embedding matcher with $\ge 0.82$ similarity threshold.
  - [ ] Integrate `cactus.dart` with compiled `.cact` weights and local FAO corpus folder as conversational fallback (see [`docs_research/cact-format.md`](../docs_research/cact-format.md) and [`docs_research/rag.md`](../docs_research/rag.md)).
- [ ] **Stage 4 ASR Speech Recognition Validation:**
  - [ ] Profile quantized Meta MMS ASR on real entry-level Android devices before enabling microphone input (see [`docs_research/transcription.md`](../docs_research/transcription.md)).
