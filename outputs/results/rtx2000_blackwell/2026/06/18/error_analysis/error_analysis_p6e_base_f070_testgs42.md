# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 824 | 58.3% |
| False Negative | 347 | 24.5% |
| Boundary Error | 243 | 17.2% |
| Abbreviation | 74 | 5.2% |
| Nested Phrase | 232 | 16.4% |
| True Positive | 590 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.61%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.00%**
- Total predicted spans: 1657 · Total gold spans: 1180

## Annotated Examples

### False Positive (824 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `drug centered <UNK>`
- spurious pred: `assistance`

### False Negative (347 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (243 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `<UNK> clinical decision support system` → pred: `clinical decision support system`

### Abbreviation (74 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (232 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `<UNK> clinical decision support system` → pred: `clinical decision support system`
