# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1120 | 48.8% |
| False Negative | 655 | 28.6% |
| Boundary Error | 518 | 22.6% |
| Abbreviation | 109 | 4.8% |
| Nested Phrase | 516 | 22.5% |
| True Positive | 1412 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **46.30%**
- Strict entity recall (TP / (TP+FN+boundary)): **54.62%**
- Total predicted spans: 3050 · Total gold spans: 2585

## Annotated Examples

### False Positive (1120 total)
- spurious pred: `<UNK>`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `hospital aki`
- spurious pred: `patients`
- spurious pred: `model`

### False Negative (655 total)
- missed gold: `feature modifications`
- missed gold: `measures`
- missed gold: `impact`
- missed gold: `investigators followed`
- missed gold: `searched`
- missed gold: `accuracy`

### Boundary Error (518 total)
- gold: `model output` → pred: `linking model output`
- gold: `model interpretations` → pred: `applicable model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `outcome variable` → pred: `outcome variable for model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `prediction model`

### Abbreviation (109 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (516 total)
- gold: `model output` → pred: `linking model output`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `outcome variable` → pred: `outcome variable for model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `prediction model`
- gold: `increases` → pred: `<UNK> increases`
