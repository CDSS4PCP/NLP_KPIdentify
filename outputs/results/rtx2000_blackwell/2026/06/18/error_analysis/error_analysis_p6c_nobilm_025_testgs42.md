# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 859 | 58.6% |
| False Negative | 359 | 24.5% |
| Boundary Error | 248 | 16.9% |
| Abbreviation | 81 | 5.5% |
| Nested Phrase | 239 | 16.3% |
| True Positive | 573 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.11%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.56%**
- Total predicted spans: 1680 · Total gold spans: 1180

## Annotated Examples

### False Positive (859 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (359 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `construction`
- missed gold: `construct`

### Boundary Error (248 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `automatically triggered`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `rules`
- gold: `<UNK> clinical decision support system` → pred: `service oriented <UNK>`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`

### Abbreviation (81 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (239 total)
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `automatically triggered`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `rules`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
- gold: `functions` → pred: `<UNK> functions`
