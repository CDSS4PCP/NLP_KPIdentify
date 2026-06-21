# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 980 | 49.0% |
| False Negative | 571 | 28.5% |
| Boundary Error | 451 | 22.5% |
| Abbreviation | 135 | 6.7% |
| Nested Phrase | 445 | 22.2% |
| True Positive | 1563 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.20%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.46%**
- Total predicted spans: 2994 · Total gold spans: 2585

## Annotated Examples

### False Positive (980 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK> algorithms`

### False Negative (571 total)
- missed gold: `clinicians`
- missed gold: `feature modifications`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `<UNK>`

### Boundary Error (451 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `model interpretations` → pred: `model`
- gold: `prediction models` → pred: `prediction models model`

### Abbreviation (135 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (445 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `model interpretations` → pred: `model`
- gold: `prediction models` → pred: `prediction models model`
