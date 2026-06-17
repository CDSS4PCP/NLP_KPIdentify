#!/usr/bin/env bash
# Phase 5 — Factorial Ablation Study (reviewer concern #3)
# Cleanly ablates the core components the paper credits for its gains, against the
# HAN-CRF SOTA configuration (token_doc_attn_gated, IOBES, adamw, lr1e-3):
#   - document attention   : token_doc_attn_gated  vs  sentence_only
#   - BiLM transfer         : --useBiLM             vs  --no-useBiLM
#   - word embeddings       : Word2Vec              vs  --useRandomEmbeddings
#   - supervision           : synthetic-only        vs  synthetic + GS fine-tune
#
# Assumes preTrain artifacts (vocab, Word2Vec, BiLM) already exist in interim_data/.
# Run `--mode createData,preTrain` once beforehand if not.
#
# Usage:
#   DRY_RUN=1 scripts/jobs/run_matrix_phase5_ablation_20260612.sh
#   scripts/jobs/run_matrix_phase5_ablation_20260612.sh
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/12"
RUN_INDEX="${LOG_DIR}/phase5_ablation_run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,context_mode,use_bilm,random_embed,gs_finetune_epochs,seed,log_file,status"

SEED="${SEED:-42}"
EPOCHS="${EPOCHS:-20}"

mkdir -p "${LOG_DIR}"
if [[ ! -f "${RUN_INDEX}" ]]; then
  echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
fi

run_one() {
  local config_id="$1"
  local context_mode="$2"   # token_doc_attn_gated | sentence_only
  local use_bilm="$3"       # true | false
  local random_embed="$4"   # true | false
  local gs_ft_epochs="$5"   # 0 disables GS fine-tuning

  local log_file="${LOG_DIR}/${config_id}.txt"
  local cmd=(
    conda run -n "${CONDA_ENV}" python src/nlp/jobs/gna_pipeline.py
    --device cuda
    --model han_crf
    --taggingSchema IOBES
    --mode train,testGS
    --optimizer adamw
    --lr 1e-3
    --batchSize 64
    --epochs "${EPOCHS}"
    --positiveUpsample 2
    --hanBatchMode fixed
    --rebalancingMode auto
    --hanContextMode "${context_mode}"
    --hanContextHeads 8
    --hanContextDropout 0.1
    --hanUseBlockDiagonal
    --no-hanFreezeEmbeddings
    --bilstmFreezeEmbeddings
    --seed "${SEED}"
    --gsFineTuneEpochs "${gs_ft_epochs}"
  )

  if [[ "${context_mode}" == "token_doc_attn_gated" ]]; then
    cmd+=(--hanUseGatedFusion)
  else
    cmd+=(--no-hanUseGatedFusion)
  fi
  if [[ "${use_bilm}" == "true" ]]; then cmd+=(--useBiLM); else cmd+=(--no-useBiLM); fi
  if [[ "${random_embed}" == "true" ]]; then cmd+=(--useRandomEmbeddings); else cmd+=(--no-useRandomEmbeddings); fi

  echo "Running ${config_id}"
  echo "Command: ${cmd[*]}"
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${cmd[*]}" | tee "${log_file}"
    echo "${config_id},${context_mode},${use_bilm},${random_embed},${gs_ft_epochs},${SEED},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  ( cd "${ROOT_DIR}" && "${cmd[@]}" ) 2>&1 | tee "${log_file}"
  local exit_code=${PIPESTATUS[0]}
  set -e
  local status="completed"; [[ ${exit_code} -ne 0 ]] && status="failed"
  echo "${config_id},${context_mode},${use_bilm},${random_embed},${gs_ft_epochs},${SEED},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"
}

# Full model (all components on) — anchor row, should reproduce HAN SOTA ~53.5 mean GS F1.
run_one "p5_full_model"        "token_doc_attn_gated" "true"  "false" "0"
# -- no document attention
run_one "p5_no_doc_attn"       "sentence_only"        "true"  "false" "0"
# -- no BiLM transfer
run_one "p5_no_bilm"           "token_doc_attn_gated" "false" "false" "0"
# -- random embeddings (no Word2Vec)
run_one "p5_random_embed"      "token_doc_attn_gated" "true"  "true"  "0"
# -- synthetic + GS fine-tuning
run_one "p5_synth_plus_gs"     "token_doc_attn_gated" "true"  "false" "10"

echo ""
echo "Phase 5 ablation complete. Run index: ${RUN_INDEX}"
echo "Summarize with: scripts/jobs/summarize_logs_phase2_20260601.sh (point LOG_DIR to 2026/06/12) or summarize_runtime_logs.py"
