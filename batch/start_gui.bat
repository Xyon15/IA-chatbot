@echo off
title Neuro-Bot - Interface Graphique
color 0B

echo.
echo =======================================================
echo          NEURO-BOT - INTERFACE GRAPHIQUE
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
echo 🎨 Démarrage de l'interface graphique...
echo.

REM Lancer l'interface graphique avec optimisation GPU automatique
python start_neuro.py --gui --auto

REM Si le script se termine avec une erreur
if %errorlevel% neq 0 (
    echo.
    echo ❌ L'interface graphique s'est fermée avec une erreur (code: %errorlevel%)
    echo.
    echo Solutions possibles:
    echo   1. Installez PySide6: pip install PySide6
    echo   2. Vérifiez les logs d'erreur
    echo   3. Relancez avec: python start_neuro.py --gui
    echo.
) else (
    echo.
    echo ✅ Interface graphique fermée proprement
)

echo.
pause