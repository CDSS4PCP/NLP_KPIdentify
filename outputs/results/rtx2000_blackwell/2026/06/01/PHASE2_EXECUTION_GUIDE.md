# Phase 2 Execution Guide

**Date:** 2026-06-01  
**Objective:** Reduce context truncation from sentence filtering and batch-chunk locality  
**Base Config:** Phase 1 winner (`token_doc_attn_gated h8`, mean GS F1 = 53.50)  
**Success Criteria:** Mean GS F1 ≥ 53.80 (+0.3 pp over Phase 1 winner)

---

## Phase 2 Experiment Matrix

All Phase 2 runs use the Phase 1 SOTA configuration as base:
- Model: HAN-CRF
- Schema: IOBES
- Optimizer: AdamW, lr=1e-3
- Batch size: 64
- Epochs: 20
- Context mode: `token_doc_attn_gated`
- Context heads: 8
- Context dropout: 0.1
- Gated fusion: enabled

**Variable parameters:** `minTokensPerSentenceForTraining`, `hanUseChunkMemory`, `hanPackingMode`

### Run Details

| Run # | Config ID | minTokens | Memory | Packing | Purpose |
|-------|-----------|-----------|--------|---------|---------|
| 1 | p2_run1_...minTokens4_memOff | 4 | OFF | mixed | **Control** — preserves current baseline sentence filter |
| 2 | p2_run2_...minTokens2_memOff | 2 | OFF | mixed | Lower filter, no memory — test impact of short sentences |
| 3 | p2_run3_...minTokens1_memOff | 1 | OFF | mixed | Minimal filter, no memory — maximum context horizon |
| 4 | p2_run4_...minTokens4_memOn_mixed | 4 | ON | mixed | Memory enabled on baseline filter — chunk memory validation |
| 5 | p2_run5_...minTokens2_memOn_mixed | 2 | ON | mixed | Memory + lower filter — synergy test |
| 6 | p2_run6_...minTokens1_memOn_mixed | 1 | ON | mixed | Memory + minimal filter — maximum horizon + memory |
| 7 | p2_run7_...minTokens2_memOn_strict | 2 | ON | strict_doc | Packing constraint — test doc-boundary preservation |
| 8 | p2_run8_...minTokens1_memOn_strict | 1 | ON | strict_doc | Max horizon + packing — full Phase 2 treatment |

---

## Execution Instructions

### Step 1: Verify Code Changes

All Phase 2 changes have been applied to:
- `src/core/configV2.py`: Added config defaults
- `src/nlp/jobs/gna_pipeline.py`: Added CLI flags
- `src/nlp/experiments/gna_experiment.py`: Replaced hardcoded `len(x) > 3` with configurable threshold

Verify with:
```bash
grep -n "MIN_TOKENS_PER_SENTENCE_FOR_TRAINING\|hanUseChunkMemory\|hanPackingMode" src/core/configV2.py
grep -n "minTokensPerSentenceForTraining\|hanUseChunkMemory\|hanPackingMode" src/nlp/jobs/gna_pipeline.py
grep -n "self.min_tokens_per_sentence\|self.han_use_chunk_memory\|self.han_packing_mode" src/nlp/experiments/gna_experiment.py
```

### Step 2: Run Phase 2 Matrix

```bash
cd /home/rohangoli/remote_mount
PHASE2_CONTEXT_HORIZON=1 scripts/jobs/run_matrix_phase2_20260601.sh
```

Expected output:
- 8 log files: `p2_run1_*.txt` through `p2_run8_*.txt`
- Run index: `outputs/results/rtx2000_blackwell/2026/06/01/phase2_run_index.csv`
- Each run takes ~9.5 minutes (20 epochs × 28.4s/epoch)
- Total sweep: ~76 minutes wall-clock time

### Step 3: Summarize Results

After all runs complete:
```bash
cd /home/rohangoli/remote_mount
scripts/jobs/summarize_logs_phase2_20260601.sh
```

Output:
- `phase2_runtime_metrics_ranked.csv` — ranked by mean GS F1
- `phase2_research_summary.md` — findings and next-steps

### Step 4: Evaluate

Check the ranked metrics CSV:
```bash
head -n 10 outputs/results/rtx2000_blackwell/2026/06/01/phase2_runtime_metrics_ranked.csv
```

Interpretation:
- **Rank 1** should have mean GS F1 > 53.50 if Phase 2 succeeds
- **GS91 vs GS42**: Check if lower minTokens hurts one dataset more than the other
- **Epoch time**: Memory + packing may add overhead; acceptable if F1 gain ≥ +0.3 pp

