# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 989 | 46.8% |
| False Negative | 693 | 32.8% |
| Boundary Error | 433 | 20.5% |
| Abbreviation | 110 | 5.2% |
| Nested Phrase | 436 | 20.6% |
| True Positive | 1459 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **50.64%**
- Strict entity recall (TP / (TP+FN+boundary)): **56.44%**
- Total predicted spans: 2881 · Total gold spans: 2585

## Annotated Examples

### False Positive (989 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK> algorithms`

### False Negative (693 total)
- missed gold: `models`
- missed gold: `feature modifications`
- missed gold: `findings`
- missed gold: `use`
- missed gold: `measures`
- missed gold: `<UNK>`

### Boundary Error (433 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `developed` → pred: `developed model`

### Abbreviation (110 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (436 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `developed` → pred: `developed model`
