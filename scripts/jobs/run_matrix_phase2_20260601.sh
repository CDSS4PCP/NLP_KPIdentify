#!/usr/bin/env bash
set -euo pipefail

# Phase 2: Context Horizon & Batching Constraints
# Goal: Reduce context truncation from sentence filtering and batch-chunk locality
# Base config: Phase 1 winner (token_doc_attn_gated h8)
# 8 runs × minTokens {1,2,4} × memory {on/off} × packing {mixed/strict_doc}

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/01"
RUN_INDEX="${LOG_DIR}/phase2_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,model,schema,optimizer,lr,batch_size,epochs,pos_upsample,han_batch_mode,han_block,han_freeze,bilstm_freeze,han_context_mode,han_context_heads,han_context_dropout,han_use_gated,min_tokens,han_memory,han_memory_size,han_packing,log_file,status"

mkdir -p "${LOG_DIR}"

if [[ ! -f "${RUN_INDEX}" ]]; then
  echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
else
  existing_header="$(head -n 1 "${RUN_INDEX}" || true)"
  if [[ "${existing_header}" != "${RUN_INDEX_HEADER}" ]]; then
    cp "${RUN_INDEX}" "${RUN_INDEX}.bak.$(date +%Y%m%d_%H%M%S)"
    echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
  fi
fi

run_one() {
  local config_id="$1"
  local model="$2"
  local schema="$3"
  local optimizer="$4"
  local lr="$5"
  local batch_size="$6"
  local epochs="$7"
  local pos_upsample="$8"
  local han_batch_mode="$9"
  local han_block="${10}"
  local han_freeze="${11}"
  local bilstm_freeze="${12}"
  local han_context_mode="${13}"
  local han_context_heads="${14}"
  local han_context_dropout="${15}"
  local han_use_gated="${16}"
  local min_tokens="${17}"
  local han_memory="${18}"
  local han_memory_size="${19}"
  local han_packing="${20}"

  local log_file="${LOG_DIR}/${config_id}.txt"
  local cmd=(
    conda run -n "${CONDA_ENV}" python src/nlp/jobs/gna_pipeline.py
    --device cuda
    --model "${model}"
    --taggingSchema "${schema}"
    --mode train,testGS
    --optimizer "${optimizer}"
    --lr "${lr}"
    --batchSize "${batch_size}"
    --epochs "${epochs}"
    --positiveUpsample "${pos_upsample}"
    --hanBatchMode "${han_batch_mode}"
    --rebalancingMode auto
    --hanContextMode "${han_context_mode}"
    --hanContextHeads "${han_context_heads}"
    --hanContextDropout "${han_context_dropout}"
    --minTokensPerSentenceForTraining "${min_tokens}"
    --hanChunkMemorySize "${han_memory_size}"
    --hanPackingMode "${han_packing}"
  )

  if [[ "${han_block}" == "true" ]]; then
    cmd+=(--hanUseBlockDiagonal)
  else
    cmd+=(--no-hanUseBlockDiagonal)
  fi

  if [[ "${han_freeze}" == "true" ]]; then
    cmd+=(--hanFreezeEmbeddings)
  else
    cmd+=(--no-hanFreezeEmbeddings)
  fi

  if [[ "${bilstm_freeze}" == "true" ]]; then
    cmd+=(--bilstmFreezeEmbeddings)
  else
    cmd+=(--no-bilstmFreezeEmbeddings)
  fi

  if [[ "${han_use_gated}" == "true" ]]; then
    cmd+=(--hanUseGatedFusion)
  else
    cmd+=(--no-hanUseGatedFusion)
  fi

  if [[ "${han_memory}" == "true" ]]; then
    cmd+=(--hanUseChunkMemory)
  else
    cmd+=(--no-hanUseChunkMemory)
  fi

  echo "Running ${config_id}"
  echo "Command: ${cmd[*]}"

  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${cmd[*]}" | tee "${log_file}"
    echo "${config_id},${model},${schema},${optimizer},${lr},${batch_size},${epochs},${pos_upsample},${han_batch_mode},${han_block},${han_freeze},${bilstm_freeze},${han_context_mode},${han_context_heads},${han_context_dropout},${han_use_gated},${min_tokens},${han_memory},${han_memory_size},${han_packing},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  (
    cd "${ROOT_DIR}"
    "${cmd[@]}"
  ) 2>&1 | tee "${log_file}"
  exit_code=${PIPESTATUS[0]}
  set -e

  local status="completed"
  if [[ $exit_code -ne 0 ]]; then
    status="failed"
  fi
  echo "${config_id},${model},${schema},${optimizer},${lr},${batch_size},${epochs},${pos_upsample},${han_batch_mode},${han_block},${han_freeze},${bilstm_freeze},${han_context_mode},${han_context_heads},${han_context_dropout},${han_use_gated},${min_tokens},${han_memory},${han_memory_size},${han_packing},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"
}

