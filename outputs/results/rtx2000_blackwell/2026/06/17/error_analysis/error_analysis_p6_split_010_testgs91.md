# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1094 | 48.5% |
| False Negative | 662 | 29.4% |
| Boundary Error | 498 | 22.1% |
| Abbreviation | 106 | 4.7% |
| Nested Phrase | 492 | 21.8% |
| True Positive | 1425 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **47.23%**
- Strict entity recall (TP / (TP+FN+boundary)): **55.13%**
- Total predicted spans: 3017 · Total gold spans: 2585

## Annotated Examples

### False Positive (1094 total)
- spurious pred: `design`
- spurious pred: `patients`
- spurious pred: `hospitals`
- spurious pred: `patients`
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`

### False Negative (662 total)
- missed gold: `models`
- missed gold: `outcome variable`
- missed gold: `measures`
- missed gold: `impact`
- missed gold: `<UNK>`
- missed gold: `interventions`

### Boundary Error (498 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `prediction models mostly`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `model interpretations` → pred: `applicable model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `prediction models` → pred: `prediction models model`

### Abbreviation (106 total)
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (492 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `prediction models mostly`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
