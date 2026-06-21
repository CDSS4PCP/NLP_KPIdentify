# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 806 | 55.2% |
| False Negative | 387 | 26.5% |
| Boundary Error | 267 | 18.3% |
| Abbreviation | 69 | 4.7% |
| Nested Phrase | 258 | 17.7% |
| True Positive | 526 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **32.90%**
- Strict entity recall (TP / (TP+FN+boundary)): **44.58%**
- Total predicted spans: 1599 · Total gold spans: 1180

## Annotated Examples

### False Positive (806 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `little assistance`

### False Negative (387 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `construct`
- missed gold: `created`

### Boundary Error (267 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (69 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- gold: `sdm` → pred: `sdm standards`
- gold: `data` → pred: `data types`

### Nested Phrase (258 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
