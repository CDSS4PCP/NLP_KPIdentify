# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 227 | 8.3% |
| False Negative | 2398 | 87.5% |
| Boundary Error | 117 | 4.3% |
| Abbreviation | 43 | 1.6% |
| Nested Phrase | 111 | 4.0% |
| True Positive | 70 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **16.91%**
- Strict entity recall (TP / (TP+FN+boundary)): **2.71%**
- Total predicted spans: 414 · Total gold spans: 2585

## Annotated Examples

### False Positive (227 total)
- spurious pred: `acute kidney injury`
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2398 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (117 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `area under the receiver operating characteristic curve auc` → pred: `receiver operating characteristic curve`
- gold: `clinical decision support <UNK>` → pred: `clinical decision support`
- gold: `<UNK> products` → pred: `<UNK>`
- gold: `<UNK>` → pred: `<UNK> biomedical knowledge`

### Abbreviation (43 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (111 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `area under the receiver operating characteristic curve auc` → pred: `receiver operating characteristic curve`
- gold: `clinical decision support <UNK>` → pred: `clinical decision support`
- gold: `<UNK> products` → pred: `<UNK>`
- gold: `<UNK>` → pred: `<UNK> biomedical knowledge`
