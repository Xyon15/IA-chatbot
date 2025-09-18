@echo off
REM ================================
REM 🤖 Neuro-Bot - Logs Viewer
REM Lanceur direct du système de logs
REM ================================

title Neuro-Bot - Logs Viewer

REM Couleurs pour un affichage moderne
color 0A

echo.
echo ================================
echo 🤖 NEURO-BOT - LOGS VIEWER
echo ================================
echo.

REM Vérification du répertoire de travail
cd /d "%~dp0"
echo 📁 Répertoire: %CD%

REM Vérification de l'environnement virtuel
if not exist "llama-venv\Scripts\python.exe" (
    echo ❌ ERREUR: Environnement virtuel llama-venv non trouvé!
    echo 💡 Assurez-vous que llama-venv existe dans le répertoire.
    pause
    exit /b 1
)

REM Vérification du fichier log viewer
if not exist "gui\tools\log_viewer_gui.py" (
    echo ❌ ERREUR: Log viewer non trouvé!
    echo 📁 Fichier manquant: gui\tools\log_viewer_gui.py
    pause
    exit /b 1
)

echo ✅ Environnement virtuel détecté
echo ✅ Log viewer détecté

REM Activation de l'environnement virtuel et lancement
echo.
echo 🚀 Lancement du visualiseur de logs...
echo.

REM Lancer le log viewer avec l'environnement virtuel
"llama-venv\Scripts\python.exe" "gui\tools\log_viewer_gui.py"

REM Gestion des codes de retour
if errorlevel 1 (
    echo.
    echo ❌ Erreur lors du lancement du log viewer
    echo 💡 Vérifiez que toutes les dépendances sont installées
    echo.
    pause
) else (
    echo.
    echo ✅ Log viewer fermé normalement
)

REM Fin du script
echo.
echo 👋 Fermeture du lanceur...
timeout /t 2 /nobreak > nul

exit /b 0