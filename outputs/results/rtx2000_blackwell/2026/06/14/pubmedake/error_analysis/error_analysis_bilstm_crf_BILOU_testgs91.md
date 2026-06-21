# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 117 | 4.3% |
| False Negative | 2549 | 94.7% |
| Boundary Error | 26 | 1.0% |
| Abbreviation | 37 | 1.4% |
| Nested Phrase | 23 | 0.9% |
| True Positive | 10 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **6.54%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.39%**
- Total predicted spans: 153 · Total gold spans: 2585

## Annotated Examples

### False Positive (117 total)
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `blood pressure`

### False Negative (2549 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (26 total)
- gold: `accessibility usability` → pred: `usability`
- gold: `monitoring` → pred: `remote patient monitoring`
- gold: `integration` → pred: `rule engine integration`
- gold: `quality` → pred: `quality of care`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `therapy` → pred: `insulin therapy`

### Abbreviation (37 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (23 total)
- gold: `accessibility usability` → pred: `usability`
- gold: `monitoring` → pred: `remote patient monitoring`
- gold: `integration` → pred: `rule engine integration`
- gold: `quality` → pred: `quality of care`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `therapy` → pred: `insulin therapy`
