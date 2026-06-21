# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1116 | 48.6% |
| False Negative | 692 | 30.1% |
| Boundary Error | 489 | 21.3% |
| Abbreviation | 117 | 5.1% |
| Nested Phrase | 483 | 21.0% |
| True Positive | 1404 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **46.66%**
- Strict entity recall (TP / (TP+FN+boundary)): **54.31%**
- Total predicted spans: 3009 · Total gold spans: 2585

## Annotated Examples

### False Positive (1116 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`
- spurious pred: `<UNK> algorithms`
- spurious pred: `decision support`

### False Negative (692 total)
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `findings`
- missed gold: `increases`

### Boundary Error (489 total)
- gold: `continuous prediction model` → pred: `prediction`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `challenges` → pred: `<UNK> connectivity challenges`
- gold: `clinician trust` → pred: `clinician`
- gold: `<UNK>` → pred: `<UNK> knowledge`

### Abbreviation (117 total)
- spurious pred: `auc`
- missed gold: `use`
- spurious pred: `nice`
- spurious pred: `plan`
- spurious pred: `use`
- spurious pred: `ed`

### Nested Phrase (483 total)
- gold: `continuous prediction model` → pred: `prediction`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `challenges` → pred: `<UNK> connectivity challenges`
- gold: `clinician trust` → pred: `clinician`
- gold: `<UNK>` → pred: `<UNK> knowledge`
