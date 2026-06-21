# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 813 | 58.7% |
| False Negative | 332 | 24.0% |
| Boundary Error | 241 | 17.4% |
| Abbreviation | 75 | 5.4% |
| Nested Phrase | 231 | 16.7% |
| True Positive | 607 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.54%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.44%**
- Total predicted spans: 1661 · Total gold spans: 1180

## Annotated Examples

### False Positive (813 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `treatment`

### False Negative (332 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (241 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (75 total)
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (231 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
