# Phase 3 Research Plan: Label Quality & Training Dynamics
**Date:** 2026-06-01 (Post-Phase 2 Analysis) | **Status:** PLANNING

---

## Strategic Rationale

Phase 2 demonstrated that **syntactic approaches (sentence filtering, batch packing) cannot overcome label noise** in synthetic training data. Phase 3 pivots to address the root cause: **poor label quality and suboptimal training dynamics**.

Two complementary strategies identified:
1. **Weak-label confidence weighting** — Down-weight ambiguous/noisy labels during training
2. **Curriculum learning** — Train on easy (high-confidence) examples first, gradually introduce hard ones

---

## Phase 3 Run Matrix (8 Runs)

### Strategic Design

The 8-run matrix is structured to:
1. **Establish baseline** (Run 1) — Phase 1 SOTA without label weighting
2. **Isolate confidence weighting effect** (Runs 2–4) — Three confidence thresholds
3. **Isolate curriculum learning effect** (Runs 5–7) — Three curriculum schedules
4. **Combine best approaches** (Run 8) — Winner from 2-4 + winner from 5-7

### Run Configurations

```
Run | Strategy           | Param 1        | Param 2         | Expected Δ | Notes
─────────────────────────────────────────────────────────────────────────────
 1  | Baseline (none)    | -              | -               | 0.00 pp    | Phase 1 SOTA reference
 2  | Confidence weight  | threshold=0.6  | -               | +0.2–0.3pp | Aggressive weighting
 3  | Confidence weight  | threshold=0.7  | -               | +0.3–0.4pp | Moderate weighting
 4  | Confidence weight  | threshold=0.8  | -               | +0.3–0.5pp | Conservative weighting
 5  | Curriculum learn   | schedule=linear | warmup=20%      | +0.2–0.3pp | Slow progression
 6  | Curriculum learn   | schedule=sqrt  | warmup=20%      | +0.2–0.4pp | Medium progression
 7  | Curriculum learn   | schedule=exp   | warmup=20%      | +0.1–0.3pp | Fast progression
 8  | Combined           | best_conf_run  | best_curric_run | +0.5–0.8pp | Synergistic effect
```

### Detailed Run Specifications

| Run | Config ID | Model | Confidence Thresh | Curriculum Sched | Warmup % | Notes |
|-----|-----------|-------|-------------------|-------------------|----------|-------|
| 1 | p3_run1_baseline | han_crf | — | — | — | Control: Phase 1 config |
| 2 | p3_run2_conf_06 | han_crf | 0.6 | — | — | Aggressive confidence filter |
| 3 | p3_run3_conf_07 | han_crf | 0.7 | — | — | **Expected WINNER (confidence)** |
| 4 | p3_run4_conf_08 | han_crf | 0.8 | — | — | Conservative confidence filter |
| 5 | p3_run5_curric_lin | han_crf | — | linear | 20% | Linear difficulty progression |
| 6 | p3_run6_curric_sqrt | han_crf | — | sqrt | 20% | **Expected WINNER (curriculum)** |
| 7 | p3_run7_curric_exp | han_crf | — | exp | 20% | Exponential difficulty progression |
| 8 | p3_run8_combined | han_crf | 0.7 | sqrt | 20% | Combined best (confidence 0.7 + sqrt curriculum) |

---

## Implementation Requirements

### 1. Confidence Weighting

**Mechanism:** Assign per-label confidence based on agreement across synthetic label sources

**Implementation in gna_experiment.py:**
```python
# During training data loading
label_confidence = compute_label_confidence(source_agreement, span_overlap_score)
# label_confidence ∈ [0, 1] where 1 = high agreement, 0 = low agreement

# During training loop
if confidence_threshold is not None:
    mask = label_confidence >= confidence_threshold
    # Training only on high-confidence labels
```

**Configuration flags:**
- `--weakLabelConfidenceThreshold`: Float in [0.0, 1.0]. Only train on labels with confidence ≥ threshold
- `--weakLabelConfidenceMetric`: Choice of {"source_agreement", "span_overlap", "combined"}

**Expected effect:**
- Removes noisiest synthetic labels
- Reduces label noise → Cleaner training signal
- May reduce training data size (acceptable trade-off)

### 2. Curriculum Learning

**Mechanism:** Order training samples by difficulty; train on easy samples first

**Difficulty metric:** Inverse of label confidence
- Easy samples: High confidence, high agreement
- Hard samples: Low confidence, conflicting labels

**Implementation in gna_experiment.py:**
```python
# Compute sample difficulty (inverse confidence)
sample_difficulty = 1 - mean_label_confidence_per_sample

# Schedule difficulty threshold over epochs
difficulty_threshold = curriculum_schedule(epoch, total_epochs, warmup_pct)

# Epoch 1: Only samples with difficulty < threshold (easy)
# Epoch N: All samples (difficulty → 1.0)
```

