# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1088 | 48.6% |
| False Negative | 671 | 30.0% |
| Boundary Error | 480 | 21.4% |
| Abbreviation | 128 | 5.7% |
| Nested Phrase | 482 | 21.5% |
| True Positive | 1434 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **47.77%**
- Strict entity recall (TP / (TP+FN+boundary)): **55.47%**
- Total predicted spans: 3002 · Total gold spans: 2585

## Annotated Examples

### False Positive (1088 total)
- spurious pred: `aki`
- spurious pred: `design`
- spurious pred: `black`
- spurious pred: `hospital aki`
- spurious pred: `patients`
- spurious pred: `korea`

### False Negative (671 total)
- missed gold: `clinical decision support`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `findings`

### Boundary Error (480 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `model interpretations` → pred: `model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`
- gold: `assessment` → pred: `real time assessment`

### Abbreviation (128 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- missed gold: `use`

### Nested Phrase (482 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `model interpretations` → pred: `model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`
- gold: `assessment` → pred: `real time assessment`
