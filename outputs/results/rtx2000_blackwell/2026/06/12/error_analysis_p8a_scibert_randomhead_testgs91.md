# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 2134 | 47.3% |
| False Negative | 1309 | 29.0% |
| Boundary Error | 1067 | 23.7% |
| Abbreviation | 0 | 0.0% |
| Nested Phrase | 1183 | 26.2% |
| True Positive | 188 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **5.55%**
- Strict entity recall (TP / (TP+FN+boundary)): **7.33%**
- Total predicted spans: 3389 · Total gold spans: 2564

## Annotated Examples

### False Positive (2134 total)
- spurious pred: `hospital`
- spurious pred: `kidney`
- spurious pred: `kidney`
- spurious pred: `and`
- spurious pred: `increased health`
- spurious pred: `costs despite`
- spurious pred: `posing significant challenges for`
- spurious pred: `mostly`

### False Negative (1309 total)
- missed gold: `clinical decision support`
- missed gold: `clinicians`
- missed gold: `prediction`
- missed gold: `lacking`
- missed gold: `prediction models`
- missed gold: `obtained`
- missed gold: `developed`
- missed gold: `outcome variable`

### Boundary Error (1067 total)
- gold: `recurrent neural networks` → pred: `recurrent neural networks for`
- gold: `external validation` → pred: `validation`
- gold: `model interpretation` → pred: `interpretation`
- gold: `patient outcomes` → pred: `patient`
- gold: `measures` → pred: `effective measures for`
- gold: `prevention` → pred: `prevention are lacking previously published`
- gold: `external validation` → pred: `validation furthermore little is known about`
- gold: `model output` → pred: `linking model output and`

### Nested Phrase (1183 total)
- gold: `recurrent neural networks` → pred: `recurrent neural networks for`
- gold: `external validation` → pred: `validation`
- gold: `model interpretation` → pred: `interpretation`
- gold: `patient outcomes` → pred: `patient`
- gold: `measures` → pred: `effective measures for`
- gold: `prevention` → pred: `prevention are lacking previously published`
- gold: `model output` → pred: `linking model output and`
- gold: `clinical decisions` → pred: `decisions`
