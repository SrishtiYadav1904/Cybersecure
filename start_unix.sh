#!/usr/bin/env bash
# CyberGuard Universal Unix Launcher (macOS & Linux)
set -e

# Dynamically resolve script directory (no hardcoded paths)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "======================================================"
echo "          CyberGuard - Starting Platform              "
echo "======================================================"

# Check and activate virtualenv if available
if [ -f ".venv/bin/activate" ]; then
    echo "[*] Activating virtual environment (.venv)..."
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    echo "[*] Activating virtual environment (venv)..."
    source venv/bin/activate
else
    echo "[*] Using system Python..."
fi

# Run python launcher
python3 run.py
