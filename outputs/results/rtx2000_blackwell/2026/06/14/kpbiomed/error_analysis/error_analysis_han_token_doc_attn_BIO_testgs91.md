# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 69 | 2.6% |
| False Negative | 2559 | 96.6% |
| Boundary Error | 20 | 0.8% |
| Abbreviation | 40 | 1.5% |
| Nested Phrase | 19 | 0.7% |
| True Positive | 6 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **6.32%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.23%**
- Total predicted spans: 95 · Total gold spans: 2585

## Annotated Examples

### False Positive (69 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2559 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (20 total)
- gold: `quality` → pred: `quality of care`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy goals` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `cancer management` → pred: `bladder cancer management`

### Abbreviation (40 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (19 total)
- gold: `quality` → pred: `quality of care`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `cancer management` → pred: `bladder cancer management`
- gold: `stroke care process` → pred: `stroke`
