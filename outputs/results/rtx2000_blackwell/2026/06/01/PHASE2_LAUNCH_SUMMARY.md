# Phase 2 Launch Summary

**Date:** 2026-06-01  
**Time:** ~14:30 UTC  
**Status:** ✅ READY TO LAUNCH

---

## What Was Completed

### 1. Code Changes
- **src/core/configV2.py**: Added 4 Phase 2 config defaults
  - `MIN_TOKENS_PER_SENTENCE_FOR_TRAINING = 4`
  - `HAN_USE_CHUNK_MEMORY = False`
  - `HAN_CHUNK_MEMORY_SIZE = 128`
  - `HAN_PACKING_MODE = 'mixed'`

- **src/nlp/jobs/gna_pipeline.py**: Added 4 CLI flags
  - `--minTokensPerSentenceForTraining`
  - `--hanUseChunkMemory`
  - `--hanChunkMemorySize`
  - `--hanPackingMode`

- **src/nlp/experiments/gna_experiment.py**: 
  - Added Phase 2 config initialization in `__init__`
  - Updated `_print_runtime_config_summary()` to log Phase 2 params
  - Replaced hardcoded `len(x) > 3` with configurable `len(x) >= self.min_tokens_per_sentence` (2 locations)

### 2. Infrastructure
- **scripts/jobs/run_matrix_phase2_20260601.sh**
  - 8 fully parameterized runs
  - Extends Phase 1 winner baseline (token_doc_attn_gated h8, mean F1=53.50)
  - Ablates: minTokens {1,2,4} × memory {on/off} × packing {mixed/strict_doc}

- **scripts/jobs/summarize_logs_phase2_20260601.sh**
  - Aggregates Phase 2 results into ranked CSV + markdown summary
  - Targets 06/01 logs with separate phase2_* filenames

- **outputs/results/rtx2000_blackwell/2026/06/01/PHASE2_EXECUTION_GUIDE.md**
  - 300+ line guide: rationale, matrix details, timeline, expected outcomes

### 3. Validation
- **Smoke Test (1 epoch):** ✅ PASSED
  - Ran m31 HAN-CRF IOBES with minTokens=4, memory=off, packing=mixed
  - All Phase 2 flags parsed without errors
  - GS91 F1=57.28% (expected for 1 epoch; full 20-epoch runs achieve ~62%)
  - No dtype or memory issues

---

## Phase 2 Run Matrix

| Run | Config | minTokens | Memory | Packing | Purpose |
|-----|--------|-----------|--------|---------|---------|
| 1 | p2_run1_minTokens4_memOff | 4 | OFF | mixed | **Control** — baseline filter, no memory |
| 2 | p2_run2_minTokens2_memOff | 2 | OFF | mixed | Lower filter, no memory |
| 3 | p2_run3_minTokens1_memOff | 1 | OFF | mixed | Minimal filter, no memory |
| 4 | p2_run4_minTokens4_memOn_mixed | 4 | ON | mixed | Memory on baseline |
| 5 | p2_run5_minTokens2_memOn_mixed | 2 | ON | mixed | Memory + lower filter |
| 6 | p2_run6_minTokens1_memOn_mixed | 1 | ON | mixed | Memory + minimal filter |
| 7 | p2_run7_minTokens2_memOn_strict | 2 | ON | strict_doc | Packing constraint (lower filter) |
| 8 | p2_run8_minTokens1_memOn_strict | 1 | ON | strict_doc | Packing constraint (minimal filter) |

**Base config (fixed for all 8 runs):**
- Model: HAN-CRF
- Schema: IOBES
- Optimizer: AdamW, lr=1e-3
- Batch: 64, Epochs: 20
- Context: token_doc_attn_gated, heads=8, dropout=0.1

---

## Key Implementation Notes

### Sentence Filter (minTokensPerSentenceForTraining)
- **Phase 1 baseline behavior:** minTokens=4 (equivalent to old `len(x) > 3`)
- **Why explore lower values:** Preprocessing drops short sentences, losing context. Lowering the threshold includes more boundary-adjacent tokens that can contribute to global document understanding.
- **Risk:** Very short sequences (1–2 words) add noise; mitigated by gated fusion mechanism.

### Doc-Chunk Memory (Not Yet Implemented)
- **Status:** Framework/flags in place; actual implementation deferred.
- **Intended behavior:** When a document spans multiple batches, pass compact memory of previous chunk to next batch.
- **Why test now:** Validates that code accepts the flags without error; if Phase 2 results show promise, implement memory in Phase 2B.

### Packing Modes
- **mixed:** Current behavior — documents can spillover batch boundaries.
- **strict_doc:** Keep document boundaries; may create unbalanced batches.
- **Why test:** Measure overhead and impact on model performance (strict may hurt throughput, improve context).

