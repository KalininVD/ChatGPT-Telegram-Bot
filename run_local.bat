@echo off
python -m pip install --upgrade pip
pip install -r requirements.txt
cls
python main_local.py
pause