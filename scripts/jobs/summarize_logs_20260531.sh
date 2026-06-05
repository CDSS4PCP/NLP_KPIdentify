#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
LOG_DIR="${ROOT_DIR}/outputs/results/rtx2000_blackwell/2026/05/31"

cd "${ROOT_DIR}"
python src/nlp/evaluation/summarize_runtime_logs.py \
  --logDir "${LOG_DIR}" \
  --csvOut "runtime_metrics_ranked.csv" \
  --summaryOut "runtime_research_summary.md"
