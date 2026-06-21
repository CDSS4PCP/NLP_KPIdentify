# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 58 | 2.2% |
| False Negative | 2557 | 97.0% |
| Boundary Error | 22 | 0.8% |
| Abbreviation | 40 | 1.5% |
| Nested Phrase | 20 | 0.8% |
| True Positive | 6 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **6.98%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.23%**
- Total predicted spans: 86 · Total gold spans: 2585

## Annotated Examples

### False Positive (58 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2557 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (22 total)
- gold: `quality` → pred: `quality of care`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy goals` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `data mining algorithm` → pred: `data mining`

### Abbreviation (40 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (20 total)
- gold: `quality` → pred: `quality of care`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `therapy` → pred: `insulin therapy`
- gold: `data mining algorithm` → pred: `data mining`
- gold: `stroke care process` → pred: `stroke`
