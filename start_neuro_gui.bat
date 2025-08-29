@echo off
title Neuro-Bot - Interface Graphique Principale
color 0B

echo.
echo ===============================================
echo       NEURO-BOT - INTERFACE GRAPHIQUE
echo               Version Consolidee
echo ===============================================
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
) else (
    echo [AVERTISSEMENT] Environnement virtuel non trouve, utilisation de Python global
    echo Pour des performances optimales, creez un environnement virtuel:
    echo   python -m venv llama-venv
    echo   llama-venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
)

REM Verification des dependances critiques
echo [INFO] Verification des dependances...
python -c "import PySide6; print('[OK] PySide6 disponible')" 2>nul || (
    echo [ERREUR] PySide6 non installe
    echo Installation automatique...
    pip install PySide6
)

python -c "import discord; print('[OK] discord.py disponible')" 2>nul || (
    echo [AVERTISSEMENT] discord.py non trouve, certaines fonctionnalites peuvent etre limitees
)

python -c "import psutil; print('[OK] psutil disponible')" 2>nul || (
    echo [AVERTISSEMENT] psutil non trouve, monitoring systeme limite
)

echo.
echo [INFO] Lancement de l'interface graphique amelioree...
echo.
echo Fonctionnalites du nouveau GUI:
echo   - Interface moderne avec indicateurs circulaires
echo   - Design sombre optimise
echo   - Monitoring temps reel (CPU/RAM/GPU)
echo   - Raccourcis clavier (F5, Ctrl+R, Ctrl+L, F1)
echo   - Logs optimises avec limite intelligente
echo   - Controle du bot Discord integre
echo.

REM Lancement de l'interface GUI améliorée (nouveau)
python launch_gui.py

REM Gestion des erreurs
if errorlevel 1 (
    echo.
    echo [ERREUR] L'interface graphique s'est fermee avec une erreur (code: %errorlevel%)
    echo.
    echo Solutions possibles:
    echo   1. Verifiez l'installation de PySide6: pip install PySide6
    echo   2. Liberez de la VRAM si vous utilisez le GPU pour autre chose
    echo   3. Verifiez les permissions sur le fichier de base de donnees
    echo   4. Consultez les logs pour plus de details
    echo.
    echo Tentative de diagnostic automatique...
    echo.
    
    REM Diagnostic de base
    python -c "import sys; print(f'Python version: {sys.version}')"
    python -c "import PySide6" >nul 2>&1 && (echo PySide6: OK) || (echo PySide6: ERREUR)
    python -c "import sqlite3" >nul 2>&1 && (echo SQLite3: OK) || (echo SQLite3: ERREUR)
    
    echo.
) else (
    echo.
    echo [OK] Interface graphique fermee proprement
    echo Merci d'avoir utilise Neuro-Bot!
)

echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul