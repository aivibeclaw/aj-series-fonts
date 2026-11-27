#!/usr/bin/env bash
# Builds fonts-aj-series_<version>_all.deb (5 families, 27 TTFs, read-only 0444 font files).
# Single implementation lives in the private foundry builder.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
PY="${AJ_PYTHON:-$ROOT/.venv/bin/python}"
[ -x "$PY" ] || PY=python3
"$PY" -B -c 'from foundry.build_headless_core_installers import build_headless_linux_default_deb as build; print(build())'
