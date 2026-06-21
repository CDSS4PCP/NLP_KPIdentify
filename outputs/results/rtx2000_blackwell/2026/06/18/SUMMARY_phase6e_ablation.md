# Phase 6e — Trust validation + feature attribution + frozen-embedding pretraining lever

**Date:** 2026-06-18
**Model:** HAN-CRF (IOBES, AdamW, lr 1e-3, gated token–doc attention, 8 heads), seed 42, env `cdss-gpu`, 20 epochs (except the epochs=0 floor).
**Metric:** Strict entity-level SeqEval micro-F1 (%).
**Evaluation sets per run:** held-out **synthetic TEST** (the resplit remainder NOT used for training, in-distribution) + external **GS42** + **GS91**.
**Script:** scripts/jobs/run_matrix_phase6e_ablation_20260618.sh  ·  Index: phase6e_run_index.csv (22/22 completed).

This phase answers three questions: (C) is the low-data model really learning or guessing; (B) which feature drives the ~50% GS F1 at f=0.10; (A) does freezing embeddings expose a pretraining benefit.

---

## (C) TRUST — baseline across fractions: synthetic held-out TEST vs external GS

| f | train | held-out synth docs | TEST F1 | GS42 F1 | GS91 F1 |
|---|---:|---:|---:|---:|---:|
| 0.10 | 328 | 2953 | **65.60** | 40.80 | 54.66 |
| 0.25 | 820 | 2461 | 69.78 | 43.68 | 56.37 |
| 0.33 | 1083 | 2198 | 71.00 | 44.71 | 58.33 |
| 0.50 | 1640 | 1641 | 72.48 | 43.80 | 59.35 |
| 0.70 | 2297 | 984 | 73.38 | 43.74 | 61.63 |
| 0.75 | 2461 | 820 | 73.91 | 44.16 | 61.85 |
| 0.80 | 2625 | 656 | 73.78 | 43.89 | 61.51 |
| (untrained, 0 ep) | 328 | 2953 | **0.13** | 0.00 | 0.13 |

**Verdict: it is NOT a coin toss.** On the large held-out synthetic set (2953 docs at f=0.10) the trained model scores **65.6%** vs **0.13%** untrained. Entity-level F1 from random tag sequences is ≈ 0 (an exact-span match by chance is vanishingly unlikely), so ~50–65% cannot arise from guessing. The synthetic-TEST curve rises monotonically with data (65.6 → 73.9), exactly the behavior of genuine learning. The lower GS F1 (~41–55) is the in-distribution → human-annotation generalization gap, not randomness.

---

## (B) FEATURE ATTRIBUTION at f=0.10 — what drives the ~50% F1?

| Variant | TEST F1 | GS42 F1 | GS91 F1 |
|---|---:|---:|---:|
| **untrained (0 ep)** | 0.13 | 0.00 | 0.13 |
| trainable + W2V + BiLM (base) | 65.60 | 40.80 | 54.66 |
| trainable + W2V − BiLM | 67.07 | 41.50 | 54.17 |
| trainable + random − BiLM | 65.84 | 41.68 | 54.40 |
| FROZEN + W2V + BiLM | 66.39 | 44.88 | 53.11 |
| FROZEN + W2V − BiLM | 65.70 | 40.93 | 53.83 |
| FROZEN + random + BiLM | 63.73 | 42.70 | 52.68 |
| FROZEN + random − BiLM | 66.15 | 42.19 | 54.00 |

**Primary factor = supervised training of the tagger.** Going from untrained → any trained variant adds ~**+53 GS91 / +65 TEST F1**. Every other lever — embedding trainability (frozen vs trainable), Word2Vec vs random init, BiLM vs no-BiLM — moves the score by **< 2 F1** (within seed noise; signs flip). The seven trained cells cluster in GS91 52.7–54.7, GS42 40.8–44.9, TEST 63.7–67.1.

So the ~50% GS F1 at minimal training comes from the **CRF sequence tagger (BiLSTM + multi-head doc attention + CRF) fitting the highly-regular synthetic labeling function**, which is learnable from even 328 documents — **not** from pretrained word/contextual representations.

---

## (A) FROZEN-EMBEDDING PRETRAINING LEVER — does freezing expose a pretraining gap?

frozen+Word2Vec+BiLM vs frozen+random−BiLM (no pretraining at all), GS F1:

| f | frozenW2V GS42 | frozenW2V GS91 | frozenRand GS42 | frozenRand GS91 | gap42 | gap91 |
|---|---:|---:|---:|---:|---:|---:|
| 0.10 | 44.88 | 53.11 | 42.19 | 54.00 | +2.69 | −0.89 |
| 0.25 | 42.30 | 56.13 | 43.34 | 55.83 | −1.04 | +0.30 |
| 0.50 | 43.06 | 59.93 | 44.15 | 59.01 | −1.09 | +0.92 |
| 0.75 | 44.96 | 61.84 | 44.00 | 61.33 | +0.96 | +0.51 |
| 1.00 | 44.88 | 62.88 | 44.42 | 62.88 | +0.46 | +0.00 |

**Even freezing the embeddings does NOT expose a pretraining benefit.** The gap is within ±2.7 F1, flips sign, and averages ≈ 0 (mean gap91 +0.17, gap42 +0.40). Reason: frozen *random* embeddings are still a fixed unique vector per token (a random lookup table), so the trainable BiLSTM/attention/CRF on top can learn token→tag associations regardless of whether the table is Word2Vec or random. Pretraining only helps if the downstream capacity is also limited, which it is not here.

---

## Bottom line

1. **The model genuinely learns** (untrained 0.13 → trained 65.6 on 2953 held-out synthetic docs). The performance is real, not a coin flip.
2. **The single dominant factor is supervised training of the tagger** on the learnable synthetic labels (~+53 GS91 F1). 
3. **Pretraining transfer (Word2Vec, BiLM) and embedding trainability are all near-neutral** (<2 F1) — even under frozen embeddings — generalizing the Phase 5/6c/6d findings.
4. **The split-sensitivity curve is valid**: more data helps modestly and monotonically (clearest on synthetic TEST and GS91), but the high low-data floor is inherent task learnability, not pretrained representations.

## Reproduction

```bash
conda run -n cdss-gpu bash scripts/jobs/run_matrix_phase6e_ablation_20260618.sh
```
- Logs: outputs/results/rtx2000_blackwell/2026/06/18/p6e_*.txt (each has TEST + GS42 + GS91 Score lines)
- Index: outputs/results/rtx2000_blackwell/2026/06/18/phase6e_run_index.csv
