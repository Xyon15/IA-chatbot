#!/usr/bin/env python3
"""
Test simple avec discord.py
"""

import os
import sys
import asyncio
from pathlib import Path
import discord

# Ajouter le répertoire parent
sys.path.append(str(Path("..").absolute()))
os.chdir(str(Path("..").absolute()))

async def test_simple():
    """Test simple"""
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("DISCORD_TOKEN")
    print(f"🔑 Token: {token[:20]}...{token[-10:]} ({len(token)} chars)")
    
    # Test très simple
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"✅ Connecté: {client.user}")
        await client.close()
    
    try:
        print("🔌 Connexion...")
        await client.start(token)
        
    except discord.LoginFailure as e:
        print(f"❌ LoginFailure: {e}")
        
        # Vérifier si c'est un problème d'intents
        print("🔧 Test sans intents message_content...")
        intents_basic = discord.Intents.default()
        client_basic = discord.Client(intents=intents_basic)
        
        @client_basic.event
        async def on_ready():
            print(f"✅ Connecté sans intents: {client_basic.user}")
            await client_basic.close()
        
        try:
            await client_basic.start(token)
        except Exception as e2:
            print(f"❌ Même erreur sans intents: {e2}")
            
    except Exception as e:
        print(f"❌ Autre erreur: {e}")

if __name__ == "__main__":
    asyncio.run(test_simple())