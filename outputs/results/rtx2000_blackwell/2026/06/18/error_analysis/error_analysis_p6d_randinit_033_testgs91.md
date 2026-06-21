# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1072 | 49.1% |
| False Negative | 632 | 28.9% |
| Boundary Error | 481 | 22.0% |
| Abbreviation | 122 | 5.6% |
| Nested Phrase | 478 | 21.9% |
| True Positive | 1472 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **48.66%**
- Strict entity recall (TP / (TP+FN+boundary)): **56.94%**
- Total predicted spans: 3025 · Total gold spans: 2585

## Annotated Examples

### False Positive (1072 total)
- spurious pred: `aki`
- spurious pred: `<UNK>`
- spurious pred: `box`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `vital signs`

### False Negative (632 total)
- missed gold: `feature modifications`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `<UNK>`
- missed gold: `interventions`

### Boundary Error (481 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`

### Abbreviation (122 total)
- spurious pred: `aki`
- spurious pred: `box`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`

### Nested Phrase (478 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
