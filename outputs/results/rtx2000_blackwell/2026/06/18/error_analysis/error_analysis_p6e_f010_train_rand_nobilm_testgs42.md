# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 812 | 56.9% |
| False Negative | 377 | 26.4% |
| Boundary Error | 239 | 16.7% |
| Abbreviation | 46 | 3.2% |
| Nested Phrase | 231 | 16.2% |
| True Positive | 564 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.92%**
- Strict entity recall (TP / (TP+FN+boundary)): **47.80%**
- Total predicted spans: 1615 · Total gold spans: 1180

## Annotated Examples

### False Positive (812 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `little assistance`

### False Negative (377 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `triggered`
- missed gold: `rules`

### Boundary Error (239 total)
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
- gold: `functions` → pred: `<UNK> functions`
- gold: `implement` → pred: `implement <UNK> models representing`

### Abbreviation (46 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- gold: `data` → pred: `data types`

### Nested Phrase (231 total)
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
- gold: `functions` → pred: `<UNK> functions`
- gold: `implement` → pred: `implement <UNK> models representing`
