@echo off
echo Redemarrage Propre de Neuro-Bot
echo =====================================

echo Nettoyage des variables d'environnement...
set DISCORD_TOKEN=
set AUTH_SECRET=

echo Positionnement dans le repertoire...
cd /d "c:\Dev\IA-chatbot"

echo Verification du token dans .env...
findstr "DISCORD_TOKEN" .env

echo Demarrage du bot avec un environnement propre...
python start_bot.py

pause