#!/usr/bin/env bash
# Run the full experiment matrix on PUBLIC datasets (KPBioMed + PubMedAKE) instead of
# synthetic labels. Covers all 7 model configurations:
#   Transformers : BioBERT, SciBERT, PubMedBERT          (token-classification head)
#   GNA          : BiLSTM-CRF, HAN-CRF(sentence_only),
#                  HAN-CRF(token_doc_attn), HAN-CRF(token_doc_attn_gated)
# GNA configs sweep tagging schemas {BIO, IOBES, BILOU}; transformers run once per dataset.
#
# Split policy (per design):
#   TRAIN = public train.json ; VALIDATION = held-out slice of train.json (--validationSplit) ;
#   TEST  = GS42 + GS91 (testGS) [+ public test.json as in-domain reference].
#
# Prereq: build the dataset folders first:
#   scripts/jobs/build_public_datasets_20260614.sh
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_all_public_20260614.sh            # preview every command
#   scripts/jobs/run_all_public_20260614.sh                      # execute
#   DATASETS="kpbiomed" SCHEMAS="IOBES" scripts/jobs/run_all_public_20260614.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
CONDA_ENV="${CONDA_ENV:-cdss-gpu}"
DATE_DIR="2026/06/14"
DEVICE="${DEVICE:-cuda}"

DATASETS="${DATASETS:-kpbiomed pubmedake}"
SCHEMAS="${SCHEMAS:-BIO IOBES BILOU}"
SEED="${SEED:-42}"

# GNA training hyper-params.
EPOCHS="${EPOCHS:-20}"
PRETRAIN_EPOCHS="${PRETRAIN_EPOCHS:-5}"
PRETRAIN_SAMPLE_SIZE="${PRETRAIN_SAMPLE_SIZE:-5000}"
TRAIN_SAMPLE_SIZE="${TRAIN_SAMPLE_SIZE:-10000}"
W2V_MIN_COUNT="${W2V_MIN_COUNT:-5}"
# Root-cause fix (2026/06/15): VAL_SPLIT=0 disables the validation-driven early
# stopping. On the label-sparse public corpora (kp_ratio ~0.055 vs synthetic
# ~0.26), the O-dominated validation loss plateaus after ~2 epochs and tripped
# early stopping, leaving a barely-trained model that predicted ~98% 'O'
# (GS F1 ~1-2%). Every earlier (working, GS F1 ~44-61%) experiment ran with
# val_docs=0 and trained the full EPOCHS. Set VAL_SPLIT>0 only if you also fix
# the early-stop criterion to monitor keyphrase F1 instead of raw loss.
BATCH_SIZE="${BATCH_SIZE:-64}"
LR="${LR:-1e-3}"
VAL_SPLIT="${VAL_SPLIT:-0}"
EARLY_STOP="${EARLY_STOP:-0}"

# Transformer hyper-params.
TF_EPOCHS="${TF_EPOCHS:-3}"
TF_BATCH="${TF_BATCH:-16}"
TF_LR="${TF_LR:-3e-5}"
TF_MAXLEN="${TF_MAXLEN:-256}"

run() {
  echo "+ $*"
  if [[ "${DRY_RUN:-0}" != "1" ]]; then
    "$@"
  fi
}

dataset_dir() {
  case "$1" in
    kpbiomed)  echo "${ROOT_DIR}/data/pubmed_data/json_data_kpbiomed" ;;
    pubmedake) echo "${ROOT_DIR}/data/pubmed_data/json_data_pubmedake" ;;
    *) echo "" ;;
  esac
}

cd "${ROOT_DIR}"

