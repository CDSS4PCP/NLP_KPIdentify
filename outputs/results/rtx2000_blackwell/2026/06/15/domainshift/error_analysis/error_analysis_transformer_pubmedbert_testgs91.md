# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 417 | 14.8% |
| False Negative | 2173 | 77.3% |
| Boundary Error | 222 | 7.9% |
| Abbreviation | 108 | 3.8% |
| Nested Phrase | 216 | 7.7% |
| True Positive | 169 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **20.92%**
- Strict entity recall (TP / (TP+FN+boundary)): **6.59%**
- Total predicted spans: 808 · Total gold spans: 2564

## Annotated Examples

### False Positive (417 total)
- spurious pred: `acute kidney injury`
- spurious pred: `acute kidney injury`
- spurious pred: `network`
- spurious pred: `clinical decision support`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2173 total)
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`
- missed gold: `measures`
- missed gold: `prediction`

### Boundary Error (222 total)
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `external validation` → pred: `validation`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `computable` → pred: `computable knowledge`
- gold: `prescribing` → pred: `opioid prescribing`

### Abbreviation (108 total)
- missed gold: `use`
- missed gold: `gaps`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (216 total)
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `external validation` → pred: `validation`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `computable` → pred: `computable knowledge`
- gold: `prescribing` → pred: `opioid prescribing`
