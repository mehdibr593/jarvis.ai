@echo off
title J.A.R.V.I.S - Mehdi Barchichou
echo.
echo  ======================================
echo   J.A.R.V.I.S - AI MAKES
echo   By Mehdi Barchichou
echo  ======================================
echo.
cd /d "%~dp0"
if not exist venv\Scripts\activate.bat (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt -q
echo Starting J.A.R.V.I.S...
python main.py
pause
