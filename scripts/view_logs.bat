@echo off
echo Démarrage du visualiseur de logs...
cd /d "%~dp0\.."
call llama-venv\Scripts\activate.bat
python tools\log_viewer_gui.py
pause