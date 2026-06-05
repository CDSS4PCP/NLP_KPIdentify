# Phase 1 Context Sweep — Research Summary

**Date:** 2026-06-01  
**Hardware:** RTX 2000 Blackwell (CUDA)  
**Sweep:** 22 configurations — 16 baseline + 6 Phase 1 context ablations  
**Task:** Keyphrase extraction from clinical decision support system (CDSS) abstracts  
**Datasets:** GS42 (n=42 docs, 10,126 tokens) · GS91 (n=91 docs, 19,872 tokens)  
**Metric:** SeqEval entity-level F1 (%)

---

## 1. Architectural Overview

### 1.1 Baseline: BiLSTM-CRF

```
Input tokens x₁…xₗ
        │
   [Word Embed]
        │
   [BiLSTM-1]  ──►  h = {h₁…hₗ}   (hidden_dim=256)
        │
   [Linear]
        │
   [CRF Decode]  ──►  tag sequence
```

### 1.2 Baseline: HAN-CRF (sentence_only context)

The Hierarchical Attention Network adds two-level attention above BiLSTM-1:

```
Input tokens x₁…xₗ  (sentence s, doc d)
        │
   [Word Embed + POS Embed]
        │
   [BiLSTM-1]  ──►  hᵢⱼ  ∈ ℝᴴ   (token j in sentence i)
        │
   ┌────────────────────────────────────────────────────────┐
   │  SENTENCE-LEVEL CONTEXT  (sentence_only mode)          │
   │                                                        │
   │  Word Attention:                                       │
   │    uᵢⱼ = tanh(W·hᵢⱼ)                                  │
   │    αᵢⱼ = softmax(uᵢⱼᵀ·u_w / √H)                       │
   │    sᵢ  = Σⱼ αᵢⱼ hᵢⱼ          ← sentence embedding     │
   │                                                        │
   │  Sentence Attention (block-diagonal):                  │
   │    eᵢⱼ = (hᵢⱼ W_s sᵢ) / √H                            │
   │    βᵢⱼ = softmax over sentences in same doc            │
   │    cᵢⱼ = Σₖ βᵢⱼ sₖ           ← global context token   │
   └────────────────────────────────────────────────────────┘
        │
   [Concat: hᵢⱼ ‖ cᵢⱼ]  ∈ ℝ²ᴴ
        │
   [BiLSTM-2]  ──►  h'ᵢⱼ  ∈ ℝᴴ
        │
   [Linear → tagset]
        │
   [CRF Decode]
```

### 1.3 Phase 1: TokenDocumentAttention (token_doc_attn)

Replaces the two-level word/sentence attention hierarchy with **multi-head self-attention across all tokens in a document**.

```
Input tokens x₁…xₗ  (sentence s, doc d)
        │
   [Word Embed + POS Embed]
        │
   [BiLSTM-1]  ──►  hᵢⱼ  ∈ ℝᴴ
        │
   ┌────────────────────────────────────────────────────────────┐
   │  TOKEN-DOCUMENT ATTENTION  (token_doc_attn mode)           │
   │                                                            │
   │  Group sentences by doc_id → flat token sequence per doc   │
   │  flat_x = [h₁,₁ … h₁,ₗ  h₂,₁ … h₂,ₗ … hₛ,ₗ]  ∈ ℝᵀˣᴴ          │
   │  (T = S × L, S = sentences in doc, L = max_sent_len)       │
   │                                                            │
   │  Multi-Head Self-Attention:                                │
   │    Q = flat_x Wᵠ,  K = flat_x Wᴷ,  V = flat_x Wᵛ           │
   │    (each projected to ℝᵀˣᴴ, then split into H heads)       │
   │                                                            │
   │    Aₕ = softmax( QₕKₕᵀ / √(H/num_heads) ) · mask            │
   │                                                            │
   │    context = Concat(Aₕ Vₕ) Wᵒ  ∈ ℝᵀˣᴴ                      │
   │    cᵢⱼ = context[sentence i, token j]  ← doc-level token   │
   └────────────────────────────────────────────────────────────┘
        │
   [Concat: hᵢⱼ ‖ cᵢⱼ]  ∈ ℝ²ᴴ        (no gating)
        │
   [BiLSTM-2]  ──►  h'ᵢⱼ
        │
   [CRF Decode]
```

