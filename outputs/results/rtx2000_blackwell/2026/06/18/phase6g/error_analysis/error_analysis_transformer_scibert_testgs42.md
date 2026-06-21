# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 821 | 59.4% |
| False Negative | 298 | 21.6% |
| Boundary Error | 262 | 19.0% |
| Abbreviation | 165 | 11.9% |
| Nested Phrase | 254 | 18.4% |
| True Positive | 612 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.11%**
- Strict entity recall (TP / (TP+FN+boundary)): **52.22%**
- Total predicted spans: 1695 · Total gold spans: 1172

## Annotated Examples

### False Positive (821 total)
- spurious pred: `guideline`
- spurious pred: `ordering system`
- spurious pred: `computer based ordering systems`
- spurious pred: `physicians`
- spurious pred: `centered`
- spurious pred: `patient`

### False Negative (298 total)
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `triggered`
- missed gold: `directs`
- missed gold: `browsing`
- missed gold: `development`

### Boundary Error (262 total)
- gold: `background process` → pred: `process`
- gold: `infer` → pred: `infer recommendations`
- gold: `satisfaction` → pred: `recommendations satisfaction`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`
- gold: `implementation` → pred: `cdsss implementation`
- gold: `integration` → pred: `cpgs integration`

### Abbreviation (165 total)
- spurious pred: `best`
- spurious pred: `jena`
- spurious pred: `jena`
- spurious pred: `cdss`
- spurious pred: `cpgs`
- spurious pred: `cdss`

### Nested Phrase (254 total)
- gold: `background process` → pred: `process`
- gold: `infer` → pred: `infer recommendations`
- gold: `satisfaction` → pred: `recommendations satisfaction`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`
- gold: `implementation` → pred: `cdsss implementation`
- gold: `integration` → pred: `cpgs integration`
