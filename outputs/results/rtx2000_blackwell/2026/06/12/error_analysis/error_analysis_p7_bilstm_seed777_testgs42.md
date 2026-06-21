# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: bilstm_crf · seed: 777

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 810 | 58.1% |
| False Negative | 341 | 24.4% |
| Boundary Error | 244 | 17.5% |
| Abbreviation | 131 | 9.4% |
| Nested Phrase | 235 | 16.8% |
| True Positive | 594 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.04%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.38%**
- Total predicted spans: 1648 · Total gold spans: 1179

## Annotated Examples

### False Positive (810 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (341 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `operates`
- missed gold: `rules`
- missed gold: `directs`
- missed gold: `development`

### Boundary Error (244 total)
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

### Nested Phrase (235 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