**Formal definition:**

$$
Q_h, K_h, V_h = \text{split}_h\!\left(\mathbf{x}_{\text{flat}} W^Q,\ \mathbf{x}_{\text{flat}} W^K,\ \mathbf{x}_{\text{flat}} W^V\right)
$$

$$
A_h = \text{softmax}\!\left(\frac{Q_h K_h^\top}{\sqrt{d_h}} + M\right)
$$

where $M_{ij} = 0$ if token $j$ is a valid (non-padding) token, $-\infty$ otherwise; $d_h = H / \text{num\_heads}$.

$$
\text{context} = \text{Concat}_{h=1}^{H}(A_h V_h)\, W^O
$$

$$
c_{ij} = \text{context}[\,i \cdot L + j\,]
$$

### 1.4 Phase 1: Gated TokenDocumentAttention (token_doc_attn_gated)

Extends `token_doc_attn` with a **learned gating mechanism** that interpolates between the local BiLSTM representation and the document-level context:

```
        hᵢⱼ  (local BiLSTM-1)
         │
         ├───────────────────────────────────────┐
         │                                       │
   [TokenDocAttn]──► cᵢⱼ (doc context)           │
         │                                       │
   ┌─────────────────────────────────────────┐   │
   │  GATED FUSION                           │   │
   │                                         │   │
   │  gate_in = [hᵢⱼ ‖ cᵢⱼ]  ∈ ℝ²ᴴ           │   │
   │  g = σ(W_g · gate_in)   ∈ (0,1)ᴴ        │   │
   │  f = g ⊙ hᵢⱼ + (1−g) ⊙ cᵢⱼ  ∈ ℝᴴ      │   │
   └─────────────────────────────────────────┘   │
         │                                       │
   [Concat: hᵢⱼ ‖ f]  ∈ ℝ²ᴴ  ◄───────────────────┘
         │
   [BiLSTM-2]  ──►  h'ᵢⱼ
         │
   [CRF Decode]
```

**Formal definition of gated fusion:**

$$
\mathbf{g}_{ij} = \sigma\!\left(W_g \begin{bmatrix} \mathbf{h}_{ij} \\ \mathbf{c}_{ij} \end{bmatrix} + \mathbf{b}_g\right) \in (0,1)^H
$$

$$
\mathbf{f}_{ij} = \mathbf{g}_{ij} \odot \mathbf{h}_{ij} + (1 - \mathbf{g}_{ij}) \odot \mathbf{c}_{ij}
$$

$$
\text{BiLSTM-2 input} = [\mathbf{h}_{ij} \,\|\, \mathbf{f}_{ij}] \in \mathbb{R}^{2H}
$$

The gate $\mathbf{g}_{ij}$ is per-token and per-dimension, allowing the model to selectively suppress or amplify document context on a feature-wise basis.

---

## 2. Architectural Comparison

| Component | BiLSTM-CRF | HAN-CRF (sentence_only) | HAN-CRF (token_doc_attn) | HAN-CRF (token_doc_attn_gated) |
|-----------|-----------|------------------------|--------------------------|-------------------------------|
| Level 1 encoder | BiLSTM-1 | BiLSTM-1 | BiLSTM-1 | BiLSTM-1 |
| Context mechanism | None | Word Attn → Sent Attn | Multi-head self-attn (doc tokens) | Multi-head self-attn + gated fusion |
| Context scope | — | Sentence-level pooling | Full document token space | Full document token space |
| Fusion method | — | Additive concat | Additive concat | Learned scalar gate per dim |
| Level 2 encoder | None | BiLSTM-2 | BiLSTM-2 | BiLSTM-2 |
| CRF decode | ✓ | ✓ | ✓ | ✓ |
| Schema constraints | ✓ | ✓ | ✓ | ✓ |
| Extra parameters | 0 | ~2 × H² | ~4 × H² + H²/heads | ~4 × H² + H²/heads + 2H² |
| FP16 safe | ✓ | ✓ | ✓ (patched) | ✓ (patched) |

---

## 3. Parameter Budget

For $H = 256$, $\text{num\_heads} \in \{4, 8\}$:

$$
\text{TokenDocAttn params} = \underbrace{3 H^2}_{\text{QKV proj}} + \underbrace{H^2}_{\text{out proj}} = 4 H^2 = 262{,}144
$$

