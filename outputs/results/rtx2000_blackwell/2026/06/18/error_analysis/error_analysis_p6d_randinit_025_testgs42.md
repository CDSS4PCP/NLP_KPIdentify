# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 840 | 58.6% |
| False Negative | 331 | 23.1% |
| Boundary Error | 262 | 18.3% |
| Abbreviation | 78 | 5.4% |
| Nested Phrase | 254 | 17.7% |
| True Positive | 587 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.75%**
- Strict entity recall (TP / (TP+FN+boundary)): **49.75%**
- Total predicted spans: 1689 · Total gold spans: 1180

## Annotated Examples

### False Positive (840 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `assistance`
- spurious pred: `treatment`
- spurious pred: `treatment`
- spurious pred: `guidelines`

### False Negative (331 total)
- missed gold: `disseminate`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (262 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (78 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (254 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
