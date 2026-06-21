# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 864 | 59.6% |
| False Negative | 307 | 21.2% |
| Boundary Error | 278 | 19.2% |
| Abbreviation | 70 | 4.8% |
| Nested Phrase | 275 | 19.0% |
| True Positive | 595 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.25%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.42%**
- Total predicted spans: 1737 · Total gold spans: 1180

## Annotated Examples

### False Positive (864 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `patient`

### False Negative (307 total)
- missed gold: `triggered`
- missed gold: `<UNK>`
- missed gold: `construction`
- missed gold: `construct`
- missed gold: `created`
- missed gold: `specification`

### Boundary Error (278 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `prescription errors` → pred: `avoid prescription errors`
- gold: `background process` → pred: `process`
- gold: `rules` → pred: `elementary rules`
- gold: `development` → pred: `under development`
- gold: `rules reasoning` → pred: `rules`

### Abbreviation (70 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (275 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `prescription errors` → pred: `avoid prescription errors`
- gold: `background process` → pred: `process`
- gold: `rules` → pred: `elementary rules`
- gold: `development` → pred: `under development`
- gold: `rules reasoning` → pred: `rules`