**Configuration flags:**
- `--curriculumLearningEnabled`: Boolean to enable curriculum
- `--curriculumSchedule`: Choice of {"linear", "sqrt", "exp"}
- `--curriculumWarmupPercent`: Percentage of epochs to spend in warmup (easier samples only)

**Schedule formulas (where epoch ∈ [0, 1]):**
```
linear: difficulty_threshold = epoch
sqrt:   difficulty_threshold = sqrt(epoch)
exp:    difficulty_threshold = exp(epoch) - 1  (normalized to [0, 1])
```

**Expected effect:**
- Stabilizes early training (easy samples first)
- Prevents catastrophic forgetting of easy patterns
- Improves generalization on hard test cases

### 3. Combined Approach (Run 8)

**Mechanism:** Use confidence weighting to pre-filter, then apply curriculum on filtered set

**Implementation:**
```python
# Step 1: Filter by confidence
filtered_data = load_training_data(confidence_threshold=0.7)

# Step 2: Sort by curriculum difficulty
sorted_data = sort_by_curriculum(filtered_data, schedule='sqrt', warmup=20%)

# Step 3: Train with curriculum scheduler
for epoch in range(total_epochs):
    batch = curriculum_sampler(sorted_data, epoch, total_epochs)
    train_one_epoch(batch)
```

**Synergy hypothesis:**
- Confidence weighting removes label noise
- Curriculum learning maximizes signal from clean labels
- Combined effect: +0.5–0.8 pp improvement

---

## Label Confidence Computation

### Data Sources for Synthetic Labels

Current PubMed training data uses weak labels from:
1. **PubMed abstract text + keyword matching** (primary)
2. **MetaMap entity linking** (secondary, experimental)
3. **BioBERT entity predictions** (tertiary, if available)

### Confidence Score Formula

```
confidence(label) = (
    w_source * source_agreement +
    w_overlap * span_overlap_score +
    w_frequency * label_frequency_score
)
```

where:
- `source_agreement ∈ [0, 1]` — Fraction of sources that agree on label
- `span_overlap_score ∈ [0, 1]` — How well span matches keyword boundaries
- `label_frequency_score ∈ [0, 1]` — How common the label is in training set
- Weights default to: w_source=0.6, w_overlap=0.3, w_frequency=0.1

### Per-Sample Difficulty (for Curriculum)

```
sample_difficulty = mean(1 - confidence) for all labels in sample
```

Samples with high mean confidence → Easy
Samples with low mean confidence → Hard

---

## Success Criteria

| Criterion | Value | Rationale |
|-----------|-------|-----------|
| **Target** | Mean F1 ≥ **54.00%** | Δ ≥ +0.50 pp vs Phase 1 (53.50%) |
| **Minimum** | Mean F1 ≥ 53.80% | Δ ≥ +0.30 pp (Phase 2 threshold) |
| **Baseline** | Mean F1 = 53.50% | Phase 1 SOTA (reference) |
| **Failure** | Mean F1 < 53.20% | Worse than Phase 2 best (53.22%) |

### Ranking Criteria (for Run 8 decision)
1. **Highest individual run mean F1** (among Runs 2–7)
2. **Consistency across GS42 & GS91** (avoid one-set overfitting)
3. **Robustness** (low variance across seeds if multi-seed, or visual inspection)

---

## Execution Plan

### Phase 3 Timeline (Estimated)

| Step | Task | Duration | Output |
|------|------|----------|--------|
| 1 | Implement confidence weighting in gna_experiment.py | 15 min | Updated code + config |
| 2 | Implement curriculum learning scheduler | 20 min | Updated code + config |
| 3 | Create Phase 3 runner script (8 runs) | 10 min | run_matrix_phase3_20260601.sh |
| 4 | Smoke test (Run 1, 1 epoch) | 2 min | Validation of infrastructure |
| 5 | Launch full Phase 3 matrix (Runs 1–8, 20 epochs each) | ~120 min | All 8 runs completed |
| 6 | Summarize results & rank | 10 min | phase3_runtime_metrics_ranked.csv |
| **Total** | | ~177 min (~3 hours) | Complete Phase 3 analysis |

### Key Milestones

- **T+15 min:** Infrastructure code deployed
- **T+30 min:** Smoke test completed, ready for launch
- **T+150 min:** All 8 runs completed
- **T+160 min:** Ranking & analysis finalized

---

## Expected Outcomes by Run

### Confidence Weighting Alone (Runs 2–4)

