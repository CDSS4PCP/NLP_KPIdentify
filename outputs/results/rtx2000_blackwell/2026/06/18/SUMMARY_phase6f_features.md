# Phase 6e — Group 4: Hand-crafted feature ablation @ f=0.10

**Question (user):** which hand-crafted feature (CEM/WFOF/POS/LEN/TI/TR) is responsible
for the "tremendous" performance at the 0.10 train ratio — it's hard to believe in
real-world ML training?

**Answer:** None of them. Removing *all six* hand-crafted features costs only
**-2.72 F1 on the synthetic held-out TEST** and **< 1 F1 on both external gold
standards** (GS42 -1.00, GS91 -0.87). No single feature is a driver; every
leave-one-out and single-feature result lies inside the ±2-3 F1 single-seed noise
band already measured in Phases 6c/6d (sign flips across metrics). The ~54% GS91
floor at f=0.10 comes from the **supervised CRF fit to the learnable synthetic
labels over word embeddings**, not the engineered features.

## Setup
- Script: `scripts/jobs/run_matrix_phase6f_handcrafted_features_20260618.sh` (11 runs).
- Run index: `outputs/results/rtx2000_blackwell/2026/06/18/phase6f_run_index.csv`.
- Representation config held FIXED at the Phase 6e baseline: trainable embeddings +
  Word2Vec + BiLM, f=0.10 (328 train / 2953 test, seed 42), 20 epochs. Only
  `--features` varied. Each run reports synthetic held-out TEST + GS42 + GS91.

## How features enter the model (verified `gna_experiment.py` ~1124-1210)
- `POS` -> `feats_pos` (nltk Penn tag id, categorical embedding input).
- `LEN`/`WFOF`/`TI`/`TR` -> `feats_cont[0..3]` (float continuous inputs).
- `CEM` -> **no-op**: present in the default list but never consumed in the feature
  builder (`rev_data` 7-tuple has no CEM slot).
- Disabling a feature **zeroes its value** (tensor shape unchanged) -> the feature is
  neutralized without altering model architecture or breaking checkpoint loading.
- The same `--features` set is applied to train + test + testGS (consistent
  featurization). `--features NONE` => no real name matches => every feature zeroed
  (word-embeddings + BiLM only).

## Results (SeqEval strict micro-F1 %)

| config | features enabled | TEST | GS42 | GS91 |
|---|---|---:|---:|---:|
| **baseline (Phase 6e p6e_base_f010)** | all (POS,WFOF,LEN,TI,TR; CEM no-op) | **65.60** | **40.80** | **54.66** |
| p6f_feat_none | none (word-emb + BiLM only) | 62.88 | 39.80 | 53.79 |
| p6f_feat_noPOS | WFOF,LEN,TI,TR | 65.06 | 40.56 | 51.88 |
| p6f_feat_noWFOF | POS,LEN,TI,TR | 64.83 | 41.21 | 54.14 |
| p6f_feat_noLEN | POS,WFOF,TI,TR | 65.67 | 41.52 | 52.58 |
| p6f_feat_noTI | POS,WFOF,LEN,TR | 66.14 | 42.67 | 54.26 |
| p6f_feat_noTR | POS,WFOF,LEN,TI | 65.21 | 42.81 | 54.71 |
| p6f_feat_onlyPOS | POS | 63.42 | 40.18 | 53.73 |
| p6f_feat_onlyLEN | LEN | 63.10 | 41.16 | 53.27 |
| p6f_feat_onlyWFOF | WFOF | 63.86 | 40.28 | 52.62 |
| p6f_feat_onlyTI | TI | 63.78 | 41.35 | 53.97 |
| p6f_feat_onlyTR | TR | 63.89 | 43.12 | 51.91 |

### Delta vs baseline (negative = feature(s) helped baseline)
| config | dTEST | dGS42 | dGS91 |
|---|---:|---:|---:|
| none (drop ALL features) | -2.72 | -1.00 | -0.87 |
| noPOS | -0.54 | -0.24 | -2.78 |
| noWFOF | -0.77 | +0.41 | -0.52 |
| noLEN | +0.07 | +0.72 | -2.08 |
| noTI | +0.54 | +1.87 | -0.40 |
| noTR | -0.39 | +2.01 | +0.05 |

## Interpretation
1. **Total feature contribution is small.** All six features together add only
   ~2.7 F1 on TEST and ~0.9 F1 on GS91 over a word-embedding+BiLM model with no
   hand-crafted features. On GS42 they add ~1 F1.
2. **No single feature dominates.** Leave-one-out drops are all within ±2.8 F1 and
   the sign flips across the three eval sets (e.g. dropping TI/TR *improves* GS42 by
   ~+2). Single-feature runs each land at ~63 TEST / ~53 GS91 — essentially the
   `none` level — so no feature alone recovers the (already tiny) full-feature gain.
3. **The engineered keyphrase-signal features are not the secret either.** TI
   (tf-idf) and TR (textrank) are the features most plausibly "leaking" keyphrase-ness;
   removing them does not hurt (even helps GS42), and using them alone does not beat
   the no-feature model. So the high f=0.10 score is not feature leakage.
4. **Consistent with Phases 6c/6d/6e.** Untrained = 0.13 F1; trained = ~54. The jump
   is the supervised fit to learnable synthetic labels over (even random, even frozen)
   word embeddings. Pretraining (W2V/BiLM), freezing, random init, AND now the
   hand-crafted features are each worth < ~3 F1 — all inside single-seed noise.

## Bottom line for the manuscript
The surprisingly strong low-data (f=0.10) performance is **robust to removing every
hand-crafted feature** (< 1 F1 drop on both external gold standards). It is therefore
*not* an artefact of a clever engineered feature; it reflects the CRF sequence tagger
learning the (genuinely learnable) synthetic labeling from ~328 documents. The
hand-crafted features provide only marginal, non-significant refinement at this scale.
Recommend reporting this as a feature-ablation row and tempering any claim that the
engineered features drive low-data performance. (Single seed; deltas this small
warrant a multi-seed CI before any directional claim about an individual feature.)
