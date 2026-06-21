# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 897 | 60.2% |
| False Negative | 314 | 21.1% |
| Boundary Error | 280 | 18.8% |
| Abbreviation | 77 | 5.2% |
| Nested Phrase | 275 | 18.4% |
| True Positive | 586 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.24%**
- Strict entity recall (TP / (TP+FN+boundary)): **49.66%**
- Total predicted spans: 1763 · Total gold spans: 1180

## Annotated Examples

### False Positive (897 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `assistance`

### False Negative (314 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `development`

### Boundary Error (280 total)
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (77 total)
- spurious pred: `cpgs`
- missed gold: `used`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (275 total)
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
