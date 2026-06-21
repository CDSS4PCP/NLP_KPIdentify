#!/usr/bin/env bash
# Phase 6c — BiLM-contribution controls for the split-sensitivity study (2026-06-18)
#
# Two follow-up controls to interpret why the low-data (f=0.10) GS floor is high
# in Phase 6/6b (see SUMMARY_phase6b_split_sensitivity.md):
#
#   A) UNTRAINED BASELINE at f=0.10 — same pretrained LM (Word2Vec + BiLM
#      transferred) but ZERO supervised epochs / random CRF head. Establishes the
#      true no-training floor (expected ~0-7 GS F1, cf. Phase 8 random-head).
#      Implemented via gna_pipeline `--epochs 0` (saves the randomly-initialized
#      model and skips training; see gna_experiment.train epochs<=0 guard).
#
#   B) NO-BiLM SWEEP over the full fraction grid 0.10, 0.25, 0.33, 0.50, 0.70,
#      0.75, 0.80, 1.00 — identical to Phase 6b but with `--no-useBiLM` so the
#      BiLM pretraining transfer is removed (Word2Vec embeddings retained). This
#      isolates the BiLM contribution as a function of supervised-data quantity:
#      we expect a large low-data gap vs. the with-BiLM curve that shrinks as
#      data grows.
#
# Design (identical mechanics to Phase 6b):
#   1. back up canonical train.json/test.json,
#   2. re-split the combined labeled corpus at the target fraction,
#   3. run `train,testGS` (fixed vocab/W2V; BiLM toggled per --useBiLM),
#   4. restore canonical files (always, via EXIT trap).
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase6c_nobilm_and_untrained_20260618.sh
#   scripts/jobs/run_matrix_phase6c_nobilm_and_untrained_20260618.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/18"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase6c_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,train_fraction,bilm,epochs,seed,log_file,status"

SEED="${SEED:-42}"
EPOCHS="${EPOCHS:-20}"

JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_synthetic_labels_v2"
BACKUP_DIR="${JSON_DIR}/_phase6c_backup"

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

# run_one <config_id> <train_fraction> <use_bilm:true|false> <epochs>
run_one() {
  local config_id="$1"
  local train_fraction="$2"
  local use_bilm="$3"
  local epochs="$4"

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
    --epochs "${epochs}"
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
  if [[ "${use_bilm}" == "true" ]]; then cmd+=(--useBiLM); else cmd+=(--no-useBiLM); fi

  echo "Running ${config_id} (trainFraction=${train_fraction}, bilm=${use_bilm}, epochs=${epochs})"
  echo "Re-split: ${resplit_cmd[*]}"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${resplit_cmd[*]}" | tee "${log_file}"
    echo "[DRY_RUN] ${cmd[*]}" | tee -a "${log_file}"
    echo "${config_id},${train_fraction},${use_bilm},${epochs},${SEED},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${resplit_cmd[@]}" ) 2>&1 | tee "${log_file}"
  local resplit_code=${PIPESTATUS[0]}
  if [[ ${resplit_code} -ne 0 ]]; then
    set -e
    echo "${config_id},${train_fraction},${use_bilm},${epochs},${SEED},$(basename "${log_file}"),resplit_failed" >> "${RUN_INDEX}"
    echo "Re-split failed for ${config_id}; skipping run."
    return
  fi
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee -a "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e
  local status="completed"; [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${train_fraction},${use_bilm},${epochs},${SEED},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"
}

# --- Control A: untrained baseline at f=0.10 (with BiLM, 0 supervised epochs) ---
run_one "p6c_untrained_f010_bilm" "0.10" "true" "0"

# --- Control B: no-BiLM sweep over the full fraction grid (20 epochs) ----------
run_one "p6c_nobilm_010" "0.10" "false" "${EPOCHS}"
run_one "p6c_nobilm_025" "0.25" "false" "${EPOCHS}"
run_one "p6c_nobilm_033" "0.33" "false" "${EPOCHS}"
run_one "p6c_nobilm_050" "0.50" "false" "${EPOCHS}"
run_one "p6c_nobilm_070" "0.70" "false" "${EPOCHS}"
run_one "p6c_nobilm_075" "0.75" "false" "${EPOCHS}"
run_one "p6c_nobilm_080" "0.80" "false" "${EPOCHS}"
run_one "p6c_nobilm_100" "1.00" "false" "${EPOCHS}"

echo ""
echo "Phase 6c (untrained baseline + no-BiLM sweep) complete. Run index: ${RUN_INDEX}"
