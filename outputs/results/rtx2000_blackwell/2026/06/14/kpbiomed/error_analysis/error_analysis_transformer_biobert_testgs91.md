# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 247 | 9.0% |
| False Negative | 2365 | 86.2% |
| Boundary Error | 131 | 4.8% |
| Abbreviation | 90 | 3.3% |
| Nested Phrase | 124 | 4.5% |
| True Positive | 68 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **15.25%**
- Strict entity recall (TP / (TP+FN+boundary)): **2.65%**
- Total predicted spans: 446 · Total gold spans: 2564

## Annotated Examples

### False Positive (247 total)
- spurious pred: `support`
- spurious pred: `acute kidney injury`
- spurious pred: `acute kidney injury`
- spurious pred: `support`
- spurious pred: `clinical decision support`
- spurious pred: `hypertension`

### False Negative (2365 total)
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`
- missed gold: `measures`

### Boundary Error (131 total)
- gold: `clinical decision support` → pred: `clinical`
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support` → pred: `clinical`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems`
- gold: `integrate clinical decision support` → pred: `clinical decision support`

### Abbreviation (90 total)
- missed gold: `use`
- missed gold: `gaps`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (124 total)
- gold: `clinical decision support` → pred: `clinical`
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support` → pred: `clinical`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems`
- gold: `integrate clinical decision support` → pred: `clinical decision support`
