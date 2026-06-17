# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 982 | 42.8% |
| False Negative | 816 | 35.5% |
| Boundary Error | 499 | 21.7% |
| Abbreviation | 0 | 0.0% |
| Nested Phrase | 507 | 22.1% |
| True Positive | 1249 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.75%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.71%**
- Total predicted spans: 2730 · Total gold spans: 2564

## Annotated Examples

### False Positive (982 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `algorithms`
- spurious pred: `model`
- spurious pred: `aki`
- spurious pred: `model`

### False Negative (816 total)
- missed gold: `performance`
- missed gold: `developed`
- missed gold: `evaluated`
- missed gold: `external validation`
- missed gold: `models`
- missed gold: `training`
- missed gold: `internal validation`
- missed gold: `external validation cohorts`

### Boundary Error (499 total)
- gold: `clinical decision support` → pred: `real time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `increases` → pred: `cds increases`
- gold: `undercontrolled` → pred: `undercontrolled cds challenges`
- gold: `data entry requests` → pred: `data entry`
- gold: `challenges` → pred: `wireless connectivity challenges`

### Nested Phrase (507 total)
- gold: `clinical decision support` → pred: `real time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `increases` → pred: `cds increases`
- gold: `undercontrolled` → pred: `undercontrolled cds challenges`
- gold: `data entry requests` → pred: `data entry`
- gold: `challenges` → pred: `wireless connectivity challenges`
