# Implementation Plan: Remaining Cases 1, 2, 3

## Scope
This plan covers only the remaining open concerns:
1. Document context is still coarse in HAN.
2. Effective document context is still constrained by preprocessing and batching.
3. Supervision remains weak and noisy due to synthetic-label generation.

Primary objective: improve external generalization on GS42 and GS91 without regressing throughput too heavily.

Primary ranking metric: mean of GS42 and GS91 F1.
Tie-breakers: GS91 F1, GS42 F1, then average epoch time.

## Baseline Anchor
Use the current winning baseline from 05/31:
- m31_han_crf_IOBES_adamw_lr1e-3
- Mean GS F1 about 53.02

All new variants must be compared against this baseline first.

## Phase 1: Case 1 Architecture Upgrade (Coarse Context)

### Goal
Move from sentence-pooled context injection to token-aware document context that can preserve boundary precision better.

### Code targets
- src/nlp/models/han_crf.py
- src/nlp/experiments/gna_experiment.py
- src/nlp/jobs/gna_pipeline.py
- src/core/configV2.py

### Implementation tasks
1. Add token-level document attention module in HAN.
- Add a new module in HAN that performs token-to-token attention within each document block.
- Use block-diagonal mask by doc_ids to avoid cross-document leakage.
- Keep existing word/sentence attention path as optional legacy mode.

2. Add gated fusion for local versus global token context.
- Add gate g in [0,1] per token.
- final_token = g * local_token + (1 - g) * global_token.
- Make gate configurable and default on for new architecture.

3. Add architecture modes for controlled ablations.
- hanContextMode choices:
  - sentence_only (current behavior)
  - token_doc_attn
  - token_doc_attn_gated

### Minimal CLI/config additions
- --hanContextMode
- --hanContextHeads
- --hanContextDropout
- --hanUseGatedFusion

### Phase 1 experiment set
Run 6 runs max:
1. sentence_only (baseline control)
2. token_doc_attn (heads=4)
3. token_doc_attn (heads=8)
4. token_doc_attn_gated (heads=4)
5. token_doc_attn_gated (heads=8)
6. token_doc_attn_gated (heads=8, lower dropout)

Keep optimizer/lr/schema fixed to current winner for this phase.

### Success criteria
- Mean GS F1 improves by at least +0.5 without more than 25 percent epoch slowdown.

## Phase 2: Case 2 Context Horizon and Batching Constraints

### Goal
Reduce context truncation from sentence filtering and batch-chunk locality.

### Code targets
- src/nlp/experiments/gna_experiment.py
- src/nlp/jobs/gna_pipeline.py
- src/core/configV2.py

### Implementation tasks
1. Make sentence-length filter configurable.
- Replace hardcoded len(x) > 3 with config threshold.
- New flag: --minTokensPerSentenceForTraining.
- Default should preserve old behavior initially for safe rollout.

2. Add doc-chunk memory mode in fixed batching.
- When a long document spans multiple fixed batches, pass forward a compact memory representation.
- First implementation can use previous-chunk sentence/token summary vectors, keyed by doc id.
- Keep this optional with a flag.

3. Improve doc packing strategy.
- Add a mode that keeps complete document boundaries where possible before spillover.
- Maintain strict doc_ids mapping for masks.

4. Add diagnostics.
- Log retained-versus-dropped sentence counts.
- Log average chunks per document.
- Log fraction of tokens receiving cross-sentence context.

### Minimal CLI/config additions
- --minTokensPerSentenceForTraining
- --hanUseChunkMemory
- --hanChunkMemorySize
- --hanPackingMode values strict_doc or mixed

### Phase 2 experiment set
Run 8 runs max on top Phase 1 winner:
1. minTokens 4, memory off (control)
2. minTokens 2, memory off
3. minTokens 1, memory off
4. minTokens 4, memory on
5. minTokens 2, memory on
6. minTokens 1, memory on
7. minTokens 2, memory on, strict_doc packing
8. minTokens 1, memory on, strict_doc packing

### Success criteria
- Mean GS F1 improves by at least +0.3 over Phase 1 winner.
- No pathological precision collapse due to very short-sentence inclusion.

## Phase 3: Case 3 Supervision Noise Reduction

### Goal
Reduce error from weak synthetic labels by confidence-aware training and better weak-label filtering.

### Code targets
- src/nlp/data/dataset.py
- src/nlp/models/preProcessData.py
- src/nlp/experiments/gna_experiment.py
- src/nlp/jobs/gna_pipeline.py
- src/core/configV2.py

### Implementation tasks
1. Add weak-label confidence scoring per sentence/document.
- Score signals can include:
  - keyword overlap confidence
  - span consistency ratio
  - entity source confidence if available
- Save confidence with training samples.

2. Add confidence-weighted loss.
- Weight each training sample loss by confidence.
- Add clipping floor and ceiling to avoid instability.

3. Add weak-label denoising filter.
- Optional removal/downweight of low-confidence pseudo-labels.
- Keep deterministic thresholds and log retained fraction.

4. Add curriculum schedule.
- Start with high-confidence pseudo-labels for first N epochs.
- Gradually include medium-confidence samples.

5. Preserve existing GS fine-tune path as final adaptation stage.

### Minimal CLI/config additions
- --weakLabelMinConfidence
- --weakLabelWeightingMode values off, linear, sqrt
- --weakLabelCurriculumEpochs
- --weakLabelDenoiseMode values off, drop, downweight

### Phase 3 experiment set
Run 8 runs max on Phase 2 winner:
1. weighting off, denoise off (control)
2. weighting linear, denoise off
3. weighting sqrt, denoise off
4. weighting linear, denoise drop
5. weighting sqrt, denoise drop
6. weighting linear, denoise downweight
7. weighting linear with curriculum
8. weighting sqrt with curriculum

### Success criteria
- Mean GS F1 improves by at least +0.5 over Phase 2 winner.
- Reduced variance between GS42 and GS91.

## Phase 4: Consolidation and Confirmation

### Final candidate selection
Pick top 3 configurations by mean GS F1 from all phases.

### Stability reruns
Run each top-3 config with 3 seeds.

### Final decision rule
Winner is highest seed-averaged mean GS F1.
Tie-breakers as declared above.

## Logging and output protocol
All logs and summaries remain in:
- outputs/results/rtx2000_blackwell/2026/05/31

Required artifacts:
1. run_index.csv with config metadata and status
2. runtime logs per config
3. runtime_metrics_ranked.csv
4. runtime_research_summary.md
5. phase-wise delta summary markdown:
- phase1_case1_results.md
- phase2_case2_results.md
- phase3_case3_results.md

## Recommended execution order
1. Implement Phase 1 code and run Phase 1 matrix.
2. Freeze Phase 1 winner and implement Phase 2.
3. Freeze Phase 2 winner and implement Phase 3.
4. Run consolidation seed reruns.

## Risk controls
1. Guard all new behavior behind flags with defaults that preserve current baseline.
2. Keep one unchanged control run in every phase.
3. Add strict runtime assertions for mask shapes and doc_ids alignment.
4. Track speed regressions continuously to avoid hidden compute blowups.

## Effort estimate
- Phase 1: 1 to 2 coding days plus 1 run day
- Phase 2: 1 coding day plus 1 run day
- Phase 3: 1 to 2 coding days plus 1 run day
- Consolidation: 1 run day

Total: about 6 to 8 days end-to-end depending on GPU queue and reruns.
