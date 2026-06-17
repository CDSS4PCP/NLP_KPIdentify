#!/usr/bin/env bash
# Phase 8 — Zero-Shot Transformer Inference (no fine-tuning) (reviewer concern #1, follow-up)
# Two complementary zero-shot baselines, both contrasted against the fine-tuned Phase 4:
#
#   Option A (random-head floor)  — mode inferGS:
#       PubMedBERT / BioBERT / SciBERT masked-LM encoders with a randomly
#       initialized (seeded) classifier head. NO trained keyphrase head exists for
#       these encoders, so this is a reproducible LOWER-BOUND establishing that a
#       task-supervised head is required (numbers approach chance).
#
#   Option B (zero-shot transfer) — mode transferGS:
#       An off-the-shelf biomedical-NER checkpoint that DOES ship a trained
#       token-classification head, applied zero-shot with a documented
#       entity->keyphrase mapping (any recognized entity span -> B-KP/I-KP). This
#       is a meaningful zero-shot transfer baseline across taxonomies.
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase8_zeroshot_20260614.sh   # preview commands
#   scripts/jobs/run_matrix_phase8_zeroshot_20260614.sh             # execute
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/12"
PRED_DIR="${LOG_DIR}/predictions"
RUN_INDEX="${LOG_DIR}/phase8_zeroshot_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,hf_model,mode,extra,max_length,seed,log_file,status"

MAX_LEN="${MAX_LEN:-256}"
BATCH_SIZE="${BATCH_SIZE:-16}"
SEED="${SEED:-42}"
TRANSFER_MODEL="${TRANSFER_MODEL:-d4data/biomedical-ner-all}"

mkdir -p "${LOG_DIR}" "${PRED_DIR}"
if [[ ! -f "${RUN_INDEX}" ]]; then
  echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
fi

run_one() {
  local config_id="$1"
  local hf_model="$2"
  local mode="$3"
  local extra="${4:-}"

  local log_file="${LOG_DIR}/${config_id}.txt"
  local pred_sub="${PRED_DIR}/${config_id}"
  local cmd=(
    conda run -n "${CONDA_ENV}" python src/nlp/jobs/transformer_pipeline.py
    --hfModel "${hf_model}"
    --mode "${mode}"
    --device cuda
    --batchSize "${BATCH_SIZE}"
    --maxLength "${MAX_LEN}"
    --seed "${SEED}"
    --dumpPredictions "${pred_sub}"
  )
  if [[ "${mode}" == "transferGS" ]]; then
    cmd+=(--transferModel "${extra}")
  fi

  echo "Running ${config_id} (mode=${mode}, no fine-tuning)"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${cmd[*]}" | tee "${log_file}"
    echo "${config_id},${hf_model},${mode},${extra},${MAX_LEN},${SEED},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e

  local status="completed"
  [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${hf_model},${mode},${extra},${MAX_LEN},${SEED},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"

  # Post-run entity-level error analysis + bootstrap CI on the dumped predictions.
  if [[ ${exit_code} -eq 0 ]]; then
    for gs in testgs42 testgs91; do
      local pred_json="${pred_sub}/predictions_${gs}.json"
      if [[ -f "${pred_json}" ]]; then
        ( cd "${ROOT_DIR}" && conda run -n "${CONDA_ENV}" python -m src.nlp.evaluation.error_analysis \
            --predictions "${pred_json}" \
            --output_report "${LOG_DIR}/error_analysis_${config_id}_${gs}.md" ) || true
        ( cd "${ROOT_DIR}" && conda run -n "${CONDA_ENV}" python -m src.nlp.evaluation.bootstrap_ci ci \
            --predictions "${pred_json}" --iters 2000 ) 2>&1 | tee -a "${log_file}" || true
      fi
    done
  fi
}

# --- Option A: random-head floor (per encoder) ---
run_one "p8a_pubmedbert_randomhead" "pubmedbert" "inferGS"
run_one "p8a_biobert_randomhead"    "biobert"    "inferGS"
run_one "p8a_scibert_randomhead"    "scibert"    "inferGS"

# --- Option B: zero-shot transfer with a real pretrained NER head ---
run_one "p8b_ner_transfer" "pubmedbert" "transferGS" "${TRANSFER_MODEL}"

echo ""
echo "Phase 8 zero-shot transformer inference complete. Run index: ${RUN_INDEX}"
