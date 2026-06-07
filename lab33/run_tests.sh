#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Installing requirements..."
python -m pip install -r requirements.txt
echo "Running pytest..."
python -m pytest -q
