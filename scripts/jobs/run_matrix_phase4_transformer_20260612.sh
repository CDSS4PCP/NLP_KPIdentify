#!/usr/bin/env bash
# Phase 4 — Biomedical Transformer Baselines (reviewer concern #1)
# Fine-tunes PubMedBERT / BioBERT / SciBERT token classifiers on the SAME synthetic
# train split and evaluates on GS42/GS91. Dumps predictions, then runs entity-level
# error analysis and bootstrap confidence intervals.
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase4_transformer_20260612.sh   # preview commands
#   scripts/jobs/run_matrix_phase4_transformer_20260612.sh             # execute
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/12"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase4_transformer_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,hf_model,epochs,batch_size,lr,max_length,seed,log_file,status"

EPOCHS="${EPOCHS:-3}"
BATCH_SIZE="${BATCH_SIZE:-16}"
LR="${LR:-3e-5}"
MAX_LEN="${MAX_LEN:-256}"
SEED="${SEED:-42}"

mkdir -p "${LOG_DIR}" "${PRED_DIR}"
if [[ ! -f "${RUN_INDEX}" ]]; then
  echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
fi

run_one() {
  local config_id="$1"
  local hf_model="$2"

  local log_file="${LOG_DIR}/${config_id}.txt"
  local pred_sub="${PRED_DIR}/${config_id}"
  local cmd=(
    conda run -n "${CONDA_ENV}" python src/nlp/jobs/transformer_pipeline.py
    --hfModel "${hf_model}"
    --mode train,testGS
    --device cuda
    --epochs "${EPOCHS}"
    --batchSize "${BATCH_SIZE}"
    --lr "${LR}"
    --maxLength "${MAX_LEN}"
    --seed "${SEED}"
    --dumpPredictions "${pred_sub}"
  )

  echo "Running ${config_id}"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${cmd[*]}" | tee "${log_file}"
    echo "${config_id},${hf_model},${EPOCHS},${BATCH_SIZE},${LR},${MAX_LEN},${SEED},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e

  local status="completed"
  [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${hf_model},${EPOCHS},${BATCH_SIZE},${LR},${MAX_LEN},${SEED},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"

  # Post-run analysis on dumped GS91 predictions (concerns #4 + #6).
  if [[ ${exit_code} -eq 0 ]]; then
    for gs in testgs42 testgs91; do
      local pred_json="${pred_sub}/predictions_${gs}.json"
      if [[ -f "${pred_json}" ]]; then
        ( cd "${ROOT_DIR}" && conda run -n "${CONDA_ENV}" python -m src.nlp.evaluation.error_analysis \
            --predictions "${pred_json}" \
            --output_report "${LOG_DIR}/error_analysis_${config_id}_${gs}.md" ) || true
        ( cd "${ROOT_DIR}" && conda run -n "${CONDA_ENV}" python -m src.nlp.evaluation.bootstrap_ci ci \
            --predictions "${pred_json}" --iters 2000 ) 2>&1 | tee -a "${log_file}" || true
      fi
    done
  fi
}

run_one "p4_pubmedbert" "pubmedbert"
run_one "p4_biobert"    "biobert"
run_one "p4_scibert"    "scibert"

echo ""
echo "Phase 4 transformer baselines complete. Run index: ${RUN_INDEX}"
