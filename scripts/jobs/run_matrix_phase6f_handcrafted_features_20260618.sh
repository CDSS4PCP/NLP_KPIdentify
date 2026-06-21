#!/usr/bin/env bash
# Phase 6e GROUP 4 — hand-crafted feature ablation at f=0.10 (2026-06-18)
#
# Question: which hand-crafted feature (CEM/WFOF/POS/LEN/TI/TR) is responsible
# for the surprisingly high performance at the 0.10 train ratio?
#
# How features are consumed (verified in gna_experiment._build_batch / feature
# generator, lines ~1124-1210):
#   POS  -> categorical token feature -> feats_pos (nltk POS tag id)
#   LEN  -> token length            -> feats_cont[0]
#   WFOF -> word first-occurrence    -> feats_cont[1]
#   TI   -> tf-idf                   -> feats_cont[2]
#   TR   -> textrank                 -> feats_cont[3]
#   CEM  -> NOT consumed anywhere (no-op; present only in the default list)
# When a feature name is absent from --features, its value is zeroed (tensor
# shape unchanged), so the feature is neutralized without changing the model.
# The same --features set is applied to train/test/testGS for consistency.
#
# Design: hold the representation config FIXED at the baseline
#   (trainable embeddings + Word2Vec + BiLM), f=0.10, 20 epochs, seed 42,
# and vary ONLY --features:
#   - ALL   (baseline = p6e_base_f010 from Phase 6e; not re-run here)
#   - NONE  (no hand-crafted features: word embeddings + BiLM only)
#   - leave-one-out (LOO): drop exactly one of POS/LEN/WFOF/TI/TR
#   - single: enable exactly one of POS/LEN/WFOF/TI/TR
# Each run reports synthetic held-out TEST + GS42 + GS91 F1 (--mode train,test,testGS).
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase6f_handcrafted_features_20260618.sh
#   scripts/jobs/run_matrix_phase6f_handcrafted_features_20260618.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/18"
RUN_INDEX="${LOG_DIR}/phase6f_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,train_fraction,features,epochs,mode,seed,log_file,status"

SEED="${SEED:-42}"
EPOCHS="${EPOCHS:-20}"
FRACTION="0.10"

JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_synthetic_labels_v2"
BACKUP_DIR="${JSON_DIR}/_phase6f_backup"

mkdir -p "${LOG_DIR}"
if [[ ! -f "${RUN_INDEX}" ]]; then
  echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
fi

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

# run_one <config_id> <features_space_separated>
run_one() {
  local config_id="$1"
  local features_str="$2"
  local mode="train,test,testGS"

  local log_file="${LOG_DIR}/${config_id}.txt"
  local resplit_cmd=(
    conda run -n "${CONDA_ENV}" python scripts/jobs/resplit_existing_dataset.py
    --trainFraction "${FRACTION}"
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
    --no-useRandomEmbeddings
    --useBiLM
    --bilstmFreezeEmbeddings
    --seed "${SEED}"
    --features
  )
  # shellcheck disable=SC2206
  local feats_arr=( ${features_str} )
  cmd+=( "${feats_arr[@]}" )

  echo "Running ${config_id} (f=${FRACTION}, features=[${features_str}], epochs=${EPOCHS}, mode=${mode})"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${cmd[*]}" | tee "${log_file}"
    echo "${config_id},${FRACTION},${features_str// /+},${EPOCHS},${mode},${SEED},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${resplit_cmd[@]}" ) 2>&1 | tee "${log_file}"
  local resplit_code=${PIPESTATUS[0]}
  if [[ ${resplit_code} -ne 0 ]]; then
    set -e
    echo "${config_id},${FRACTION},${features_str// /+},${EPOCHS},${mode},${SEED},$(basename "${log_file}"),resplit_failed" >> "${RUN_INDEX}"
    echo "Re-split failed for ${config_id}; skipping run."
    return
  fi
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee -a "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e
  local status="completed"; [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${FRACTION},${features_str// /+},${EPOCHS},${mode},${SEED},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"
}

# NONE: no hand-crafted features consumed (NONE is an unrecognized name => all zeroed)
run_one "p6f_feat_none"    "NONE"

# Leave-one-out (drop exactly one real feature; CEM kept as harmless no-op filler)
run_one "p6f_feat_noPOS"   "CEM WFOF LEN TI TR"
run_one "p6f_feat_noWFOF"  "CEM POS LEN TI TR"
run_one "p6f_feat_noLEN"   "CEM WFOF POS TI TR"
run_one "p6f_feat_noTI"    "CEM WFOF POS LEN TR"
run_one "p6f_feat_noTR"    "CEM WFOF POS LEN TI"

# Single-feature (enable exactly one real feature)
run_one "p6f_feat_onlyPOS"  "POS"
run_one "p6f_feat_onlyLEN"  "LEN"
run_one "p6f_feat_onlyWFOF" "WFOF"
run_one "p6f_feat_onlyTI"   "TI"
run_one "p6f_feat_onlyTR"   "TR"

echo ""
echo "Phase 6e Group 4 (hand-crafted feature ablation @ f=0.10) complete. Run index: ${RUN_INDEX}"
echo "Baseline ALL-features reference = p6e_base_f010 (Phase 6e): TEST 65.60 / GS42 40.80 / GS91 54.66"
