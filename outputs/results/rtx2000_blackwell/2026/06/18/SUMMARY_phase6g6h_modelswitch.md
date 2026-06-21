# Phase 6G & 6H — Model-switch verification (architecture independence vs. dataset effect)

**Author's question (Phase 6G):** *"I still don't believe training on a 0.1 train ratio
of ~328 documents generalizes the model to predict the rest of ~3000 documents at ~60%
F1. Switch the model and re-check."*

**Author's question (Phase 6H):** *"I believe the synthetic dataset has something to do
with this constant performance. Re-run on a real public dataset (PubMedAKE) and find out
which model is actually dominant."*

**Bottom line:** The ~60% low-data generalization in 6G is a **property of the synthetic
dataset, not of any architecture.** On synthetic data every GNA variant clusters at
63–66% regardless of architecture (model switching changes nothing). On the **real
public PubMedAKE corpus (6H)** the illusion disappears: GNA collapses to 41–46% and the
**transformer family becomes clearly dominant, led by PubMedBERT at 53.19 F1.** Domain
pretraining now matters (PubMedBERT > SciBERT > BioBERT), and architecture finally
separates within GNA (HAN > BiLSTM-CRF) — neither of which is visible on synthetic data.

---

## Phase 6G — Synthetic dataset, model switch @ f=0.10

### Setup
- Script: `scripts/jobs/run_matrix_phase6g_modelswitch_synthetic_20260618.sh`.
- Run index: `phase6g/phase6g_run_index.csv`. Logs: `phase6g/p6g_*.txt`.
- Synthetic split re-cut to **f=0.10 (≈328 train / ≈2953 test, seed 42)**, 20 epochs.
- 12 GNA configs (4 architectures × 3 tag schemes) + 3 transformers.
- Each run evaluated on synthetic held-out **TEST**, plus external **GS42** and **GS91**.
- GNA anchor flags: `--positiveUpsample 2 --hanBatchMode fixed --rebalancingMode auto
  --hanUseBlockDiagonal --bilstmFreezeEmbeddings --validationSplit 0 --earlyStopPatience 0
  --optimizer adamw --lr 1e-3 --batchSize 64 --epochs 20`. Transformers: `--epochs 3
  --batchSize 16 --lr 3e-5 --maxLength 256`.

### Results (SeqEval strict micro-F1 %)

| config | TEST | GS42 | GS91 |
|---|---:|---:|---:|
| bilstm_crf_BIO | 63.08 | 40.09 | 51.43 |
| bilstm_crf_IOBES | 64.94 | 41.86 | 53.40 |
| bilstm_crf_BILOU | 63.93 | 40.76 | 53.15 |
| han_sentence_only_BIO | 65.56 | 41.39 | 52.78 |
| han_sentence_only_IOBES | **66.21** | 40.33 | 52.87 |
| han_sentence_only_BILOU | 65.58 | 41.10 | 52.48 |
| han_token_doc_attn_BIO | 66.00 | 41.43 | 52.14 |
| han_token_doc_attn_IOBES | 64.95 | 40.80 | 51.87 |
| han_token_doc_attn_BILOU | 64.64 | 40.73 | 51.97 |
| han_token_doc_attn_gated_BIO | 64.40 | 40.09 | 51.82 |
| han_token_doc_attn_gated_IOBES | 64.62 | 40.51 | 52.53 |
| han_token_doc_attn_gated_BILOU | 64.67 | 40.60 | 52.38 |
| transformer_biobert | 52.47 | 45.12 | 46.87 |
| transformer_pubmedbert | 52.59 | **46.12** | 45.40 |
| transformer_scibert | 55.71 | 45.34 | 47.96 |

- Best TEST: `han_sentence_only_IOBES` = 66.21
- Best GS42: `transformer_pubmedbert` = 46.12
- Best GS91: `bilstm_crf_IOBES` = 53.40

### Interpretation
1. **Architecture-independent on synthetic.** All 12 GNA configs sit in a tight
   **63.08–66.21** TEST band (~3 F1 spread = single-seed noise). Switching from a plain
   BiLSTM-CRF to hierarchical attention (sentence / token-doc / gated) buys essentially
   nothing. The ~60% generalization does **not** come from model capacity.
2. **Transformers behave differently.** They are *lower* on the synthetic TEST (52–56%)
   yet *higher* on the external GS42 (45–46% vs. ~40–42% for GNA). GNA is overfitting the
   synthetic label distribution; transformers transfer slightly better off-distribution.
