#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/06/01"
RUN_INDEX="${LOG_DIR}/run_index.csv"
CONDA_ENV="cdss-gpu"
RUN_INDEX_HEADER="config_id,model,schema,optimizer,lr,batch_size,epochs,pos_upsample,han_batch_mode,han_block,han_freeze,bilstm_freeze,han_context_mode,han_context_heads,han_context_dropout,han_use_gated,log_file,status"

mkdir -p "${LOG_DIR}"

if [[ ! -f "${RUN_INDEX}" ]]; then
  echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
else
  existing_header="$(head -n 1 "${RUN_INDEX}" || true)"
  if [[ "${existing_header}" != "${RUN_INDEX_HEADER}" ]]; then
    cp "${RUN_INDEX}" "${RUN_INDEX}.bak.$(date +%Y%m%d_%H%M%S)"
    echo "${RUN_INDEX_HEADER}" > "${RUN_INDEX}"
  fi
fi

run_one() {
  local config_id="$1"
  local model="$2"
  local schema="$3"
  local optimizer="$4"
  local lr="$5"
  local batch_size="$6"
  local epochs="$7"
  local pos_upsample="$8"
  local han_batch_mode="$9"
  local han_block="${10}"
  local han_freeze="${11}"
  local bilstm_freeze="${12}"
  local han_context_mode="${13}"
  local han_context_heads="${14}"
  local han_context_dropout="${15}"
  local han_use_gated="${16}"

  local log_file="${LOG_DIR}/${config_id}.txt"
  local cmd=(
    conda run -n "${CONDA_ENV}" python src/nlp/jobs/gna_pipeline.py
    --device cuda
    --model "${model}"
    --taggingSchema "${schema}"
    --mode train,testGS
    --optimizer "${optimizer}"
    --lr "${lr}"
    --batchSize "${batch_size}"
    --epochs "${epochs}"
    --positiveUpsample "${pos_upsample}"
    --hanBatchMode "${han_batch_mode}"
    --rebalancingMode auto
    --hanContextMode "${han_context_mode}"
    --hanContextHeads "${han_context_heads}"
    --hanContextDropout "${han_context_dropout}"
  )

  if [[ "${han_block}" == "true" ]]; then
    cmd+=(--hanUseBlockDiagonal)
  else
    cmd+=(--no-hanUseBlockDiagonal)
  fi

  if [[ "${han_freeze}" == "true" ]]; then
    cmd+=(--hanFreezeEmbeddings)
  else
    cmd+=(--no-hanFreezeEmbeddings)
  fi

  if [[ "${bilstm_freeze}" == "true" ]]; then
    cmd+=(--bilstmFreezeEmbeddings)
  else
    cmd+=(--no-bilstmFreezeEmbeddings)
  fi

  if [[ "${han_use_gated}" == "true" ]]; then
    cmd+=(--hanUseGatedFusion)
  else
    cmd+=(--no-hanUseGatedFusion)
  fi

  echo "Running ${config_id}"
  echo "Command: ${cmd[*]}"

  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    echo "[DRY_RUN] ${cmd[*]}" | tee "${log_file}"
    echo "${config_id},${model},${schema},${optimizer},${lr},${batch_size},${epochs},${pos_upsample},${han_batch_mode},${han_block},${han_freeze},${bilstm_freeze},${han_context_mode},${han_context_heads},${han_context_dropout},${han_use_gated},$(basename "${log_file}"),dry_run" >> "${RUN_INDEX}"
    return
  fi

  set +e
  (
    cd "${ROOT_DIR}"
    "${cmd[@]}"
  ) 2>&1 | tee "${log_file}"
  exit_code=${PIPESTATUS[0]}
  set -e

  local status="completed"
  if [[ ${exit_code} -ne 0 ]]; then
    status="failed"
  fi

  echo "${config_id},${model},${schema},${optimizer},${lr},${batch_size},${epochs},${pos_upsample},${han_batch_mode},${han_block},${han_freeze},${bilstm_freeze},${han_context_mode},${han_context_heads},${han_context_dropout},${han_use_gated},$(basename "${log_file}"),${status}" >> "${RUN_INDEX}"

  if [[ ${exit_code} -ne 0 ]]; then
    echo "Run ${config_id} failed with exit code ${exit_code}" >&2
  fi
}

# Medium-budget screening matrix (16 runs)
for model in bilstm_crf han_crf; do
  for schema in BIO IOBES; do
    for optimizer in adamw sgd; do
      for lr in 1e-3 5e-4; do
        config_id="m31_${model}_${schema}_${optimizer}_lr${lr//./p}"
        han_batch_mode="fixed"
        han_block="true"
        han_freeze="false"
        bilstm_freeze="true"
        han_context_mode="sentence_only"
        han_context_heads="4"
        han_context_dropout="0.1"
        han_use_gated="false"

        if [[ "${model}" == "han_crf" ]]; then
          han_freeze="false"
        fi

        run_one "${config_id}" "${model}" "${schema}" "${optimizer}" "${lr}" 64 20 2 "${han_batch_mode}" "${han_block}" "${han_freeze}" "${bilstm_freeze}" "${han_context_mode}" "${han_context_heads}" "${han_context_dropout}" "${han_use_gated}"
      done
    done
  done
done

# Optional Phase 1 architecture sweep (HAN only).
if [[ "${PHASE1_CONTEXT_SWEEP:-0}" == "1" ]]; then
  for context_mode in sentence_only token_doc_attn token_doc_attn_gated; do
    for heads in 4 8; do
      context_dropout="0.1"
      use_gated="false"
      if [[ "${context_mode}" == "token_doc_attn_gated" ]]; then
        use_gated="true"
      fi
      config_id="m31_p1_han_IOBES_adamw_lr1e-3_${context_mode}_h${heads}"
      run_one "${config_id}" "han_crf" "IOBES" "adamw" "1e-3" 64 20 2 "fixed" "true" "false" "true" "${context_mode}" "${heads}" "${context_dropout}" "${use_gated}"
    done
  done
fi

echo "Run index written to ${RUN_INDEX}"
