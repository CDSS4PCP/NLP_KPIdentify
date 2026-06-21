#!/usr/bin/env bash
# Phase 6H — model-switch comparison on the PUBLIC PubMedAKE corpus at train fraction 0.10.
#
# Question (user): "I believe the synthetic dataset has something to do with the constant
# performance." Training on the public KPBioMed/PubMedAKE corpora gave much lower GS F1
# (cross-domain). 6H isolates the dataset effect by training on PubMedAKE itself and
# testing IN-DOMAIN on the remainder — NO synthetic data, NO Gold-Standard sets — to find
# which architecture is genuinely dominant on a real public keyphrase corpus.
#
# Models (same 7 as Phase 6G):
#   Native BiLSTM-CRF, HAN-CRF(sentence_only), HAN-CRF(token_doc_attn),
#   HAN-CRF(token_doc_attn_gated)  — each in {BIO, IOBES, BILOU} —
#   + transformers BioBERT, PubMedBERT, SciBERT.
# All: 20 epochs, trainFraction 0.10, --mode train,test (in-domain TEST = the 0.90
# remainder). PubMedAKE total ≈ 82,011 docs => 0.10 split ≈ 8,201 train / 73,810 test.
#
# Per-experiment design (per user): DO NOT use synthetic or GS data here. Word2Vec/BiLM
# are pretrained ONLY on the 0.10 train split (strict low-resource), so this run is
# self-contained on PubMedAKE.
#
# IMPORTANT (interim_data is shared, NOT namespaced per dataset): this script's preTrain
# OVERWRITES the synthetic vocab/Word2Vec/BiLM in interim_data/. Run Phase 6G FIRST.
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase6h_pubmedake_modelswitch_20260618.sh
#   scripts/jobs/run_matrix_phase6h_pubmedake_modelswitch_20260618.sh
#   SCHEMAS="BIO" TRAIN_SAMPLE_SIZE=4000 scripts/jobs/run_matrix_phase6h_pubmedake_modelswitch_20260618.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/18/phase6h"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase6h_run_index.csv"
CONDA_ENV="${CONDA_ENV:-cdss-gpu}"
DEVICE="${DEVICE:-cuda}"
RUN_INDEX_HEADER="experiment,family,model,context,schema,train_fraction,seed,mode,log_file,status"

DS="pubmedake"
JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_${DS}"

SEED="${SEED:-42}"
EPOCHS="${EPOCHS:-20}"
TRAIN_FRACTION="${TRAIN_FRACTION:-0.10}"
SCHEMAS="${SCHEMAS:-BIO IOBES BILOU}"

# GNA hyper-params (identical to Phase 6G for cross-experiment comparability).
BATCH_SIZE="${BATCH_SIZE:-64}"
LR="${LR:-1e-3}"
# Optional supervised-train cap (empty = use the full 0.10 split, ≈8,201 docs).
# Set e.g. TRAIN_SAMPLE_SIZE=4000 to bound runtime (changes the effective ratio).
TRAIN_SAMPLE_SIZE="${TRAIN_SAMPLE_SIZE:-}"

# preTrain on the 0.10 split only. >8201 => uses the whole split.
PRETRAIN_EPOCHS="${PRETRAIN_EPOCHS:-5}"
PRETRAIN_SAMPLE_SIZE="${PRETRAIN_SAMPLE_SIZE:-10000}"
W2V_MIN_COUNT="${W2V_MIN_COUNT:-5}"

# Transformer hyper-params.
TF_EPOCHS="${TF_EPOCHS:-3}"
TF_BATCH="${TF_BATCH:-16}"
TF_LR="${TF_LR:-3e-5}"
TF_MAXLEN="${TF_MAXLEN:-256}"

BACKUP_DIR="${JSON_DIR}/_phase6h_backup"

mkdir -p "${LOG_DIR}" "${PRED_DIR}"
[[ -f "${RUN_INDEX}" ]] || echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"

# --- Backup PubMedAKE split and guarantee restore on any exit ----------------
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
    echo "Restored original PubMedAKE train.json/test.json from backup."
  fi
}
trap restore_split EXIT

record() {
  local family="$1" model="$2" context="$3" schema="$4" log="$5" status="$6" mode="$7"
  if [[ "${DRY_RUN:-0}" != "1" ]]; then
    echo "phase6h,${family},${model},${context},${schema},${TRAIN_FRACTION},${SEED},${mode},$(basename "${log}"),${status}" >> "${RUN_INDEX}"
  fi
}

cd "${ROOT_DIR}"
backup_split

# --- Re-split PubMedAKE once at f=TRAIN_FRACTION (combine existing train+test) -
echo "Re-splitting PubMedAKE at f=${TRAIN_FRACTION} (seed ${SEED})."
if [[ "${DRY_RUN:-0}" == "1" ]]; then
  echo "+ conda run -n ${CONDA_ENV} python scripts/jobs/resplit_existing_dataset.py --jsonDir ${JSON_DIR} --trainFraction ${TRAIN_FRACTION} --seed ${SEED}"
else
  conda run --no-capture-output -n "${CONDA_ENV}" python -u scripts/jobs/resplit_existing_dataset.py \
    --jsonDir "${JSON_DIR}" --trainFraction "${TRAIN_FRACTION}" --seed "${SEED}" 2>&1 | tee "${LOG_DIR}/p6h_resplit.txt"
fi