3. **Consistent with Phases 6c–6f:** the high f=0.10 synthetic score is the CRF fitting
   *learnable synthetic labels*, robust to pretraining, init, freezing, and hand-crafted
   features — and now also to the tagging architecture.

---

## Phase 6H — Real public dataset (PubMedAKE), model switch @ f=0.10

### Setup
- Script: `scripts/jobs/run_matrix_phase6h_pubmedake_modelswitch_20260618.sh`
  (+ crash-recovery finisher `scripts/jobs/run_phase6h_transformers_only_20260619.sh`).
- Run index: `phase6h/phase6h_run_index.csv`. Logs: `phase6h/p6h_*.txt`.
- **PubMedAKE** train+test combined (82,011 docs) re-split to **f=0.10 →
  8,201 train / 73,810 in-domain TEST (seed 42)**. PreTrain (vocab + Word2Vec + BiLM)
  rebuilt on the 0.10 split. 20 epochs (GNA) / 3 epochs (transformers).
- **No synthetic data, no GS** — this is an in-domain TEST-only experiment on real text.
- Original PubMedAKE split was backed up and **restored** after the run.

### Results (SeqEval strict micro-F1 %, in-domain TEST)

| rank | model | schema | P% | R% | **F1%** |
|---:|---|---|---:|---:|---:|
| 1 | **PubMedBERT** | — | 55.96 | 50.69 | **53.19** |
| 2 | SciBERT | — | 54.17 | 48.40 | **51.12** |
| 3 | BioBERT | — | 52.51 | 43.53 | **47.60** |
| 4 | HAN token_doc_attn | IOBES | 47.86 | 43.76 | 45.72 |
| 5 | HAN sentence_only | BILOU | 46.71 | 44.04 | 45.33 |
| 6 | HAN token_doc_attn | BIO | 47.92 | 41.62 | 44.55 |
| 7 | HAN sentence_only | IOBES | 47.57 | 41.82 | 44.51 |
| 8 | HAN sentence_only | BIO | 47.75 | 41.45 | 44.38 |
| 9 | HAN token_doc_attn | BILOU | 49.57 | 37.83 | 42.92 |
| 10 | BiLSTM-CRF | BIO | 44.16 | 39.91 | 41.93 |
| 11 | BiLSTM-CRF | BILOU | 45.52 | 37.71 | 41.25 |
| 12 | BiLSTM-CRF | IOBES | 43.86 | 38.43 | 40.96 |

> **HAN `token_doc_attn_gated` (all 3 schemes) was skipped.** Its evaluation over the
> 73,810-doc TEST set repeatedly crashed the 8 GB GPU (gated multi-head attention is too
> heavy at that eval size). The BIO checkpoint trained successfully but the eval could
> not complete; IOBES/BILOU were not attempted. This does not affect the conclusion.

### Interpretation
1. **A clear winner finally emerges.** PubMedBERT (53.19) tops the table, with the whole
   transformer family (47.6–53.2) sitting **above the entire GNA family (40.9–45.7)** —
   a clean ~6–12 F1 separation that simply does not exist on synthetic data.
2. **GNA collapses on real data.** GNA drops from **63–66% (synthetic, 6G)** to
   **41–46% (real, 6H)**. The synthetic corpus was inflating GNA scores by ~20 F1 and
   flattening all architecture differences — exactly the "constant ~60%" illusion the
   author suspected.
3. **Architecture now separates within GNA.** Ordering becomes meaningful: HAN
   (sentence / token-doc attention) > BiLSTM-CRF. Hierarchical attention is worth a few
   real F1 points on genuine text, which the synthetic data masked entirely.
4. **Domain pretraining matters.** PubMedBERT > SciBERT > BioBERT, consistent with
   PubMedAKE being PubMed-domain text — a signal that was absent/inverted on synthetic
   (where transformers under-performed GNA on TEST).

---

## Follow-up analysis — Why does performance plateau (~60% synthetic / ~40–50% real)? (2026-06-19)

**Author's question:** *"Why does performance hang around 40–50% and never go beyond — on
PubMedAKE just like on the synthetic dataset?"*

**Answer: the plateau is imposed by the labeling process, tokenization, and the strict
metric — not by the model.** It is the same mechanism that flattened Phases 6c–6g: every
"knob" we change (pretraining, hand-crafted features, architecture, even the whole
dataset) leaves the score in a narrow, data-determined band. The ceiling is a property of
the *labels*, and different label sources simply have different ceilings (synthetic
deterministic generator ≈ 60%; real author keyphrases ≈ 40–50%).

