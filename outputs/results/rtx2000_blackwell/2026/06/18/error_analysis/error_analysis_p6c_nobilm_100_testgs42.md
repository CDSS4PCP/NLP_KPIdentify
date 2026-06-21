# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 859 | 59.6% |
| False Negative | 337 | 23.4% |
| Boundary Error | 245 | 17.0% |
| Abbreviation | 76 | 5.3% |
| Nested Phrase | 235 | 16.3% |
| True Positive | 598 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.14%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.68%**
- Total predicted spans: 1702 · Total gold spans: 1180

## Annotated Examples

### False Positive (859 total)
- spurious pred: `<UNK>`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (337 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (245 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`

### Abbreviation (76 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (235 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
