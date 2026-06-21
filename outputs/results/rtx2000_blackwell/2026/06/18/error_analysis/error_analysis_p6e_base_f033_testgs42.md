# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 816 | 57.7% |
| False Negative | 345 | 24.4% |
| Boundary Error | 252 | 17.8% |
| Abbreviation | 78 | 5.5% |
| Nested Phrase | 250 | 17.7% |
| True Positive | 583 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.31%**
- Strict entity recall (TP / (TP+FN+boundary)): **49.41%**
- Total predicted spans: 1651 · Total gold spans: 1180

## Annotated Examples

### False Positive (816 total)
- spurious pred: `<UNK>`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `treatment`
- spurious pred: `art information`

### False Negative (345 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `<UNK>`

### Boundary Error (252 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `automatically triggered elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `rules`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (78 total)
- spurious pred: `used`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (250 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `automatically triggered elementary rules`
- missed gold: `rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `rules`
- gold: `generate` → pred: `generate recommendations`
