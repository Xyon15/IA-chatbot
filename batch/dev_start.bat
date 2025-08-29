@echo off
title Neuro-Bot - Mode Développeur
color 0E

echo.
echo =======================================================
echo           NEURO-BOT - MODE DÉVELOPPEUR
echo =======================================================
echo.

REM Changer vers le dossier parent du projet (sortir du dossier batch)
cd /d "%~dp0.."

REM Vérifier si l'environnement virtuel existe
if not exist "llama-venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé!
    echo.
    echo Configuration automatique...
    echo.
    
    REM Créer l'environnement virtuel
    python -m venv llama-venv
    if %errorlevel% neq 0 (
        echo ❌ Impossible de créer l'environnement virtuel
        pause
        exit /b 1
    )
    
    REM Activer et installer les dépendances
    call llama-venv\Scripts\activate.bat
    pip install -r requirements.txt
    
    echo ✅ Environnement configuré!
    echo.
) else (
    echo 🔄 Activation de l'environnement virtuel...
    call llama-venv\Scripts\activate.bat
)

echo.
echo 🧪 Mode développeur - Lancement avec logs détaillés...
echo.
echo Options disponibles:
echo   - CTRL+C pour arrêter proprement
echo   - Les erreurs s'affichent en détail
echo   - Rechargement automatique de la config GPU
echo.

REM Lancer en mode développeur avec auto-optimisation GPU
python start_neuro.py --auto

echo.
if %errorlevel% equ 0 (
    echo ✅ Arrêt propre du bot
) else (
    echo ❌ Erreur détectée - Code: %errorlevel%
    echo.
    echo 📋 Vérifications recommandées:
    echo   1. Fichier .env correctement configuré?
    echo   2. Modèles LLM présents dans le dossier 'models'?
    echo   3. Base de données accessible?
    echo   4. Token Discord valide?
)

echo.
echo 🔧 Appuyez sur une touche pour fermer...
pause >nul