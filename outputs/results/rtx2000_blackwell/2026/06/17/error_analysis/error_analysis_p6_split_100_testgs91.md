# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 911 | 47.9% |
| False Negative | 569 | 29.9% |
| Boundary Error | 421 | 22.1% |
| Abbreviation | 120 | 6.3% |
| Nested Phrase | 421 | 22.1% |
| True Positive | 1595 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **54.49%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.70%**
- Total predicted spans: 2927 · Total gold spans: 2585

## Annotated Examples

### False Positive (911 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `<UNK>`
- spurious pred: `interpretation`
- spurious pred: `patients`
- spurious pred: `end stage`
- spurious pred: `development`

### False Negative (569 total)
- missed gold: `clinicians`
- missed gold: `training`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `interventions`

### Boundary Error (421 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `assessment` → pred: `provide real time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `<UNK> challenges`

### Abbreviation (120 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (421 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `assessment` → pred: `provide real time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `<UNK> challenges`
