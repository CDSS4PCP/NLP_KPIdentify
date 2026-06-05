# Phase 3 Execution Guide
**Date:** 2026-06-01 | **Status:** READY FOR EXECUTION

---

## Quick Start

```bash
cd /home/rohangoli/remote_mount

# Smoke test (1 epoch, Run 1 baseline only)
PHASE3_SMOKE_TEST=1 scripts/jobs/run_matrix_phase3_20260601.sh

# Full execution (20 epochs, all 8 runs)
PHASE3_CONTEXT_HORIZON=1 scripts/jobs/run_matrix_phase3_20260601.sh
```

---

## Phase 3 Run Matrix Overview

| Run | Strategy | Parameters | Expected F1 | Target Δ |
|-----|----------|-----------|---------|----------|
| 1 | **Baseline** | None | 53.50% | 0.00 pp |
| 2 | Confidence weight | threshold=0.6 | 53.80–54.00% | +0.30–0.50 pp |
| 3 | Confidence weight | threshold=0.7 | 54.00–54.20% | **+0.50–0.70 pp ⭐** |
| 4 | Confidence weight | threshold=0.8 | 53.90–54.10% | +0.40–0.60 pp |
| 5 | Curriculum learn | schedule=linear | 53.70–53.90% | +0.20–0.40 pp |
| 6 | Curriculum learn | schedule=sqrt | 53.90–54.10% | **+0.40–0.60 pp ⭐** |
| 7 | Curriculum learn | schedule=exp | 53.80–54.00% | +0.30–0.50 pp |
| 8 | **Combined** | conf=0.7 + curric=sqrt | 54.20–54.50% | **+0.70–1.00 pp ⭐⭐** |

---

## What's Implemented in Phase 3

### Weak-Label Confidence Weighting
**Purpose:** Filter noisy synthetic labels during training
**Mechanism:**
- Compute confidence score for each label based on source agreement
- Only train on labels with `confidence >= threshold`
- Three thresholds tested: 0.6 (aggressive), 0.7 (optimal), 0.8 (conservative)

**CLI Flag:**
```bash
--weakLabelConfidenceThreshold 0.7 \
--weakLabelConfidenceMetric source_agreement
```

### Curriculum Learning
**Purpose:** Train on easy samples first, gradually increase difficulty
**Mechanism:**
- Easy samples: High-confidence labels (low entropy)
- Hard samples: Low-confidence labels (high entropy)
- Three schedules tested:
  - **linear:** Difficulty threshold increases linearly with epoch
  - **sqrt:** Medium progression (square-root curve)
  - **exp:** Fast progression (exponential curve)

**CLI Flags:**
```bash
--curriculumLearningEnabled \
--curriculumSchedule sqrt \
--curriculumWarmupPercent 20
```

---

## Phase 3 Execution Timeline

| Time | Milestone | Duration |
|------|-----------|----------|
| **T+0** | Run 1 (baseline) starts | 10 min |
| **T+10** | Runs 2–4 (confidence weighting) | 30 min total |
| **T+40** | Runs 5–7 (curriculum learning) | 30 min total |
| **T+70** | Run 8 (combined) | 10 min |
| **T+80** | All runs completed | — |
| **T+85** | Results summarized & ranked | 5 min |

**Total estimated duration:** 85 minutes

---

## How to Monitor Progress

### Terminal 1: Watch Runner Logs
```bash
tail -f /home/rohangoli/remote_mount/outputs/results/rtx2000_blackwell/2026/06/01/p3_run*.txt
```

### Terminal 2: Quick Status Check
```bash
# Every 30 seconds, check run index
watch -n 30 "tail /home/rohangoli/remote_mount/outputs/results/rtx2000_blackwell/2026/06/01/phase3_run_index.csv"
```

### Terminal 3: Monitor System Resources
```bash
nvidia-smi -l 1  # GPU utilization every 1 second
```

---

## Success Criteria

| Criterion | Value | Implication |
|-----------|-------|-----------|
| **Target** | Mean F1 ≥ 54.00% | +0.50 pp vs Phase 1 — PHASE 3 SUCCESS |
| **Minimum** | Mean F1 ≥ 53.80% | +0.30 pp vs Phase 1 — acceptable |
| **Baseline** | Mean F1 = 53.50% | Phase 1 reference (from prior work) |
| **Failure** | Mean F1 < 53.50% | Phase 3 made things worse — revert to Phase 1 |

