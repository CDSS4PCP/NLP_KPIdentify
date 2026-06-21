# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1204 | 49.4% |
| False Negative | 701 | 28.7% |
| Boundary Error | 534 | 21.9% |
| Abbreviation | 246 | 10.1% |
| Nested Phrase | 546 | 22.4% |
| True Positive | 1329 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **43.33%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.83%**
- Total predicted spans: 3067 · Total gold spans: 2564

## Annotated Examples

### False Positive (1204 total)
- spurious pred: `real`
- spurious pred: `aki`
- spurious pred: `design`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `patients`

### False Negative (701 total)
- missed gold: `models`
- missed gold: `training`
- missed gold: `internal validation`
- missed gold: `external validation cohorts`
- missed gold: `model development`
- missed gold: `missing data`

### Boundary Error (534 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `increases` → pred: `cds increases`

### Abbreviation (246 total)
- spurious pred: `real`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (546 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `increases` → pred: `cds increases`
