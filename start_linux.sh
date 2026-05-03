#!/bin/bash
echo ""
echo " ======================================"
echo "  J.A.R.V.I.S - AI MAKES"
echo "  By Mehdi Barchichou"
echo " ======================================"
echo ""
cd "$(dirname "$0")"
if [ ! -d "venv_final" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv venv_final
fi
source venv_final/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt -q
xhost +local: 2>/dev/null
export DISPLAY=${DISPLAY:-:1}
echo "Starting J.A.R.V.I.S..."
python main.py