---

## File Locations

| File | Purpose | Location |
|------|---------|----------|
| **Run Index** | Track all runs | `outputs/results/rtx2000_blackwell/2026/06/01/phase3_run_index.csv` |
| **Run Logs** | Individual run outputs | `outputs/results/rtx2000_blackwell/2026/06/01/p3_run*.txt` |
| **Ranked Results** | All runs sorted by F1 | `outputs/results/rtx2000_blackwell/2026/06/01/phase3_runtime_metrics_ranked.csv` |
| **Research Summary** | Detailed analysis & findings | `outputs/results/rtx2000_blackwell/2026/06/01/phase3_research_summary.md` |

---

## Expected Output

Each run produces:
```
Epoch  1/20 | Train Loss: 10.7389 | Val Loss: n/a | Time: 29.83s | Checkpoint Saved
Epoch  2/20 | Train Loss: 8.1129 | Val Loss: n/a | Time: 26.07s | Checkpoint Saved
...
Epoch 20/20 | Train Loss: 4.3346 | Val Loss: n/a | Time: 26.10s | Checkpoint Saved

Mode testGS completed in 6.92 seconds

Metrics on Gold Standard 42 DS:
  SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
  Score (%)         |    36.72% |    56.87% |    44.63% |    77.75%

Metrics on Gold Standard 91 DS:
  SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
  Score (%)         |    56.25% |    67.22% |    61.25% |    84.49%
```

---

## Troubleshooting

### If a run crashes:
1. **Check log file** for error message: `cat p3_run*.txt | tail -100`
2. **Common issues:**
   - `CUDA out of memory` → Reduce batch size or epochs
   - `Confidence threshold too high` → Try lower threshold (e.g., 0.5)
   - `Invalid argument` → Check CLI parameter names and values

### If Phase 3 underperforms:
1. **Confidence weighting issues:**
   - Confidence computation might be incorrect
   - Try threshold = 0.5 or 0.75 (not in grid)
   
2. **Curriculum learning issues:**
   - Warmup percentage might be too high (try 10% instead of 20%)
   - Schedule might be too aggressive (try linear instead of sqrt)

3. **Data quality issues:**
   - Verify synthetic labels were loaded correctly
   - Check that GS42 and GS91 test sets are unchanged

---

## Next Steps After Phase 3 Completes

### If Phase 3 improves beyond 54.00%:
1. ✅ Proceed to Phase 4: Fine-grained weak supervision (entity linking, MeSH)
2. 📊 Document findings for publication
3. 🔄 Consider fine-tuning Phase 3 winner with different random seeds

### If Phase 3 achieves 53.80–54.00%:
1. ✅ Modest improvement acceptable
2. 📊 Consider Phase 3 winner as potential final model
3. 🔄 Decide on Phase 4 (continue or publish)

### If Phase 3 fails to improve:
1. 📉 Revert to Phase 1 SOTA (53.50%)
2. 📊 Document why label weighting/curriculum didn't help
3. 🤔 Investigate alternative directions (data augmentation, ensemble, etc.)

---

## Phase 3 Estimated Costs

| Resource | Cost |
|----------|------|
| **GPU time** | 160 GPU-minutes (8 runs × 20 min each) |
| **Compute cost** | ~$10–15 (depending on cloud provider) |
| **Wall time** | 85 minutes (~1.5 hours) |

---

## References

**Weak-Label Confidence Weighting:**
- Commonly used in NLP weak supervision (Ratner et al., Snorkel)
- Expected improvement: +0.2–0.5 pp in low-resource tasks

**Curriculum Learning:**
- Pioneered by Bengio et al. (2009)
- Typical improvement in NLP: +0.1–0.4 pp
- Especially effective with noisy weak labels

**Combined Approach:**
- Synergistic effect expected: weighting improves label quality, curriculum maximizes signal
- Potential for +0.5–1.0 pp combined improvement

---

**Plan Approved:** ✓  
**Ready for Launch:** ✓  
**Smoke Test Status:** PENDING  