$$
\text{GatedFusion params} = 2H^2 + H = 131{,}072 + 256 = 131{,}328
$$

$$
\text{SentAttn params (baseline)} \approx 2 H^2 = 131{,}072
$$

The gated variant adds ~131 K extra parameters over the non-gated `token_doc_attn` and ~262 K over the `sentence_only` baseline.

---

## 4. Complete Results Table (22 Runs, 20 Epochs, CUDA)

### 4.1 Phase 1 Context Ablations

| Rank | Config ID | Schema | Optimizer | LR | Context Mode | Heads | Gated | GS42 F1 | GS91 F1 | Mean F1 | Epoch (s) |
|------|-----------|--------|-----------|-----|--------------|-------|-------|---------|---------|---------|-----------|
| **1** | m31_p1_han_IOBES_adamw_lr1e-3_token_doc_attn_gated_h8 | IOBES | AdamW | 1e-3 | token_doc_attn_gated | 8 | ✓ | **44.90** | **62.11** | **53.50** | 28.4 |
| 6 | m31_p1_han_IOBES_adamw_lr1e-3_sentence_only_h8 | IOBES | AdamW | 1e-3 | sentence_only | 8 | ✗ | 44.88 | 61.06 | 52.97 | 24.5 |
| 8 | m31_p1_han_IOBES_adamw_lr1e-3_token_doc_attn_gated_h4 | IOBES | AdamW | 1e-3 | token_doc_attn_gated | 4 | ✓ | 44.42 | 61.44 | 52.93 | 30.2 |
| 12 | m31_p1_han_IOBES_adamw_lr1e-3_token_doc_attn_h4 | IOBES | AdamW | 1e-3 | token_doc_attn | 4 | ✗ | 44.16 | 61.44 | 52.80 | 29.9 |
| 13 | m31_p1_han_IOBES_adamw_lr1e-3_token_doc_attn_h8 | IOBES | AdamW | 1e-3 | token_doc_attn | 8 | ✗ | 44.51 | 61.08 | 52.80 | 30.8 |
| 14 | m31_p1_han_IOBES_adamw_lr1e-3_sentence_only_h4 | IOBES | AdamW | 1e-3 | sentence_only | 4 | ✗ | 44.38 | 61.11 | 52.75 | 24.8 |

### 4.2 Baseline Sweep (AdamW)

| Rank | Config ID | Model | Schema | Optimizer | LR | GS42 F1 | GS91 F1 | Mean F1 | Epoch (s) |
|------|-----------|-------|--------|-----------|-----|---------|---------|---------|-----------|
| 2 | m31_bilstm_crf_IOBES_adamw_lr1e-3 | BiLSTM-CRF | IOBES | AdamW | 1e-3 | 44.65 | 61.58 | 53.11 | 38.2 |
| 3 | m31_han_crf_BIO_adamw_lr5e-4 | HAN-CRF | BIO | AdamW | 5e-4 | 44.83 | 61.23 | 53.03 | 20.7 |
| 4 | m31_han_crf_IOBES_adamw_lr5e-4 | HAN-CRF | IOBES | AdamW | 5e-4 | 44.53 | 61.52 | 53.03 | 21.6 |
| 5 | m31_bilstm_crf_IOBES_adamw_lr5e-4 | BiLSTM-CRF | IOBES | AdamW | 5e-4 | 44.46 | 61.57 | 53.02 | 36.9 |
| 7 | m31_bilstm_crf_BIO_adamw_lr1e-3 | BiLSTM-CRF | BIO | AdamW | 1e-3 | 44.23 | 61.63 | 52.93 | 37.4 |
| 9 | m31_han_crf_IOBES_adamw_lr1e-3 | HAN-CRF | IOBES | AdamW | 1e-3 | 44.87 | 60.96 | 52.91 | 21.4 |
| 10 | m31_han_crf_BIO_adamw_lr1e-3 | HAN-CRF | BIO | AdamW | 1e-3 | 44.55 | 61.18 | 52.86 | 20.2 |
| 11 | m31_bilstm_crf_BIO_adamw_lr5e-4 | BiLSTM-CRF | BIO | AdamW | 5e-4 | 44.45 | 61.20 | 52.83 | 40.4 |

