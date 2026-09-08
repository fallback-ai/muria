# Fall Armyworm fine-tuning dataset

## Source and scope
This dataset is distilled from the structure of `combined_train.integrated.jsonl` and expanded using authoritative fall-armyworm guidance and research:
- FAO, **FAW Guidance Note 2 — Scouting** (2018): systematic W-pattern scouting, 10-plant stations, current infestation defined by recent damage/fresh frass, natural-enemy observation and record keeping.
- FAO, **Integrated management of the fall armyworm on maize** (2018): integrated, ecological management, manual destruction of egg masses/young larvae, crop diversification, avoidance of late planting and conservation of natural enemies.
- CABI, **Fall Armyworm Field Handbook: Identification and Management**: larval diagnostic markings and frass.
- FAO/FAMEWS monitoring guidance: recording and early-warning use.
- Jibril & Ahmed (2025), indexed in FAO AGRIS: Nigeria field evidence on maize–soybean intercropping and FAW incidence/damage.

## Format
The dataset preserves the existing three-field JSONL schema:
`instruction`, `response`, `lang`

Languages:
- `en` English
- `ha` Hausa
- `ig` Igbo
- `yo` Yoruba
- `pcm` Nigerian Pidgin

## Coverage
Total: **145** examples
- Training: **125**
- Evaluation: **20**
- 29 examples per language
- Each language contains:
  - 19 single-turn examples
  - 5 multi-turn examples
  - 5 low-confidence Tier-1 clarification examples

## Safety/data-quality choice
The source file contained examples that treated pesticide concentrations as universal. Those figures were intentionally not propagated. This dataset instead teaches the model to avoid guessing a pesticide dose and to defer to the locally registered product label and appropriate agricultural guidance.

## Fine-tuning notes
- The examples are intentionally FAW-specific; generic crop/livestock questions are excluded.
- Answers are concise and action-oriented.
- Source attribution is embedded directly in each response, so the model learns to cite its basis.
- Low-confidence examples explicitly teach the assistant to ask a targeted follow-up question rather than forcing a diagnosis.
- Multi-turn examples teach the assistant to retain the FAW context across follow-up questions.
