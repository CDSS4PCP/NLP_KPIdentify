#!/usr/bin/env bash

# Phase 3 Run Matrix Orchestrator: Label Quality & Training Dynamics
# Executes 8 runs ablating weak-label confidence weighting and curriculum learning
# Total estimated duration: 120–150 minutes (20 epochs × 8 runs)

set -e

WORKING_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${WORKING_DIR}/outputs/results/rtx2000_blackwell/2026/06/01"
RUN_INDEX="${LOG_DIR}/phase3_run_index.csv"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

cd "$WORKING_DIR"

# Create run index if not exists
if [[ ! -f "$RUN_INDEX" ]]; then
  echo "config_id,model,schema,optimizer,lr,batch_size,epochs,pos_upsample,han_batch_mode,han_block,han_freeze,bilstm_freeze,han_context_mode,han_context_heads,han_context_dropout,han_use_gated,min_tokens,han_memory,han_memory_size,han_packing,weak_conf_threshold,weak_conf_metric,curriculum_enabled,curriculum_schedule,curriculum_warmup,log_file,status" > "$RUN_INDEX"
fi

# Run orchestrator function
run_one() {
  local run_num=$1
  local config_id=$2
  local weak_conf=$3
  local weak_metric=$4
  local curric_enabled=$5
  local curric_sched=$6
  local curric_warmup=$7

  echo ""
  echo "============================================================"
  echo "Running p3_run${run_num}: ${config_id}"
  echo "============================================================"

  local log_file="${LOG_DIR}/p3_run${run_num}_${config_id}.txt"

  # Build command with all Phase 3 parameters
  local cmd="conda run -n cdss-gpu python src/nlp/jobs/gna_pipeline.py"
  cmd="$cmd --device cuda"
  cmd="$cmd --model han_crf"
  cmd="$cmd --taggingSchema IOBES"
  cmd="$cmd --mode train,testGS"
  cmd="$cmd --optimizer adamw"
  cmd="$cmd --lr 1e-3"
  cmd="$cmd --batchSize 64"
  cmd="$cmd --epochs 20"
  cmd="$cmd --positiveUpsample 2"
  cmd="$cmd --hanBatchMode fixed"
  cmd="$cmd --rebalancingMode auto"
  cmd="$cmd --hanContextMode token_doc_attn_gated"
  cmd="$cmd --hanContextHeads 8"
  cmd="$cmd --hanContextDropout 0.1"
  cmd="$cmd --minTokensPerSentenceForTraining 4"
  cmd="$cmd --hanChunkMemorySize 128"
  cmd="$cmd --hanPackingMode mixed"
  cmd="$cmd --hanUseBlockDiagonal"
  cmd="$cmd --no-hanFreezeEmbeddings"
  cmd="$cmd --bilstmFreezeEmbeddings"
  cmd="$cmd --hanUseGatedFusion"

  # Add Phase 3 parameters
  if [[ "$weak_conf" != "-" ]]; then
    cmd="$cmd --weakLabelConfidenceThreshold $weak_conf"
  fi
  if [[ "$weak_metric" != "-" ]]; then
    cmd="$cmd --weakLabelConfidenceMetric $weak_metric"
  fi
  if [[ "$curric_enabled" == "true" ]]; then
    cmd="$cmd --curriculumLearningEnabled"
    cmd="$cmd --curriculumSchedule $curric_sched"
    cmd="$cmd --curriculumWarmupPercent $curric_warmup"
  else
    cmd="$cmd --no-curriculumLearningEnabled"
  fi

  echo "Command: $cmd"
  echo ""

  # Run and capture output
  start_time=$(date +%s)
  if $cmd > "$log_file" 2>&1; then
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    status="completed"
    echo "✓ Run $run_num completed in ${duration}s"
  else
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    status="failed"
    echo "✗ Run $run_num FAILED after ${duration}s"
  fi

  # Append to run index
  echo "$config_id,han_crf,IOBES,adamw,1e-3,64,20,2,fixed,true,false,true,token_doc_attn_gated,8,0.1,true,4,false,128,mixed,$weak_conf,$weak_metric,$curric_enabled,$curric_sched,$curric_warmup,p3_run${run_num}_${config_id}.txt,$status" >> "$RUN_INDEX"

  # Brief pause before next run
  sleep 2
}

# Phase 3 Run Definitions (8 runs)
# Run 1: Baseline (no weighting, no curriculum)
run_one 1 "han_IOBES_adamw_lr1e-3_baseline" "-" "-" "false" "-" "-"

# Runs 2–4: Confidence weighting only (varying thresholds)
run_one 2 "han_IOBES_adamw_lr1e-3_conf06" "0.6" "source_agreement" "false" "-" "-"
run_one 3 "han_IOBES_adamw_lr1e-3_conf07" "0.7" "source_agreement" "false" "-" "-"
run_one 4 "han_IOBES_adamw_lr1e-3_conf08" "0.8" "source_agreement" "false" "-" "-"

# Runs 5–7: Curriculum learning only (varying schedules)
run_one 5 "han_IOBES_adamw_lr1e-3_curric_lin" "-" "-" "true" "linear" "20"
run_one 6 "han_IOBES_adamw_lr1e-3_curric_sqrt" "-" "-" "true" "sqrt" "20"
run_one 7 "han_IOBES_adamw_lr1e-3_curric_exp" "-" "-" "true" "exp" "20"

# Run 8: Combined (best confidence threshold + best curriculum schedule)
# Expected: conf=0.7 (from Run 3 results) + sqrt (from Run 6 results)
run_one 8 "han_IOBES_adamw_lr1e-3_combined_conf07_sqrt" "0.7" "source_agreement" "true" "sqrt" "20"

echo ""
echo "============================================================"
echo "Phase 3 experiment matrix completed."
echo "============================================================"
echo ""
echo "Results logged to: $RUN_INDEX"
echo "Run logs available in: $LOG_DIR"
echo ""
echo "To summarize results:"
echo "  python3 src/nlp/evaluation/summarize_runtime_logs.py --logDir $LOG_DIR --csvOut ${LOG_DIR}/phase3_runtime_metrics_ranked.csv --summaryOut ${LOG_DIR}/phase3_research_summary.md"
