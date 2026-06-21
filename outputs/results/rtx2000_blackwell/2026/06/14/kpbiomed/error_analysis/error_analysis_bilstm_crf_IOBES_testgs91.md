# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 117 | 4.4% |
| False Negative | 2526 | 94.5% |
| Boundary Error | 29 | 1.1% |
| Abbreviation | 40 | 1.5% |
| Nested Phrase | 27 | 1.0% |
| True Positive | 30 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **17.05%**
- Strict entity recall (TP / (TP+FN+boundary)): **1.16%**
- Total predicted spans: 176 · Total gold spans: 2585

## Annotated Examples

### False Positive (117 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2526 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (29 total)
- gold: `<UNK>` → pred: `<UNK> knowledge`
- gold: `monitoring` → pred: `remote patient monitoring`
- gold: `point of care decision support system` → pred: `decision support`
- gold: `quality` → pred: `quality of care`
- gold: `electronic health record ehr decision support` → pred: `decision support`
- gold: `decision support improved` → pred: `decision support`

### Abbreviation (40 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (27 total)
- gold: `<UNK>` → pred: `<UNK> knowledge`
- gold: `monitoring` → pred: `remote patient monitoring`
- gold: `point of care decision support system` → pred: `decision support`
- gold: `quality` → pred: `quality of care`
- gold: `electronic health record ehr decision support` → pred: `decision support`
- gold: `decision support improved` → pred: `decision support`
