# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 248 | 9.0% |
| False Negative | 2370 | 86.5% |
| Boundary Error | 123 | 4.5% |
| Abbreviation | 43 | 1.6% |
| Nested Phrase | 117 | 4.3% |
| True Positive | 92 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **19.87%**
- Strict entity recall (TP / (TP+FN+boundary)): **3.56%**
- Total predicted spans: 463 · Total gold spans: 2585

## Annotated Examples

### False Positive (248 total)
- spurious pred: `interpretation`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `children`
- spurious pred: `hypertension`
- spurious pred: `blood pressure`

### False Negative (2370 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (123 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `external validation` → pred: `validation`
- gold: `data management` → pred: `<UNK> medical data management`
- gold: `hospital information systems <UNK>` → pred: `hospital information systems`
- gold: `mathematical modeling` → pred: `modeling`

### Abbreviation (43 total)
- missed gold: `use`
- missed gold: `gaps`
- spurious pred: `nice`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`

### Nested Phrase (117 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `external validation` → pred: `validation`
- gold: `data management` → pred: `<UNK> medical data management`
- missed gold: `<UNK>`
- gold: `hospital information systems <UNK>` → pred: `hospital information systems`
