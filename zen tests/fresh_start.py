#!/usr/bin/env python3
"""
Démarrage frais avec nettoyage complet
"""

import os
import subprocess
import sys
from pathlib import Path

def create_restart_script():
    """Crée un script de redémarrage propre"""
    
    restart_script = '''
@echo off
echo 🔄 Redémarrage Propre de Neuro-Bot
echo =====================================

echo 🧹 Nettoyage des variables d'environnement...
set DISCORD_TOKEN=
set AUTH_SECRET=

echo 📂 Positionnement dans le répertoire...
cd /d "c:\\Dev\\IA-chatbot"

echo 🔍 Vérification du token dans .env...
findstr "DISCORD_TOKEN" .env

echo 🚀 Démarrage du bot avec un environnement propre...
python start_bot.py

pause
'''
    
    with open('restart_clean.bat', 'w') as f:
        f.write(restart_script)
    
    print("📝 Script restart_clean.bat créé")

def create_test_script():
    """Crée un script de test simple"""
    
    test_script = '''#!/usr/bin/env python3
import os
from dotenv import load_dotenv

print("🔬 Test Simple Post-Redémarrage")
print("=" * 35)

# Nettoyage complet
for var in ['DISCORD_TOKEN', 'AUTH_SECRET']:
    if var in os.environ:
        del os.environ[var]
        print(f"🧹 {var} supprimé")

# Chargement frais
load_dotenv('.env')
token = os.getenv('DISCORD_TOKEN')

if token:
    print(f"🔑 Token chargé: {token[:20]}...{token[-10:]}")
    print(f"📏 Longueur: {len(token)}")
    
    # Test rapide avec requests
    import requests
    
    headers = {"Authorization": f"Bot {token}"}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
    
    print(f"📡 Statut Discord: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Bot: {data['username']}#{data.get('discriminator', '0000')}")
        print("🎉 TOKEN VALIDE!")
    else:
        print(f"❌ Erreur: {response.text}")
else:
    print("❌ Aucun token trouvé")
'''
    
    with open('test_fresh.py', 'w') as f:
        f.write(test_script)
    
    print("📝 Script test_fresh.py créé")

def main():
    """Fonction principale"""
    print("🔧 Préparation du Redémarrage Propre")
    print("=" * 40)
    
    # Se placer dans le bon répertoire
    os.chdir("c:/Dev/IA-chatbot/zen tests")
    
    # Créer les scripts
    create_restart_script()
    create_test_script()
    
    print("\n📋 Instructions pour Redémarrage Propre:")
    print("1. 🔴 Fermez cette fenêtre PowerShell")
    print("2. 🆕 Ouvrez une NOUVELLE fenêtre PowerShell")
    print("3. 📂 Allez dans: cd 'c:\\Dev\\IA-chatbot\\zen tests'")
    print("4. 🧪 Testez: python test_fresh.py")
    print("5. 🚀 Ou lancez: .\\restart_clean.bat")
    
    print("\n💡 Cela garantira un environnement 100% propre")

if __name__ == "__main__":
    main()