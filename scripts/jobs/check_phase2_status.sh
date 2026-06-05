#!/usr/bin/env bash
# Quick Phase 2 status check

LOG_DIR="/home/rohangoli/remote_mount/outputs/results/rtx2000_blackwell/2026/06/01"
RUN_INDEX="${LOG_DIR}/phase2_run_index.csv"

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║           PHASE 2 STATUS CHECK — $(date '+%H:%M:%S')                  ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📊 RUN INDEX:"
if [[ -f "${RUN_INDEX}" ]]; then
  completed=$(tail -n +2 "${RUN_INDEX}" | grep -c "completed" || echo "0")
  total=$(tail -n +2 "${RUN_INDEX}" | wc -l)
  echo "  Runs completed: $completed / $total (expected: 0–8)"
  if [[ $total -gt 0 ]]; then
    echo ""
    echo "  Status breakdown:"
    grep -v "^config_id" "${RUN_INDEX}" | awk -F, '{print $NF}' | sort | uniq -c
  fi
else
  echo "  ⚠️  Run index not found"
fi

echo ""
echo "📁 LOG FILES:"
log_count=$(ls -1 "${LOG_DIR}"/p2_run*.txt 2>/dev/null | wc -l)
echo "  Log files created: $log_count / 8"

if [[ $log_count -gt 0 ]]; then
  echo ""
  for i in {1..8}; do
    log="${LOG_DIR}/p2_run${i}_"*".txt"
    if [[ -f $log ]]; then
      size=$(du -h "$log" | awk '{print $1}')
      epochs=$(grep -c "Epoch.*completed" "$log" 2>/dev/null || echo "0")
      status=$(if grep -q "testGS completed" "$log" 2>/dev/null; then echo "✓ DONE"; elif grep -q "Epoch" "$log" 2>/dev/null; then echo "▶ Running"; else echo "⏳ Starting"; fi)
      printf "    [%d] %s (${size}) — Epochs: %d — %s\n" $i "$(basename "$log" | cut -c1-50)" $epochs "$status"
    fi
  done
fi

echo ""
echo "⏱️  TIMING:"
if [[ -d "${LOG_DIR}" ]]; then
  start_log=$(ls -t "${LOG_DIR}"/p2_run*.txt 2>/dev/null | tail -1)
  if [[ -n "$start_log" ]]; then
    elapsed=$(($(date +%s) - $(stat -c %Y "$start_log")))
    echo "  Elapsed: $((elapsed / 60)) min $((elapsed % 60)) sec"
    echo "  Estimated total: 76 min"
  fi
fi

echo ""
echo "🎯 SUCCESS CRITERIA:"
echo "  Target: Mean GS F1 ≥ 53.80 (Phase 1 baseline: 53.50)"
echo ""
echo "═══════════════════════════════════════════════════════════════════════"
