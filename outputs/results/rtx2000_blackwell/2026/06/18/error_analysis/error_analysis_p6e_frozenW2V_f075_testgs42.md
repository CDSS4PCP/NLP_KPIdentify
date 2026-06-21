# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 819 | 58.4% |
| False Negative | 341 | 24.3% |
| Boundary Error | 242 | 17.3% |
| Abbreviation | 76 | 5.4% |
| Nested Phrase | 232 | 16.5% |
| True Positive | 597 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.01%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.59%**
- Total predicted spans: 1658 · Total gold spans: 1180

## Annotated Examples

### False Positive (819 total)
- spurious pred: `<UNK>`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`

### False Negative (341 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (242 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `implementation` → pred: `<UNK> implementation`

### Abbreviation (76 total)
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ae`

### Nested Phrase (232 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `implementation` → pred: `<UNK> implementation`