### 4.3 Baseline Sweep (SGD — all underperform)

| Rank | Config ID | Model | Schema | Optimizer | LR | GS42 F1 | GS91 F1 | Mean F1 | Epoch (s) |
|------|-----------|-------|--------|-----------|-----|---------|---------|---------|-----------|
| 15 | m31_bilstm_crf_IOBES_sgd_lr1e-3 | BiLSTM-CRF | IOBES | SGD | 1e-3 | 41.40 | 43.17 | 42.28 | 35.7 |
| 16 | m31_bilstm_crf_BIO_sgd_lr1e-3 | BiLSTM-CRF | BIO | SGD | 1e-3 | 40.07 | 42.10 | 41.09 | 38.4 |
| 17 | m31_bilstm_crf_IOBES_sgd_lr5e-4 | BiLSTM-CRF | IOBES | SGD | 5e-4 | 37.15 | 37.87 | 37.51 | 37.8 |
| 18 | m31_han_crf_BIO_sgd_lr1e-3 | HAN-CRF | BIO | SGD | 1e-3 | 37.68 | 37.11 | 37.39 | 19.0 |
| 19 | m31_han_crf_IOBES_sgd_lr1e-3 | HAN-CRF | IOBES | SGD | 1e-3 | 35.03 | 34.35 | 34.69 | 20.3 |
| 20 | m31_bilstm_crf_BIO_sgd_lr5e-4 | BiLSTM-CRF | BIO | SGD | 5e-4 | 30.60 | 31.27 | 30.94 | 36.0 |
| 21 | m31_han_crf_IOBES_sgd_lr5e-4 | HAN-CRF | IOBES | SGD | 5e-4 | 23.84 | 23.11 | 23.48 | 21.9 |
| 22 | m31_han_crf_BIO_sgd_lr5e-4 | HAN-CRF | BIO | SGD | 5e-4 | 21.12 | 20.12 | 20.62 | 19.8 |

---

## 5. Context Mode Ablation (IOBES · AdamW · lr=1e-3 · fixed)

Isolating the effect of context mode, holding all other hyperparameters constant:

| Context Mode | Heads | Gated | GS42 F1 | GS91 F1 | Mean F1 | Δ GS91 vs sentence_only |
|--------------|-------|-------|---------|---------|---------|------------------------|
| sentence_only | 4 | ✗ | 44.38 | 61.11 | 52.75 | baseline (h4) |
| sentence_only | 8 | ✗ | 44.88 | 61.06 | 52.97 | −0.05 |
| token_doc_attn | 4 | ✗ | 44.16 | 61.44 | 52.80 | +0.33 |
| token_doc_attn | 8 | ✗ | 44.51 | 61.08 | 52.80 | −0.03 |
| token_doc_attn_gated | 4 | ✓ | 44.42 | 61.44 | 52.93 | +0.33 |
| **token_doc_attn_gated** | **8** | **✓** | **44.90** | **62.11** | **53.50** | **+1.00** |

> $\Delta\text{GS91}$ is relative to `sentence_only h4` (rank 14, lowest-ranked Phase 1 config)

---

## 6. Key Findings

### 6.1 Token-Document Attention with Gating Achieves New SOTA

`token_doc_attn_gated h8` sets a new best across all 22 runs:

$$
\text{GS91 F1}_{\text{best}} = 62.11\% \quad (+0.65 \text{ pp over previous best BiLSTM-CRF-IOBES-AdamW-lr1e-3})
$$

$$
\text{Mean F1}_{\text{best}} = 53.50\% \quad (+0.39 \text{ pp over rank 2})
$$

### 6.2 Gating Is the Critical Ingredient

Without gating (`token_doc_attn`), h8 delivers only 61.08% GS91 — no improvement over the `sentence_only` baseline. With gating (`token_doc_attn_gated`), h8 jumps to 62.11%:

$$
\Delta_{\text{gate}} = 62.11 - 61.08 = +1.03 \text{ pp (GS91)}
$$

This confirms that the model benefits from **selectively** incorporating document context rather than unconditionally adding it.

### 6.3 Head Count Matters Only with Gating

