# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 770 | 53.8% |
| False Negative | 409 | 28.6% |
| Boundary Error | 251 | 17.6% |
| Abbreviation | 67 | 4.7% |
| Nested Phrase | 247 | 17.3% |
| True Positive | 520 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.74%**
- Strict entity recall (TP / (TP+FN+boundary)): **44.07%**
- Total predicted spans: 1541 · Total gold spans: 1180

## Annotated Examples

### False Positive (770 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK> systems`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `treatment`
- spurious pred: `treatment`

### False Negative (409 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `construction`

### Boundary Error (251 total)
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
- spurious pred: `ed`
- spurious pred: `ed`
- spurious pred: `ed`

### Nested Phrase (247 total)
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
