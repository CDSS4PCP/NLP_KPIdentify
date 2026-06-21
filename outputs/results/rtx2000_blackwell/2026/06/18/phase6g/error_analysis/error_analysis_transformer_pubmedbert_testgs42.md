# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 837 | 59.6% |
| False Negative | 304 | 21.7% |
| Boundary Error | 263 | 18.7% |
| Abbreviation | 153 | 10.9% |
| Nested Phrase | 266 | 18.9% |
| True Positive | 605 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.48%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.62%**
- Total predicted spans: 1705 · Total gold spans: 1172

## Annotated Examples

### False Positive (837 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `ordering system`
- spurious pred: `computer based ordering systems`
- spurious pred: `physicians`
- spurious pred: `drug centered checks`

### False Negative (304 total)
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `triggered`
- missed gold: `browsing`
- missed gold: `elicited`
- missed gold: `jena rules`

### Boundary Error (263 total)
- gold: `clinical practice guidelines` → pred: `practice guidelines`
- gold: `prescription errors` → pred: `avoid prescription errors`
- gold: `background process` → pred: `background`
- gold: `infer` → pred: `infer recommendations`
- gold: `satisfaction` → pred: `recommendations satisfaction`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`

### Abbreviation (153 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `cdss`
- gold: `data sharing` → pred: `data`
- spurious pred: `cdss`
- spurious pred: `soa`

### Nested Phrase (266 total)
- gold: `clinical practice guidelines` → pred: `practice guidelines`
- gold: `prescription errors` → pred: `avoid prescription errors`
- gold: `background process` → pred: `background`
- gold: `infer` → pred: `infer recommendations`
- gold: `satisfaction` → pred: `recommendations satisfaction`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`
