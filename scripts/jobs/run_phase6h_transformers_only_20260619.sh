#!/usr/bin/env bash
# Phase 6H — transformers-only finish (2026-06-19).
# The HAN gated-BIO test repeatedly crashed the GPU (excessive load on 73,810-doc HAN
# attention inference), so it is SKIPPED per user request. This runs only the transformer
# family on the existing PubMedAKE 0.10 split, then restores the original split.
#
# Prereq state (verified): pubmedake split = 8201 train / 73810 test; backup in _phase6h_backup.
set -uo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/18/phase6h"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase6h_run_index.csv"
CONDA_ENV="${CONDA_ENV:-cdss-gpu}"
DEVICE="${DEVICE:-cuda}"

DS="pubmedake"
JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_${DS}"
BACKUP_DIR="${JSON_DIR}/_phase6h_backup"

SEED="${SEED:-42}"
TF_EPOCHS="${TF_EPOCHS:-3}"
TF_BATCH="${TF_BATCH:-16}"
TF_LR="${TF_LR:-3e-5}"
TF_MAXLEN="${TF_MAXLEN:-256}"
TFS="${TFS:-biobert pubmedbert scibert}"

mkdir -p "${LOG_DIR}" "${PRED_DIR}"

restore_split() {
  if [[ -f "${BACKUP_DIR}/train.json" ]]; then
    cp -f "${BACKUP_DIR}/train.json" "${JSON_DIR}/train.json"
    cp -f "${BACKUP_DIR}/test.json"  "${JSON_DIR}/test.json"
    echo "Restored original PubMedAKE train.json/test.json from backup."
  fi
}
trap restore_split EXIT

record() {
  local family="$1" model="$2" log="$3" status="$4"
  echo "phase6h,${family},${model},n/a,n/a,0.10,${SEED},train,test,$(basename "${log}"),${status}" >> "${RUN_INDEX}"
}

cd "${ROOT_DIR}"

TRAIN_N=$(python -c "import json;print(len(json.load(open('${JSON_DIR}/train.json'))))")
echo "PubMedAKE split: train=${TRAIN_N} (expect 8201)."
if [[ "${TRAIN_N}" != "8201" ]]; then
  echo "ERROR: train.json is not the 0.10 re-split (${TRAIN_N} != 8201). Aborting."
  exit 1
fi

for tf in ${TFS}; do
  config_id="transformer_${tf}"
  log_file="${LOG_DIR}/p6h_${config_id}.txt"
  echo "----- Transformer ${tf} on ${DS} (train,test) -----"
  set +e
  conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/transformer_pipeline.py \
    --hfModel "${tf}" --mode train,test \
    --dataSource "${DS}" --jsonDataDir "${JSON_DIR}" \
    --device "${DEVICE}" \
    --epochs "${TF_EPOCHS}" --batchSize "${TF_BATCH}" --lr "${TF_LR}" --maxLength "${TF_MAXLEN}" \
    --seed "${SEED}" --dumpPredictions "${PRED_DIR}/${config_id}" \
    2>&1 | tee "${log_file}"
  ec=${PIPESTATUS[0]}
  set -e 2>/dev/null || true
  st="completed"; [[ ${ec} -ne 0 ]] && st="failed"
  record transformer "${tf}" "${log_file}" "${st}"
  echo "Transformer ${tf} -> ${st}"
done

echo ""
echo "Phase 6H transformers-only finish complete (gated BIO test skipped). Run index: ${RUN_INDEX}"