# --- preTrain Word2Vec + BiLM on the 0.10 split ONLY (overwrites interim_data) -
echo "----- GNA preTrain on PubMedAKE 0.10 split -----"
PRETRAIN_LOG="${LOG_DIR}/p6h_preTrain_${DS}.txt"
if [[ "${DRY_RUN:-0}" == "1" ]]; then
  echo "+ conda run -n ${CONDA_ENV} python src/nlp/jobs/gna_pipeline.py --mode preTrain --dataSource ${DS} --jsonDataDir ${JSON_DIR} --device ${DEVICE} --epochs ${PRETRAIN_EPOCHS} --dataSampleSize ${PRETRAIN_SAMPLE_SIZE} --w2vMinCount ${W2V_MIN_COUNT} --valFraction 0 --seed ${SEED}"
else
  conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/gna_pipeline.py \
    --mode preTrain --dataSource "${DS}" --jsonDataDir "${JSON_DIR}" \
    --device "${DEVICE}" --epochs "${PRETRAIN_EPOCHS}" \
    --dataSampleSize "${PRETRAIN_SAMPLE_SIZE}" --w2vMinCount "${W2V_MIN_COUNT}" \
    --valFraction 0 --seed "${SEED}" 2>&1 | tee "${PRETRAIN_LOG}"
fi

# --- GNA family: 4 model configs x {BIO,IOBES,BILOU}, mode train,test ---------
# id -> "model:context"  (BiLSTM ignores context; "doc_attn" == token_doc_attn_gated).
declare -A GNA_CONFIGS=(
  [bilstm_crf]="bilstm_crf:sentence_only"
  [han_sentence_only]="han_crf:sentence_only"
  [han_token_doc_attn]="han_crf:token_doc_attn"
  [han_token_doc_attn_gated]="han_crf:token_doc_attn_gated"
)

run_gna() {
  local cfg="$1" schema="$2"
  local spec="${GNA_CONFIGS[$cfg]}"
  local model="${spec%%:*}"
  local ctx="${spec##*:}"
  local config_id="${cfg}_${schema}"
  local log_file="${LOG_DIR}/p6h_${config_id}.txt"

  local han_flags=()
  if [[ "${model}" == "han_crf" ]]; then
    han_flags=( --hanContextMode "${ctx}" )
    if [[ "${ctx}" == "token_doc_attn_gated" ]]; then
      han_flags+=( --hanUseGatedFusion --hanContextHeads 8 )
    fi
  fi

  local sample_flags=()
  [[ -n "${TRAIN_SAMPLE_SIZE}" ]] && sample_flags=( --trainSampleSize "${TRAIN_SAMPLE_SIZE}" )

  local cmd=(
    conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/gna_pipeline.py
    --mode train,test
    --model "${model}" --taggingSchema "${schema}"
    --dataSource "${DS}" --jsonDataDir "${JSON_DIR}"
    --device "${DEVICE}"
    --optimizer adamw --lr "${LR}" --batchSize "${BATCH_SIZE}" --epochs "${EPOCHS}"
    --validationSplit 0 --earlyStopPatience 0
    --positiveUpsample 2 --hanBatchMode fixed --rebalancingMode auto
    --hanUseBlockDiagonal --bilstmFreezeEmbeddings
    --seed "${SEED}" --dumpPredictions "${PRED_DIR}/${config_id}"
    "${sample_flags[@]}" "${han_flags[@]}"
  )

  echo "----- GNA ${config_id} (${model}/${ctx}/${schema}) on ${DS} -----"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "+ ${cmd[*]}"
    record gna "${model}" "${ctx}" "${schema}" "${log_file}" dry_run "train,test"
    return
  fi
  set +e
  "${cmd[@]}" 2>&1 | tee "${log_file}"
  local ec=${PIPESTATUS[0]}
  set -e
  local st="completed"; [[ ${ec} -ne 0 ]] && st="failed"
  record gna "${model}" "${ctx}" "${schema}" "${log_file}" "${st}" "train,test"
}

for cfg in bilstm_crf han_sentence_only han_token_doc_attn han_token_doc_attn_gated; do
  for schema in ${SCHEMAS}; do
    run_gna "${cfg}" "${schema}"
  done
done

# --- Transformer family: BioBERT, PubMedBERT, SciBERT, mode train,test --------
run_transformer() {
  local tf="$1"
  local config_id="transformer_${tf}"
  local log_file="${LOG_DIR}/p6h_${config_id}.txt"

  local sample_flags=()
  [[ -n "${TRAIN_SAMPLE_SIZE}" ]] && sample_flags=( --trainSampleSize "${TRAIN_SAMPLE_SIZE}" )

  local cmd=(
    conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/transformer_pipeline.py
    --hfModel "${tf}" --mode train,test
    --dataSource "${DS}" --jsonDataDir "${JSON_DIR}"
    --device "${DEVICE}"
    --epochs "${TF_EPOCHS}" --batchSize "${TF_BATCH}" --lr "${TF_LR}" --maxLength "${TF_MAXLEN}"
    --seed "${SEED}" --dumpPredictions "${PRED_DIR}/${config_id}"
    "${sample_flags[@]}"
  )
  echo "----- Transformer ${tf} on ${DS} -----"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "+ ${cmd[*]}"
    record transformer "${tf}" "n/a" "n/a" "${log_file}" dry_run "train,test"
    return
  fi
  set +e
  "${cmd[@]}" 2>&1 | tee "${log_file}"
  local ec=${PIPESTATUS[0]}
  set -e
  local st="completed"; [[ ${ec} -ne 0 ]] && st="failed"
  record transformer "${tf}" "n/a" "n/a" "${log_file}" "${st}" "train,test"
}

for tf in biobert pubmedbert scibert; do
  run_transformer "${tf}"
done

echo ""
echo "Phase 6H (PubMedAKE model-switch @ f=${TRAIN_FRACTION}) complete. Run index: ${RUN_INDEX}"
