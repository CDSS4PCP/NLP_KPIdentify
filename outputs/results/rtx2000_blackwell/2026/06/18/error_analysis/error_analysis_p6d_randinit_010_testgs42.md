# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 883 | 59.0% |
| False Negative | 360 | 24.0% |
| Boundary Error | 254 | 17.0% |
| Abbreviation | 86 | 5.7% |
| Nested Phrase | 250 | 16.7% |
| True Positive | 566 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.24%**
- Strict entity recall (TP / (TP+FN+boundary)): **47.97%**
- Total predicted spans: 1703 · Total gold spans: 1180

## Annotated Examples

### False Positive (883 total)
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `centered <UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (360 total)
- missed gold: `<UNK>`
- missed gold: `triggered`
- missed gold: `<UNK>`
- missed gold: `development`
- missed gold: `construction`
- missed gold: `construct`

### Boundary Error (254 total)
- gold: `clinical practice guidelines` → pred: `evidence based clinical practice guidelines`
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`

### Abbreviation (86 total)
- spurious pred: `art`
- spurious pred: `use`
- spurious pred: `cpgs`
- missed gold: `used`
- gold: `data sharing` → pred: `data`
- missed gold: `used`

### Nested Phrase (250 total)
- gold: `clinical practice guidelines` → pred: `evidence based clinical practice guidelines`
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`
