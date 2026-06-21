# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 246 | 9.0% |
| False Negative | 2352 | 85.9% |
| Boundary Error | 139 | 5.1% |
| Abbreviation | 82 | 3.0% |
| Nested Phrase | 133 | 4.9% |
| True Positive | 73 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **15.94%**
- Strict entity recall (TP / (TP+FN+boundary)): **2.85%**
- Total predicted spans: 458 · Total gold spans: 2564

## Annotated Examples

### False Positive (246 total)
- spurious pred: `acute kidney injury`
- spurious pred: `acute kidney injury`
- spurious pred: `clinical decision support`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2352 total)
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`
- missed gold: `measures`
- missed gold: `prediction`

### Boundary Error (139 total)
- gold: `recurrent neural networks` → pred: `neural`
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support`
- gold: `decision support` → pred: `support`
- gold: `integrate clinical decision support` → pred: `clinical decision support`

### Abbreviation (82 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `fhir`
- missed gold: `fhir`
- missed gold: `gaps`
- missed gold: `plan`

### Nested Phrase (133 total)
- gold: `recurrent neural networks` → pred: `neural`
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support`
- gold: `decision support` → pred: `support`
- gold: `integrate clinical decision support` → pred: `clinical decision support`
