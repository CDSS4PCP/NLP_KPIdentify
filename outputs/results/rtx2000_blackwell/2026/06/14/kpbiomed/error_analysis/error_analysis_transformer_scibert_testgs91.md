# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 270 | 9.8% |
| False Negative | 2353 | 85.3% |
| Boundary Error | 137 | 5.0% |
| Abbreviation | 107 | 3.9% |
| Nested Phrase | 127 | 4.6% |
| True Positive | 74 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **15.38%**
- Strict entity recall (TP / (TP+FN+boundary)): **2.89%**
- Total predicted spans: 481 · Total gold spans: 2564

## Annotated Examples

### False Positive (270 total)
- spurious pred: `acute kidney injury`
- spurious pred: `acute kidney injury`
- spurious pred: `clinical decision support`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2353 total)
- missed gold: `clinical decision support`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`
- missed gold: `measures`

### Boundary Error (137 total)
- gold: `recurrent neural networks` → pred: `neural`
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems`
- gold: `fast healthcare interoperability resources fhir` → pred: `fhir`
- gold: `fhir interoperability standards` → pred: `fhir`

### Abbreviation (107 total)
- missed gold: `use`
- missed gold: `gaps`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (127 total)
- gold: `recurrent neural networks` → pred: `neural`
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems`
- gold: `fast healthcare interoperability resources fhir` → pred: `fhir`
- gold: `fhir interoperability standards` → pred: `fhir`
