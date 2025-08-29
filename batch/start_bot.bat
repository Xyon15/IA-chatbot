@echo off
title Neuro-Bot - Démarrage
color 0A

echo.
echo =======================================================
echo            NEURO-BOT - DEMARRAGE AUTOMATIQUE
echo =======================================================
echo.

REM Changer vers le dossier parent du projet (sortir du dossier batch)
cd /d "%~dp0.."

REM Vérifier si l'environnement virtuel existe
if not exist "llama-venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé!
    echo.
    echo Pour configurer le projet, exécutez d'abord:
    echo   setup.bat
    echo.
    pause
    exit /b 1
)

echo 🔄 Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo 🚀 Démarrage du bot Discord avec optimisation GPU...
echo.

REM Lancer le bot avec optimisation GPU automatique
python start_neuro.py --auto

REM Si le script se termine avec une erreur
if %errorlevel% neq 0 (
    echo.
    echo ❌ Le bot s'est arrêté avec une erreur (code: %errorlevel%)
    echo.
    echo Solutions possibles:
    echo   1. Vérifiez le fichier .env (DISCORD_TOKEN)
    echo   2. Vérifiez votre connexion internet
    echo   3. Consultez les logs dans le dossier 'logs'
    echo.
    echo Pour plus d'informations, relancez avec:
    echo   python start_neuro.py
    echo.
) else (
    echo.
    echo ✅ Bot arrêté proprement
)

echo.
pause