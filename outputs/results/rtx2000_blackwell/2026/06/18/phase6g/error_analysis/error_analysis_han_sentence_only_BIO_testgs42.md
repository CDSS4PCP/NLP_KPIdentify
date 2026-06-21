# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 836 | 57.9% |
| False Negative | 355 | 24.6% |
| Boundary Error | 252 | 17.5% |
| Abbreviation | 71 | 4.9% |
| Nested Phrase | 243 | 16.8% |
| True Positive | 573 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.50%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.56%**
- Total predicted spans: 1661 · Total gold spans: 1180

## Annotated Examples

### False Positive (836 total)
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `treatment`

### False Negative (355 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `construct`

### Boundary Error (252 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (71 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `ed`
- spurious pred: `ed`
- missed gold: `sdm`

### Nested Phrase (243 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
