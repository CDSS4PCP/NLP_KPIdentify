# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 861 | 59.9% |
| False Negative | 321 | 22.3% |
| Boundary Error | 255 | 17.7% |
| Abbreviation | 82 | 5.7% |
| Nested Phrase | 248 | 17.3% |
| True Positive | 604 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.12%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.19%**
- Total predicted spans: 1720 · Total gold spans: 1180

## Annotated Examples

### False Positive (861 total)
- spurious pred: `<UNK>`
- spurious pred: `drug <UNK> system`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `evidence`

### False Negative (321 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construction`

### Boundary Error (255 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (82 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (248 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
