# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 812 | 58.1% |
| False Negative | 351 | 25.1% |
| Boundary Error | 234 | 16.8% |
| Abbreviation | 69 | 4.9% |
| Nested Phrase | 224 | 16.0% |
| True Positive | 595 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.26%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.42%**
- Total predicted spans: 1641 · Total gold spans: 1180

## Annotated Examples

### False Positive (812 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK>`
- spurious pred: `<UNK> systems`
- spurious pred: `assistance`
- spurious pred: `patient`

### False Negative (351 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (234 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (69 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (224 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
