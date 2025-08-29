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

echo [*] Reconstruction complete de l'environnement virtuel...
echo.

REM Supprimer l'ancien environnement virtuel
echo [-] Suppression de l'ancien environnement virtuel...
if exist "llama-venv" (
    rmdir /s /q "llama-venv"
    echo [OK] Ancien environnement supprime
) else (
    echo [INFO] Pas d'ancien environnement a supprimer
)

echo.
echo [+] Creation du nouvel environnement virtuel...
python -m venv llama-venv
if %errorlevel% neq 0 (
    echo [ERREUR] Echec de la creation de l'environnement virtuel
    echo Verifiez que Python 3.10+ est installe
    pause
    exit /b 1
)
echo [OK] Nouvel environnement cree

echo.
echo [*] Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo [*] Mise a jour de pip...
python -m pip install --upgrade pip

echo.
echo [*] Installation des dependances essentielles...
pip install python-dotenv
pip install discord.py
pip install pyotp
pip install pynvml
pip install aiohttp
pip install selectolax
pip install transformers

echo.
echo [*] Installation de llama-cpp-python (peut prendre du temps)...
pip install llama-cpp-python

echo.
echo [*] Installation des dependances optionnelles...
pip install PySide6

echo.
echo [*] Test final des imports...
python -c "import dotenv; print('[OK] python-dotenv: OK')"
python -c "import discord; print('[OK] discord.py: OK')"
python -c "import pyotp; print('[OK] pyotp: OK')"
python -c "import llama_cpp; print('[OK] llama-cpp-python: OK')"
python -c "import PySide6; print('[OK] PySide6: OK')"

echo.
echo [*] Test de la base de donnees...
python -c "from database import init_database; init_database(); print('[OK] Base de donnees OK')"

echo.
echo [OK] RECONSTRUCTION TERMINEE AVEC SUCCES!
echo.
echo [*] Vous pouvez maintenant lancer le bot:
echo   batch\launch_neuro.bat
echo.
pause