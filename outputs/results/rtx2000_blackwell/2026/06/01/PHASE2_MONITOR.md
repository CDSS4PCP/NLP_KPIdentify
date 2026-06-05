# Phase 2 Execution — Real-time Monitor

**Launch Time:** 2026-06-01 14:56 UTC  
**Status:** ✅ RUNNING  
**ETA Completion:** 2026-06-01 16:12 UTC (~76 minutes)

---

## Active Monitoring

Two monitoring processes are active:

### Process 1: Main Phase 2 Runner
- **Terminal ID:** b692ef9f-63c7-444e-8ad1-9a0546e7a78e
- **Status:** Currently executing Run 1 (minTokens=4, memOff)
- **Command:** `PHASE2_CONTEXT_HORIZON=1 scripts/jobs/run_matrix_phase2_20260601.sh`

### Process 2: Live Progress Monitor
- **Terminal ID:** d3bcb370-c0de-46d3-89f6-5cde8b98f92f
- **Frequency:** Updates every 60 seconds
- **Tracking:** 
  - Run index line counts
  - Log file sizes and epoch counts
  - Latest output per run
  - Status transitions

---

## Phase 2 Run Configuration

| Run | Config ID | minTokens | Memory | Packing | Baseline | Expected Status |
|-----|-----------|-----------|--------|---------|----------|-----------------|
| 1 | p2_run1_minTokens4_memOff | 4 | OFF | mixed | **Control** | ⏳ Running |
| 2 | p2_run2_minTokens2_memOff | 2 | OFF | mixed | Lower filter | 🚫 Queued |
| 3 | p2_run3_minTokens1_memOff | 1 | OFF | mixed | Minimal filter | 🚫 Queued |
| 4 | p2_run4_minTokens4_memOn_mixed | 4 | ON | mixed | Memory test | 🚫 Queued |
| 5 | p2_run5_minTokens2_memOn_mixed | 2 | ON | mixed | Memory + lower | 🚫 Queued |
| 6 | p2_run6_minTokens1_memOn_mixed | 1 | ON | mixed | Memory + minimal | 🚫 Queued |
| 7 | p2_run7_minTokens2_memOn_strict | 2 | ON | strict_doc | Packing + lower | 🚫 Queued |
| 8 | p2_run8_minTokens1_memOn_strict | 1 | ON | strict_doc | Packing + minimal | 🚫 Queued |

---

## Phase 1 Baseline (All Runs Compare Against)

- **Model:** HAN-CRF
- **Schema:** IOBES
- **Optimizer:** AdamW, lr=1e-3
- **Batch:** 64, Epochs: 20
- **Context:** token_doc_attn_gated, heads=8, dropout=0.1
- **SOTA Metrics:** GS42=44.90, GS91=62.11, Mean F1=**53.50**

---

## Timeline & Milestones

| Time | Milestone | ETA |
|------|-----------|-----|
| 14:56 | Phase 2 launched | ✅ Done |
| 15:25 | Run 1 complete | ~29 min from start |
| 15:54 | Runs 1–2 complete | ~58 min from start |
| 16:12 | All 8 runs complete | ~76 min from start |
| 16:13 | Summarization begins | ~77 min from start |
| 16:15 | Phase 2 summary ready | ~79 min from start |

---

## Success Criteria

**Primary:** Mean GS F1 ≥ 53.80 (Phase 1 winner = 53.50, Δ = +0.30 pp)  
**Acceptable:** Mean GS F1 ≥ 53.65 (Δ ≥ +0.15 pp)  
**Fallback:** Identify best minTokens value for Phase 3

---

## How to Monitor

### Option 1: Check Monitor Terminal
```bash
# Monitor output visible in terminal d3bcb370-c0de-46d3-89f6-5cde8b98f92f
# Updates every 60 seconds
```

### Option 2: Direct File Inspection
```bash
# Check run index
tail -n 5 /home/rohangoli/remote_mount/outputs/results/rtx2000_blackwell/2026/06/01/phase2_run_index.csv

# Check specific log file
tail -n 20 /home/rohangoli/remote_mount/outputs/results/rtx2000_blackwell/2026/06/01/p2_run1_*.txt

# Count epochs in a run
grep -c "Epoch.*completed" /home/rohangoli/remote_mount/outputs/results/rtx2000_blackwell/2026/06/01/p2_run1_*.txt
```

