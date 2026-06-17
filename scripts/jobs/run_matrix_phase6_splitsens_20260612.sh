#!/usr/bin/env bash
# Phase 6 — Train/Validation Split Sensitivity (reviewer concern #5)
# The paper used a synthetic train/test split; this sweeps the train fraction to
# test sensitivity: 0.33 (≈ original 1:2), 0.70, 0.80.
#
# IMPLEMENTATION NOTE:
#   The canonical `createData` mode re-runs the sciSpacy synthetic-keyword NER
#   model, whose static vectors are broken in this environment (spaCy E896:
#   "blis.gemm shape mismatch (N, 0)"). Because the synthetic labels already
#   exist in train.json + test.json, split sensitivity does NOT need re-labeling
#   — it only needs to re-partition the existing labeled corpus at each fraction.
#   We therefore:
#     1. back up the canonical train.json/test.json,
#     2. re-split the combined labeled corpus at the target fraction
#        (scripts/jobs/resplit_existing_dataset.py — mirrors dataset.py logic),
#     3. run only `train,testGS` (reusing the FIXED pretrained vocab/W2V/BiLM so
#        the LM is held constant and we isolate the supervised-data quantity),
#     4. restore the canonical files (always, via EXIT trap).
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase6_splitsens_20260612.sh
#   scripts/jobs/run_matrix_phase6_splitsens_20260612.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/12"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase6_splitsens_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,train_fraction,seed,log_file,status"

SEED="${SEED:-42}"
EPOCHS="${EPOCHS:-20}"

JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_synthetic_labels_v2"
BACKUP_DIR="${JSON_DIR}/_phase6_backup"

mkdir -p "${LOG_DIR}" "${PRED_DIR}"
if [[ ! -f "${RUN_INDEX}" ]]; then
  echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
fi

# --- Backup canonical split and guarantee restore on any exit ---------------
backup_split() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then return; fi
  mkdir -p "${BACKUP_DIR}"
  cp -f "${JSON_DIR}/train.json" "${BACKUP_DIR}/train.json"
  cp -f "${JSON_DIR}/test.json"  "${BACKUP_DIR}/test.json"
}

restore_split() {
  if [[ -f "${BACKUP_DIR}/train.json" ]]; then
    cp -f "${BACKUP_DIR}/train.json" "${JSON_DIR}/train.json"
    cp -f "${BACKUP_DIR}/test.json"  "${JSON_DIR}/test.json"
    echo "Restored canonical train.json/test.json from backup."
  fi
}
trap restore_split EXIT

backup_split

run_one() {
  local config_id="$1"
  local train_fraction="$2"

  local log_file="${LOG_DIR}/${config_id}.txt"
  local resplit_cmd=(
    conda run -n "${CONDA_ENV}" python scripts/jobs/resplit_existing_dataset.py
    --trainFraction "${train_fraction}"
    --seed "${SEED}"
  )
  local cmd=(
    conda run -n "${CONDA_ENV}" python src/nlp/jobs/gna_pipeline.py
    --device cuda
    --model han_crf
    --taggingSchema IOBES
    --mode train,testGS
    --optimizer adamw
    --lr 1e-3
    --batchSize 64
    --epochs "${EPOCHS}"
    --positiveUpsample 2
    --hanBatchMode fixed
    --rebalancingMode auto
    --hanContextMode token_doc_attn_gated
    --hanContextHeads 8
    --hanContextDropout 0.1
    --hanUseBlockDiagonal
    --hanUseGatedFusion
    --no-hanFreezeEmbeddings
    --bilstmFreezeEmbeddings
    --seed "${SEED}"
    --dumpPredictions "${PRED_DIR}/${config_id}"
  )

  echo "Running ${config_id} (trainFraction=${train_fraction})"
  echo "Re-split: ${resplit_cmd[*]}"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${resplit_cmd[*]}" | tee "${log_file}"
    echo "[DRY_RUN] ${cmd[*]}" | tee -a "${log_file}"
    echo "${config_id},${train_fraction},${SEED},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${resplit_cmd[@]}" ) 2>&1 | tee "${log_file}"
  local resplit_code=${PIPESTATUS[0]}
  if [[ ${resplit_code} -ne 0 ]]; then
    set -e
    echo "${config_id},${train_fraction},${SEED},$(basename "${log_file}"),resplit_failed" >> "${RUN_INDEX}"
    echo "Re-split failed for ${config_id}; skipping run."
    return
  fi
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee -a "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e
  local status="completed"; [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${train_fraction},${SEED},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"
}

run_one "p6_split_033" "0.33"   # ≈ original 1:2 ratio
run_one "p6_split_070" "0.70"   # 70:30
run_one "p6_split_080" "0.80"   # 80:20

echo ""
echo "Phase 6 split sensitivity complete. Run index: ${RUN_INDEX}"
