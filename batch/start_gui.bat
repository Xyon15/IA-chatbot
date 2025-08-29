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

REM Verifier si l'environnement virtuel existe
if not exist "llama-venv\Scripts\activate.bat" (
    echo [ERREUR] Environnement virtuel non trouve!
    echo.
    echo Pour configurer le projet, executez d'abord:
    echo   setup.bat
    echo.
    pause
    exit /b 1
)

echo [*] Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo [*] Demarrage de l'interface graphique...
echo.

REM Lancer l'interface graphique avec optimisation GPU automatique
python start_neuro.py --gui --auto

REM Si le script se termine avec une erreur
if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] L'interface graphique s'est fermee avec une erreur (code: %errorlevel%)
    echo.
    echo Solutions possibles:
    echo   1. Installez PySide6: pip install PySide6
    echo   2. Verifiez les logs d'erreur
    echo   3. Relancez avec: python start_neuro.py --gui
    echo.
) else (
    echo.
    echo [OK] Interface graphique fermee proprement
)

echo.
pause