# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 777 | 54.4% |
| False Negative | 378 | 26.5% |
| Boundary Error | 272 | 19.1% |
| Abbreviation | 65 | 4.6% |
| Nested Phrase | 271 | 19.0% |
| True Positive | 530 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.57%**
- Strict entity recall (TP / (TP+FN+boundary)): **44.92%**
- Total predicted spans: 1579 · Total gold spans: 1180

## Annotated Examples

### False Positive (777 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK> systems`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `treatment`
- spurious pred: `treatment`

### False Negative (378 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `construct`

### Boundary Error (272 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (65 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (271 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
