# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 844 | 59.2% |
| False Negative | 327 | 22.9% |
| Boundary Error | 255 | 17.9% |
| Abbreviation | 90 | 6.3% |
| Nested Phrase | 248 | 17.4% |
| True Positive | 598 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.24%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.68%**
- Total predicted spans: 1697 · Total gold spans: 1180

## Annotated Examples

### False Positive (844 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (327 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`

### Boundary Error (255 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `integration` → pred: `cpgs integration`

### Abbreviation (90 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (248 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `integration` → pred: `cpgs integration`
