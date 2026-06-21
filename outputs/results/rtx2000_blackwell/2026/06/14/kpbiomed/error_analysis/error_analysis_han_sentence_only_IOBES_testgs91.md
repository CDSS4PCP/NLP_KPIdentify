# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 59 | 2.2% |
| False Negative | 2567 | 97.2% |
| Boundary Error | 15 | 0.6% |
| Abbreviation | 40 | 1.5% |
| Nested Phrase | 13 | 0.5% |
| True Positive | 3 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **3.90%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.12%**
- Total predicted spans: 77 · Total gold spans: 2585

## Annotated Examples

### False Positive (59 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2567 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (15 total)
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `intensive insulin therapy`
- gold: `cancer management` → pred: `bladder cancer`
- gold: `cancer management` → pred: `bladder cancer`
- gold: `stroke care process` → pred: `stroke`
- gold: `cancer` → pred: `breast cancer`

### Abbreviation (40 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (13 total)
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `intensive insulin therapy`
- gold: `stroke care process` → pred: `stroke`
- gold: `cancer` → pred: `breast cancer`
- gold: `cancer` → pred: `breast cancer`
- gold: `cancer` → pred: `breast cancer`
