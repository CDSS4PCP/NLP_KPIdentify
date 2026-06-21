# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 853 | 59.9% |
| False Negative | 316 | 22.2% |
| Boundary Error | 254 | 17.8% |
| Abbreviation | 77 | 5.4% |
| Nested Phrase | 252 | 17.7% |
| True Positive | 610 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.53%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.69%**
- Total predicted spans: 1717 · Total gold spans: 1180

## Annotated Examples

### False Positive (853 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `treatment`

### False Negative (316 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construction`
- missed gold: `construct`

### Boundary Error (254 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `<UNK> clinical decision support system` → pred: `<UNK>`

### Abbreviation (77 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (252 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
