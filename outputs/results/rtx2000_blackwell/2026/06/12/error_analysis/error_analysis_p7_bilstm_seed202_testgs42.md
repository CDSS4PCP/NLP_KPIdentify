# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: bilstm_crf · seed: 202

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 838 | 58.9% |
| False Negative | 343 | 24.1% |
| Boundary Error | 241 | 16.9% |
| Abbreviation | 144 | 10.1% |
| Nested Phrase | 233 | 16.4% |
| True Positive | 595 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.54%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.47%**
- Total predicted spans: 1674 · Total gold spans: 1179

## Annotated Examples

### False Positive (838 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `drug ordering system`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `patient`

### False Negative (343 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (241 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `implementation`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (144 total)
- spurious pred: `asti`
- spurious pred: `used`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`

### Nested Phrase (233 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `implementation`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
