# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 859 | 58.6% |
| False Negative | 337 | 23.0% |
| Boundary Error | 271 | 18.5% |
| Abbreviation | 69 | 4.7% |
| Nested Phrase | 261 | 17.8% |
| True Positive | 572 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.61%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.47%**
- Total predicted spans: 1702 · Total gold spans: 1180

## Annotated Examples

### False Positive (859 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `assistance`

### False Negative (337 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `development`

### Boundary Error (271 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (69 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (261 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
