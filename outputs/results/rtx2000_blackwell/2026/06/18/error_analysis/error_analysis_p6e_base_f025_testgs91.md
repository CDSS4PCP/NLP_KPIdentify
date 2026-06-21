# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1116 | 49.5% |
| False Negative | 661 | 29.3% |
| Boundary Error | 478 | 21.2% |
| Abbreviation | 127 | 5.6% |
| Nested Phrase | 479 | 21.2% |
| True Positive | 1446 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **47.57%**
- Strict entity recall (TP / (TP+FN+boundary)): **55.94%**
- Total predicted spans: 3040 · Total gold spans: 2585

## Annotated Examples

### False Positive (1116 total)
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK>`
- spurious pred: `model`
- spurious pred: `aki`

### False Negative (661 total)
- missed gold: `feature modifications`
- missed gold: `described`
- missed gold: `settings`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `clinician trust`

### Boundary Error (478 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`

### Abbreviation (127 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `or`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (479 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`
