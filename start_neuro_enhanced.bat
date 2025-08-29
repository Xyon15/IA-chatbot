@echo off
title Neuro-Bot - Interface Principale Amelioree

echo.
echo ==========================================
echo   NEURO-BOT - INTERFACE PRINCIPALE
echo           (Version Amelioree)
echo ==========================================
echo.

REM Verification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Activation de l'environnement virtuel si il existe
if exist "llama-venv\Scripts\activate.bat" (
    echo [INFO] Activation de l'environnement virtuel...
    call llama-venv\Scripts\activate.bat
    echo.
)

echo [INFO] Lancement de l'interface principale amelioree...
echo.
echo Fonctionnalites:
echo   - Indicateurs circulaires temps reel
echo   - Design moderne sombre
echo   - Raccourcis clavier (F5, Ctrl+R, Ctrl+L, F1)
echo   - Logs optimises avec horodatage
echo   - Monitoring GPU/CPU/RAM complet
echo.

REM Lancement de l'interface améliorée
python launch_enhanced_gui.py

REM Gestion des erreurs
if errorlevel 1 (
    echo.
    echo [ERREUR] Une erreur s'est produite lors du lancement
    echo Verifiez que PySide6 est installe: pip install PySide6
)

echo.
echo Interface fermee. Appuyez sur une touche pour quitter...
pause >nul