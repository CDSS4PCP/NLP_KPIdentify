# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1038 | 46.3% |
| False Negative | 697 | 31.1% |
| Boundary Error | 505 | 22.5% |
| Abbreviation | 107 | 4.8% |
| Nested Phrase | 501 | 22.4% |
| True Positive | 1383 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **47.27%**
- Strict entity recall (TP / (TP+FN+boundary)): **53.50%**
- Total predicted spans: 2926 · Total gold spans: 2585

## Annotated Examples

### False Positive (1038 total)
- spurious pred: `design`
- spurious pred: `patients`
- spurious pred: `hospitals`
- spurious pred: `model`
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`

### False Negative (697 total)
- missed gold: `models`
- missed gold: `outcome variable`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `<UNK>`

### Boundary Error (505 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `prediction models mostly`
- gold: `model output` → pred: `linking model output`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `model interpretations` → pred: `model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`

### Abbreviation (107 total)
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (501 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `prediction models mostly`
- gold: `model output` → pred: `linking model output`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `model interpretations` → pred: `model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
