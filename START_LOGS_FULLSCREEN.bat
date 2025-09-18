@echo off
cd /d "c:\Dev\IA-chatbot"
title Log Viewer Fullscreen Launcher
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              📊 LOG VIEWER FULLSCREEN                   ║
echo ║               Lanceur Rapide Windows                     ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Vérifier si le venv existe
if exist "llama-venv\Scripts\activate.bat" (
    echo ✅ Environnement virtuel détecté - Activation...
    call llama-venv\Scripts\activate.bat
) else (
    echo ⚠️ Environnement virtuel non trouvé - Utilisation Python système
)

echo.
echo 🚀 Lancement du Log Viewer en plein écran...
echo 📊 Raccourcis: F11=Plein écran, F5=Actualiser
echo.

python launch_logs_fullscreen.py

echo.
echo 👋 Appuyez sur une touche pour fermer...
pause >nul