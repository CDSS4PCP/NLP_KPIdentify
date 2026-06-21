# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 116 | 4.3% |
| False Negative | 2523 | 94.5% |
| Boundary Error | 31 | 1.2% |
| Abbreviation | 40 | 1.5% |
| Nested Phrase | 28 | 1.0% |
| True Positive | 31 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **17.42%**
- Strict entity recall (TP / (TP+FN+boundary)): **1.20%**
- Total predicted spans: 178 · Total gold spans: 2585

## Annotated Examples

### False Positive (116 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2523 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (31 total)
- gold: `<UNK>` → pred: `<UNK> knowledge`
- gold: `monitoring` → pred: `remote patient monitoring`
- gold: `point of care decision support system` → pred: `decision support`
- gold: `quality` → pred: `quality of care`
- gold: `electronic health record ehr decision support` → pred: `decision support`
- gold: `therapy` → pred: `intensive insulin therapy`

### Abbreviation (40 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (28 total)
- gold: `<UNK>` → pred: `<UNK> knowledge`
- gold: `monitoring` → pred: `remote patient monitoring`
- gold: `point of care decision support system` → pred: `decision support`
- gold: `quality` → pred: `quality of care`
- gold: `electronic health record ehr decision support` → pred: `decision support`
- gold: `therapy` → pred: `intensive insulin therapy`
