@echo off
echo Démarrage de l'optimiseur GPU...
cd /d "%~dp0\.."
call llama-venv\Scripts\activate.bat
python tools\gpu_optimizer.py
pause