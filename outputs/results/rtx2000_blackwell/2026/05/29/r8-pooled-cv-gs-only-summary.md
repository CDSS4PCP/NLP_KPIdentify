# R8 Summary: Pooled In-Domain CV with GS-Only Final Evaluation

## Protocol
- Train mode pools in-domain `train.json` + `test.json`.
- Model selection uses 5-fold CV split (`k=5`, folds 0..4).
- Final evaluation mode runs only on GS datasets (`testGS`): GS42 and GS91.
- Settings: HAN-CRF, BIO, freeze embeddings, fixed batch mode, block diagonal mask, early stop patience=3.

## Per-Fold SeqEval F1 (%)
| Fold | GS42 | GS91 |
|---|---:|---:|
| 0 | 42.45 | 53.05 |
| 1 | 42.96 | 53.22 |
| 2 | 42.05 | 53.46 |
| 3 | 42.80 | 53.95 |
| 4 | 43.09 | 53.37 |

## Aggregate (5-fold)
- GS42 mean: 42.67 (std 0.38)
- GS91 mean: 53.41 (std 0.30)

## Comparison to R7 (train-only CV, GS final)
- R7 GS42 mean: 41.75
- R7 GS91 mean: 52.45
- Delta (R8 - R7): GS42 +0.92, GS91 +0.96

## Artifacts
- Fold logs:
  - outputs/results/rtx2000_blackwell/2026/05/29/r8-han-k5cv-pooledtraintest-fold0.md
  - outputs/results/rtx2000_blackwell/2026/05/29/r8-han-k5cv-pooledtraintest-fold1.md
  - outputs/results/rtx2000_blackwell/2026/05/29/r8-han-k5cv-pooledtraintest-fold2.md
  - outputs/results/rtx2000_blackwell/2026/05/29/r8-han-k5cv-pooledtraintest-fold3.md
  - outputs/results/rtx2000_blackwell/2026/05/29/r8-han-k5cv-pooledtraintest-fold4.md
- Fold metrics CSV:
  - outputs/results/rtx2000_blackwell/2026/05/29/r8-fold-metrics.csv