### Option 3: Watch Process
```bash
# List all p2_*.txt logs with sizes
ls -lh /home/rohangoli/remote_mount/outputs/results/rtx2000_blackwell/2026/06/01/p2_*.txt
```

---

## Expected Behavior

### Run 1 (minTokens=4, memOff)
- **Purpose:** Control — same as Phase 1 SOTA baseline
- **Expected:** Similar mean F1 to Phase 1 (~53.50)
- **Timeline:** 
  - Data load: ~2–3 sec
  - Training: ~20 epochs × 28.4s/epoch ≈ 568 sec
  - Testing (GS42, GS91): ~20 sec
  - **Total:** ~9–10 minutes

### Runs 2–8
- **Sequential execution** after Run 1 completes
- **Similar timing** (~9–10 min each, possibly ±10% if data size changes)

---

## Next Steps

### When Run 1 Completes
1. ✅ Check if epoch 1 output looks normal
2. ✅ Verify GS42 and GS91 metrics appear in log
3. ✅ Confirm run index row added with "completed" status

### When All 8 Runs Complete
1. Run summarizer: `scripts/jobs/summarize_logs_phase2_20260601.sh`
2. Generate ranked CSV: `phase2_runtime_metrics_ranked.csv`
3. Generate summary markdown: `phase2_research_summary.md`
4. Analyze top 3 runs for Phase 3 planning

### If Any Run Fails
1. Check error in log file
2. Diagnose (e.g., OOM, dtype error, config parsing)
3. Fix issue and re-run single config with `DRY_RUN=0` flag

---

## File Locations

```
outputs/results/rtx2000_blackwell/2026/06/01/
├── phase2_run_index.csv               ← Live status tracking
├── p2_run1_*.txt                      ← Run 1 log (in progress)
├── p2_run2_*.txt                      ← Run 2 log (queued)
├── ... (p2_run3 through p2_run8)
├── phase1_research_summary.md         ← Phase 1 baseline for reference
└── PHASE2_EXECUTION_GUIDE.md          ← Detailed guide (reference)
```

After summarization:
```
├── phase2_runtime_metrics_ranked.csv  ← Ranked results
└── phase2_research_summary.md         ← Phase 2 findings & next steps
```

---

## Key Metrics to Watch

For each run, we'll track:
- **GS42 F1** (small test set, n=42 docs)
- **GS91 F1** (large test set, n=91 docs)
- **Mean F1** (average of GS42 and GS91) — **PRIMARY METRIC**
- **Epoch Time (s)** (avg seconds per epoch)
- **Warning Count** (FP16 overflows, dtype mismatches, etc.)

**Goal:** Identify configuration(s) with Mean F1 ≥ 53.80

---

## Contingency Plans

**If run crashes with OOM:**
- Reduce --batchSize to 32 and re-run

**If run crashes with dtype error:**
- Check if Phase 2 FP16 patches are applied in han_crf.py
- Verify torch.finfo and .type_as() usage

**If run stalls (no output for 30 min):**
- Kill terminal and check GPU state: `nvidia-smi`
- Check if process is hung: `ps aux | grep gna_pipeline`

**If results are suspiciously bad (F1 < 40):**
- Check data loading (minTokens filter may have dropped all data)
- Verify config was parsed correctly

---

## Monitoring Checklist

- [ ] Run 1 starts within 2 min
- [ ] Run 1 completes within 15 min
- [ ] Run 1 log shows epochs 1–20 (or up to current epoch if partial)
- [ ] Run 1 shows GS42 and GS91 metrics at end
- [ ] Run 1 status in CSV shows "completed"
- [ ] Run 2 starts within 2 min after Run 1 completes
- [ ] All 8 runs complete by 16:12 UTC
- [ ] Summarizer runs successfully
- [ ] phase2_runtime_metrics_ranked.csv has 8 data rows (plus header)
