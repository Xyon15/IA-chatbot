#!/usr/bin/env python3
"""
Bot fonctionnel simplifié pour tester
"""

import os
import sys
import asyncio
import discord
from pathlib import Path

# Setup
sys.path.append(str(Path("..").absolute()))
os.chdir(str(Path("..").absolute()))

# Nettoyage environnement
for var in ['DISCORD_TOKEN', 'AUTH_SECRET']:
    if var in os.environ:
        del os.environ[var]

modules_to_remove = [name for name in sys.modules if any(k in name.lower() for k in ['config', 'dotenv'])]
for module in modules_to_remove:
    del sys.modules[module]

# Chargement frais
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('DISCORD_TOKEN')

print("🤖 Bot Discord Simplifié")
print("========================")
print(f"Token: {token[:20]}...{token[-10:]}")

# Configuration Discord
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot connecté: {client.user}")
    print(f"🆔 ID: {client.user.id}")
    print(f"🔗 Guilds: {len(client.guilds)}")
    
    for guild in client.guilds:
        print(f"  📍 {guild.name} ({guild.id})")
    
    print("\n🎉 Bot en ligne! Tapez des messages dans Discord...")
    print("Press Ctrl+C to stop")

@client.event
async def on_message(message):
    # Éviter de répondre à soi-même
    if message.author == client.user:
        return
    
    print(f"📨 Message de {message.author}: {message.content}")
    
    # Réponse simple
    if "hello" in message.content.lower() or "salut" in message.content.lower():
        await message.channel.send(f"👋 Salut {message.author.mention}! Je fonctionne parfaitement!")
    
    if "test" in message.content.lower():
        await message.channel.send("🧪 Test réussi! Le bot fonctionne correctement avec le nouveau token!")

@client.event
async def on_error(event, *args, **kwargs):
    print(f"❌ Erreur Discord: {event}")
    import traceback
    traceback.print_exc()

async def main():
    try:
        print("🚀 Démarrage du bot...")
        await client.start(token)
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt demandé")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        if not client.is_closed():
            await client.close()
        print("👋 Bot arrêté")

if __name__ == "__main__":
    asyncio.run(main())