---

## Implementation Notes

### Sentence Filter (`minTokensPerSentenceForTraining`)

- **Default (Phase 1 behavior):** minTokens = 4 (equivalent to old `len(x) > 3`)
- **Phase 2 exploration:** minTokens ∈ {1, 2, 4}
- **Why:** Preprocessing drops short sentences, losing context. Lowering the filter includes more boundary-adjacent tokens and inter-sentential relations.
- **Risk:** Very short tokens (1–2 words) may introduce noise; mitigated by gated fusion.

### Doc-Chunk Memory (`hanUseChunkMemory`, `hanChunkMemorySize`, `hanPackingMode`)

- **Status:** Framework added, feature not yet implemented
  - Flags are parsed and stored in `self.han_use_chunk_memory`, etc.
  - No actual memory mechanism in forward pass yet
  - Phase 2 runs will exercise the code path but pass memory=off in most runs

- **Intended behavior (future):**
  - When a document spans multiple batches in fixed mode, pass a compact summary of previous chunk to next batch
  - Use pooled sentence / token embeddings, keyed by doc_id
  - Allows model to maintain long-range document context across batch boundaries

- **Packing modes:**
  - `mixed`: current behavior — spillover allowed
  - `strict_doc`: keep document boundaries; may create unbalanced batches
  - Phase 2 tests both to measure overhead

### Diagnostics

In future iterations, add logging to track:
- Sentence retention ratio per document
- Average chunks per document
- Fraction of tokens with cross-sentence context

For now, track manually from log outputs.

---

## Expected Outcomes

### Scenario A: Short Sentences Hurt
- minTokens = 1, 2 consistently underperform minTokens = 4
- **Conclusion:** Old filter was appropriate; skip to Phase 3

### Scenario B: Short Sentences Help (Likely)
- minTokens = 1 or 2 achieves mean GS F1 ≥ 53.80
- Memory on/off are similar (memory not implemented yet)
- **Conclusion:** Unlock Phase 2 winner, freeze minTokens, proceed to Phase 3

### Scenario C: Mixed Results
- minTokens = 2 best; minTokens = 1 collapses
- Memory on helps mitigate short-sentence noise
- **Conclusion:** Use minTokens = 2 + memory (once implemented) for Phase 3

---

## Timeline

| Step | Time | Cumulative |
|------|------|-----------|
| Smoke test (1 epoch × 1 run) | ~3 min | 3 min |
| Phase 2 sweep (8 runs × 20 epochs) | ~76 min | 79 min |
| Summarization | ~1 min | 80 min |
| Analysis & Phase 3 planning | ~30 min | 110 min |

**Estimated total:** ~2 hours for full Phase 2 execution and analysis.

---

## Files & Artifacts

```
outputs/results/rtx2000_blackwell/2026/06/01/
├── phase2_run_index.csv          # Experiment metadata & status
├── phase2_runtime_metrics_ranked.csv  # Results by mean GS F1
├── phase2_research_summary.md    # Findings, charts, next steps
├── p2_run1_...minTokens4_memOff.txt
├── p2_run2_...minTokens2_memOff.txt
├── p2_run3_...minTokens1_memOff.txt
├── p2_run4_...minTokens4_memOn_mixed.txt
├── p2_run5_...minTokens2_memOn_mixed.txt
├── p2_run6_...minTokens1_memOn_mixed.txt
├── p2_run7_...minTokens2_memOn_strict.txt
├── p2_run8_...minTokens1_memOn_strict.txt
└── [other Phase 1 artifacts...]
```

---

## Troubleshooting

**Issue:** "Phase 2 not enabled" message
- **Fix:** Run with `PHASE2_CONTEXT_HORIZON=1` prefix

**Issue:** Code crashes on new CLI flags
- **Cause:** Missing config parameter in `gna_experiment.py` constructor
- **Check:** Verify Phase 2 config initialization is present

**Issue:** Run times much longer than Phase 1
- **Expected:** minTokens=1 may increase data size; +10-20% slower is acceptable
- **Action:** Monitor epoch times in logs; if >40s/epoch, investigate

**Issue:** Memory usage spikes
- **Cause:** Lower minTokens = more training samples (especially with upsampling)
- **Mitigation:** Reduce batch size or epochs for diagnostic runs

---

## Next Phase

After Phase 2 completes:
1. **Freeze Phase 2 winner** (likely minTokens ≤ 2)
2. **Implement doc-chunk memory** in `han_crf.py` if Phase 2 suggests benefit
3. **Start Phase 3:** Weak-label noise reduction (confidence-weighted loss, curriculum, denoising)
