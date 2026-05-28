#!/usr/bin/env bash
set -euo pipefail

# Build Docker image from a local filesystem staging directory to avoid heavy
# Docker context reads over SSHFS-mounted source trees.

IMAGE_NAME="${IMAGE_NAME:-nlp_kp}"
LOCAL_BUILD_DIR="${LOCAL_BUILD_DIR:-$HOME/.cache/nlp_kp_build}"

# Repository root = parent of this script directory.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

mkdir -p "${LOCAL_BUILD_DIR}"

echo "[1/3] Syncing project to local staging directory: ${LOCAL_BUILD_DIR}"
rsync -a --delete \
  --exclude '.git/' \
  --exclude '__pycache__/' \
  --exclude '.ipynb_checkpoints/' \
  --exclude '.DS_Store' \
  --exclude 'outputs/' \
  --exclude 'interim_data/' \
  "${REPO_ROOT}/" "${LOCAL_BUILD_DIR}/"

echo "[2/3] Building Docker image '${IMAGE_NAME}' from local disk"
docker build -t "${IMAGE_NAME}" "${LOCAL_BUILD_DIR}"

echo "[3/3] Done"
echo "Run with: docker run --rm --gpus all -v \"${REPO_ROOT}/outputs:/app/outputs\" ${IMAGE_NAME} --device cuda --mode train --epochs 20"
