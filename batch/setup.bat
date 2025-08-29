@echo off
echo.
echo =======================================================
echo                NEURO-BOT SETUP
echo =======================================================
echo.

echo 1. Activation de l'environnement virtuel...
call llama-venv\Scripts\activate.bat

echo.
echo 2. Installation/mise a jour des dependances...
pip install -r requirements.txt

echo.
echo 3. Verification de la configuration...
if not exist .env (
    echo ATTENTION: Fichier .env manquant!
    echo Copiez le fichier .env.example et configurez vos tokens.
    pause
    exit /b 1
)

echo.
echo 4. Test d'import des modules principaux...
python -c "import discord; import llama_cpp; from tools.gpu_optimizer import gpu_optimizer; print('[OK] Tous les imports OK')"

if %errorlevel% neq 0 (
    echo [ERREUR] Erreur dans les imports
    pause
    exit /b 1
)

echo.
echo [OK] Setup termine avec succes!
echo.
echo Pour demarrer:
echo   - Bot Discord: python start_neuro.py
echo   - Interface graphique: python start_neuro.py --gui
echo.
pause