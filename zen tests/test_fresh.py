#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Aller dans le bon repertoire
os.chdir(str(Path("..").absolute()))

from dotenv import load_dotenv

print("Test Simple Post-Redemarrage")
print("=" * 35)

# Nettoyage complet
for var in ['DISCORD_TOKEN', 'AUTH_SECRET']:
    if var in os.environ:
        del os.environ[var]
        print(f"Variable {var} supprimee")

# Nettoyage des modules
modules_to_remove = [name for name in sys.modules if any(k in name.lower() for k in ['config', 'dotenv'])]
for module in modules_to_remove:
    del sys.modules[module]
    print(f"Module {module} supprime")

# Chargement frais
load_dotenv('.env')
token = os.getenv('DISCORD_TOKEN')

if token:
    print(f"Token charge: {token[:20]}...{token[-10:]}")
    print(f"Longueur: {len(token)}")
    
    # Test rapide avec requests
    try:
        import requests
        
        headers = {"Authorization": f"Bot {token}"}
        response = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
        
        print(f"Statut Discord: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Bot connecte: {data['username']}#{data.get('discriminator', '0000')}")
            print("TOKEN VALIDE!")
            
            print("\nLancement du bot maintenant...")
            import subprocess
            subprocess.run(["python", "start_bot.py"])
            
        else:
            print(f"Erreur: {response.text}")
    except ImportError:
        print("Module requests non disponible, test avec aiohttp...")
        
        import asyncio
        import aiohttp
        
        async def test_token():
            headers = {"Authorization": f"Bot {token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"Bot: {data['username']}#{data.get('discriminator', '0000')}")
                        print("TOKEN VALIDE!")
                        return True
                    else:
                        print(f"Erreur: {response.status}")
                        return False
        
        success = asyncio.run(test_token())
        if success:
            print("Lancement du bot...")
            import subprocess
            subprocess.run(["python", "start_bot.py"])
else:
    print("Aucun token trouve")