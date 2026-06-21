# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 817 | 58.0% |
| False Negative | 347 | 24.6% |
| Boundary Error | 245 | 17.4% |
| Abbreviation | 75 | 5.3% |
| Nested Phrase | 235 | 16.7% |
| True Positive | 588 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.64%**
- Strict entity recall (TP / (TP+FN+boundary)): **49.83%**
- Total predicted spans: 1650 · Total gold spans: 1180

## Annotated Examples

### False Positive (817 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `drug centered <UNK>`

### False Negative (347 total)
- missed gold: `<UNK>`
- missed gold: `triggered`
- missed gold: `<UNK>`
- missed gold: `<UNK>`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (245 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`

### Abbreviation (75 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (235 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
