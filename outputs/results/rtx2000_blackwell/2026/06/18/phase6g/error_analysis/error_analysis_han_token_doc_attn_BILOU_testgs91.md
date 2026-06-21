# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1235 | 51.1% |
| False Negative | 639 | 26.4% |
| Boundary Error | 545 | 22.5% |
| Abbreviation | 114 | 4.7% |
| Nested Phrase | 530 | 21.9% |
| True Positive | 1401 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **44.04%**
- Strict entity recall (TP / (TP+FN+boundary)): **54.20%**
- Total predicted spans: 3181 · Total gold spans: 2585

## Annotated Examples

### False Positive (1235 total)
- spurious pred: `aki`
- spurious pred: `hospital aki`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `<UNK> algorithms`
- spurious pred: `aki`

### False Negative (639 total)
- missed gold: `model interpretations`
- missed gold: `feature modifications`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `detection control`

### Boundary Error (545 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `prediction models` → pred: `prediction models model`
- gold: `prediction` → pred: `aki prediction model`
- gold: `assessment` → pred: `time assessment`

### Abbreviation (114 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (530 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `prediction models` → pred: `prediction models model`
- gold: `prediction` → pred: `aki prediction model`
- gold: `assessment` → pred: `time assessment`
