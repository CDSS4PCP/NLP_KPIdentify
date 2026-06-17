#!/usr/bin/env bash
# Build public-dataset JSON_DATA folders (KPBioMed + PubMedAKE) to replace synthetic labels.
#
# For each dataset this:
#   1. Copies the Gold Standard testsets (testgs42/testgs91 + feature files) into the dataset
#      folder so testGS evaluation + GS fine-tuning resolve them.
#   2. Runs `gna_pipeline.py --mode createData --dataSource <ds>` which streams/loads the public
#      dataset, normalizes it into the canonical record schema, and writes train.json/test.json
#      plus tf_idf.json/textrank.json (and recomputes GS feature dicts).
#
# Split policy:
#   train.json -> training corpus ; validation is carved from train.json at train time
#                 (--validationSplit / --kFolds), keeping GS out of validation.
#   test.json  -> held-out PUBLIC in-domain reference split.
#   testgs42/91 -> headline GOLD STANDARD test set (testGS mode).
#
# Usage:
#   DRY_RUN=1 scripts/jobs/build_public_datasets_20260614.sh        # preview
#   SAMPLE_SIZE=5000 scripts/jobs/build_public_datasets_20260614.sh # build both
#   DATASETS="kpbiomed" scripts/jobs/build_public_datasets_20260614.sh
#
# PubMedAKE requires the Zenodo files to be downloaded first (record 6330817):
#   small_train.json etc. placed under data/pubmed_data/raw_data/pubmedake/
set -euo pipefail

ROOT_DIR="/home/rohangoli/remote_mount"
CONDA_ENV="${CONDA_ENV:-cdss-gpu}"
SAMPLE_SIZE="${SAMPLE_SIZE:-5000}"
VAL_FRACTION="${VAL_FRACTION:-0.1}"
KPBIOMED_SUBSET="${KPBIOMED_SUBSET:-small}"
SEED="${SEED:-42}"
DATASETS="${DATASETS:-kpbiomed pubmedake}"

SYNTH_DIR="${ROOT_DIR}/data/pubmed_data/json_data_synthetic_labels_v2"
KPBIOMED_DIR="${ROOT_DIR}/data/pubmed_data/json_data_kpbiomed"
PUBMEDAKE_DIR="${ROOT_DIR}/data/pubmed_data/json_data_pubmedake"
PUBMEDAKE_RAW="${ROOT_DIR}/data/pubmed_data/raw_data/pubmedake/small_train.json"

run() {
  echo "+ $*"
  if [[ "${DRY_RUN:-0}" != "1" ]]; then
    "$@"
  fi
}

copy_gs_files() {
  local dest="$1"
  run mkdir -p "${dest}"
  for f in testgs42.json testgs91.json; do
    if [[ -f "${SYNTH_DIR}/${f}" ]]; then
      run cp "${SYNTH_DIR}/${f}" "${dest}/${f}"
    else
      echo "WARNING: ${SYNTH_DIR}/${f} not found; testGS for ${dest} will be unavailable."
    fi
  done
}

build_one() {
  local ds="$1"
  echo "=================================================================="
  echo "Building public dataset: ${ds}"
  echo "=================================================================="

  local dest
  local extra=()
  case "${ds}" in
    kpbiomed)
      dest="${KPBIOMED_DIR}"
      extra=( --kpbiomedSubset "${KPBIOMED_SUBSET}" )
      ;;
    pubmedake)
      dest="${PUBMEDAKE_DIR}"
      if [[ ! -f "${PUBMEDAKE_RAW}" ]]; then
        echo "ERROR: PubMedAKE raw file missing: ${PUBMEDAKE_RAW}"
        echo "       Download Zenodo record 6330817 (small_train.json) into that location first."
        return 1
      fi
      extra=( --pubmedakeFile "${PUBMEDAKE_RAW}" )
      ;;
    *)
      echo "Unknown dataset: ${ds}"; return 1 ;;
  esac

  copy_gs_files "${dest}"

  run conda run -n "${CONDA_ENV}" python src/nlp/jobs/gna_pipeline.py \
    --mode createData \
    --dataSource "${ds}" \
    --jsonDataDir "${dest}" \
    --dataSampleSize "${SAMPLE_SIZE}" \
    --valFraction "${VAL_FRACTION}" \
    --seed "${SEED}" \
    "${extra[@]}"

  echo "Done: ${ds} -> ${dest}"
}

cd "${ROOT_DIR}"
for ds in ${DATASETS}; do
  build_one "${ds}"
done

echo ""
echo "Public dataset build complete for: ${DATASETS}"
