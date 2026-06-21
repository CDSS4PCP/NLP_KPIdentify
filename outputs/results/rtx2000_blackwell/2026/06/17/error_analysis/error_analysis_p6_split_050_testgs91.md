# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1063 | 50.3% |
| False Negative | 574 | 27.2% |
| Boundary Error | 476 | 22.5% |
| Abbreviation | 112 | 5.3% |
| Nested Phrase | 466 | 22.1% |
| True Positive | 1535 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **49.93%**
- Strict entity recall (TP / (TP+FN+boundary)): **59.38%**
- Total predicted spans: 3074 · Total gold spans: 2585

## Annotated Examples

### False Positive (1063 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK> algorithms`

### False Negative (574 total)
- missed gold: `clinicians`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `searched`
- missed gold: `clinical setting`

### Boundary Error (476 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `model interpretations` → pred: `model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`

### Abbreviation (112 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (466 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `model interpretations` → pred: `model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
