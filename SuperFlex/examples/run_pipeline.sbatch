#!/bin/bash
#SBATCH --job-name=shape_pipeline
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --mem=24G
#SBATCH --time=00:15:00
#SBATCH --output=shape_pipeline_%j.out
#SBATCH --error=shape_pipeline_%j.err
# Set your cluster partition/QoS and load its existing CUDA/Conda modules.
# Required exported variables: SHAPE_CODE, SHAPE_MANIFEST, SHAPE_CONFIG,
# SHAPE_OUTPUT, MOGE_REPO, SUPERFLEX_REPO. Paths must be absolute.
# Optional: DA_ENV, MOGE_ENV, SF_ENV, HF_HOME, TORCH_EXTENSIONS_DIR.
set -euo pipefail
eval "$(conda shell.bash hook)"
: "${SHAPE_CODE:?}" "${SHAPE_MANIFEST:?}" "${SHAPE_CONFIG:?}" "${SHAPE_OUTPUT:?}"
: "${MOGE_REPO:?}" "${SUPERFLEX_REPO:?}"
export OMP_NUM_THREADS=4 HF_HUB_OFFLINE=1
for SHAPE_STAGE in da moge clouds superflex export; do
  case "$SHAPE_STAGE" in
    da) conda activate "${DA_ENV:-cv-epic-depth}"; export PYTHONPATH="$SHAPE_CODE/src" ;;
    moge) conda activate "${MOGE_ENV:-cv-moge2}"; export PYTHONPATH="$SHAPE_CODE/src:$MOGE_REPO" ;;
    *) conda activate "${SF_ENV:-cv-superflex}"; export PYTHONPATH="$SHAPE_CODE/src:$SUPERFLEX_REPO" ;;
  esac
  python -u -m shape_tools.pipeline "$SHAPE_STAGE" --manifest "$SHAPE_MANIFEST" --config "$SHAPE_CONFIG" --output "$SHAPE_OUTPUT"
done
