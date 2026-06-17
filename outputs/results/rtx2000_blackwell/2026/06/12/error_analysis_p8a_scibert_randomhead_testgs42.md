# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1175 | 52.7% |
| False Negative | 574 | 25.8% |
| Boundary Error | 479 | 21.5% |
| Abbreviation | 0 | 0.0% |
| Nested Phrase | 469 | 21.1% |
| True Positive | 119 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **6.71%**
- Strict entity recall (TP / (TP+FN+boundary)): **10.15%**
- Total predicted spans: 1773 · Total gold spans: 1172

## Annotated Examples

### False Positive (1175 total)
- spurious pred: `a`
- spurious pred: `drug ordering`
- spurious pred: `for`
- spurious pred: `existing`
- spurious pred: `based ordering`
- spurious pred: `for`
- spurious pred: `drug centered checks but offer little`
- spurious pred: `overall`

### False Negative (574 total)
- missed gold: `developed`
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `rules`
- missed gold: `directs`
- missed gold: `construct`
- missed gold: `created`
- missed gold: `development`

### Boundary Error (479 total)
- gold: `optimizing` → pred: `for optimizing`
- gold: `clinical practice guidelines` → pred: `centered treatment strategy evidence based clinical practice guidelines have been developed`
- gold: `prescription errors` → pred: `avoid prescription errors and`
- gold: `background process` → pred: `compliance with best therapeutic practices the critic mode operates as a background process and corrects the`
- gold: `triggered` → pred: `basis of automatically triggered elementary rules that`
- gold: `browsing` → pred: `by browsing`
- gold: `decision tree` → pred: `decision`
- gold: `rules reasoning` → pred: `reasoning objective`

### Nested Phrase (469 total)
- gold: `optimizing` → pred: `for optimizing`
- gold: `clinical practice guidelines` → pred: `centered treatment strategy evidence based clinical practice guidelines have been developed`
- gold: `prescription errors` → pred: `avoid prescription errors and`
- gold: `background process` → pred: `compliance with best therapeutic practices the critic mode operates as a background process and corrects the`
- gold: `triggered` → pred: `basis of automatically triggered elementary rules that`
- gold: `browsing` → pred: `by browsing`
- gold: `decision tree` → pred: `decision`
- missed gold: `developed`
