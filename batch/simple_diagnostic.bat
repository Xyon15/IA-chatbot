@echo off
title Neuro-Bot - Diagnostic Simple
color 0C

echo.
echo =======================================================
echo          NEURO-BOT - DIAGNOSTIC SIMPLE
echo =======================================================
echo.

REM Aller vers le dossier parent du projet
cd /d "%~dp0.."

echo 🔍 Diagnostic rapide...
echo.

echo === FICHIERS REQUIS ===
if exist "llama-venv\Scripts\activate.bat" (echo ✅ Environnement virtuel) else (echo ❌ Environnement virtuel manquant)
if exist ".env" (echo ✅ Fichier .env) else (echo ❌ Fichier .env manquant)
if exist "requirements.txt" (echo ✅ Requirements.txt) else (echo ❌ Requirements.txt manquant)
if exist "start_neuro.py" (echo ✅ Script principal) else (echo ❌ Script principal manquant)

echo.
echo === TEST PYTHON ET ENVIRONNEMENT VIRTUEL ===
python --version
if %errorlevel% neq 0 (
    echo ❌ Python non disponible
    goto END_DIAGNOSTIC
)

if exist "llama-venv\Scripts\activate.bat" (
    echo 🔄 Test de l'environnement virtuel...
    call llama-venv\Scripts\activate.bat
    
    echo 📦 Test des imports de base...
    python -c "import sys; print('✅ Python fonctionne dans venv')"
    if %errorlevel% neq 0 (
        echo ❌ Problème avec l'environnement virtuel
        goto END_DIAGNOSTIC
    )
    
    echo 🧪 Test modules essentiels...
    python -c "import dotenv" 2>nul && echo ✅ python-dotenv || echo ❌ python-dotenv manquant
    python -c "import discord" 2>nul && echo ✅ discord.py || echo ❌ discord.py manquant  
    python -c "import pyotp" 2>nul && echo ✅ pyotp || echo ❌ pyotp manquant
    python -c "import llama_cpp" 2>nul && echo ✅ llama-cpp-python || echo ❌ llama-cpp-python manquant
    python -c "import PySide6" 2>nul && echo ✅ PySide6 || echo ⚠️ PySide6 manquant (optionnel)
) else (
    echo ❌ Environnement virtuel non trouvé
)

:END_DIAGNOSTIC
echo.
echo === RECOMMANDATIONS ===
if not exist "llama-venv\Scripts\activate.bat" (
    echo 🏗️ Utilisez rebuild_env.bat pour recréer l'environnement
)
echo 🔧 En cas de modules manquants, utilisez repair.bat
echo 📖 Consultez batch\README.md pour plus d'informations

echo.
pause