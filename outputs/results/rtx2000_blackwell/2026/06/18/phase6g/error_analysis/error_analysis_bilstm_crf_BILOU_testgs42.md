# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BILOU · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 817 | 56.1% |
| False Negative | 376 | 25.8% |
| Boundary Error | 263 | 18.1% |
| Abbreviation | 61 | 4.2% |
| Nested Phrase | 254 | 17.4% |
| True Positive | 541 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.37%**
- Strict entity recall (TP / (TP+FN+boundary)): **45.85%**
- Total predicted spans: 1621 · Total gold spans: 1180

## Annotated Examples

### False Positive (817 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `treatment`

### False Negative (376 total)
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `construct`
- missed gold: `created`
- missed gold: `specification`
- missed gold: `elicited`

### Boundary Error (263 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `development` → pred: `under development`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `clinical decision support system <UNK>` → pred: `clinical decision support system`

### Abbreviation (61 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- gold: `sdm` → pred: `sdm standards`
- gold: `data` → pred: `data types`

### Nested Phrase (254 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `development` → pred: `under development`
- gold: `rules reasoning` → pred: `reasoning`
