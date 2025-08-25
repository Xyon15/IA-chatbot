#!/usr/bin/env python3
"""
Debug final pour comprendre le problème Discord.py vs autres méthodes
"""

import os
import sys
import asyncio
from pathlib import Path

# Setup
sys.path.append(str(Path("..").absolute()))
os.chdir(str(Path("..").absolute()))

# Nettoyage
for var in ['DISCORD_TOKEN', 'AUTH_SECRET']:
    if var in os.environ:
        del os.environ[var]

modules_to_remove = [name for name in sys.modules if any(k in name.lower() for k in ['config', 'dotenv'])]
for module in modules_to_remove:
    del sys.modules[module]

from dotenv import load_dotenv
load_dotenv()

token = os.getenv('DISCORD_TOKEN')

async def test_all_methods():
    """Test toutes les méthodes possibles"""
    
    print("=== DEBUG FINAL DISCORD ===")
    print(f"Token: {token[:20]}...{token[-10:]}")
    print(f"Longueur: {len(token)}")
    
    # 1. Test requests (sync)
    print("\n1. TEST REQUESTS")
    try:
        import requests
        response = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": f"Bot {token}"},
            timeout=10
        )
        print(f"Requests: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: {data['username']}#{data.get('discriminator', '0000')}")
        else:
            print(f"FAIL: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 2. Test aiohttp direct
    print("\n2. TEST AIOHTTP DIRECT")
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://discord.com/api/v10/users/@me",
                headers={"Authorization": f"Bot {token}"}
            ) as response:
                print(f"Aiohttp: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"SUCCESS: {data['username']}#{data.get('discriminator', '0000')}")
                else:
                    text = await response.text()
                    print(f"FAIL: {text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 3. Test discord.py HTTPClient bas niveau
    print("\n3. TEST DISCORD.PY HTTP CLIENT")
    try:
        import discord
        import aiohttp
        
        # Créer une session manuelle
        session = aiohttp.ClientSession()
        
        # Créer un HTTPClient Discord SANS loop deprecated
        http = discord.http.HTTPClient(session)
        
        # Test login
        data = await http.static_login(token)
        print(f"Discord HTTPClient: SUCCESS")
        print(f"Bot: {data['username']}#{data.get('discriminator', '0000')}")
        
        await session.close()
        
    except Exception as e:
        print(f"Discord HTTPClient ERROR: {e}")
        if 'session' in locals():
            await session.close()
    
    # 4. Test discord.py Client complet
    print("\n4. TEST DISCORD.PY CLIENT")
    try:
        import discord
        
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
        
        connected = False
        
        @client.event
        async def on_ready():
            nonlocal connected
            print(f"Discord Client: SUCCESS")
            print(f"Bot: {client.user}")
            connected = True
            await client.close()
        
        @client.event
        async def on_error(event, *args, **kwargs):
            print(f"Discord Client ERROR: {event}")
            await client.close()
        
        # Timeout pour éviter l'attente infinie
        try:
            await asyncio.wait_for(client.start(token), timeout=15.0)
        except asyncio.TimeoutError:
            print("Discord Client: TIMEOUT")
            if not client.is_closed():
                await client.close()
        except Exception as e:
            print(f"Discord Client ERROR: {e}")
            if not client.is_closed():
                await client.close()
        
        if not connected:
            print("Discord Client: FAILED TO CONNECT")
        
    except Exception as e:
        print(f"Discord Client SETUP ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_all_methods())