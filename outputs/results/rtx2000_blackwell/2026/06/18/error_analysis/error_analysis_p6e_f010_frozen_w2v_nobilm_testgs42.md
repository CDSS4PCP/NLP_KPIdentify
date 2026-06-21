# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 836 | 57.1% |
| False Negative | 343 | 23.4% |
| Boundary Error | 284 | 19.4% |
| Abbreviation | 72 | 4.9% |
| Nested Phrase | 276 | 18.9% |
| True Positive | 553 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.05%**
- Strict entity recall (TP / (TP+FN+boundary)): **46.86%**
- Total predicted spans: 1673 · Total gold spans: 1180

## Annotated Examples

### False Positive (836 total)
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (343 total)
- missed gold: `<UNK>`
- missed gold: `triggered`
- missed gold: `development`
- missed gold: `construction`
- missed gold: `construct`
- missed gold: `created`

### Boundary Error (284 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules` → pred: `elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (72 total)
- spurious pred: `use`
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (276 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules` → pred: `elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
