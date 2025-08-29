@echo off
title Neuro-Bot - Reconstruction Environnement
color 0D

echo.
echo =======================================================
echo      NEURO-BOT - RECONSTRUCTION ENVIRONNEMENT
echo =======================================================
echo.

REM Aller vers le dossier parent du projet
cd /d "%~dp0.."

echo 🔧 Reconstruction complète de l'environnement virtuel...
echo.

REM Supprimer l'ancien environnement virtuel
echo 🗑️ Suppression de l'ancien environnement virtuel...
if exist "llama-venv" (
    rmdir /s /q "llama-venv"
    echo ✅ Ancien environnement supprimé
) else (
    echo ℹ️ Pas d'ancien environnement à supprimer
)

echo.
echo 🆕 Création du nouvel environnement virtuel...
python -m venv llama-venv
if %errorlevel% neq 0 (
    echo ❌ Échec de la création de l'environnement virtuel
    echo Vérifiez que Python 3.10+ est installé
    pause
    exit /b 1
)
echo ✅ Nouvel environnement créé

echo.
echo 🔄 Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo 📦 Mise à jour de pip...
python -m pip install --upgrade pip

echo.
echo 📋 Installation des dépendances essentielles...
pip install python-dotenv
pip install discord.py
pip install pyotp
pip install pynvml
pip install aiohttp
pip install selectolax
pip install transformers

echo.
echo 🚀 Installation de llama-cpp-python (peut prendre du temps)...
pip install llama-cpp-python

echo.
echo 🎨 Installation des dépendances optionnelles...
pip install PySide6

echo.
echo 🧪 Test final des imports...
python -c "import dotenv; print('✅ python-dotenv: OK')"
python -c "import discord; print('✅ discord.py: OK')"
python -c "import pyotp; print('✅ pyotp: OK')"
python -c "import llama_cpp; print('✅ llama-cpp-python: OK')"
python -c "import PySide6; print('✅ PySide6: OK')"

echo.
echo 🗄️ Test de la base de données...
python -c "from database import init_database; init_database(); print('✅ Base de données OK')"

echo.
echo ✅ RECONSTRUCTION TERMINÉE AVEC SUCCÈS!
echo.
echo 🚀 Vous pouvez maintenant lancer le bot:
echo   batch\launch_neuro.bat
echo.
pause