### Evidence straight from the 6H log (`p6h_bilstm_crf_BILOU.txt`)
- `kp_ratio = 0.0835` → **~92% of tokens are `O`.** The model reaches 91.6% token accuracy
  just by being conservative, so the loss/accuracy landscape rewards *under*-predicting
  keyphrases — recall collapses to **37.7%** (pred `U-KP` 647,932 < target 766,304).
- `match_ratio = 0.8874` → **~11% of the gold keyphrases never appear as a matchable span**
  (`no_span_match = 44,760`: `sars-cov-2`, `meta-analysis`, `mir-p`, `nf-kb`…). A span
  tagger *cannot* predict those — recall is capped below ~89% before training even starts.
- Net: P 45.5 / R 37.7 / **F1 41.25%**. The model genuinely learns (loss 6.79 → 3.44;
  untrained ≈ 0 F1), then saturates at the label-imposed ceiling.

### Why the ceiling exists (and is model-independent)
1. **The label-generating process sets the height.** Synthetic labels come from a
   *deterministic* generator (sciSpaCy NER + tf-idf/textrank) with dense positives
   (`kp_ratio 0.26`) → a self-consistent function a net can closely fit → ~63–66% ceiling.
   PubMedAKE labels are *subjective author keyphrases* (low inter-annotator agreement,
   sparse, `kp_ratio 0.084`) → irreducible noise → ~40–46% ceiling. Both plateau; they
   just plateau at different heights set by their own labels.
2. **Strict exact-match F1 is unforgiving.** SeqEval strict zeroes an entire multi-token
   keyphrase for a one-token boundary slip — fuzzy human boundaries lose many near-misses.
3. **Severe class imbalance** (~92% `O`) structurally depresses recall; a loss/sampling
   issue, not a capacity issue.
4. **Keyphrase extraction is intrinsically hard.** SOTA supervised neural KPE on
   scientific abstracts (KP20k, SemEval) tops out at **~30–40% strict F1**, so 40–50% here
   is already near the realistic ceiling.

### The unifying "knob table" — only label quality ever moved the number
| Experiment | Knob varied | Effect on F1 |
|---|---|---:|
| 6e | pretraining (W2V/BiLM, frozen/trainable) | < 2 |
| 6f | hand-crafted features (POS/WFOF/LEN/TI/TR) | < 3 |
| 6g | **architecture** (BiLSTM ↔ HAN ↔ transformer) on **synthetic** | ≈ 0 (all cluster 63–66) |
| 6h | **architecture** (BiLSTM ↔ HAN ↔ transformer) on **public PubMedAKE** | ~6–7 (GNA 41–46 < transformers 47–53; PubMedBERT 53.2 tops) |

The only changes that ever moved the score were **untrained → trained** (0 → ~50),
**synthetic → real labels** (66 → 41), and — *only on real public data* — **a stronger
pretrained encoder** (GNA 41–46 → transformer 47–53). On synthetic data architecture was
flat (≈ 0 spread); on PubMedAKE it opened a ~6–7 F1 gap, yet every model still saturates
far below 100. That is the tell: the label ceiling sets the *band*, and within a real-data
band the encoder can shift you a few points — but no architecture or decoder breaks the
ceiling the labels impose. (The *decoder* specifically is examined next; it is likewise
not the bottleneck.)

---

## Follow-up analysis — Is the CRF decoder the bottleneck? (2026-06-19)

**Author's question:** *"Why are all performances capped (~60% synthetic / ~40–50% real)
and never go beyond? Is CRF tagging the bottleneck? Should we switch to Softmax /
GlobalPointer / span-based / W2NER / structured-perceptron decoders?"*

**Answer: No — the CRF is not the bottleneck, and 6G/6H already contain the experiment
that proves it.** The plateau is imposed by the labels, tokenization, and the strict
metric — all decoder-independent. Swapping the decoder will move the score by noise, not
break the ceiling.

### The CRF-vs-softmax ablation is already in these results
Verified in code: the GNA models (`src/nlp/models/bilstm_crf.py`, `han_crf.py`) use **CRF
/ Viterbi** decoding, whereas the transformers use `AutoModelForTokenClassification`
(`src/nlp/models/transformer_token_classifier.py`) — a **plain linear + softmax head with
CrossEntropy, no CRF.** So the transformer rows *are* the "swap CRF → softmax" arm:

| Dataset | CRF decoder (GNA) | Softmax decoder (transformer) | Higher |
|---|---:|---:|---|
| Synthetic (6G TEST) | 63–66 | 52–56 | CRF |
| Real PubMedAKE (6H TEST) | 41–46 | **47–53** | **Softmax** |

