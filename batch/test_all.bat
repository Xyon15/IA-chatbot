@echo off
title Test Scripts Batch
color 0E

echo.
echo =======================================================
echo          TEST COMPLET DES SCRIPTS BATCH
echo =======================================================
echo.

cd /d "%~dp0.."

echo 🧪 Test de la structure des dossiers...
if exist "llama-venv" (echo ✅ Environnement virtuel) else (echo ❌ Environnement virtuel manquant)
if exist ".env" (echo ✅ Fichier .env) else (echo ❌ Fichier .env manquant)
if exist "start_neuro.py" (echo ✅ Script principal) else (echo ❌ Script principal manquant)

echo.
echo 🧪 Test de Python et activation environnement...
python --version
call llama-venv\Scripts\activate.bat
python -c "import sys; print(f'✅ Python dans venv: {sys.executable}')"

echo.
echo 🧪 Test des chemins des scripts...
echo Dossier actuel: %cd%
if exist "batch\final_diagnostic.bat" (echo ✅ final_diagnostic.bat trouvé) else (echo ❌ final_diagnostic.bat manquant)
if exist "batch\start_bot.bat" (echo ✅ start_bot.bat trouvé) else (echo ❌ start_bot.bat manquant)
if exist "batch\start_gui.bat" (echo ✅ start_gui.bat trouvé) else (echo ❌ start_gui.bat manquant)
if exist "batch\launch_neuro.bat" (echo ✅ launch_neuro.bat trouvé) else (echo ❌ launch_neuro.bat manquant)

echo.
echo 🧪 Test modules Python critiques...
python -c "import dotenv; print('✅ dotenv OK')" || echo ❌ dotenv ÉCHEC
python -c "import discord; print('✅ discord OK')" || echo ❌ discord ÉCHEC
python -c "import llama_cpp; print('✅ llama_cpp OK')" || echo ❌ llama_cpp ÉCHEC

echo.
echo === RÉSUMÉ ===
echo ✅ Tests terminés - Vérifiez les résultats ci-dessus
echo.
echo 📖 Pour plus de détails: batch\final_diagnostic.bat
echo 🚀 Pour démarrer: batch\start_bot.bat
echo.
pause