# R7 Comparison Summary (Full 5-Fold Aggregate)

## Experiment Definitions
- R2: HAN, mask-fix baseline, fixed batch + block diagonal defaults
- R3: R2 + frozen embeddings
- R4: R3 + validation split (0.1) + early stop (patience=3)
- R6: BiLSTM control + validation split (0.1) + early stop (patience=3)
- R7: HAN with K-fold validation split during training (`k=5`, seed=42), frozen embeddings, fixed batch + block diagonal defaults, early stop (patience=3)

## R7 Per-Fold SeqEval F1 (%)
| Fold | Test | GS42 | GS91 |
|---|---:|---:|---:|
| 0 | 75.87 | 41.91 | 51.76 |
| 1 | 75.24 | 41.67 | 52.92 |
| 2 | 75.61 | 40.87 | 52.21 |
| 3 | 74.82 | 41.47 | 52.48 |
| 4 | 75.22 | 42.84 | 52.89 |

## Aggregate SeqEval F1 (%)
| Experiment | Test | GS42 | GS91 |
|---|---:|---:|---:|
| R2 | 75.39 | 42.52 | 55.67 |
| R3 | 75.77 | 41.77 | 54.26 |
| R4 | 75.87 | 43.79 | 53.29 |
| R6 | 75.70 | 42.41 | 52.31 |
| R7 (5-fold mean) | 75.35 | 41.75 | 52.45 |

## R7 Variability (Std Dev Across Folds)
- Test std: 0.36
- GS42 std: 0.64
- GS91 std: 0.44

## Key Deltas for R7 (5-fold mean) vs Earlier
- R7 vs R4: Test -0.52, GS42 -2.04, GS91 -0.84
- R7 vs R2: Test -0.04, GS42 -0.77, GS91 -3.22
- R7 vs R6: Test -0.35, GS42 -0.66, GS91 +0.14

## Current Interpretation
- Full 5-fold R7 does not outperform R4 or R2 on any of the external GS sets.
- R7 is effectively tied with R2 on Test but with weaker GS42/GS91 transfer.
- Compared to BiLSTM control (R6), R7 is lower on Test and GS42, slightly higher on GS91.

## Artifacts
- Per-fold metrics CSV: `outputs/results/rtx2000_blackwell/2026/05/29/r7-fold-metrics.csv`
- Fold logs:
	- `outputs/results/rtx2000_blackwell/2026/05/29/r7-han-k5cv-fold0-live.md`
	- `outputs/results/rtx2000_blackwell/2026/05/29/r7-han-k5cv-fold1-live.md`
	- `outputs/results/rtx2000_blackwell/2026/05/29/r7-han-k5cv-fold2-live.md`
	- `outputs/results/rtx2000_blackwell/2026/05/29/r7-han-k5cv-fold3-live.md`
	- `outputs/results/rtx2000_blackwell/2026/05/29/r7-han-k5cv-fold4-live.md`
