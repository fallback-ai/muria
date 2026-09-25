# FAW fine-tuning dataset — improvement plan

Prepared 2026-09-24. Maps the dataset review to concrete, verifiable changes against the current files
(`faw_finetune_train.jsonl`, `faw_finetune_eval.jsonl`).

## Ground truth (measured, not estimated)

| Metric | Train (125) | Eval (20) |
|---|---|---|
| Per language (en/ha/ig/yo/pcm) | 25 each | 4 each |
| Source citation present | 125 (100%) | 20 (100%) |
| frass/whorl referenced | 52 (42%) | **17 (85%)** |
| Multi-turn examples | 24 | 6 |
| Max dialogue depth | **2 exchanges** | 2 |
| intercrop / cultural controls | 3 | 0 |
| pesticide / dose handling | 6 | 0 |
| egg-mass diagnostics | 18 | 0 |
| life-cycle education | 23 | 6 |
| out-of-scope, weather, out-of-stock, persona | 0 | 0 |

**What holds up:** 100% citation compliance, dose-safety deferral, Tier-1 vision handoff, balanced
language counts. **What the numbers expose:** the eval set is 85% frass — it barely tests anything else,
so eval scores will not reflect the broader toolkit we want.

## Priority 0 — Format / turn-token alignment (do first: mechanical, verifiable, no new claims)

Multi-turn examples currently encode dialogue as literal text inside `instruction`:

```
"instruction": "Farmer: Ahụrụ m egg mass n'akwụkwọ.\nAssistant: Lelee ya nke ọma.\nFarmer: Kedu ihe m ga-achọ?"
```

The model learns to *emit the strings* "Farmer:"/"Assistant:" rather than to hold a real turn structure.
Gemma expects turn tokens: `<start_of_turn>user … <end_of_turn><start_of_turn>model … <end_of_turn>`.

**Action:** add a `messages` array to each row (keep `instruction`/`response` for backward compat, or
migrate fully — decide with the trainer). Single-turn → 1 user + 1 model turn. Multi-turn → parse the
`Farmer:`/`Assistant:` segments into alternating `user`/`model` turns. This is a scripted transform with a
round-trip check (no content invented). ~24 train + 6 eval rows change shape; all 145 get a `messages` field.

## Priority 1 — Rebalance the eval set

Eval currently can't measure most target behaviors. Rebuild the 20-row eval so no single diagnostic
(frass/whorl) exceeds ~30%, and each capability below has at least one probe per the languages it covers.
Keep 4 per language for balance. This is the cheapest change with the biggest signal improvement.

## Priority 2 — Diagnostic diversity (reduce frass dependence)

Add scenarios beyond "check fresh frass in the whorl", each grounded in the already-cited sources:
- windowpane/scraping damage on young leaves; ragged/elongated holes vs. clean-cut (cutworm/stem borer)
- larval markings (inverted-Y head, four dorsal spots) — CABI handbook
- egg-mass appearance and location — CABI handbook
- damage severity by density, natural-enemy presence — FAO scouting note
- distinguishing look-alikes (stem borer, cutworm, African armyworm)

## Priority 3 — Deeper multi-turn (4–5 exchanges)

Extend dialogues past 2 turns to match real farmer interactions: scout → interpret → decide action →
follow-up constraint (product unavailable / rain forecast) → next step. This is the conversational edge
over one-shot tools; it needs the P0 format fix in place first.

## Priority 4 — Topic coverage (new areas from the review)

- Growth-stage guidance: seedling vs. whorl vs. tassel management (FAO integrated-management note)
- Cultural/mechanical controls: push-pull, trap crops, tillage, manual egg-mass destruction
- Out-of-stock fallback: alternative when a named product is unavailable at the agro-dealer
- FAW life-cycle education (basic)
- Weather follow-ups: rain shortly after spraying

## Priority 5 — Persona and out-of-scope boundaries

- Identity: assistant recognizes itself as **Muria**, states its FAW-on-maize scope naturally
- Gentle fallback for non-FAW queries (rice blast, livestock, other pests) — decline + redirect, keep
  the citation habit or explicitly say it's outside scope

## Priority 6 — Volume (25 → 800–1000)

Each behavior currently rests on ~25 examples spread across 5 languages and 4+ capabilities at once.
Scale after P0–P5 define the templates, so growth is structured, not noisy.

### Open decision blocking P2–P6 at scale
Non-English rows (ha/ig/yo/pcm) train a model farmers act on. I can author and verify **English** grounded
in the cited sources; I cannot validate agronomic accuracy of machine-produced Hausa/Igbo/Yoruba/Pidgin.
**Recommendation:** author English-first, mark non-English generation for native/domain review before it
enters training, rather than silently shipping unvalidated multilingual advice.

## Suggested order of execution
1. P0 format transform (scripted, reversible) + round-trip verification
2. P1 eval rebalance
3. P2/P3 English templates for diversity + depth
4. P4/P5 new-topic + persona/out-of-scope English rows
5. Decide multilingual strategy, then P6 scale-up