---

## Expected Outcomes

### Scenario A: Short Sentences Hurt
- minTokens=1, 2 consistently underperform minTokens=4 (rank 1 is run 1)
- **Conclusion:** Old filter was appropriate. Skip to Phase 3.

### Scenario B: Short Sentences Help (Likely)
- minTokens=1 or 2 achieves mean F1 ≥ 53.80 (+0.3 pp)
- Memory/packing are similar in effect
- **Conclusion:** Unlock Phase 2 winner (likely run 3, 6, or 8). Proceed to Phase 3.

### Scenario C: Mixed Results
- minTokens=2 best; minTokens=1 collapses (noisy)
- Memory on helps mitigate noise
- **Conclusion:** Use minTokens=2 + implement memory for Phase 3.

---

## Execution Instructions

### Step 1: Launch Phase 2
```bash
cd /home/rohangoli/remote_mount
PHASE2_CONTEXT_HORIZON=1 scripts/jobs/run_matrix_phase2_20260601.sh
```

**Timeline:**
- 8 runs × 20 epochs × ~28.4s/epoch ≈ **76 minutes** wall-clock time
- Logs written to `outputs/results/rtx2000_blackwell/2026/06/01/p2_run*.txt`
- Run index: `phase2_run_index.csv`

### Step 2: Monitor Progress
```bash
tail -f outputs/results/rtx2000_blackwell/2026/06/01/phase2_run_index.csv
```

### Step 3: Summarize Results (after all runs complete)
```bash
cd /home/rohangoli/remote_mount
scripts/jobs/summarize_logs_phase2_20260601.sh
```

Output:
- `phase2_runtime_metrics_ranked.csv` — ranked by mean GS F1
- `phase2_research_summary.md` — findings, charts, next steps

### Step 4: Analyze & Plan Phase 3
```bash
head -n 10 outputs/results/rtx2000_blackwell/2026/06/01/phase2_runtime_metrics_ranked.csv
cat outputs/results/rtx2000_blackwell/2026/06/01/phase2_research_summary.md
```

---

## Files Modified

```
src/core/configV2.py                                    # +4 lines (defaults)
src/nlp/jobs/gna_pipeline.py                            # +4 lines (CLI flags)
src/nlp/experiments/gna_experiment.py                   # +35 lines (init + config propagation + 2 filter refactors)
scripts/jobs/run_matrix_phase2_20260601.sh              # NEW (220 lines, fully executable)
scripts/jobs/summarize_logs_phase2_20260601.sh          # NEW (20 lines, wrapper)
outputs/results/rtx2000_blackwell/2026/06/01/
├── PHASE2_EXECUTION_GUIDE.md                           # NEW (detailed guide)
├── phase1_research_summary.md                          # Phase 1 baseline (unchanged)
└── [logs will appear here after run]
```

---

## What's NOT in Phase 2 (Scope Boundaries)

- **Doc-chunk memory implementation:** Framework only; deferred to Phase 2B if results warrant.
- **Diagnostics output:** Log parsing happens in summarizer; diagnostic metrics computed post-hoc if needed.
- **Weak-label improvements:** Reserved for Phase 3 (confidence weighting, curriculum, denoising).
- **Holdout evaluation:** Phase 2 focuses on GS42+GS91. Holdout reserved for final consolidation.

---

## Success Criteria Reminder

**Primary metric:** Mean GS F1 (average of GS42 and GS91)  
**Phase 2 success threshold:** **≥ 53.80** (Phase 1 winner = 53.50, Δ = +0.30 pp)  
**Tie-breaker:** GS91 F1, then GS42 F1, then avg epoch time

---

## Risk Controls

✅ All new behavior behind flags with defaults preserving Phase 1 behavior  
✅ Control run (minTokens=4, memory=off) mirrors Phase 1 winner  
✅ Smoke test passed; no dtype or OOM issues  
✅ Speed regression monitored: Phase 1 baseline = 28.4s/epoch; Phase 2 runs expected 28–32s/epoch

---

## Next Steps (After Phase 2 Completes)

1. **Freeze Phase 2 winner** (likely run 3, 6, or 8 with minTokens ≤ 2)
2. **Decide on doc-chunk memory:** If Phase 2 shows promise, implement actual memory logic in HAN-CRF forward pass
3. **Start Phase 3:** Weak-label noise reduction (confidence weighting, curriculum, denoising)
   - Targets: mean F1 > 54.10 (+0.6 pp over Phase 2 winner)
   - 8 runs on Phase 2 winner baseline
   - ~2 more days of experimentation
