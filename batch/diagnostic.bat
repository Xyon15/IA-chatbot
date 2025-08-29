@echo off
title Neuro-Bot - Diagnostic
color 0C

echo.
echo =======================================================
echo          NEURO-BOT - DIAGNOSTIC COMPLET
echo =======================================================
echo.

REM Aller vers le dossier parent du projet
cd /d "%~dp0.."

echo 🔍 Diagnostic de l'environnement...
echo.

echo === VERIFICATION DES FICHIERS ===
if exist "llama-venv\Scripts\activate.bat" (
    echo ✅ Environnement virtuel : PRESENT
) else (
    echo ❌ Environnement virtuel : ABSENT
)

if exist ".env" (
    echo ✅ Fichier .env : PRESENT
) else (
    echo ❌ Fichier .env : ABSENT
)

if exist "requirements.txt" (
    echo ✅ Requirements.txt : PRESENT
) else (
    echo ❌ Requirements.txt : ABSENT
)

echo.
echo === TEST DE L'ENVIRONNEMENT VIRTUEL ===
if exist "llama-venv\Scripts\activate.bat" (
    echo 🔄 Activation de l'environnement virtuel...
    call llama-venv\Scripts\activate.bat
    
    echo.
    echo 🐍 Version Python:
    python --version
    
    echo.
    echo 📦 Test des modules critiques:
    python -c "try: import dotenv; print('✅ python-dotenv: OK')
except ImportError: print('❌ python-dotenv: MANQUANT')"
    python -c "try: import discord; print('✅ discord.py: OK')
except ImportError: print('❌ discord.py: MANQUANT')"
    python -c "try: import llama_cpp; print('✅ llama-cpp-python: OK')
except ImportError: print('❌ llama-cpp-python: MANQUANT')"
    python -c "try: import pyotp; print('✅ pyotp: OK')
except ImportError: print('❌ pyotp: MANQUANT')"
    python -c "try: import PySide6; print('✅ PySide6: OK')
except ImportError: print('❌ PySide6: MANQUANT')"
    
    echo.
    echo 📋 Liste des packages installés:
    pip list | findstr -i "discord dotenv llama pyotp pyside"
    
) else (
    echo ❌ Impossible de tester - environnement virtuel absent
)

echo.
echo === RECOMMANDATIONS ===
if not exist "llama-venv\Scripts\activate.bat" (
    echo 1. Créer l'environnement virtuel: python -m venv llama-venv
)
echo 2. Installer les dépendances: pip install -r requirements.txt
echo 3. Vérifier le fichier .env avec DISCORD_TOKEN
echo.

pause