| Run | Threshold | Expected F1 | Rationale |
|-----|-----------|-------------|-----------|
| 2 | 0.6 | 53.8–54.0% | Aggressive; removes ~30% of data but keeps good labels |
| 3 | 0.7 | 54.0–54.2% | **Optimal** — removes noise, keeps most good labels |
| 4 | 0.8 | 53.9–54.1% | Conservative; may under-filter noise |

### Curriculum Learning Alone (Runs 5–7)

| Run | Schedule | Expected F1 | Rationale |
|-----|----------|-------------|-----------|
| 5 | linear | 53.7–53.9% | Slow progression may not challenge model enough |
| 6 | sqrt | 53.9–54.1% | **Optimal** — balanced progression |
| 7 | exp | 53.8–54.0% | Fast progression may be too aggressive |

### Combined (Run 8)

| Configuration | Expected F1 | Rationale |
|---|---|---|
| conf=0.7 + curric=sqrt | **54.2–54.5%** | **Expected WINNER** — Synergy of both approaches |

**Hypothesis:** Combined approach yields +0.5–0.8 pp over baseline due to synergistic effects (confidence weighting removes noise, curriculum learning leverages clean labels optimally).

---

## Fallback Plan (If Phase 3 Underperforms)

If all Phase 3 runs score **< 53.50%** (worse than Phase 1):

1. **Debug confidence computation** — Verify label agreement scores are correct
2. **Adjust confidence threshold** — Try 0.5 or 0.75 (not 0.6–0.8 grid)
3. **Use harder curriculum** — Increase warmup % (40% instead of 20%)
4. **Revert to Phase 1 config** — Accept Phase 1 SOTA as final model

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Confidence weighting removes too many labels | Low (30%) | High (model underfits) | Fallback to threshold=0.5 |
| Curriculum learning doesn't help | Medium (40%) | Medium (wasted run) | Covered by single-strategy runs |
| Code bugs in new features | Low (20%) | High (crashes) | Smoke test before launch |
| Combined approach overcomplicates training | Low (25%) | Medium (marginal gain) | Acceptable if > 54.0% achieved |

---

## Code Changes Checklist

### Files to Modify

- [ ] `src/nlp/experiments/gna_experiment.py` — Add confidence weighting & curriculum learning logic
- [ ] `src/core/configV2.py` — Add new configuration parameters
- [ ] `src/nlp/jobs/gna_pipeline.py` — Add CLI flags for new parameters
- [ ] Create `scripts/jobs/run_matrix_phase3_20260601.sh` — Phase 3 orchestrator

### New Parameters (to configV2.py & gna_pipeline.py)

```python
# Weak-label confidence
WEAK_LABEL_CONFIDENCE_THRESHOLD = None  # Default: off (None = no threshold)
WEAK_LABEL_CONFIDENCE_METRIC = "source_agreement"

# Curriculum learning
CURRICULUM_LEARNING_ENABLED = False  # Default: off
CURRICULUM_SCHEDULE = "linear"  # Options: linear, sqrt, exp
CURRICULUM_WARMUP_PERCENT = 20  # Percentage of epochs in easy-sample-only phase
```

### CLI Flags (to gna_pipeline.py)

```bash
--weakLabelConfidenceThreshold THRESHOLD
--weakLabelConfidenceMetric METRIC
--curriculumLearningEnabled
--curriculumSchedule SCHEDULE
--curriculumWarmupPercent PERCENT
```

---

## Documentation Files to Generate

1. **phase3_execution_guide.md** — How to run Phase 3
2. **phase3_runner_script.sh** — Orchestrates 8 runs
3. **phase3_monitor.md** — Live monitoring during execution

---

## Next Actions

1. ✓ **Approve Phase 3 plan** (this document)
2. **Implement confidence weighting** in gna_experiment.py
3. **Implement curriculum learning scheduler** in gna_experiment.py
4. **Create Phase 3 runner script** with all 8 run configurations
5. **Smoke test** Run 1 (1 epoch) to validate infrastructure
6. **Launch Phase 3 matrix** (120–150 min estimated)
7. **Summarize results** and decide on next research direction (Phase 4 or publication)

---

## References

### Confidence Weighting in Weak Supervision
- Label weighting by source agreement reduces label noise in NLP tasks
- Typical threshold range: [0.5, 0.8] for binary/multi-source labels
- Expected improvement: +0.2–0.5 pp over unweighted baseline

### Curriculum Learning
- Training on easy examples first improves generalization in NLP
- Common schedules: linear, sqrt (medium), exp (fast)
- Warmup phase typically: 10–30% of total epochs
- Expected improvement: +0.1–0.4 pp over standard training
- Combined with label weighting: +0.3–0.8 pp synergistic gain

---

**Status:** READY FOR IMPLEMENTATION  
**Approval Required:** ✓ Proceed with Phase 3 infrastructure build
