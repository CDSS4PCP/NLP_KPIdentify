# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1178 | 49.9% |
| False Negative | 674 | 28.5% |
| Boundary Error | 510 | 21.6% |
| Abbreviation | 119 | 5.0% |
| Nested Phrase | 509 | 21.5% |
| True Positive | 1401 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.35%**
- Strict entity recall (TP / (TP+FN+boundary)): **54.20%**
- Total predicted spans: 3089 · Total gold spans: 2585

## Annotated Examples

### False Positive (1178 total)
- spurious pred: `aki`
- spurious pred: `clinical practice`
- spurious pred: `health care`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `patients`

### False Negative (674 total)
- missed gold: `clinicians`
- missed gold: `lacking`
- missed gold: `feature modifications`
- missed gold: `settings`
- missed gold: `increases`
- missed gold: `measures`

### Boundary Error (510 total)
- gold: `recurrent neural network <UNK>` → pred: `<UNK>`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `hospitalized` → pred: `hospitalized for`
- gold: `demographic data laboratory values vital signs` → pred: `laboratory values vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`

### Abbreviation (119 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (509 total)
- gold: `recurrent neural network <UNK>` → pred: `<UNK>`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `hospitalized` → pred: `hospitalized for`
- gold: `demographic data laboratory values vital signs` → pred: `laboratory values vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
