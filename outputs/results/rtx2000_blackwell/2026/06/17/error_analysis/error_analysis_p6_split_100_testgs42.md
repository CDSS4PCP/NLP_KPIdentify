# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 818 | 58.5% |
| False Negative | 328 | 23.4% |
| Boundary Error | 253 | 18.1% |
| Abbreviation | 79 | 5.6% |
| Nested Phrase | 244 | 17.4% |
| True Positive | 599 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.87%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.76%**
- Total predicted spans: 1670 · Total gold spans: 1180

## Annotated Examples

### False Positive (818 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `treatment`

### False Negative (328 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`

### Boundary Error (253 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
- gold: `functions` → pred: `<UNK> functions`

### Abbreviation (79 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `ed`

### Nested Phrase (244 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
- gold: `functions` → pred: `<UNK> functions`
