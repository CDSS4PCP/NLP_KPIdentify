# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1096 | 46.4% |
| False Negative | 726 | 30.7% |
| Boundary Error | 539 | 22.8% |
| Abbreviation | 0 | 0.0% |
| Nested Phrase | 543 | 23.0% |
| True Positive | 1299 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **44.27%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.66%**
- Total predicted spans: 2934 · Total gold spans: 2564

## Annotated Examples

### False Positive (1096 total)
- spurious pred: `real`
- spurious pred: `aki`
- spurious pred: `challenges`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `patients`

### False Negative (726 total)
- missed gold: `lacking`
- missed gold: `models`
- missed gold: `training`
- missed gold: `internal validation`
- missed gold: `external validation cohorts`
- missed gold: `model development`
- missed gold: `missing data`
- missed gold: `estimated`

### Boundary Error (539 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `developed` → pred: `developed model`
- gold: `challenges` → pred: `cds challenges`
- gold: `data entry requests` → pred: `data entry`
- gold: `challenges` → pred: `wireless connectivity challenges`
- gold: `clinician trust` → pred: `clinician`

### Nested Phrase (543 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `developed` → pred: `developed model`
- gold: `challenges` → pred: `cds challenges`
- gold: `data entry requests` → pred: `data entry`
- gold: `challenges` → pred: `wireless connectivity challenges`
- gold: `clinician trust` → pred: `clinician`
