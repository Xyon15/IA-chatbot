@echo off
echo Demarrage de l'interface principale amelioree de Neuro-Bot...
echo.

REM Activation de l'environnement virtuel si il existe
if exist "llama-venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call llama-venv\Scripts\activate.bat
)

REM Lancement de l'interface
echo Lancement de l'interface graphique...
python launch_enhanced_gui.py

echo.
echo Interface fermee. Appuyez sur une touche pour quitter...
pause >nul