# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 148 | 5.4% |
| False Negative | 2545 | 93.4% |
| Boundary Error | 31 | 1.1% |
| Abbreviation | 37 | 1.4% |
| Nested Phrase | 26 | 1.0% |
| True Positive | 9 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **4.79%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.35%**
- Total predicted spans: 188 · Total gold spans: 2585

## Annotated Examples

### False Positive (148 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `blood pressure`
- spurious pred: `hypertension`

### False Negative (2545 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (31 total)
- gold: `longitudinal disease measurements` → pred: `longitudinal disease`
- gold: `patients attitude` → pred: `attitude`
- gold: `knowledge management` → pred: `knowledge`
- gold: `knowledge management` → pred: `knowledge`
- gold: `integrated knowledge engine` → pred: `knowledge engine`
- gold: `quality` → pred: `quality of care`

### Abbreviation (37 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (26 total)
- gold: `longitudinal disease measurements` → pred: `longitudinal disease`
- gold: `patients attitude` → pred: `attitude`
- gold: `knowledge management` → pred: `knowledge`
- gold: `knowledge management` → pred: `knowledge`
- gold: `integrated knowledge engine` → pred: `knowledge engine`
- gold: `quality` → pred: `quality of care`
