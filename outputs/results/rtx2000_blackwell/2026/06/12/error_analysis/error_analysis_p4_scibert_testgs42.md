# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 776 | 57.7% |
| False Negative | 312 | 23.2% |
| Boundary Error | 257 | 19.1% |
| Abbreviation | 132 | 9.8% |
| Nested Phrase | 242 | 18.0% |
| True Positive | 603 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.86%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.45%**
- Total predicted spans: 1636 · Total gold spans: 1172

## Annotated Examples

### False Positive (776 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `computer`
- spurious pred: `systems`
- spurious pred: `physicians`
- spurious pred: `patient`

### False Negative (312 total)
- missed gold: `operates`
- missed gold: `background process`
- missed gold: `directs`
- missed gold: `browsing`
- missed gold: `construct`
- missed gold: `created`

### Boundary Error (257 total)
- gold: `clinical practice guidelines` → pred: `practice guidelines`
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `infer` → pred: `infer recommendations`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (132 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- spurious pred: `cdss`
- spurious pred: `cpgs`

### Nested Phrase (242 total)
- gold: `clinical practice guidelines` → pred: `practice guidelines`
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `infer` → pred: `infer recommendations`
- gold: `evaluation` → pred: `evaluation studies`
