@echo off
echo Nettoyage des fichiers temporaires...
cd /d "%~dp0\.."

echo.
echo Suppression des caches Python...
if exist __pycache__ rmdir /s /q __pycache__
if exist commands\__pycache__ rmdir /s /q commands\__pycache__
if exist events\__pycache__ rmdir /s /q events\__pycache__
if exist tools\__pycache__ rmdir /s /q tools\__pycache__

echo.
echo Suppression des fichiers temporaires...
del /q *.tmp 2>nul
del /q *.log~ 2>nul
del /q data\*.db-shm 2>nul
del /q data\*.db-wal 2>nul

echo.
echo Suppression des anciens backups...
del /q data\*.backup_* 2>nul

echo.
echo ✅ Nettoyage terminé !
pause