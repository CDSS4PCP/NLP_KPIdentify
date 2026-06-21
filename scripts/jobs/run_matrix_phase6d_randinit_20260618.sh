#!/usr/bin/env bash
# Phase 6d — fully-random-init sweep for the split-sensitivity study (2026-06-18)
#
# Motivation: Phase 6c showed that removing BiLM (--no-useBiLM, Word2Vec retained)
# barely changes GS F1 across the fraction grid (deltas within +-2.4 F1, sign
# flips), so BiLM is NOT the source of the high low-data floor. The untested
# lever is the pre-trained Word2Vec embeddings themselves. This sweep removes ALL
# pretraining transfer:
#
#   --useRandomEmbeddings : random word-embedding init (skip LM_word2vec.bin)
#   --no-useBiLM          : skip BiLM weight transfer (random LSTM init)
#
# Expectation: with no pretrained representations, low-data fractions should
# collapse sharply and the curve should vary strongly with supervised-data
# quantity — the "clearly varying results" demonstration. Compare against the
# with-BiLM (Phase 6/6b) and no-BiLM (Phase 6c) curves.
#
# Design (identical mechanics to Phase 6b/6c):
#   1. back up canonical train.json/test.json,
#   2. re-split the combined labeled corpus at the target fraction,
#   3. run `train,testGS` (random embeddings + random LSTM init),
#   4. restore canonical files (always, via EXIT trap).
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase6d_randinit_20260618.sh
#   scripts/jobs/run_matrix_phase6d_randinit_20260618.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/18"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase6d_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,train_fraction,randinit,bilm,epochs,seed,log_file,status"

SEED="${SEED:-42}"
EPOCHS="${EPOCHS:-20}"

JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_synthetic_labels_v2"
BACKUP_DIR="${JSON_DIR}/_phase6d_backup"

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

# run_one <config_id> <train_fraction> <epochs>
run_one() {
  local config_id="$1"
  local train_fraction="$2"
  local epochs="$3"

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
    --useRandomEmbeddings
    --no-useBiLM
    --seed "${SEED}"
    --dumpPredictions "${PRED_DIR}/${config_id}"
  )

  echo "Running ${config_id} (trainFraction=${train_fraction}, randinit=true, bilm=false, epochs=${epochs})"
  echo "Re-split: ${resplit_cmd[*]}"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${resplit_cmd[*]}" | tee "${log_file}"
    echo "[DRY_RUN] ${cmd[*]}" | tee -a "${log_file}"
    echo "${config_id},${train_fraction},true,false,${epochs},${SEED},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${resplit_cmd[@]}" ) 2>&1 | tee "${log_file}"
  local resplit_code=${PIPESTATUS[0]}
  if [[ ${resplit_code} -ne 0 ]]; then
    set -e
    echo "${config_id},${train_fraction},true,false,${epochs},${SEED},$(basename "${log_file}"),resplit_failed" >> "${RUN_INDEX}"
    echo "Re-split failed for ${config_id}; skipping run."
    return
  fi
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee -a "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e
  local status="completed"; [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${train_fraction},true,false,${epochs},${SEED},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"
}

# --- Fully-random-init sweep over the full fraction grid (20 epochs) ----------
run_one "p6d_randinit_010" "0.10" "${EPOCHS}"
run_one "p6d_randinit_025" "0.25" "${EPOCHS}"
run_one "p6d_randinit_033" "0.33" "${EPOCHS}"
run_one "p6d_randinit_050" "0.50" "${EPOCHS}"
run_one "p6d_randinit_070" "0.70" "${EPOCHS}"
run_one "p6d_randinit_075" "0.75" "${EPOCHS}"
run_one "p6d_randinit_080" "0.80" "${EPOCHS}"
run_one "p6d_randinit_100" "1.00" "${EPOCHS}"

echo ""
echo "Phase 6d (fully-random-init sweep) complete. Run index: ${RUN_INDEX}"
