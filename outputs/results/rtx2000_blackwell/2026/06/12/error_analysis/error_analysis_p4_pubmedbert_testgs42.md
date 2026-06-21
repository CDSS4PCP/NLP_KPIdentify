# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 757 | 56.8% |
| False Negative | 331 | 24.8% |
| Boundary Error | 244 | 18.3% |
| Abbreviation | 121 | 9.1% |
| Nested Phrase | 238 | 17.9% |
| True Positive | 597 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **37.36%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.94%**
- Total predicted spans: 1598 · Total gold spans: 1172

## Annotated Examples

### False Positive (757 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `computer based`
- spurious pred: `physicians`
- spurious pred: `treatment strategy evidence`
- spurious pred: `treatment strategy`

### False Negative (331 total)
- missed gold: `operates`
- missed gold: `background process`
- missed gold: `triggered`
- missed gold: `directs`
- missed gold: `browsing`
- missed gold: `development`

### Boundary Error (244 total)
- gold: `clinical practice guidelines` → pred: `practice guidelines`
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules` → pred: `elementary rules`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`
- gold: `implementation` → pred: `cdsss implementation`

### Abbreviation (121 total)
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `cdss`
- spurious pred: `cpgs`
- spurious pred: `cdss`
- spurious pred: `cdss`

### Nested Phrase (238 total)
- gold: `clinical practice guidelines` → pred: `practice guidelines`
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules` → pred: `elementary rules`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`
- gold: `implementation` → pred: `cdsss implementation`
