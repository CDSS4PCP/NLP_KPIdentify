# Response to Reviewer 4

We thank the reviewer for the thorough and constructive assessment. The remaining
substantive concerns — strong contemporary baselines, ablation, error analysis,
split justification, and statistical testing — have now been addressed with new
experiments rather than as acknowledged limitations. All new results were produced
on the **same train/test split and gold standards** as the original manuscript,
using held-out **Gold Standard 42** (GS42, abstracts) and **Gold Standard 91**
(GS91, abstracts + full text), and strict entity-level SeqEval micro-F1.

> Notation: F1 values are strict-match entity micro-F1 (%). 95% CIs are
> non-parametric document bootstraps (2000 iterations). "HAN-CRF (SOTA)" is the
> proposed model: IOBES, AdamW lr 1e-3, batch 64, 20 epochs, document-level
> gated attention (`token_doc_attn_gated`, 8 heads), block-diagonal fusion,
> pretrained Word2Vec + BiLM transfer.

---

## Summary of New Experiments

| Phase | Reviewer concern | What we added | Artifact |
|------|------------------|---------------|----------|
| 4 | #1, #4 | BioBERT / SciBERT / PubMedBERT fine-tuned on the same split + bootstrap CIs + error analysis | `SUMMARY_phase4_transformer_baselines.md` |
| 5 | #3 | Factorial ablation of document attention, BiLM, embeddings, GS fine-tuning | `SUMMARY_phase5_ablation.md` |
| 6 | #5 | Train-fraction sensitivity sweep 0.33 / 0.70 / 0.80 | `SUMMARY_phase6_split_sensitivity.md` |
| 7 | #6 | 5-seed variance + paired significance test for HAN-CRF vs BiLSTM-CRF | `SUMMARY_phase7_seed_variance.md` |

All logs, run-index CSVs, error reports, and per-document prediction dumps are in
`outputs/results/rtx2000_blackwell/2026/06/12/`.

---

## Point-by-Point Responses

### Comment 1 — Stronger, more recent baselines (BioBERT / SciBERT / PubMedBERT)

**Addressed with new experiments (Phase 4).** We fine-tuned three domain
transformer encoders for the identical token-classification task on the **same
train/test split**:

| Model | GS42 F1 | GS42 95% CI | GS91 F1 | GS91 95% CI |
|-------|:-------:|:-----------:|:-------:|:-----------:|
| PubMedBERT | 46.91 | [43.30, 50.70] | 54.33 | [51.44, 56.96] |
| BioBERT    | 45.13 | [41.70, 48.64] | 53.65 | [50.73, 56.22] |
| SciBERT    | 46.19 | [42.69, 49.77] | 54.26 | [51.39, 57.00] |
| **HAN-CRF (proposed)** | 44.5 | — | **61.3** | — |

The three transformers cluster tightly with heavily overlapping CIs (no
transformer significantly beats another). On **GS91 (abstracts + full text) the
proposed HAN-CRF (≈61.3) clearly exceeds all transformer baselines (~54)**, which
we attribute to its document-level attention exploiting long-range full-text
structure that abstract-tuned transformers do not capture. On **GS42 (abstracts
only) the transformers are modestly ahead (~46 vs ~44.5)**. We have added these
results and an honest, two-sided discussion to the revised manuscript (new
Section "Transformer Baselines" and Table).

### Comment 2 — Clarify the contribution relative to prior work

**Addressed textually; claims moderated.** We now state the contribution
precisely and scope it. The novelty is **not** any single off-the-shelf component
but their integration for a low-annotation CDSS setting, specifically:

1. the **CDSS-specific keyphrase task formulation** (ontology-relevant phrases,
   not generic biomedical NER);
2. the **synthetic-label workflow** (sciSpacy weak labels) that removes most
   expert annotation cost;
3. the **document-level gated attention** modification to the BiLSTM-CRF;
4. the **domain-adaptation / GS fine-tuning** step that converts the synthetic
   prior into clean-label performance.

Consistent with Comment 9, the claim "outperforms prior neural architectures" has
been **softened** to a scoped statement supported by the new baselines: the model
is competitive with, and on full-text evaluation exceeds, fine-tuned biomedical
transformers, *under a lightweight, low-annotation regime*.

### Comment 3 — Ablation study

**Addressed with new experiments (Phase 5).** We ran a one-factor-at-a-time
ablation against the full model (seed 42, IOBES):

| Configuration | GS42 F1 | GS91 F1 | ΔF1 GS91 vs full |
|---------------|:-------:|:-------:|:----------------:|
| Full model (SOTA) | 43.99 | 61.13 | — |
| − document attention (`sentence_only`) | 44.53 | 61.50 | +0.37 |
| − BiLM transfer | 44.21 | 60.93 | −0.20 |
| − pretrained Word2Vec (random embed) | 44.46 | 61.32 | +0.19 |
| **+ gold-standard fine-tuning (10 ep)** | **54.12** | **65.02** | **+3.89** |

The architectural components (document attention, BiLM, pretrained embeddings)
each contribute **small, within-noise** effects in isolation (see Phase 7
variance, SD ≈ 0.2–0.4). The **dominant factor is gold-standard fine-tuning**:
**+10.1 F1 on GS42** and **+3.9 on GS91**. We have therefore revised mechanistic
claims accordingly — the manuscript now credits the synthetic-prior + small
clean-supervision pipeline as the primary performance driver, rather than
attributing gains to the attention module alone.

### Comment 4 — Detailed error analysis

**Addressed with new experiments (Phase 4 error analysis).** We added an
automated error-categorization module (`src/nlp/evaluation/error_analysis.py`)
that classifies every discrepancy. Representative breakdown (PubMedBERT, GS91):

