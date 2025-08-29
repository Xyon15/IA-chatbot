@echo off
title Neuro-Bot - Lanceur
color 0F

:MENU
cls
echo.
echo =======================================================
echo                NEURO-BOT - LANCEUR
echo =======================================================
echo.
echo Choisissez le mode de démarrage:
echo.
echo [1] Bot Discord (mode automatique)
echo [2] Interface Graphique 
echo [3] Bot Discord (mode interactif)
echo [4] Configuration et tests
echo [5] Diagnostic et réparation
echo [6] Quitter
echo.

set /p choix="Votre choix (1-6): "

if "%choix%"=="1" goto BOT_AUTO
if "%choix%"=="2" goto GUI
if "%choix%"=="3" goto BOT_INTERACTIF
if "%choix%"=="4" goto SETUP
if "%choix%"=="5" goto DIAGNOSTIC
if "%choix%"=="6" goto END

echo Option invalide!
timeout /t 2 >nul
goto MENU

:BOT_AUTO
cls
echo.
echo =======================================================
echo            BOT DISCORD - MODE AUTOMATIQUE
echo =======================================================
echo.

cd /d "%~dp0.."

if not exist "llama-venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé!
    call :SHOW_SETUP_HELP
    goto MENU
)

echo 🔄 Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo 🚀 Démarrage automatique avec optimisation GPU...
python start_neuro.py --auto

if %errorlevel% neq 0 (
    call :SHOW_ERROR %errorlevel%
)

echo.
echo Appuyez sur une touche pour retourner au menu...
pause >nul
goto MENU

:BOT_INTERACTIF
cls
echo.
echo =======================================================
echo            BOT DISCORD - MODE INTERACTIF
echo =======================================================
echo.

cd /d "%~dp0.."

if not exist "llama-venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé!
    call :SHOW_SETUP_HELP
    goto MENU
)

echo 🔄 Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo 🚀 Démarrage interactif (vous pourrez choisir les options GPU)...
python start_neuro.py

if %errorlevel% neq 0 (
    call :SHOW_ERROR %errorlevel%
)

echo.
echo Appuyez sur une touche pour retourner au menu...
pause >nul
goto MENU

:GUI
cls
echo.
echo =======================================================
echo              INTERFACE GRAPHIQUE
echo =======================================================
echo.

cd /d "%~dp0.."

if not exist "llama-venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé!
    call :SHOW_SETUP_HELP
    goto MENU
)

echo 🔄 Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo 🎨 Démarrage de l'interface graphique...
python start_neuro.py --gui --auto

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors du démarrage de l'interface graphique
    echo.
    echo Solutions:
    echo   - Installez PySide6: pip install PySide6
    echo   - Vérifiez les logs d'erreur
)

echo.
echo Appuyez sur une touche pour retourner au menu...
pause >nul
goto MENU

:SETUP
cls
echo.
echo =======================================================
echo              CONFIGURATION ET TESTS
echo =======================================================
echo.

cd /d "%~dp0.."

if exist "batch\setup.bat" (
    echo 🔧 Lancement de la configuration...
    call batch\setup.bat
) else (
    echo ❌ Fichier setup.bat non trouvé!
    echo.
    echo Assurez-vous d'être dans le bon dossier et que tous les fichiers sont présents.
)

echo.
echo Appuyez sur une touche pour retourner au menu...
pause >nul
goto MENU

:SHOW_SETUP_HELP
echo.
echo Pour configurer le projet, exécutez d'abord:
echo   setup.bat
echo.
echo Ou créez l'environnement virtuel manuellement:
echo   python -m venv llama-venv
echo   llama-venv\Scripts\activate.bat
echo   pip install -r requirements.txt
goto :eof

:SHOW_ERROR
echo.
echo ❌ Le programme s'est arrêté avec une erreur (code: %1)
echo.
echo Solutions possibles:
echo   1. Vérifiez le fichier .env (DISCORD_TOKEN, AUTH_SECRET)
echo   2. Vérifiez votre connexion internet
echo   3. Consultez les logs dans le dossier 'logs'
echo   4. Relancez en mode interactif pour plus d'informations
goto :eof

:DIAGNOSTIC
cls
echo.
echo =======================================================
echo            DIAGNOSTIC ET REPARATION
echo =======================================================
echo.

echo Choisissez une option:
echo.
echo [1] Diagnostic rapide
echo [2] Réparation automatique 
echo [3] Reconstruction complète de l'environnement
echo [4] Retour au menu principal
echo.

set /p diag_choix="Votre choix (1-4): "

cd /d "%~dp0.."

if "%diag_choix%"=="1" (
    echo 🔍 Diagnostic en cours...
    call batch\diagnostic.bat
) else if "%diag_choix%"=="2" (
    echo 🛠️ Réparation en cours...
    call batch\repair.bat
) else if "%diag_choix%"=="3" (
    echo 🏗️ Reconstruction complète...
    call batch\rebuild_env.bat
) else if "%diag_choix%"=="4" (
    goto MENU
) else (
    echo Option invalide!
    timeout /t 2 >nul
    goto DIAGNOSTIC
)

echo.
echo Appuyez sur une touche pour retourner au menu...
pause >nul
goto MENU

:END
cls
echo.
echo =======================================================
echo                    AU REVOIR!
echo =======================================================
echo.
echo Merci d'avoir utilisé Neuro-Bot!
echo.
timeout /t 2 >nul
exit /b 0