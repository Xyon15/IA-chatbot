@echo off
title Neuro-Bot - Reparation
color 0A

echo.
echo =======================================================
echo          NEURO-BOT - REPARATION AUTOMATIQUE
echo =======================================================
echo.

REM Aller vers le dossier parent du projet
cd /d "%~dp0.."

echo [*] Reparation de l'environnement Neuro-Bot...
echo.

REM Verifier si Python est disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH!
    echo Installez Python 3.10+ depuis https://python.org
    pause
    exit /b 1
)

echo [OK] Python detecte: 
python --version

echo.
echo [*] Verification/creation de l'environnement virtuel...
if not exist "llama-venv" (
    echo [+] Creation de l'environnement virtuel...
    python -m venv llama-venv
    if %errorlevel% neq 0 (
        echo [ERREUR] Echec de la creation de l'environnement virtuel
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel cree
) else (
    echo [OK] Environnement virtuel existe deja
)

echo.
echo [*] Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo [*] Mise a jour de pip...
python -m pip install --upgrade pip

echo.
echo [*] Installation/mise a jour des dependances...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ATTENTION] Certaines dependances ont echoue, installation manuelle...
        echo.
        echo [*] Installation des packages essentiels...
        pip install discord.py
        pip install llama-cpp-python
        pip install python-dotenv
        pip install pyotp
        pip install pynvml
        pip install aiohttp
        pip install selectolax
        pip install transformers
        echo.
        echo [*] Installation des packages optionnels...
        pip install PySide6
    )
) else (
    echo [ERREUR] Fichier requirements.txt non trouve!
    echo Installation manuelle des packages essentiels...
    pip install discord.py llama-cpp-python python-dotenv pyotp pynvml aiohttp selectolax transformers PySide6
)

echo.
echo [*] Test des imports critiques...
python -c "try: import dotenv; print('[OK] python-dotenv: OK')
except ImportError: print('[ERREUR] python-dotenv: ECHEC')"

python -c "try: import discord; print('[OK] discord.py: OK')
except ImportError: print('[ERREUR] discord.py: ECHEC')"

python -c "try: import llama_cpp; print('[OK] llama-cpp-python: OK')
except ImportError: print('[ERREUR] llama-cpp-python: ECHEC')"

python -c "try: import pyotp; print('[OK] pyotp: OK')
except ImportError: print('[ERREUR] pyotp: ECHEC')"

echo.
echo [*] Verification du fichier .env...
if exist ".env" (
    echo [OK] Fichier .env present
    findstr /C:"DISCORD_TOKEN" .env >nul
    if %errorlevel% equ 0 (
        echo [OK] DISCORD_TOKEN configure
    ) else (
        echo [ATTENTION] DISCORD_TOKEN non trouve dans .env
    )
) else (
    echo [ERREUR] Fichier .env manquant!
    echo.
    echo Creez un fichier .env avec:
    echo DISCORD_TOKEN=votre_token_ici
    echo AUTH_SECRET=votre_secret_2fa_optionnel
)

echo.
echo [*] Initialisation de la base de donnees...
python -c "try: from database import init_database; init_database(); print('[OK] Base de donnees initialisee')
except Exception as e: print('[ATTENTION] Erreur base de donnees:', str(e))"

echo.
if %errorlevel% equ 0 (
    echo [OK] REPARATION TERMINEE AVEC SUCCES!
    echo.
    echo [*] Vous pouvez maintenant lancer:
    echo   - launch_neuro.bat (menu principal)
    echo   - start_bot.bat (bot Discord)
    echo   - start_gui.bat (interface graphique)
) else (
    echo [ATTENTION] Reparation terminee avec des avertissements
    echo Verifiez les messages ci-dessus
)

echo.
pause