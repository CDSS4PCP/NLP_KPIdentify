# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 376 | 13.2% |
| False Negative | 2274 | 80.1% |
| Boundary Error | 189 | 6.7% |
| Abbreviation | 109 | 3.8% |
| Nested Phrase | 179 | 6.3% |
| True Positive | 101 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **15.17%**
- Strict entity recall (TP / (TP+FN+boundary)): **3.94%**
- Total predicted spans: 666 · Total gold spans: 2564

## Annotated Examples

### False Positive (376 total)
- spurious pred: `acute kidney injury`
- spurious pred: `acute kidney injury`
- spurious pred: `clinical decision support`
- spurious pred: `pediatric hypertension`
- spurious pred: `hypertension`
- spurious pred: `children`

### False Negative (2274 total)
- missed gold: `clinical decision support`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`
- missed gold: `measures`

### Boundary Error (189 total)
- gold: `recurrent neural networks` → pred: `recurrent neural`
- gold: `prediction models` → pred: `prediction`
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `computable products` → pred: `computable`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems`

### Abbreviation (109 total)
- missed gold: `use`
- missed gold: `gaps`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nhs`
- spurious pred: `nice`

### Nested Phrase (179 total)
- gold: `recurrent neural networks` → pred: `recurrent neural`
- gold: `prediction models` → pred: `prediction`
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `computable products` → pred: `computable`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems`
