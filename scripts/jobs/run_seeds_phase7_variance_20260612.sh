#!/usr/bin/env bash
# Phase 7 — Multi-Seed Variance + Bootstrap CI for Main Comparisons (reviewer concern #6)
# The main comparison table reported "Experiment Runs = 1". This re-runs the main
# models across 5 seeds (mean ± SD) and dumps predictions per seed so bootstrap
# confidence intervals and paired significance tests can be computed.
#
# Models compared: BiLSTM-CRF (baseline) and HAN-CRF SOTA.
# Assumes preTrain artifacts already exist in interim_data/.
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_seeds_phase7_variance_20260612.sh
#   scripts/jobs/run_seeds_phase7_variance_20260612.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/12"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase7_variance_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,model,context_mode,seed,log_file,status"

SEEDS="${SEEDS:-13 42 101 202 777}"
EPOCHS="${EPOCHS:-20}"

mkdir -p "${LOG_DIR}" "${PRED_DIR}"
if [[ ! -f "${RUN_INDEX}" ]]; then
  echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
fi

run_one() {
  local config_id="$1"
  local model="$2"
  local context_mode="$3"
  local seed="$4"

  local log_file="${LOG_DIR}/${config_id}.txt"
  local pred_sub="${PRED_DIR}/${config_id}"
  local cmd=(
    conda run -n "${CONDA_ENV}" python src/nlp/jobs/gna_pipeline.py
    --device cuda
    --model "${model}"
    --taggingSchema IOBES
    --mode train,testGS
    --optimizer adamw
    --lr 1e-3
    --batchSize 64
    --epochs "${EPOCHS}"
    --positiveUpsample 2
    --hanBatchMode fixed
    --rebalancingMode auto
    --hanContextMode "${context_mode}"
    --hanContextHeads 8
    --hanContextDropout 0.1
    --hanUseBlockDiagonal
    --no-hanFreezeEmbeddings
    --bilstmFreezeEmbeddings
    --seed "${seed}"
    --dumpPredictions "${pred_sub}"
  )
  if [[ "${model}" == "han_crf" && "${context_mode}" == "token_doc_attn_gated" ]]; then
    cmd+=(--hanUseGatedFusion)
  else
    cmd+=(--no-hanUseGatedFusion)
  fi

  echo "Running ${config_id} (seed=${seed})"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${cmd[*]}" | tee "${log_file}"
    echo "${config_id},${model},${context_mode},${seed},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e
  local status="completed"; [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${model},${context_mode},${seed},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"
}

for seed in ${SEEDS}; do
  run_one "p7_bilstm_seed${seed}" "bilstm_crf" "sentence_only"        "${seed}"
  run_one "p7_han_seed${seed}"    "han_crf"    "token_doc_attn_gated" "${seed}"
done

echo ""
echo "Phase 7 variance runs complete. Run index: ${RUN_INDEX}"
echo "Example paired significance (seed 42 BiLSTM vs HAN, GS91):"
echo "  conda run -n ${CONDA_ENV} python -m src.nlp.evaluation.bootstrap_ci paired \\"
echo "    --predictions_a ${PRED_DIR}/p7_han_seed42/predictions_testgs91.json \\"
echo "    --predictions_b ${PRED_DIR}/p7_bilstm_seed42/predictions_testgs91.json --iters 2000"
