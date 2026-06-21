#!/usr/bin/env bash
# Phase 6G — model-switch verification on the SYNTHETIC corpus at train fraction 0.10.
#
# Question (user): "I still don't believe training on 0.10 train ratio of ~328 docs
# generalizes to the remaining ~3000 docs at ~60% F1." Phase 6e already proved this for
# the HAN gated model. Phase 6G repeats the check while SWITCHING THE MODEL ARCHITECTURE,
# to show the result is not an artefact of one architecture:
#   Native BiLSTM-CRF, HAN-CRF(sentence_only), HAN-CRF(token_doc_attn),
#   HAN-CRF(token_doc_attn_gated) — each in {BIO, IOBES, BILOU} — plus the three
#   transformer baselines BioBERT, PubMedBERT, SciBERT.
#
# All models: 20 epochs, f=0.10 (≈328 train / ≈2953 test). Each run is evaluated on
#   1) the held-out SYNTHETIC test.json (the ≈0.90 remainder NOT used for training),
#   2) GS42, 3) GS91 — i.e. --mode train,test,testGS (3 Score lines per GNA log).
#
# Mechanics mirror Phase 6e: back up the canonical synthetic split, re-split the existing
# labeled corpus once at f=0.10, run every model against that SAME split, then restore the
# canonical files via an EXIT trap. The GNA models reuse the existing fixed pretrained
# vocab/Word2Vec/BiLM (a guard re-creates them only if missing) — identical to Phase 6e.
#
# IMPORTANT (interim_data is shared, NOT namespaced per dataset): run this BEFORE the
# Phase 6H PubMedAKE script, because 6H's preTrain overwrites the synthetic
# vocab/Word2Vec/BiLM artifacts in interim_data/.
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase6g_modelswitch_synthetic_20260618.sh
#   scripts/jobs/run_matrix_phase6g_modelswitch_synthetic_20260618.sh
#   SCHEMAS="BIO" scripts/jobs/run_matrix_phase6g_modelswitch_synthetic_20260618.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/18/phase6g"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase6g_run_index.csv"
CONDA_ENV="${CONDA_ENV:-cdss-gpu}"
DEVICE="${DEVICE:-cuda}"
RUN_INDEX_HEADER="experiment,family,model,context,schema,train_fraction,seed,mode,log_file,status"

SEED="${SEED:-42}"
EPOCHS="${EPOCHS:-20}"
TRAIN_FRACTION="${TRAIN_FRACTION:-0.10}"
SCHEMAS="${SCHEMAS:-BIO IOBES BILOU}"

# GNA hyper-params (Phase 6e anchor — identical to Phase 6H for comparability).
BATCH_SIZE="${BATCH_SIZE:-64}"
LR="${LR:-1e-3}"

# Transformer hyper-params.
TF_EPOCHS="${TF_EPOCHS:-3}"
TF_BATCH="${TF_BATCH:-16}"
TF_LR="${TF_LR:-3e-5}"
TF_MAXLEN="${TF_MAXLEN:-256}"

# Synthetic preTrain guard params (only used if artifacts are missing).
PRETRAIN_EPOCHS="${PRETRAIN_EPOCHS:-5}"

JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_synthetic_labels_v2"
INTERIM_DIR="${ROOT_DIR}/interim_data"
BACKUP_DIR="${JSON_DIR}/_phase6g_backup"

mkdir -p "${LOG_DIR}" "${PRED_DIR}"
[[ -f "${RUN_INDEX}" ]] || echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"

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
    echo "Restored canonical synthetic train.json/test.json from backup."
  fi
}
trap restore_split EXIT

record() {
  local family="$1" model="$2" context="$3" schema="$4" log="$5" status="$6" mode="$7"
  if [[ "${DRY_RUN:-0}" != "1" ]]; then
    echo "phase6g,${family},${model},${context},${schema},${TRAIN_FRACTION},${SEED},${mode},$(basename "${log}"),${status}" >> "${RUN_INDEX}"
  fi
}

cd "${ROOT_DIR}"
backup_split

# --- Guard: ensure synthetic pretrained artifacts exist (reuse, like Phase 6e) ---
# Runs preTrain on the FULL canonical synthetic corpus ONLY if vocab/W2V/BiLM are absent.
ensure_pretrain() {
  if [[ -f "${INTERIM_DIR}/int2token.json" && -f "${INTERIM_DIR}/LM_word2vec.bin" && -f "${INTERIM_DIR}/BiLM.pt" ]]; then
    echo "Synthetic pretrained artifacts present in interim_data/ — reusing (matches Phase 6e)."
    return
  fi
  echo "Synthetic pretrained artifacts MISSING — running preTrain on full canonical corpus."
  local pre_log="${LOG_DIR}/p6g_preTrain_synthetic.txt"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "+ conda run -n ${CONDA_ENV} python src/nlp/jobs/gna_pipeline.py --mode preTrain --device ${DEVICE} --epochs ${PRETRAIN_EPOCHS} --seed ${SEED}"
    return
  fi
  conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/gna_pipeline.py \
    --mode preTrain --device "${DEVICE}" --epochs "${PRETRAIN_EPOCHS}" --seed "${SEED}" \
    2>&1 | tee "${pre_log}"
}
ensure_pretrain

