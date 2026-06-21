# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 129 | 4.8% |
| False Negative | 2497 | 93.5% |
| Boundary Error | 44 | 1.6% |
| Abbreviation | 41 | 1.5% |
| Nested Phrase | 41 | 1.5% |
| True Positive | 44 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **20.28%**
- Strict entity recall (TP / (TP+FN+boundary)): **1.70%**
- Total predicted spans: 217 · Total gold spans: 2585

## Annotated Examples

### False Positive (129 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2497 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (44 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `longitudinal disease measurements` → pred: `longitudinal disease`
- gold: `probabilistic decision support <UNK>` → pred: `probabilistic decision support`
- gold: `monitoring` → pred: `remote patient monitoring`
- gold: `adverse drug event <UNK>` → pred: `adverse drug event`
- gold: `point of care decision support system` → pred: `decision support system`

### Abbreviation (41 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (41 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `longitudinal disease measurements` → pred: `longitudinal disease`
- gold: `probabilistic decision support <UNK>` → pred: `probabilistic decision support`
- gold: `monitoring` → pred: `remote patient monitoring`
- gold: `adverse drug event <UNK>` → pred: `adverse drug event`
- gold: `point of care decision support system` → pred: `decision support system`
