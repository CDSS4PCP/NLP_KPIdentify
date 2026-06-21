# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 975 | 46.7% |
| False Negative | 669 | 32.0% |
| Boundary Error | 444 | 21.3% |
| Abbreviation | 121 | 5.8% |
| Nested Phrase | 444 | 21.3% |
| True Positive | 1472 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **50.92%**
- Strict entity recall (TP / (TP+FN+boundary)): **56.94%**
- Total predicted spans: 2891 · Total gold spans: 2585

## Annotated Examples

### False Positive (975 total)
- spurious pred: `hospital acute kidney`
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (669 total)
- missed gold: `findings`
- missed gold: `settings`
- missed gold: `findings`
- missed gold: `challenges`
- missed gold: `data entry <UNK>`
- missed gold: `clinician trust`

### Boundary Error (444 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `assessment` → pred: `time assessment`
- gold: `described` → pred: `studies described`
- gold: `detection control` → pred: `detection`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`

### Abbreviation (121 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `plan`
- spurious pred: `rule`
- spurious pred: `ed`
- spurious pred: `ards`

### Nested Phrase (444 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `assessment` → pred: `time assessment`
- gold: `described` → pred: `studies described`
- gold: `detection control` → pred: `detection`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
