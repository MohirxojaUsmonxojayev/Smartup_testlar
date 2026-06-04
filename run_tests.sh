#!/bin/bash
# Mac/Linux wrapper. Cross-platform runner: python scripts/run_tests.py

set -e

if [[ -x "./.venv/bin/python" ]]; then
  PYTHON_BIN="./.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  PYTHON_BIN="python"
fi

exec "$PYTHON_BIN" scripts/run_tests.py "$@"
