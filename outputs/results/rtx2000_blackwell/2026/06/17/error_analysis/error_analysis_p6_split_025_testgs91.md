# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1081 | 48.3% |
| False Negative | 727 | 32.5% |
| Boundary Error | 431 | 19.2% |
| Abbreviation | 128 | 5.7% |
| Nested Phrase | 423 | 18.9% |
| True Positive | 1427 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **48.55%**
- Strict entity recall (TP / (TP+FN+boundary)): **55.20%**
- Total predicted spans: 2939 · Total gold spans: 2585

## Annotated Examples

### False Positive (1081 total)
- spurious pred: `aki`
- spurious pred: `model`
- spurious pred: `model`
- spurious pred: `aki`
- spurious pred: `model <UNK> interpretation`
- spurious pred: `<UNK>`

### False Negative (727 total)
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `<UNK>`
- missed gold: `challenges`

### Boundary Error (431 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model interpretations` → pred: `applicable model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `prediction model`

### Abbreviation (128 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- missed gold: `use`
- spurious pred: `plan`

### Nested Phrase (423 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `prediction model`
- gold: `increases` → pred: `<UNK> increases`
