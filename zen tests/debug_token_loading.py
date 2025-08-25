#!/usr/bin/env python3
"""
Debug détaillé du chargement du token
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent
sys.path.append(str(Path("..").absolute()))
os.chdir(str(Path("..").absolute()))

def patch_config_loading():
    """Patche le chargement de config pour voir les détails"""
    
    # Supprimer tous les modules config/dotenv du cache
    modules_to_remove = []
    for name in sys.modules:
        if any(keyword in name.lower() for keyword in ['config', 'dotenv']):
            modules_to_remove.append(name)
    
    for name in modules_to_remove:
        del sys.modules[name]
        print(f"🧹 Module {name} supprimé")
    
    # Nettoyer l'environnement
    for var in ['DISCORD_TOKEN', 'AUTH_SECRET']:
        if var in os.environ:
            del os.environ[var]
            print(f"🧹 Variable {var} supprimée")
    
    # Monkey patch load_dotenv pour déboguer
    from dotenv import load_dotenv as original_load_dotenv
    
    def debug_load_dotenv(*args, **kwargs):
        print(f"🔍 load_dotenv appelé avec: args={args}, kwargs={kwargs}")
        result = original_load_dotenv(*args, **kwargs)
        print(f"🔍 load_dotenv résultat: {result}")
        
        # Afficher ce qui a été chargé
        token = os.getenv("DISCORD_TOKEN")
        if token:
            print(f"🔑 Token chargé: {token[:20]}...{token[-10:]} (len: {len(token)})")
        else:
            print("❌ Aucun token chargé")
        
        return result
    
    # Remplacer load_dotenv
    import dotenv
    dotenv.load_dotenv = debug_load_dotenv
    
    # Monkey patch os.getenv pour déboguer
    original_getenv = os.getenv
    
    def debug_getenv(key, default=None):
        value = original_getenv(key, default)
        if key in ['DISCORD_TOKEN', 'AUTH_SECRET']:
            if value:
                print(f"🔍 os.getenv('{key}') = {value[:20] if len(value) > 20 else value}{'...' if len(value) > 20 else ''}")
            else:
                print(f"🔍 os.getenv('{key}') = None")
        return value
    
    os.getenv = debug_getenv

def test_step_by_step():
    """Test étape par étape"""
    print("🔬 Test Étape par Étape du Chargement")
    print("=" * 45)
    
    # 1. Lire le fichier .env manuellement
    print("ÉTAPE 1: Lecture manuelle .env")
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
    
    for i, line in enumerate(content.split('\n'), 1):
        if line.startswith('DISCORD_TOKEN='):
            token = line.split('=', 1)[1]
            print(f"  Ligne {i}: Token manuel {token[:20]}...{token[-10:]} (len: {len(token)})")
    
    # 2. Tester dotenv
    print("\nÉTAPE 2: Test dotenv direct")
    from dotenv import load_dotenv
    result = load_dotenv('.env')
    print(f"  load_dotenv résultat: {result}")
    
    # 3. Tester la config
    print("\nÉTAPE 3: Test Config classe")
    from config import Config
    
    config = Config()
    print(f"  Config.TOKEN: {config.TOKEN[:20] if config.TOKEN else 'None'}...{config.TOKEN[-10:] if config.TOKEN and len(config.TOKEN) > 30 else config.TOKEN or 'None'}")

async def test_discord_connection_debug():
    """Test de connexion Discord avec debug"""
    print("\nÉTAPE 4: Test Connexion Discord")
    
    import aiohttp
    from config import Config
    
    config = Config()
    
    if not config.TOKEN:
        print("❌ Pas de token dans la config")
        return False
    
    print(f"🔑 Token utilisé: {config.TOKEN[:20]}...{config.TOKEN[-10:]}")
    
    headers = {
        "Authorization": f"Bot {config.TOKEN}",
        "User-Agent": "Neuro-Bot-Debug"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as response:
                print(f"📡 Réponse Discord: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Bot connecté: {data['username']}#{data.get('discriminator', '0000')}")
                    return True
                else:
                    print(f"❌ Erreur Discord: {response.status}")
                    text = await response.text()
                    print(f"   Réponse: {text}")
                    return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🔬 Debug Détaillé du Token Discord")
    print("=" * 45)
    
    # Patcher pour déboguer
    patch_config_loading()
    
    # Test étape par étape
    test_step_by_step()
    
    # Test Discord
    import asyncio
    success = asyncio.run(test_discord_connection_debug())
    
    if success:
        print("\n🎉 Token fonctionne! Le problème est ailleurs...")
    else:
        print("\n❌ Token ne fonctionne pas dans ce contexte")