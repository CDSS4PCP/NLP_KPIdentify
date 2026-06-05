#!/usr/bin/env bash
# Phase 2 Summarizer: Parse Phase 2 logs and generate ranked results + research summary

set -euo pipefail

LOG_DIR="${1:-.}/outputs/results/rtx2000_blackwell/2026/06/01"
PHASE2_RUN_INDEX="${LOG_DIR}/phase2_run_index.csv"
PHASE2_METRICS="${LOG_DIR}/phase2_runtime_metrics_ranked.csv"
PHASE2_SUMMARY="${LOG_DIR}/phase2_research_summary.md"

if [[ ! -d "${LOG_DIR}" ]]; then
  echo "Error: Log directory not found: ${LOG_DIR}"
  exit 1
fi

if [[ ! -f "${PHASE2_RUN_INDEX}" ]]; then
  echo "Error: Phase 2 run index not found: ${PHASE2_RUN_INDEX}"
  exit 1
fi

echo "Summarizing Phase 2 logs from: ${LOG_DIR}"

# Run the summarizer script
conda run -n cdss-gpu python src/nlp/evaluation/summarize_runtime_logs.py \
  --log_dir "${LOG_DIR}" \
  --run_index "${PHASE2_RUN_INDEX}" \
  --output_metrics "${PHASE2_METRICS}" \
  --output_summary "${PHASE2_SUMMARY}" \
  || true

echo "Phase 2 summarization completed."
echo "Metrics: ${PHASE2_METRICS}"
echo "Summary: ${PHASE2_SUMMARY}"
