# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 857 | 58.6% |
| False Negative | 372 | 25.4% |
| Boundary Error | 233 | 15.9% |
| Abbreviation | 65 | 4.4% |
| Nested Phrase | 231 | 15.8% |
| True Positive | 575 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.53%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.73%**
- Total predicted spans: 1665 · Total gold spans: 1180

## Annotated Examples

### False Positive (857 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `centered treatment`

### False Negative (372 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `<UNK>`

### Boundary Error (233 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `development` → pred: `modified ontology development`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> clinical decision support system` → pred: `<UNK>`
- gold: `implementation` → pred: `<UNK> implementation`

### Abbreviation (65 total)
- spurious pred: `art`
- spurious pred: `used`
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `ed`

### Nested Phrase (231 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `development` → pred: `modified ontology development`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> clinical decision support system` → pred: `<UNK>`