# --- Re-split the canonical synthetic corpus once at f=TRAIN_FRACTION ---------
echo "Re-splitting synthetic corpus at f=${TRAIN_FRACTION} (seed ${SEED})."
if [[ "${DRY_RUN:-0}" == "1" ]]; then
  echo "+ conda run -n ${CONDA_ENV} python scripts/jobs/resplit_existing_dataset.py --trainFraction ${TRAIN_FRACTION} --seed ${SEED}"
else
  conda run --no-capture-output -n "${CONDA_ENV}" python -u scripts/jobs/resplit_existing_dataset.py \
    --trainFraction "${TRAIN_FRACTION}" --seed "${SEED}" 2>&1 | tee "${LOG_DIR}/p6g_resplit.txt"
fi

# --- GNA family: 4 model configs x {BIO,IOBES,BILOU}, mode train,test,testGS --
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
  local log_file="${LOG_DIR}/p6g_${config_id}.txt"

  local han_flags=()
  if [[ "${model}" == "han_crf" ]]; then
    han_flags=( --hanContextMode "${ctx}" )
    if [[ "${ctx}" == "token_doc_attn_gated" ]]; then
      han_flags+=( --hanUseGatedFusion --hanContextHeads 8 )
    fi
  fi

  local cmd=(
    conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/gna_pipeline.py
    --mode train,test,testGS
    --model "${model}" --taggingSchema "${schema}"
    --device "${DEVICE}"
    --optimizer adamw --lr "${LR}" --batchSize "${BATCH_SIZE}" --epochs "${EPOCHS}"
    --validationSplit 0 --earlyStopPatience 0
    --positiveUpsample 2 --hanBatchMode fixed --rebalancingMode auto
    --hanUseBlockDiagonal --bilstmFreezeEmbeddings
    --seed "${SEED}" --dumpPredictions "${PRED_DIR}/${config_id}"
    "${han_flags[@]}"
  )

  echo "----- GNA ${config_id} (${model}/${ctx}/${schema}) -----"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "+ ${cmd[*]}"
    record gna "${model}" "${ctx}" "${schema}" "${log_file}" dry_run "train,test,testGS"
    return
  fi
  set +e
  "${cmd[@]}" 2>&1 | tee "${log_file}"
  local ec=${PIPESTATUS[0]}
  set -e
  local st="completed"; [[ ${ec} -ne 0 ]] && st="failed"
  record gna "${model}" "${ctx}" "${schema}" "${log_file}" "${st}" "train,test,testGS"
}

for cfg in bilstm_crf han_sentence_only han_token_doc_attn han_token_doc_attn_gated; do
  for schema in ${SCHEMAS}; do
    run_gna "${cfg}" "${schema}"
  done
done

# --- Transformer family: BioBERT, PubMedBERT, SciBERT, mode train,test,testGS -
run_transformer() {
  local tf="$1"
  local config_id="transformer_${tf}"
  local log_file="${LOG_DIR}/p6g_${config_id}.txt"
  local cmd=(
    conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/transformer_pipeline.py
    --hfModel "${tf}" --mode train,test,testGS
    --device "${DEVICE}"
    --epochs "${TF_EPOCHS}" --batchSize "${TF_BATCH}" --lr "${TF_LR}" --maxLength "${TF_MAXLEN}"
    --seed "${SEED}" --dumpPredictions "${PRED_DIR}/${config_id}"
  )
  echo "----- Transformer ${tf} -----"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "+ ${cmd[*]}"
    record transformer "${tf}" "n/a" "n/a" "${log_file}" dry_run "train,test,testGS"
    return
  fi
  set +e
  "${cmd[@]}" 2>&1 | tee "${log_file}"
  local ec=${PIPESTATUS[0]}
  set -e
  local st="completed"; [[ ${ec} -ne 0 ]] && st="failed"
  record transformer "${tf}" "n/a" "n/a" "${log_file}" "${st}" "train,test,testGS"
}

for tf in biobert pubmedbert scibert; do
  run_transformer "${tf}"
done

echo ""
echo "Phase 6G (synthetic model-switch @ f=${TRAIN_FRACTION}) complete. Run index: ${RUN_INDEX}"
