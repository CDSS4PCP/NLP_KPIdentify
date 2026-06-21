# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 846 | 59.3% |
| False Negative | 333 | 23.3% |
| Boundary Error | 248 | 17.4% |
| Abbreviation | 89 | 6.2% |
| Nested Phrase | 240 | 16.8% |
| True Positive | 599 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.38%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.76%**
- Total predicted spans: 1693 · Total gold spans: 1180

## Annotated Examples

### False Positive (846 total)
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (333 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (248 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (89 total)
- spurious pred: `art`
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (240 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
