# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 852 | 58.2% |
| False Negative | 346 | 23.6% |
| Boundary Error | 266 | 18.2% |
| Abbreviation | 74 | 5.1% |
| Nested Phrase | 257 | 17.6% |
| True Positive | 568 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.69%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.14%**
- Total predicted spans: 1686 · Total gold spans: 1180

## Annotated Examples

### False Positive (852 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `treatment`

### False Negative (346 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (266 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`

### Abbreviation (74 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `ed`
- spurious pred: `ed`

### Nested Phrase (257 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
