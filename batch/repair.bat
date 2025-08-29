@echo off
title Neuro-Bot - Réparation
color 0A

echo.
echo =======================================================
echo          NEURO-BOT - REPARATION AUTOMATIQUE
echo =======================================================
echo.

REM Aller vers le dossier parent du projet
cd /d "%~dp0.."

echo 🔧 Réparation de l'environnement Neuro-Bot...
echo.

REM Vérifier si Python est disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou pas dans le PATH!
    echo Installez Python 3.10+ depuis https://python.org
    pause
    exit /b 1
)

echo ✅ Python détecté: 
python --version

echo.
echo 📁 Vérification/création de l'environnement virtuel...
if not exist "llama-venv" (
    echo 🆕 Création de l'environnement virtuel...
    python -m venv llama-venv
    if %errorlevel% neq 0 (
        echo ❌ Échec de la création de l'environnement virtuel
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé
) else (
    echo ✅ Environnement virtuel existe déjà
)

echo.
echo 🔄 Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo 📦 Mise à jour de pip...
python -m pip install --upgrade pip

echo.
echo 📋 Installation/mise à jour des dépendances...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ⚠️ Certaines dépendances ont échoué, installation manuelle...
        echo.
        echo 📦 Installation des packages essentiels...
        pip install discord.py
        pip install llama-cpp-python
        pip install python-dotenv
        pip install pyotp
        pip install pynvml
        pip install aiohttp
        pip install selectolax
        pip install transformers
        echo.
        echo 📦 Installation des packages optionnels...
        pip install PySide6
    )
) else (
    echo ❌ Fichier requirements.txt non trouvé!
    echo Installation manuelle des packages essentiels...
    pip install discord.py llama-cpp-python python-dotenv pyotp pynvml aiohttp selectolax transformers PySide6
)

echo.
echo 🧪 Test des imports critiques...
python -c "try: import dotenv; print('✅ python-dotenv: OK')
except ImportError: print('❌ python-dotenv: ÉCHEC')"

python -c "try: import discord; print('✅ discord.py: OK')
except ImportError: print('❌ discord.py: ÉCHEC')"

python -c "try: import llama_cpp; print('✅ llama-cpp-python: OK')
except ImportError: print('❌ llama-cpp-python: ÉCHEC')"

python -c "try: import pyotp; print('✅ pyotp: OK')
except ImportError: print('❌ pyotp: ÉCHEC')"

echo.
echo 📄 Vérification du fichier .env...
if exist ".env" (
    echo ✅ Fichier .env présent
    findstr /C:"DISCORD_TOKEN" .env >nul
    if %errorlevel% equ 0 (
        echo ✅ DISCORD_TOKEN configuré
    ) else (
        echo ⚠️ DISCORD_TOKEN non trouvé dans .env
    )
) else (
    echo ❌ Fichier .env manquant!
    echo.
    echo Créez un fichier .env avec:
    echo DISCORD_TOKEN=votre_token_ici
    echo AUTH_SECRET=votre_secret_2fa_optionnel
)

echo.
echo 🗄️ Initialisation de la base de données...
python -c "try: from database import init_database; init_database(); print('✅ Base de données initialisée')
except Exception as e: print('⚠️ Erreur base de données:', str(e))"

echo.
if %errorlevel% equ 0 (
    echo ✅ RÉPARATION TERMINÉE AVEC SUCCÈS!
    echo.
    echo 🚀 Vous pouvez maintenant lancer:
    echo   - launch_neuro.bat ^(menu principal^)
    echo   - start_bot.bat ^(bot Discord^)
    echo   - start_gui.bat ^(interface graphique^)
) else (
    echo ⚠️ Réparation terminée avec des avertissements
    echo Vérifiez les messages ci-dessus
)

echo.
pause