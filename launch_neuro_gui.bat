@echo off
title Neuro-Bot - Selecteur d'Interface

echo.
echo ================================
echo   NEURO-BOT - LANCEUR PRINCIPAL
echo ================================
echo.

REM Verification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.10+ et l'ajouter au PATH
    pause
    exit /b 1
)

REM Activation de l'environnement virtuel si il existe
if exist "llama-venv\Scripts\activate.bat" (
    echo [INFO] Activation de l'environnement virtuel...
    call llama-venv\Scripts\activate.bat
    echo.
)

REM Verification du repertoire de travail
if not exist "gui\" (
    echo [ERREUR] Le dossier 'gui' n'existe pas
    echo Verifiez que vous etes dans le bon repertoire
    pause
    exit /b 1
)

echo [INFO] Lancement du selecteur d'interface...
echo.

REM Lancement du selecteur
python select_gui.py

REM Gestion des erreurs
if errorlevel 1 (
    echo.
    echo [ERREUR] Une erreur s'est produite lors du lancement
    echo Verifiez les dependances et la configuration
)

echo.
echo Interface fermee. Appuyez sur une touche pour quitter...
pause >nul