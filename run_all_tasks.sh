#!/usr/bin/env bash
set -euo pipefail

PY_BIN="${PYTHON:-python}"
if ! command -v "$PY_BIN" >/dev/null 2>&1; then
  PY_BIN="/c/Users/19252/AppData/Local/Programs/Python/Python312/python.exe"
fi

echo "=== Running CSA0715 Computer Networks Verification Harness (CO1 - CO5) ==="
"$PY_BIN" "ASSIGNMNET CO1/run_co1.py"
"$PY_BIN" "ASSIGNMENT CO2/run_co2.py"
"$PY_BIN" "ASSIGNMENT CO3/run_co3.py"
"$PY_BIN" "ASSIGNMENT CO4/run_co4.py"
"$PY_BIN" "ASSSIGNMENT CO5/run_co5.py"
echo "=== All CO1-CO5 tasks verified successfully ==="
