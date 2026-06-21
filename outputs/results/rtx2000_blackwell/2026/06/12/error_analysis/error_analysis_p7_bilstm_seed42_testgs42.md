# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 807 | 58.4% |
| False Negative | 329 | 23.8% |
| Boundary Error | 246 | 17.8% |
| Abbreviation | 131 | 9.5% |
| Nested Phrase | 237 | 17.1% |
| True Positive | 604 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.45%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.23%**
- Total predicted spans: 1657 · Total gold spans: 1179

## Annotated Examples

### False Positive (807 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `treatment`

### False Negative (329 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `operates`
- missed gold: `triggered`
- missed gold: `rules`
- missed gold: `directs`

### Boundary Error (246 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (131 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`
- spurious pred: `cdss`

### Nested Phrase (237 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
