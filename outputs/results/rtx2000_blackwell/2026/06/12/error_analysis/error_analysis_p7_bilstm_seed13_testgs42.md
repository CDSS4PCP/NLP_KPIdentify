# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: bilstm_crf · seed: 13

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 815 | 58.1% |
| False Negative | 343 | 24.5% |
| Boundary Error | 244 | 17.4% |
| Abbreviation | 134 | 9.6% |
| Nested Phrase | 236 | 16.8% |
| True Positive | 592 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.86%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.21%**
- Total predicted spans: 1651 · Total gold spans: 1179

## Annotated Examples

### False Positive (815 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (343 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `operates`
- missed gold: `triggered`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (244 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (134 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`
- spurious pred: `cdss`

### Nested Phrase (236 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