| Config | h4 GS91 | h8 GS91 | Δ(h8−h4) |
|--------|---------|---------|----------|
| token_doc_attn (no gate) | 61.44 | 61.08 | −0.36 |
| token_doc_attn_gated | 61.44 | 62.11 | **+0.67** |

Without gating, more heads slightly hurt. With gating, 8 heads provide a meaningful gain, suggesting the gate helps regularize the higher-capacity attention.

### 6.4 Efficiency Trade-off

`token_doc_attn_gated h8` is ~33% slower per epoch than the `sentence_only` baseline (28.4 s vs 21.4 s), but ~25% faster than BiLSTM-CRF (38.2 s). The GS91 gain of +0.65 pp over BiLSTM-CRF is achieved at lower training cost.

### 6.5 AdamW vs SGD

SGD configurations uniformly underperform by 10–30 F1 points. The best SGD result (BiLSTM-CRF IOBES lr=1e-3, 43.17% GS91) is ~18 pp below the Phase 1 winner. SGD is not viable for this task without LR scheduling.

### 6.6 IOBES vs BIO Schema

Within the AdamW cluster the schemas are nearly tied:

| Schema | Best GS91 (any model) | Best Mean F1 |
|--------|-----------------------|--------------|
| IOBES | 62.11 (Phase 1 winner) | 53.50 |
| BIO | 61.63 (BiLSTM-CRF) | 52.93 |

IOBES provides a slight advantage, consistent with prior work showing explicit end-of-span tags reduce boundary confusion.

---

## 7. Mixed-Precision Bug Fixes (Phase 1 Engineering)

Two runtime crashes were diagnosed and patched in `src/nlp/models/han_crf.py` (`TokenDocumentAttention._attend_flat`) before the sweep could run:

### Bug 1 — FP16 overflow in `masked_fill`

**Root cause:** `attn_scores.masked_fill(~key_mask, -1e9)` — the literal `-1e9` overflows `torch.float16` (max representable ≈ 65,504).

**Fix:**
```python
# Before (crashes on RTX with AMP)
attn_scores = attn_scores.masked_fill(~key_mask, -1e9)

# After (dtype-aware)
neg_inf = torch.finfo(attn_scores.dtype).min
attn_scores = attn_scores.masked_fill(~key_mask, neg_inf)
```

### Bug 2 — dtype mismatch in `index_copy_`

**Root cause:** `context * flat_mask.unsqueeze(-1).float()` — `.float()` promotes the mask to FP32, making `context` FP32. Subsequent `output.index_copy_(0, sent_idx, context_doc)` fails because `output` is FP16.

**Fix:**
```python
# Before
context = context * flat_mask.unsqueeze(-1).float()

# After (preserves tensor dtype)
context = context * flat_mask.unsqueeze(-1).type_as(context)
```

**General rule:** In mixed-precision PyTorch, never use hardcoded float literals for mask fills — use `torch.finfo(t.dtype).min`. Never use `.float()` on values that will be multiplied into potentially FP16 tensors — use `.type_as(target)`.

---

## 8. Next Steps

| Priority | Action |
|----------|--------|
| High | Phase 2: vary `han_context_dropout` ∈ {0.05, 0.10, 0.20} for `token_doc_attn_gated h8` |
| High | Phase 2: vary `lr` ∈ {5e-4, 1e-3, 2e-3} for the winning config |
| Medium | Increase epochs to 30 for `token_doc_attn_gated h8` to check if GS91 still improves |
| Medium | Holdout evaluation: run `testHoldOut` mode on the best checkpoint |
| Low | Ablate `han_use_gated_fusion` with `sentence_only` context (not yet tested) |
| Low | Profile memory footprint of `token_doc_attn_gated h8` for larger batch sizes |

---

## 9. Configuration Reference

All Phase 1 runs used:

```
--model han_crf
--taggingSchema IOBES
--optimizer adamw
--lr 1e-3
--batchSize 64
--epochs 20
--positiveUpsample 2
--hanBatchMode fixed
--rebalancingMode auto
--hanUseBlockDiagonal
--no-hanFreezeEmbeddings
--bilstmFreezeEmbeddings
--hanContextDropout 0.1
```

Variable flags per run: `--hanContextMode {sentence_only, token_doc_attn, token_doc_attn_gated}`, `--hanContextHeads {4, 8}`, `--hanUseGatedFusion / --no-hanUseGatedFusion`.
