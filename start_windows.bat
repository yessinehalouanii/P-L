@echo off
cd /d %~dp0
python -m pip install -r backend\requirements.txt
python run.py
pause
