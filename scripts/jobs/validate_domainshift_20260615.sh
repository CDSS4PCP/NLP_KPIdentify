#!/usr/bin/env bash
# Domain-shift validation (2026/06/15).
# Goal: show ALL architectures resonate the SAME behaviour under the early-stop FIX:
#   healthy IN-DOMAIN F1 (public test.json) vs collapsed CROSS-DOMAIN F1 (CDSS GS42/GS91).
# Models: HAN-CRF(token_doc_attn_gated)+BIO, BioBERT, SciBERT, PubMedBERT.
# Dataset: PubMedAKE (reuses existing pubmedake preTrain artifacts for the GNA/HAN run).
# Runs sequentially (8 GB VRAM -> no concurrent GPU jobs).
set -uo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
CONDA_ENV="cdss-gpu"
DS="pubmedake"
JSON_DIR="${ROOT_DIR}/data/pubmed_data/json_data_${DS}"
DEVICE="cuda"
SEED=42

EPOCHS=20
BATCH_SIZE=64
LR="1e-3"
VAL_SPLIT=0          # FIX: no validation split -> no early stopping -> full EPOCHS
EARLY_STOP=0
TRAIN_SAMPLE_SIZE=10000

TF_EPOCHS=3
TF_BATCH=16
TF_LR="3e-5"
TF_MAXLEN=256

LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/15/domainshift"
PRED_DIR="${LOG_DIR}/predictions"
mkdir -p "${LOG_DIR}" "${PRED_DIR}"
RUN_INDEX="${LOG_DIR}/domainshift_run_index.csv"
[[ -f "${RUN_INDEX}" ]] || echo "model,family,schema,seed,log_file,status" > "${RUN_INDEX}"

cd "${ROOT_DIR}"

echo "############################################################"
echo "# DOMAIN-SHIFT VALIDATION on ${DS}  (mode=train,test,testGS)"
echo "############################################################"

# ----- HAN-CRF (token_doc_attn_gated) + BIO  (reuses pubmedake preTrain artifacts) -----
HAN_LOG="${LOG_DIR}/han_token_doc_attn_gated_BIO.txt"
echo "----- HAN gated BIO -----"
set +e
conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/gna_pipeline.py \
    --mode train,test,testGS \
    --model han_crf --taggingSchema BIO \
    --dataSource "${DS}" --jsonDataDir "${JSON_DIR}" \
    --device "${DEVICE}" \
    --epochs "${EPOCHS}" --batchSize "${BATCH_SIZE}" --lr "${LR}" \
    --validationSplit "${VAL_SPLIT}" --earlyStopPatience "${EARLY_STOP}" \
    --trainSampleSize "${TRAIN_SAMPLE_SIZE}" \
    --seed "${SEED}" --dumpPredictions "${PRED_DIR}/han_token_doc_attn_gated_BIO" \
    --hanContextMode token_doc_attn_gated --hanUseGatedFusion --hanContextHeads 8 \
    > "${HAN_LOG}" 2>&1
ec=$?
set -e 2>/dev/null || true
[[ ${ec} -eq 0 ]] && st="completed" || st="failed"
echo "han_crf,gna,BIO,${SEED},$(basename "${HAN_LOG}"),${st}" >> "${RUN_INDEX}"
echo "HAN gated BIO -> ${st}"

# ----- Transformers: BioBERT, SciBERT, PubMedBERT -----
for tf in biobert scibert pubmedbert; do
  TF_LOG="${LOG_DIR}/transformer_${tf}.txt"
  echo "----- Transformer ${tf} -----"
  set +e
  conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/transformer_pipeline.py \
      --hfModel "${tf}" --mode train,test,testGS \
      --dataSource "${DS}" --jsonDataDir "${JSON_DIR}" \
      --device "${DEVICE}" \
      --epochs "${TF_EPOCHS}" --batchSize "${TF_BATCH}" --lr "${TF_LR}" \
      --maxLength "${TF_MAXLEN}" --trainSampleSize "${TRAIN_SAMPLE_SIZE}" --seed "${SEED}" \
      --dumpPredictions "${PRED_DIR}/transformer_${tf}" \
      > "${TF_LOG}" 2>&1
  ec=$?
  set -e 2>/dev/null || true
  [[ ${ec} -eq 0 ]] && st="completed" || st="failed"
  echo "${tf},transformer,n/a,${SEED},$(basename "${TF_LOG}"),${st}" >> "${RUN_INDEX}"
  echo "Transformer ${tf} -> ${st}"
done

echo ""
echo "Domain-shift validation complete. Run index: ${RUN_INDEX}"
