#!/usr/bin/env bash
# Phase 6H RESUME (2026-06-19) after a mid-run PC crash.
#
# State at crash (verified): pubmedake split still re-split (8201 train / 73810 test);
# 9 runs recorded (bilstm x3, han_sentence x3, han_token_doc x3); han_token_doc_attn_gated
# BIO finished TRAINING (interim_data/HAN-CRF_BIO.pt saved at 14:11) but crashed during its
# TEST evaluation; gated IOBES/BILOU never ran. preTrain artifacts (vocab/W2V/BiLM) intact.
#
# This script (per user request):
#   1) resumes the TEST evaluation of han_token_doc_attn_gated BIO by reloading the saved
#      checkpoint (--mode test, same architecture flags),
#   2) runs the transformer family BioBERT, PubMedBERT, SciBERT (--mode train,test),
#   3) SKIPS gated IOBES and gated BILOU,
#   4) restores the original pubmedake split from backup on exit.
#
# Does NOT re-split or re-preTrain (already done). Sequential only (single 8GB GPU).
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
BATCH_SIZE="${BATCH_SIZE:-64}"
LR="${LR:-1e-3}"
TF_EPOCHS="${TF_EPOCHS:-3}"
TF_BATCH="${TF_BATCH:-16}"
TF_LR="${TF_LR:-3e-5}"
TF_MAXLEN="${TF_MAXLEN:-256}"

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
  local family="$1" model="$2" context="$3" schema="$4" log="$5" status="$6" mode="$7"
  echo "phase6h,${family},${model},${context},${schema},0.10,${SEED},${mode},$(basename "${log}"),${status}" >> "${RUN_INDEX}"
}

cd "${ROOT_DIR}"

# Sanity: split must still be the 0.10 re-split so the saved checkpoint matches.
TRAIN_N=$(python -c "import json;print(len(json.load(open('${JSON_DIR}/train.json'))))")
TEST_N=$(python -c "import json;print(len(json.load(open('${JSON_DIR}/test.json'))))")
echo "PubMedAKE split: train=${TRAIN_N} test=${TEST_N} (expect 8201/73810)."
if [[ "${TRAIN_N}" != "8201" ]]; then
  echo "ERROR: train.json is not the 0.10 re-split (${TRAIN_N} != 8201). Aborting to avoid checkpoint mismatch."
  exit 1
fi

# --- 1) Resume gated-BIO TEST eval (reload interim_data/HAN-CRF_BIO.pt) --------
GATED_LOG="${LOG_DIR}/p6h_han_token_doc_attn_gated_BIO.txt"
echo "----- RESUME: han_token_doc_attn_gated BIO (mode test) -----"
set +e
conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/gna_pipeline.py \
  --mode test \
  --model han_crf --taggingSchema BIO \
  --dataSource "${DS}" --jsonDataDir "${JSON_DIR}" \
  --device "${DEVICE}" \
  --hanContextMode token_doc_attn_gated --hanUseGatedFusion --hanContextHeads 8 \
  --hanBatchMode fixed --hanUseBlockDiagonal --bilstmFreezeEmbeddings \
  --seed "${SEED}" --dumpPredictions "${PRED_DIR}/han_token_doc_attn_gated_BIO" \
  2>&1 | tee -a "${GATED_LOG}"
ec=${PIPESTATUS[0]}
set -e 2>/dev/null || true
st="completed"; [[ ${ec} -ne 0 ]] && st="failed"
record gna han_crf token_doc_attn_gated BIO "${GATED_LOG}" "${st}" "test(resumed)"
echo "Gated BIO test -> ${st}"

# --- 2) Transformer family: BioBERT, PubMedBERT, SciBERT (train,test) ----------
for tf in biobert pubmedbert scibert; do
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
  record transformer "${tf}" n/a n/a "${log_file}" "${st}" "train,test"
  echo "Transformer ${tf} -> ${st}"
done

echo ""
echo "Phase 6H RESUME complete (gated BIO test + 3 transformers; skipped gated IOBES/BILOU)."
echo "Run index: ${RUN_INDEX}"
