@echo off
title Neuro-Bot - Diagnostic Final  
color 0C

echo.
echo =======================================================
echo          NEURO-BOT - DIAGNOSTIC FINAL
echo =======================================================
echo.

REM Aller vers le dossier parent du projet
cd /d "%~dp0.."

echo [*] Diagnostic de l'environnement Neuro-Bot...
echo.

echo === VERIFICATION DES FICHIERS REQUIS ===
if exist "llama-venv\Scripts\activate.bat" (
    echo [OK] Environnement virtuel: PRESENT
    set "VENV_EXISTS=1"
) else (
    echo [ERREUR] Environnement virtuel: ABSENT  
    set "VENV_EXISTS=0"
)

if exist ".env" (echo [OK] Fichier .env: PRESENT) else (echo [ERREUR] Fichier .env: ABSENT)
if exist "requirements.txt" (echo [OK] Requirements.txt: PRESENT) else (echo [ERREUR] Requirements.txt: ABSENT)
if exist "start_neuro.py" (echo [OK] Script principal: PRESENT) else (echo [ERREUR] Script principal: ABSENT)

echo.
echo === TEST PYTHON ===
python --version
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas disponible dans le PATH
    echo Installez Python 3.10+ depuis https://python.org
    goto SHOW_RECOMMENDATIONS
)

echo.
echo === TEST ENVIRONNEMENT VIRTUEL ===
if "%VENV_EXISTS%"=="1" (
    echo [*] Activation de l'environnement virtuel...
    call llama-venv\Scripts\activate.bat
    
    echo [*] Test du Python dans l'environnement virtuel:
    python -c "import sys; print(f'[OK] Python venv: {sys.executable}')"
    
    echo.
    echo [*] Test des modules critiques:
    call :TEST_MODULE dotenv "python-dotenv"
    call :TEST_MODULE discord "discord.py"
    call :TEST_MODULE pyotp "pyotp"  
    call :TEST_MODULE llama_cpp "llama-cpp-python"
    call :TEST_MODULE PySide6 "PySide6 (GUI)"
    
    echo.
    echo [*] Test de la base de donnees:
    python -c "from database import init_database; print('[OK] Database module OK')" 2>nul && echo [OK] Base de donnees accessible || echo [ATTENTION] Probleme avec la base de donnees
    
    goto SHOW_RECOMMENDATIONS
) else (
    echo [ERREUR] Environnement virtuel absent - impossible de tester les modules
)

:SHOW_RECOMMENDATIONS
echo.
echo === ETAT GLOBAL ===
if "%VENV_EXISTS%"=="1" (
    echo [OK] Environnement virtuel configure
) else (
    echo [ERREUR] Environnement virtuel requis
)

echo.
echo === ACTIONS RECOMMANDEES ===
if "%VENV_EXISTS%"=="0" (
    echo [*] Reconstruire l'environnement: batch\rebuild_env.bat
) else (
    echo [*] Reparer si modules manquants: batch\repair.bat
)
echo [*] Documentation complete: batch\README.md
echo [*] Demarrage: batch\launch_neuro.bat

echo.
pause
exit /b 0

:TEST_MODULE
python -c "import %1" 2>nul
if %errorlevel% equ 0 (
    echo [OK] %~2
) else (
    echo [ERREUR] %~2 manquant
)
goto :eof