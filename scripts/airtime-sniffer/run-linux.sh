#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
if [[ ! -x local-data/sniffer-venv/bin/python ]]; then
  python3 -m venv local-data/sniffer-venv
fi
local-data/sniffer-venv/bin/python -m pip install -r scripts/airtime-sniffer/requirements.txt
exec local-data/sniffer-venv/bin/python scripts/airtime-sniffer/sniffer.py --gui "$@"
