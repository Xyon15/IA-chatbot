@echo off
cd /d "c:\Dev\IA-chatbot"
title Kira-Bot Fullscreen Launcher
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                🤖 KIRA-BOT FULLSCREEN                   ║
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
echo 🚀 Lancement de Kira-Bot en plein écran...
echo 📍 Raccourcis: F11=Plein écran, F5=Bot ON/OFF, F1=Aide
echo.

python launch_kira_fullscreen.py

echo.
echo 👋 Appuyez sur une touche pour fermer...
pause >nul
