# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 46 | 1.7% |
| False Negative | 2569 | 97.7% |
| Boundary Error | 15 | 0.6% |
| Abbreviation | 40 | 1.5% |
| Nested Phrase | 15 | 0.6% |
| True Positive | 1 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **1.61%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.04%**
- Total predicted spans: 62 · Total gold spans: 2585

## Annotated Examples

### False Positive (46 total)
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `syncope`

### False Negative (2569 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (15 total)
- gold: `therapy` → pred: `intensive insulin therapy`
- gold: `therapy` → pred: `intensive insulin therapy`
- gold: `therapy` → pred: `intensive insulin therapy`
- gold: `models` → pred: `surgical models`
- gold: `stroke care process` → pred: `stroke`
- gold: `cancer` → pred: `breast cancer`

### Abbreviation (40 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (15 total)
- gold: `therapy` → pred: `intensive insulin therapy`
- gold: `therapy` → pred: `intensive insulin therapy`
- gold: `therapy` → pred: `intensive insulin therapy`
- gold: `models` → pred: `surgical models`
- gold: `stroke care process` → pred: `stroke`
- gold: `cancer` → pred: `breast cancer`
