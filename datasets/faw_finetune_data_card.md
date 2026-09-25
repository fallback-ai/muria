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

### Multi-turn turn-token alignment
Multi-turn examples no longer encode dialogue as literal `Farmer:`/`Assistant:` text (previously
`Manomi:`/`Mataimaki:` in Hausa and `Àgbẹ̀:`/`Olùrànlọ́wọ́:` in Yoruba). Intermediate turns now use
Gemma turn tokens directly inside `instruction`, so they align with the format seen at inference.
Single-turn rows are unchanged. The `instruction` for a multi-turn row is written to compose with the
standard Gemma wrapper the trainer applies:

```
<start_of_turn>user
{instruction}<end_of_turn>
<start_of_turn>model
{response}<end_of_turn>
```

That is, a multi-turn `instruction` embeds `…<end_of_turn>\n<start_of_turn>model\n…<end_of_turn>\n<start_of_turn>user\n…`
for the prior turns, with the final model reply kept in `response`. **If your training loop does not apply
that exact `user … model` wrapper, adjust the wrapper (not the data) so the embedded tokens are not
double-wrapped.**

## Coverage
Total: **550** examples
- Training: **530** (106 per language) — see `faw_finetune_manifest.md` for provenance
- Vetted core: **285** (`faw_finetune_train.seed.jsonl`, 57 per language) — the reviewable set
- Evaluation: **20** (4 per language)

> The 530-row train file is the 285-row vetted seed plus 245 augmentation variants, **capped at 2 rows
> per distinct answer** (1.86× average duplication, down from an earlier 3.2×). There are **285 distinct
> responses**. For zero duplication, train on `faw_finetune_train.seed.jsonl` directly. **See the manifest
> for what still needs a native/agronomic pass before a farmer-facing release.**

Original balanced core (per language: en/ha/ig/yo/pcm):
- 19 single-turn examples
- 5 multi-turn examples
- 5 low-confidence Tier-1 clarification examples

### English-first expansion (P2/P3)
14 new **English** training rows were added, so the per-language balance is intentionally uneven
for now (en 39; ha/ig/yo/pcm 25 each):
- **10 diagnostic-diversity rows (P2):** windowpane scraping, ragged-hole vs stem-borer tunnelling,
  cutworm-at-base vs whorl feeding, African-armyworm marching vs FAW, one-larva-per-whorl cannibalism,
  egg-mass appearance, natural-enemy/parasitoid signs, reproductive-stage cob damage, old-vs-fresh
  damage, and multi-sign confirmation. This broadens diagnosis beyond "fresh frass in the whorl".
- **4 deeper multi-turn dialogues (P3):** 3–4 exchanges each (scout → interpret → threshold →
  cultural control / out-of-stock / rain-after-spray / worn label), all using the Gemma turn-token
  format above and deferring doses and thresholds to the local product label / extension guidance.

### Topic coverage, persona and out-of-scope (P4/P5)
A further 18 **English** training rows were added (en now 57; ha/ig/yo/pcm 25 each):
- **10 topic-coverage rows (P4):** growth-stage guidance (seedling / whorl / tassel), cultural and
  mechanical controls (push-pull, trap crops/intercropping, tillage), out-of-stock alternatives, basic
  FAW life-cycle education, why infestations recur, and rain-after-spraying. All cite a source and defer
  doses/thresholds to the local product label and extension guidance.
- **8 persona / out-of-scope rows (P5):** the assistant identifies itself as **Muria**, states its
  fall-armyworm-on-maize scope, and gives gentle fallbacks for non-FAW queries (rice blast, livestock
  health, tomato aphids, market prices, non-FAW maize symptoms), redirecting to extension or a vet.

**Citation note:** the P5 persona/out-of-scope rows intentionally carry **no** `Source:` line because
they make no agronomic claim. All 149 rows that give FAW technical guidance are cited (100% of technical
rows); 8 persona/scope rows are deliberately citation-free. Do not "fix" this by adding citations to
scope statements — that would teach the model to fabricate sources.

**Non-English parallels now exist (P6):** Hausa, Igbo, Yoruba and Pidgin versions of the 32 new English
rows (P2–P5), including the deeper dialogues, were added, and the languages are re-balanced (180 each in
train). These were machine-produced and anchored to already-vetted dataset vocabulary; **Hausa, Igbo and
Yoruba still require a native + agronomic review** before a farmer-facing release. See
`faw_finetune_manifest.md`.

### Evaluation-set composition (rebalanced)
The 20-row eval (4 per language) previously concentrated ~85% of items on fresh-frass-in-the-whorl
identification. It was rebalanced to measure a broader diagnostic and agronomic toolkit while holding
the 4-per-language balance and 100% citation rate:

| Capability | Rows |
|---|---|
| Vision handoff / low-confidence clarification | 4 |
| Look-alike diagnostic (larval Y-mark and dorsal spots) | 3 |
| Frass/whorl "current infestation" signs | 3 |
| Scouting method (W-pattern, 10-plant stations) | 2 |
| Egg-mass diagnostics | 3 |
| Life-cycle reasoning (a moth ≠ whole-field infestation) | 2 |
| Cultural/mechanical control (intercropping, manual destruction) | 2 |
| Pesticide dose-safety deferral | 1 |

Fresh-frass-as-primary-diagnostic dropped from ~85% to ~35% (retained only where "current infestation"
is the concept under test). New non-English eval items were adapted from already-vetted train-set
phrasings and citations; they still warrant a native-speaker spot-check before being treated as final.
No eval instruction or response duplicates a train row verbatim (leakage check passed).

## Safety/data-quality choice
The source file contained examples that treated pesticide concentrations as universal. Those figures were intentionally not propagated. This dataset instead teaches the model to avoid guessing a pesticide dose and to defer to the locally registered product label and appropriate agricultural guidance.

## Fine-tuning notes
- The examples are intentionally FAW-specific; generic crop/livestock questions are excluded.
- Answers are concise and action-oriented.
- Source attribution is embedded directly in each response, so the model learns to cite its basis.
- Low-confidence examples explicitly teach the assistant to ask a targeted follow-up question rather than forcing a diagnosis.
- Multi-turn examples teach the assistant to retain the FAW context across follow-up questions.
