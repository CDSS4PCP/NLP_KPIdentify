# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 62 | 2.3% |
| False Negative | 2562 | 97.0% |
| Boundary Error | 16 | 0.6% |
| Abbreviation | 40 | 1.5% |
| Nested Phrase | 14 | 0.5% |
| True Positive | 7 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **8.24%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.27%**
- Total predicted spans: 85 · Total gold spans: 2585

## Annotated Examples

### False Positive (62 total)
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2562 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (16 total)
- gold: `<UNK>` → pred: `<UNK> knowledge`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `cancer management` → pred: `bladder cancer`
- gold: `cancer management` → pred: `bladder cancer`

### Abbreviation (40 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (14 total)
- gold: `<UNK>` → pred: `<UNK> knowledge`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `cancer` → pred: `breast cancer`
- gold: `cancer` → pred: `breast cancer`
