# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 808 | 56.5% |
| False Negative | 366 | 25.6% |
| Boundary Error | 257 | 18.0% |
| Abbreviation | 89 | 6.2% |
| Nested Phrase | 250 | 17.5% |
| True Positive | 557 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.34%**
- Strict entity recall (TP / (TP+FN+boundary)): **47.20%**
- Total predicted spans: 1622 · Total gold spans: 1180

## Annotated Examples

### False Positive (808 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (366 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (257 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (89 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (250 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