# ============================================================================
# Phase 2 Experiment Set (8 runs)
# Base: m31 · han_crf · IOBES · adamw · lr=1e-3 · 64 batch · 20 epochs
# Context: token_doc_attn_gated · heads=8 · dropout=0.1
# Variable: minTokens {1, 2, 4} × memory {on, off} × packing {mixed, strict_doc}
# ============================================================================

if [[ "${PHASE2_CONTEXT_HORIZON=}" != "1" ]]; then
  echo "Phase 2 not enabled. Run with PHASE2_CONTEXT_HORIZON=1 to start."
  exit 0
fi

# Run 1: Control (minTokens=4, memory=off, packing=mixed)
run_one "p2_run1_han_IOBES_adamw_lr1e-3_minTokens4_memOff" \
        "han_crf" "IOBES" "adamw" "1e-3" "64" "20" "2" \
        "fixed" "true" "false" "true" \
        "token_doc_attn_gated" "8" "0.1" "true" \
        "4" "false" "128" "mixed"

# Run 2: minTokens=2, memory=off
run_one "p2_run2_han_IOBES_adamw_lr1e-3_minTokens2_memOff" \
        "han_crf" "IOBES" "adamw" "1e-3" "64" "20" "2" \
        "fixed" "true" "false" "true" \
        "token_doc_attn_gated" "8" "0.1" "true" \
        "2" "false" "128" "mixed"

# Run 3: minTokens=1, memory=off
run_one "p2_run3_han_IOBES_adamw_lr1e-3_minTokens1_memOff" \
        "han_crf" "IOBES" "adamw" "1e-3" "64" "20" "2" \
        "fixed" "true" "false" "true" \
        "token_doc_attn_gated" "8" "0.1" "true" \
        "1" "false" "128" "mixed"

# Run 4: minTokens=4, memory=on, packing=mixed
run_one "p2_run4_han_IOBES_adamw_lr1e-3_minTokens4_memOn_mixed" \
        "han_crf" "IOBES" "adamw" "1e-3" "64" "20" "2" \
        "fixed" "true" "false" "true" \
        "token_doc_attn_gated" "8" "0.1" "true" \
        "4" "true" "128" "mixed"

# Run 5: minTokens=2, memory=on, packing=mixed
run_one "p2_run5_han_IOBES_adamw_lr1e-3_minTokens2_memOn_mixed" \
        "han_crf" "IOBES" "adamw" "1e-3" "64" "20" "2" \
        "fixed" "true" "false" "true" \
        "token_doc_attn_gated" "8" "0.1" "true" \
        "2" "true" "128" "mixed"

# Run 6: minTokens=1, memory=on, packing=mixed
run_one "p2_run6_han_IOBES_adamw_lr1e-3_minTokens1_memOn_mixed" \
        "han_crf" "IOBES" "adamw" "1e-3" "64" "20" "2" \
        "fixed" "true" "false" "true" \
        "token_doc_attn_gated" "8" "0.1" "true" \
        "1" "true" "128" "mixed"

# Run 7: minTokens=2, memory=on, packing=strict_doc
run_one "p2_run7_han_IOBES_adamw_lr1e-3_minTokens2_memOn_strict" \
        "han_crf" "IOBES" "adamw" "1e-3" "64" "20" "2" \
        "fixed" "true" "false" "true" \
        "token_doc_attn_gated" "8" "0.1" "true" \
        "2" "true" "128" "strict_doc"

# Run 8: minTokens=1, memory=on, packing=strict_doc
run_one "p2_run8_han_IOBES_adamw_lr1e-3_minTokens1_memOn_strict" \
        "han_crf" "IOBES" "adamw" "1e-3" "64" "20" "2" \
        "fixed" "true" "false" "true" \
        "token_doc_attn_gated" "8" "0.1" "true" \
        "1" "true" "128" "strict_doc"

echo "Phase 2 experiment matrix completed."
