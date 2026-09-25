# FAW fine-tuning dataset — provenance & review manifest

Generated 2026-09-25. Read this before training or publishing.

## Files
| File | Rows | What it is |
|---|---|---|
| `faw_finetune_train.seed.jsonl` | 285 | **The vetted core.** 57 rows/language. Every distinct concept and answer lives here. Review this file. |
| `faw_finetune_train.jsonl` | 530 | Training set: the 285 seed rows + 245 augmented variants (106 rows/language), **capped at 2 rows per distinct answer**. |
| `faw_finetune_eval.jsonl` | 20 | Held-out eval, 4/language, rebalanced across 8 capabilities. No instruction overlaps train. |

## Provenance of the 530 train rows
- **285 seed rows** = the original balanced core + English-authored P2–P5 rows + their ha/ig/yo/pcm translations.
- **245 augmented rows** = variants of seed rows, chosen to **prefer meaningful input variety**
  (vision-signal scenarios with different confidence percentages and confusable pests) over shallow
  question rephrasings, and hard-capped so **no answer appears more than twice**.
- **285 distinct responses; duplication reduced from ~3.2× to 1.86× (max 2 copies of any answer).**
  Deduplicated (0 exact-duplicate instructions), 0 train/eval leakage. To train on the cleanest set with
  zero duplication, use `faw_finetune_train.seed.jsonl` (285) directly.

## What still needs a human pass (do not skip before a farmer-facing release)
1. **Non-English accuracy (ha/ig/yo).** The 96 non-English seed rows (P2–P5) and their augmented variants
   were machine-produced, anchored to already-vetted dataset vocabulary. Pidgin is most reliable;
   **Hausa, Igbo and Yoruba need a native + agronomic reviewer.** Review the seed file, not all 900.
2. **Augmentation ratio.** Now capped at 2× (1.86× average). If you still see memorisation, drop to the
   285-row seed (zero duplication) and compare eval loss.
3. **Agronomic claims** are grounded in FAO Guidance Note 2, FAO Integrated Management, and the CABI Field
   Handbook, and all doses/thresholds are deferred to the local product label / extension — verify this
   deferral held in the non-English rows during review.

## Reproducing
Scripts used (in the session scratchpad): `transform.py` (P0 turn tokens), eval rebuild (P1),
`add_p2p3.py`, `add_p4p5.py`, `translate.py`, `augment.py`. Backups of each pre-change train state were
kept in the scratchpad during generation.
