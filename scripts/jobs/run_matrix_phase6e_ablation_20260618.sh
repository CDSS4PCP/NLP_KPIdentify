#!/usr/bin/env bash
# Phase 6e — consolidated ablation: trust validation + feature attribution + frozen-embedding pretraining lever (2026-06-18)
#
# Addresses three questions:
#   (C) TRUST: For fractions 0.10..0.80 (1.00 excluded, no remaining data),
#       evaluate the trained model on the held-out *synthetic* test.json (the
#       portion NOT used for training) IN ADDITION to GS42/GS91. A coin-flip /
#       random model scores ~0 entity-F1 (cf. untrained baseline), so a clear
#       synthetic-test learning curve proves the model is really learning.
#   (B) FEATURE ATTRIBUTION at f=0.10: full factorial over
#       {trainable|frozen embeddings} x {Word2Vec|random init} x {BiLM|no-BiLM}
#       plus an untrained (epochs=0) floor. Isolates which feature drives the
#       ~50% GS F1 at minimal training.
#   (A) PRETRAINING LEVER: with FROZEN embeddings, sweep Word2Vec+BiLM vs
#       fully-random across fractions 0.10..1.00 to show the pretraining gap as
#       a function of supervised-data quantity (the gap should be visible only
#       when embeddings cannot be fine-tuned).
#
# Every run uses `--mode train,test,testGS`, so each log contains 3 Score lines:
#   1) EVALUATION SUMMARY ON TEST            (held-out synthetic remainder)
#   2) EVALUATION SUMMARY ON GOLD STANDARD 42
#   3) EVALUATION SUMMARY ON GOLD STANDARD 91
# (f=1.00 runs use `train,testGS` only, since the synthetic remainder is empty.)
#
# Mechanics identical to Phase 6b/6c/6d: backup canonical split, external
# re-split at the target fraction, run, restore canonical files via EXIT trap.
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase6e_ablation_20260618.sh
#   scripts/jobs/run_matrix_phase6e_ablation_20260618.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/18"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase6e_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,train_fraction,freeze_emb,random_emb,bilm,epochs,mode,seed,log_file,status"

SEED="${SEED:-42}"
EPOCHS="${EPOCHS:-20}"

JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_synthetic_labels_v2"
BACKUP_DIR="${JSON_DIR}/_phase6e_backup"

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

# run_one <config_id> <train_fraction> <freeze:true|false> <random_emb:true|false> <bilm:true|false> <epochs> <mode>
run_one() {
  local config_id="$1"
  local train_fraction="$2"
  local freeze_emb="$3"
  local random_emb="$4"
  local use_bilm="$5"
  local epochs="$6"
  local mode="${7:-train,test,testGS}"

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
    --mode "${mode}"
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
    --bilstmFreezeEmbeddings
    --seed "${SEED}"
    --dumpPredictions "${PRED_DIR}/${config_id}"
  )
  if [[ "${freeze_emb}" == "true" ]]; then cmd+=(--hanFreezeEmbeddings); else cmd+=(--no-hanFreezeEmbeddings); fi
  if [[ "${random_emb}" == "true" ]]; then cmd+=(--useRandomEmbeddings); else cmd+=(--no-useRandomEmbeddings); fi
  if [[ "${use_bilm}" == "true" ]]; then cmd+=(--useBiLM); else cmd+=(--no-useBiLM); fi

  echo "Running ${config_id} (f=${train_fraction}, freeze=${freeze_emb}, random=${random_emb}, bilm=${use_bilm}, epochs=${epochs}, mode=${mode})"
  echo "Re-split: ${resplit_cmd[*]}"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${resplit_cmd[*]}" | tee "${log_file}"
    echo "[DRY_RUN] ${cmd[*]}" | tee -a "${log_file}"
    echo "${config_id},${train_fraction},${freeze_emb},${random_emb},${use_bilm},${epochs},${mode},${SEED},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${resplit_cmd[@]}" ) 2>&1 | tee "${log_file}"
  local resplit_code=${PIPESTATUS[0]}
  if [[ ${resplit_code} -ne 0 ]]; then
    set -e
    echo "${config_id},${train_fraction},${freeze_emb},${random_emb},${use_bilm},${epochs},${mode},${SEED},$(basename "${log_file}"),resplit_failed" >> "${RUN_INDEX}"
    echo "Re-split failed for ${config_id}; skipping run."
    return
  fi
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee -a "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e
  local status="completed"; [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${train_fraction},${freeze_emb},${random_emb},${use_bilm},${epochs},${mode},${SEED},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"
}

