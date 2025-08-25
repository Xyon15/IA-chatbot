#!/usr/bin/env python3
"""
Test minimaliste avec discord.py
"""

import os
import sys
import asyncio
from pathlib import Path
import discord

# Ajouter le répertoire parent
sys.path.append(str(Path("..").absolute()))
os.chdir(str(Path("..").absolute()))

def clear_environment():
    """Nettoie l'environnement"""
    for var in ['DISCORD_TOKEN', 'AUTH_SECRET']:
        if var in os.environ:
            del os.environ[var]
    
    # Nettoyer les modules
    modules_to_remove = [name for name in sys.modules if any(k in name.lower() for k in ['config', 'dotenv'])]
    for module in modules_to_remove:
        del sys.modules[module]

async def test_discord_py_minimal():
    """Test minimaliste avec discord.py"""
    print("🧪 Test Discord.py Minimaliste")
    print("=" * 35)
    
    # Charger le token directement
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Token non trouvé")
        return False
    
    print(f"🔑 Token: {token[:20]}...{token[-10:]}")
    print(f"📏 Longueur: {len(token)}")
    
    # Créer un client Discord minimal
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"✅ Bot connecté: {client.user}")
        print(f"🆔 ID: {client.user.id}")
        
        # Arrêter immédiatement après connexion
        await client.close()
    
    @client.event
    async def on_error(event, *args, **kwargs):
        print(f"❌ Erreur Discord: {event}")
        import traceback
        traceback.print_exc()
    
    try:
        print("🔌 Connexion à Discord...")
        await client.start(token)
        return True
        
    except discord.LoginFailure as e:
        print(f"❌ Échec de connexion Discord: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur Discord générale: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_discord_http_direct():
    """Test direct avec discord.http"""
    print("\n🌐 Test Discord HTTP Direct")
    print("=" * 30)
    
    from discord.http import HTTPClient
    import aiohttp
    
    token = os.getenv("DISCORD_TOKEN")
    
    try:
        # Créer un HTTPClient Discord
        session = aiohttp.ClientSession()
        http = HTTPClient(session, loop=asyncio.get_event_loop())
        
        # Test de login
        print("🔌 Test de login Discord HTTP...")
        data = await http.static_login(token)
        
        print("✅ Login réussi!")
        print(f"🤖 Bot: {data['username']}#{data.get('discriminator', '0000')}")
        
        await session.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur HTTP Discord: {e}")
        if 'session' in locals():
            await session.close()
        return False

def main():
    """Fonction principale"""
    print("🔬 Diagnostic Discord.py - Neuro-Bot")
    print("=" * 45)
    
    # Nettoyer l'environnement
    clear_environment()
    
    async def run_tests():
        # Test 1: HTTP direct
        http_success = await test_discord_http_direct()
        
        if not http_success:
            print("\n❌ Le token ne fonctionne pas avec Discord HTTP")
            return
        
        # Test 2: Client minimal
        client_success = await test_discord_py_minimal()
        
        if client_success:
            print("\n🎉 Discord.py fonctionne!")
            print("🤔 Le problème est dans le code du bot principal")
        else:
            print("\n❌ Problème avec Discord.py détecté")
    
    # Lancer les tests
    asyncio.run(run_tests())

if __name__ == "__main__":
    main()