for DS in ${DATASETS}; do
  JSON_DIR="$(dataset_dir "${DS}")"
  if [[ -z "${JSON_DIR}" ]]; then
    echo "Unknown dataset ${DS}; skipping."; continue
  fi
  if [[ ! -f "${JSON_DIR}/train.json" && "${DRY_RUN:-0}" != "1" ]]; then
    echo "ERROR: ${JSON_DIR}/train.json missing. Run build_public_datasets_20260614.sh first."
    exit 1
  fi

  LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/${DATE_DIR}/${DS}"
  PRED_DIR="${LOG_DIR}/predictions"
  RUN_INDEX="${LOG_DIR}/public_matrix_run_index.csv"
  run mkdir -p "${LOG_DIR}" "${PRED_DIR}"
  if [[ "${DRY_RUN:-0}" != "1" && ! -f "${RUN_INDEX}" ]]; then
    echo "dataset,config_id,family,model,schema,seed,log_file,status" > "${RUN_INDEX}"
  fi

  echo "##################################################################"
  echo "# DATASET: ${DS}  (JSON_DATA=${JSON_DIR})"
  echo "##################################################################"

  record() {
    local cfg="$1" fam="$2" model="$3" schema="$4" log="$5" status="$6"
    if [[ "${DRY_RUN:-0}" != "1" ]]; then
      echo "${DS},${cfg},${fam},${model},${schema},${SEED},$(basename "${log}"),${status}" >> "${RUN_INDEX}"
    fi
  }

  # ---------------------------------------------------------------- GNA family
  # Pre-train Word2Vec + BiLM once on this dataset's train corpus (shared by all GNA configs).
  PRETRAIN_LOG="${LOG_DIR}/preTrain_${DS}.txt"
  echo "----- GNA preTrain on ${DS} -----"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "+ conda run -n ${CONDA_ENV} python src/nlp/jobs/gna_pipeline.py --mode preTrain --dataSource ${DS} --jsonDataDir ${JSON_DIR} --device ${DEVICE} --epochs ${PRETRAIN_EPOCHS} --dataSampleSize ${PRETRAIN_SAMPLE_SIZE} --w2vMinCount ${W2V_MIN_COUNT} --valFraction ${VAL_SPLIT} --seed ${SEED}"
  else
    ( conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/gna_pipeline.py \
        --mode preTrain --dataSource "${DS}" --jsonDataDir "${JSON_DIR}" \
        --device "${DEVICE}" --epochs "${PRETRAIN_EPOCHS}" \
        --dataSampleSize "${PRETRAIN_SAMPLE_SIZE}" --w2vMinCount "${W2V_MIN_COUNT}" \
        --valFraction "${VAL_SPLIT}" --seed "${SEED}" ) 2>&1 | tee "${PRETRAIN_LOG}" || true
  fi

  # GNA model configs: id -> "model:hanContextMode" (sentence_only used as placeholder for BiLSTM).
  declare -A GNA_CONFIGS=(
    [bilstm_crf]="bilstm_crf:sentence_only"
    [han_sentence_only]="han_crf:sentence_only"
    [han_token_doc_attn]="han_crf:token_doc_attn"
    [han_token_doc_attn_gated]="han_crf:token_doc_attn_gated"
  )

  for cfg in bilstm_crf han_sentence_only han_token_doc_attn han_token_doc_attn_gated; do
    spec="${GNA_CONFIGS[$cfg]}"
    model="${spec%%:*}"
    ctx="${spec##*:}"
    for schema in ${SCHEMAS}; do
      config_id="${cfg}_${schema}"
      log_file="${LOG_DIR}/${config_id}.txt"
      pred_sub="${PRED_DIR}/${config_id}"

      han_flags=()
      if [[ "${model}" == "han_crf" ]]; then
        han_flags=( --hanContextMode "${ctx}" )
        if [[ "${ctx}" == "token_doc_attn_gated" ]]; then
          han_flags+=( --hanUseGatedFusion --hanContextHeads 8 )
        fi
      fi

      echo "----- GNA ${config_id} (${model}/${ctx}/${schema}) on ${DS} -----"
      if [[ "${DRY_RUN:-0}" == "1" ]]; then
        echo "+ conda run -n ${CONDA_ENV} python src/nlp/jobs/gna_pipeline.py --mode train,test,testGS --model ${model} --taggingSchema ${schema} --dataSource ${DS} --jsonDataDir ${JSON_DIR} --device ${DEVICE} --epochs ${EPOCHS} --batchSize ${BATCH_SIZE} --lr ${LR} --validationSplit ${VAL_SPLIT} --earlyStopPatience ${EARLY_STOP} --trainSampleSize ${TRAIN_SAMPLE_SIZE} --seed ${SEED} --dumpPredictions ${pred_sub} ${han_flags[*]}"
        record "${config_id}" gna "${model}" "${schema}" "${log_file}" dry_run
        continue
      fi

      set +e
      ( conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/gna_pipeline.py \
          --mode train,test,testGS \
          --model "${model}" --taggingSchema "${schema}" \
          --dataSource "${DS}" --jsonDataDir "${JSON_DIR}" \
          --device "${DEVICE}" \
          --epochs "${EPOCHS}" --batchSize "${BATCH_SIZE}" --lr "${LR}" \
          --validationSplit "${VAL_SPLIT}" --earlyStopPatience "${EARLY_STOP}" \
          --trainSampleSize "${TRAIN_SAMPLE_SIZE}" \
          --seed "${SEED}" --dumpPredictions "${pred_sub}" \
          "${han_flags[@]}" ) 2>&1 | tee "${log_file}"
      ec=${PIPESTATUS[0]}
      set -e
      [[ ${ec} -eq 0 ]] && st="completed" || st="failed"
      record "${config_id}" gna "${model}" "${schema}" "${log_file}" "${st}"
    done
  done

  # ------------------------------------------------------- Transformer family
  for tf in biobert scibert pubmedbert; do
    config_id="transformer_${tf}"
    log_file="${LOG_DIR}/${config_id}.txt"
    pred_sub="${PRED_DIR}/${config_id}"

    echo "----- Transformer ${tf} on ${DS} -----"
    if [[ "${DRY_RUN:-0}" == "1" ]]; then
      echo "+ conda run -n ${CONDA_ENV} python src/nlp/jobs/transformer_pipeline.py --hfModel ${tf} --mode train,test,testGS --dataSource ${DS} --jsonDataDir ${JSON_DIR} --device ${DEVICE} --epochs ${TF_EPOCHS} --batchSize ${TF_BATCH} --lr ${TF_LR} --maxLength ${TF_MAXLEN} --trainSampleSize ${TRAIN_SAMPLE_SIZE} --seed ${SEED} --dumpPredictions ${pred_sub}"
      record "${config_id}" transformer "${tf}" "n/a" "${log_file}" dry_run
      continue
    fi

    set +e
    ( conda run --no-capture-output -n "${CONDA_ENV}" python -u src/nlp/jobs/transformer_pipeline.py \
        --hfModel "${tf}" --mode train,testGS \
        --dataSource "${DS}" --jsonDataDir "${JSON_DIR}" \
        --device "${DEVICE}" \
        --epochs "${TF_EPOCHS}" --batchSize "${TF_BATCH}" --lr "${TF_LR}" \
        --maxLength "${TF_MAXLEN}" --trainSampleSize "${TRAIN_SAMPLE_SIZE}" --seed "${SEED}" \
        --dumpPredictions "${pred_sub}" ) 2>&1 | tee "${log_file}"
    ec=${PIPESTATUS[0]}
    set -e
    [[ ${ec} -eq 0 ]] && st="completed" || st="failed"
    record "${config_id}" transformer "${tf}" "n/a" "${log_file}" "${st}"
  done

  echo "Dataset ${DS} matrix complete. Run index: ${RUN_INDEX}"
done

echo ""
echo "All public-dataset experiments complete for: ${DATASETS}"
echo "Note: phase-specific ablations (Phase 2/3/5/6/7/8) can be run per dataset by passing"
echo "      DATASET + --jsonDataDir to the existing scripts/jobs/run_matrix_phase*.sh scripts."
