#!/bin/bash
cd "$(dirname "$0")"
source venv_final/bin/activate 2>/dev/null || true
python3 run.py 2>/dev/null || python3 main.py
