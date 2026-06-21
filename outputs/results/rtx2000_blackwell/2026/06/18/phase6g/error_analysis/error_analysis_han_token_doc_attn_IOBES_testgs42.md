# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 876 | 59.0% |
| False Negative | 340 | 22.9% |
| Boundary Error | 270 | 18.2% |
| Abbreviation | 67 | 4.5% |
| Nested Phrase | 263 | 17.7% |
| True Positive | 570 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.22%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.31%**
- Total predicted spans: 1716 · Total gold spans: 1180

## Annotated Examples

### False Positive (876 total)
- spurious pred: `<UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `treatment`
- spurious pred: `evidence`

### False Negative (340 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `construct`

### Boundary Error (270 total)
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (67 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (263 total)
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