# =========================================================================
# GROUP 1 — TRUST VALIDATION (Part C): baseline config (trainable + W2V + BiLM)
#   across fractions 0.10..0.80, evaluating held-out synthetic test + GS.
# =========================================================================
run_one "p6e_base_f010" "0.10" "false" "false" "true" "${EPOCHS}"
run_one "p6e_base_f025" "0.25" "false" "false" "true" "${EPOCHS}"
run_one "p6e_base_f033" "0.33" "false" "false" "true" "${EPOCHS}"
run_one "p6e_base_f050" "0.50" "false" "false" "true" "${EPOCHS}"
run_one "p6e_base_f070" "0.70" "false" "false" "true" "${EPOCHS}"
run_one "p6e_base_f075" "0.75" "false" "false" "true" "${EPOCHS}"
run_one "p6e_base_f080" "0.80" "false" "false" "true" "${EPOCHS}"

# =========================================================================
# GROUP 2 — FEATURE FACTORIAL at f=0.10 (Part B)
#   base (trainable+W2V+BiLM) = p6e_base_f010 above. Remaining cells:
# =========================================================================
run_one "p6e_f010_untrained"          "0.10" "false" "false" "true"  "0"           # epochs=0 floor
run_one "p6e_f010_train_w2v_nobilm"   "0.10" "false" "false" "false" "${EPOCHS}"
run_one "p6e_f010_train_rand_nobilm"  "0.10" "false" "true"  "false" "${EPOCHS}"
run_one "p6e_f010_frozen_w2v_bilm"    "0.10" "true"  "false" "true"  "${EPOCHS}"
run_one "p6e_f010_frozen_w2v_nobilm"  "0.10" "true"  "false" "false" "${EPOCHS}"
run_one "p6e_f010_frozen_rand_bilm"   "0.10" "true"  "true"  "true"  "${EPOCHS}"
run_one "p6e_f010_frozen_rand_nobilm" "0.10" "true"  "true"  "false" "${EPOCHS}"

# =========================================================================
# GROUP 3 — FROZEN-EMBEDDING PRETRAINING LEVER (Part A)
#   frozen+W2V+BiLM vs frozen+random-noBiLM across fractions.
#   f=0.10 points reuse p6e_f010_frozen_w2v_bilm / p6e_f010_frozen_rand_nobilm.
# =========================================================================
# frozen + Word2Vec + BiLM
run_one "p6e_frozenW2V_f025"  "0.25" "true" "false" "true" "${EPOCHS}"
run_one "p6e_frozenW2V_f050"  "0.50" "true" "false" "true" "${EPOCHS}"
run_one "p6e_frozenW2V_f075"  "0.75" "true" "false" "true" "${EPOCHS}"
run_one "p6e_frozenW2V_f100"  "1.00" "true" "false" "true" "${EPOCHS}" "train,testGS"
# frozen + random + no-BiLM (no pretraining, frozen)
run_one "p6e_frozenRand_f025" "0.25" "true" "true" "false" "${EPOCHS}"
run_one "p6e_frozenRand_f050" "0.50" "true" "true" "false" "${EPOCHS}"
run_one "p6e_frozenRand_f075" "0.75" "true" "true" "false" "${EPOCHS}"
run_one "p6e_frozenRand_f100" "1.00" "true" "true" "false" "${EPOCHS}" "train,testGS"

echo ""
echo "Phase 6e (trust + feature ablation + frozen pretraining lever) complete. Run index: ${RUN_INDEX}"
