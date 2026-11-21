#!/usr/bin/env bash
# Dev environment for TOFF: the conda-forge dependencies from docs/source/installation.md,
# TOFF itself in editable mode, plus what is only needed for development:
# pytest/flake8 (as in .github/workflows/tests.yml) and the docs toolchain (.conda_create_env/environment.yml).
set -euo pipefail
cd "$(dirname "$0")/.."

# safe.directory avoids git "dubious ownership" errors, which versioningit would hit on the mounted repo.
git config --global --add safe.directory '*'

ENV_NAME=toff

# The container runs as linux/amd64 (see devcontainer.json), so espaloma (needs dgl) is always available.
micromamba create -n "$ENV_NAME" -c conda-forge --override-channels -y \
    python=3.12 pip \
    openff-toolkit openmm openmmforcefields ambertools parmed importlib-resources \
    rdkit pyyaml numpy \
    pytest pytest-cov flake8 \
    sphinx myst-nb myst-parser sphinx-book-theme sphinx-design sphinx-copybutton \
    sphinx-inline-tabs ipython ipykernel sphinx-autobuild \
    "espaloma>=0.3.2"

# Note: the base image (Ubuntu 22.04, glibc 2.35) does not need the patchelf --clear-execstack
# workaround for Espaloma's PyTorch; that only applies to glibc >= 2.41 (see installation.md).

micromamba run -n "$ENV_NAME" python -m pip install --no-deps -e '.[dev]'

# Smoke test
micromamba run -n "$ENV_NAME" python -c "import toff; print('toff', toff.__version__)"