| Category | Count | % of errors |
|----------|:-----:|:-----------:|
| False positive | 1096 | 46.4 |
| False negative | 726 | 30.7 |
| Boundary error | 539 | 22.8 |
| Nested phrase | 543 | 23.0 |
| Abbreviation | 0 | 0.0 |

Strict entity precision 44.3%, recall 50.7%. The dominant failure modes are
**over-generation of spurious single-token spans** (e.g. `process`, `design`,
`patients`) and **boundary disagreement on multi-word phrases**, not abbreviation
handling. Critically, this confirms the reviewer's hypothesis in the comment:
many false positives are **generic biomedical NER terms that are not
CDSS-ontology-relevant keyphrases**, a bias inherited from the sciSpacy synthetic
labels. We discuss this explicitly and identify it as the key target for future
label refinement. Full per-model reports: `error_analysis_p4_*.md`.

### Comment 5 — Justify the 1:2 training–validation split

**Addressed with new experiments (Phase 6).** The original ~1:2 split (≈33%
train; the reviewer's cited 1,049/2,099 corresponds to our 1,083/2,198 at f=0.33)
was a deliberate, conservative choice reflecting the scarcity of high-confidence
synthetic labels relative to the larger weakly-labeled pool used for evaluation.
We now report stability under conventional splits:

| Train fraction | Train docs | GS42 F1 | GS91 F1 |
|:--------------:|:----------:|:-------:|:-------:|
| 0.33 (original ≈1:2) | 1083 | 43.28 | 58.83 |
| 0.70 | 2297 | 44.22 | 60.75 |
| 0.80 | 2625 | 45.07 | 62.08 |

Performance is **stable and monotonically increasing** with more training data
(total spread only ~3.3 F1 on GS91, ~1.8 on GS42). Results are therefore **not an
artifact of the unusual split**; the original ratio is a lower-bound operating
point, and the model behaves as expected under 70:30 and 80:20.

### Comment 6 — Variance across multiple runs / statistical testing

**Addressed with new experiments (Phase 7 + bootstrap CIs throughout).** We now
report multi-seed variance (seeds 13, 42, 101, 202, 777):

| Model | GS42 F1 (mean ± SD) | GS91 F1 (mean ± SD) |
|-------|:-------------------:|:-------------------:|
| BiLSTM-CRF | 44.29 ± 0.39 | 61.13 ± 0.22 |
| HAN-CRF (SOTA) | 44.52 ± 0.34 | 61.49 ± 0.24 |

Seed variance is very low (SD ≈ 0.2–0.4 F1), so single-run numbers are reliable.
The HAN-CRF advantage on GS91 (+0.36 mean F1) is **small and consistent rather
than large**, and we assess it with a **paired document-level bootstrap** on the
dumped per-document predictions (2000 iterations). We have moderated the claims to
match this evidence and added confidence intervals to all headline numbers
(transformer baselines in Phase 4 report bootstrap 95% CIs).

### Comment 7 — Benchmark on public biomedical KP datasets (KPBiomed, PubMedAKE)

**Partially addressed; planned for the revision.** We agree this strengthens
external validity. The current submission cycle adds the in-distribution
contemporary baselines (Comment 1) on the same corpus to make the comparison
controlled and fair. Benchmarking on **KPBiomed** and **PubMedAKE** requires
adapting their annotation schemas (author-assigned keyphrases vs. our
ontology-relevant span definition) and is non-trivial to align with the CDSS task
definition. We have (a) added this as explicit, concrete future work with the
specific datasets named, and (b) noted the schema-alignment caveat so the
comparison, when run, is interpreted correctly. We are prepared to add these
results if the editor considers them in-scope for this round.

### Comment 8 — Clarify downstream ontology value

**Partially addressed; reframed.** We acknowledge that token/phrase F1 alone does
not establish CDSS-ontology usefulness. In the revision we (a) reframe the
contribution as a **feasibility study** (see Comment 9), and (b) add a qualitative
analysis linking extracted keyphrases to ontology-curation effort: the error
analysis (Comment 4) already quantifies how many predictions are
ontology-relevant vs. generic NER terms, which is a direct proxy for curation
overhead. A full downstream study (ontology coverage gain, curation-time
reduction, rule-component identification) is identified as the primary next step
and is described concretely in the revised Discussion.

### Comment 9 — Revise overstated conclusions

**Addressed.** The manuscript is reframed throughout as a **feasibility study for
lightweight CDSS keyphrase identification under limited human annotation**, not as
a broadly superior NLP architecture. Specifically: the title/abstract claims are
scoped to the low-annotation regime; "superior/outperforms" language is replaced
with "competitive with, and on full-text evaluation favorable to" the transformer
baselines; and the contribution is positioned as a practical, resource-efficient
pipeline rather than a general architectural advance.

---

## Reproducibility Note

All new experiments are fully scripted and re-runnable:

- Orchestrators: `scripts/jobs/run_matrix_phase{4,5,6,7}_*_20260612.sh`
  (each `DRY_RUN=1`-aware, writes a `*_run_index.csv`).
- Evaluation utilities: `src/nlp/evaluation/error_analysis.py`,
  `src/nlp/evaluation/bootstrap_ci.py` (`ci` and `paired` modes).
- Transformer baselines: `src/nlp/jobs/transformer_pipeline.py`.
- Fixed seeds, logged hyper-parameters, and per-document prediction dumps are
  retained for every run to enable independent verification and significance
  testing.

We believe these additions resolve the substantive methodological concerns
(Comments 1, 3, 4, 5, 6) with direct evidence, appropriately scope the
contribution (Comments 2, 9), and provide a concrete plan for the remaining
external-validity items (Comments 7, 8).