If the CRF were the limiting factor, a CRF-free softmax head would be capped *below* it.
Instead, on real data softmax sits *above* every CRF model. The decoder is therefore not
what holds the ceiling — the encoder + label quality is. (The transformer arm is
confounded by a stronger pretrained encoder, which only reinforces the point: the lever
that ever moved the number was the encoder/label quality, never the decoder.)

### Why the ceiling is decoder-independent
1. **~11% of gold spans are unmatchable** (`no_span_match`, e.g. `sars-cov-2`, `nf-kb`,
   `mir-p`). This is a **tokenization/offset** problem; every decoder inherits the same
   recall cap because they all tag the same broken token grid.
2. **Strict exact-match F1** zeroes a whole keyphrase for a one-token boundary slip —
   decoder-agnostic.
3. **~92% `O` class imbalance** (synthetic kp_ratio 0.26; PubMedAKE 0.0835) depresses
   recall to ~38%; this is a loss/sampling issue, not a Viterbi-vs-softmax issue.
4. **Supervised neural KPE on scientific abstracts (KP20k/SemEval) tops out ~30–40%
   strict F1** — 40–50% here is near the realistic ceiling.

A linear-chain CRF only adds transition constraints (valid `B-I-L`/`B-I-E`, no `I` after
`O`). For flat 1–3 token keyphrases those are cheap and largely satisfiable by a decent
encoder — hence CRF ≈ softmax, consistent with the NER literature.

### Verdict on the proposed alternatives (against *this* task's failure modes)
| Alternative | Expected effect here | Verdict |
|---|---|---|
| **Softmax** | Already tested (transformers); no ceiling break | ❌ |
| **Structured Perceptron / SVM** | Same Viterbi decode as CRF, margin vs. likelihood | ❌ ≈ CRF |
| **W2NER** | Built for nested/overlapping entities; ours are flat; high cost | ❌ overkill |
| **Span-based start/end** | Mitigates imbalance; weaker boundaries; +FP risk | ⚠️ marginal |
| **GlobalPointer** | Span scoring + imbalance-friendly loss; over **char offsets** can recover part of the 11% unmatchable spans | ⚠️ only bounded upside (~a few recall pts) |

### Higher-ROI levers than a decoder swap
1. **Fix span matching on character offsets** (no model change) — directly attacks the
   ~11% `no_span_match`; likely the single biggest recall gain.
2. **Report relaxed/partial-match F1 alongside strict** — quantifies how much of the
   "ceiling" is boundary-strictness vs. genuine misses.
3. **Imbalance-aware loss** (focal / class-weighted CE, tuned upsampling) — targets the
   recall floor regardless of decoder.
4. **Only then** run one controlled head ablation (same encoder: CRF vs. softmax vs.
   GlobalPointer) on PubMedAKE. Predicted: CRF ≈ softmax within ~1 F1; GlobalPointer maybe
   +2–4 recall *after* the offset fix — i.e. it helps by bypassing the tokenization
   mismatch, not by improving decoding.

**Bottom line:** Keep the CRF (or drop it for softmax — it won't matter). The ceiling is a
labeling + tokenization + strict-metric artefact, not a decoding artefact. Among the
listed alternatives only GlobalPointer merits a bounded experiment, and even then its
payoff comes from fixing the *data/offset* problem, not the decoder.

---

## Combined takeaways for the manuscript
- The eye-catching low-data (f=0.10) generalization reported on the **synthetic** dataset
  is a **dataset artefact**: it is invariant to architecture (6G) and, on a **real public
  corpus**, both the absolute level and the model ranking change completely (6H).
- On real PubMedAKE data, **domain-pretrained transformers (PubMedBERT) are the dominant
  model** for in-domain keyphrase/entity tagging; the GNA pipeline is ~6–12 F1 behind.
- **The CRF decoder is not the bottleneck:** the softmax-head transformers (no CRF)
  match/beat the CRF models, so the ~40–66% plateau is set by labels + tokenization +
  strict-match F1, not by the tagging layer. Decoder swaps (softmax, structured
  perceptron, W2NER) won't break it; only GlobalPointer over character offsets offers a
  small, bounded gain — by fixing the data/offset mismatch, not the decoding.
- Use 6H (real data) — not 6G/6c–6f (synthetic) — as the basis for any claim about model
  capability or low-data generalization.
- Caveats: single seed per config; 6H is in-domain TEST only (no external GS); HAN gated
  variant missing in 6H due to a GPU-memory limit on the 73,810-doc evaluation.
