# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1130 | 50.2% |
| False Negative | 624 | 27.7% |
| Boundary Error | 497 | 22.1% |
| Abbreviation | 148 | 6.6% |
| Nested Phrase | 497 | 22.1% |
| True Positive | 1464 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **47.36%**
- Strict entity recall (TP / (TP+FN+boundary)): **56.63%**
- Total predicted spans: 3091 · Total gold spans: 2585

## Annotated Examples

### False Positive (1130 total)
- spurious pred: `aki`
- spurious pred: `challenges`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `aki`
- spurious pred: `patients`

### False Negative (624 total)
- missed gold: `clinical decision support`
- missed gold: `feature modifications`
- missed gold: `findings`
- missed gold: `<UNK>`
- missed gold: `clinician trust`
- missed gold: `measures`

### Boundary Error (497 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`

### Abbreviation (148 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (497 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`
- gold: `assessment` → pred: `real time assessment`
