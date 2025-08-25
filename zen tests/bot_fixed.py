#!/usr/bin/env python3
"""
Version corrigée du bot principal avec chargement de token fiable
"""

import os
import sys
import asyncio
import json
import discord
from pathlib import Path

# Setup et nettoyage comme dans la version qui fonctionne
sys.path.append(str(Path("..").absolute()))
os.chdir(str(Path("..").absolute()))

# Nettoyage environnement AVANT d'importer config
for var in ['DISCORD_TOKEN', 'AUTH_SECRET']:
    if var in os.environ:
        del os.environ[var]

modules_to_remove = [name for name in sys.modules if any(k in name.lower() for k in ['config', 'dotenv'])]
for module in modules_to_remove:
    del sys.modules[module]

# Chargement frais AVANT d'importer config
from dotenv import load_dotenv
load_dotenv()

# Vérifier que le token est chargé
token = os.getenv('DISCORD_TOKEN')
if not token:
    print("❌ Token non trouvé après chargement frais")
    exit(1)

print(f"✅ Token chargé: {token[:20]}...{token[-10:]}")

# MAINTENANT on peut importer config en sécurité
try:
    from config import config, logger
    print("✅ Config importé avec succès")
except Exception as e:
    print(f"❌ Erreur import config: {e}")
    exit(1)

# Imports du bot original
from utils import count_tokens, truncate_text_to_tokens, shorten_response
from memory import get_history, save_fact, save_interaction, clear_memory, get_facts
from model import generate_reply
from web import duckduckgo_search, duckduckgo_html_fallback, load_web_state, save_web_state

from commands import setup_all_commands
from events import setup_all_events

print("✅ Tous les modules importés")

# Configuration Discord identique au bot original
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Fonction identique au bot original
def get_max_reply_length() -> int:
    """Récupère la limite maximale de réponse"""
    try:
        with open(config.LIMITS_FILE, "r", encoding="utf-8") as f:
            limits_config = json.load(f)
            return limits_config.get("max_reply_length", 1900)
    except Exception:
        return 1900

def create_bot():
    """Crée et configure l'instance du bot Discord identique à l'original"""
    logger.info("Création de l'instance du bot Discord...")
    
    from discord.ext import commands
    import time
    
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
    bot.waiting_for_2fa = {}
    
    # Charge dynamiquement le context_limit
    try:
        with open(config.CONFIG_PATH, "r", encoding="utf-8") as f:
            bot_config = json.load(f)
            bot.current_context_limit = bot_config.get("context_limit", 10)
        logger.info(f"Context limit chargé: {bot.current_context_limit}")
    except Exception as e:
        bot.current_context_limit = 10
        logger.warning(f"Erreur chargement context limit: {e}, utilisation valeur par défaut")

    # Charge dynamiquement l'état auto_reply
    try:
        with open(config.AUTO_REPLY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            bot.auto_reply_enabled = data.get("enabled", False)
        logger.info(f"Auto reply chargé: {bot.auto_reply_enabled}")
    except Exception as e:
        bot.auto_reply_enabled = False
        logger.warning(f"Erreur chargement auto reply: {e}, utilisation valeur par défaut")

    bot.web_enabled = load_web_state()
    bot.DB_PATH = config.DB_PATH
    bot.bot_start_time = time.time()
    
    # Configuration des commandes et événements
    setup_all_commands(bot)
    setup_all_events(bot)
    
    logger.info("Bot Discord configuré avec succès")
    
    return bot

async def start_bot():
    """Fonction de démarrage du bot identique à l'original"""
    
    # Créer et configurer le bot
    bot = create_bot()
    
    try:
        logger.info("Démarrage du bot Discord...")
        await bot.start(config.TOKEN)
    except discord.LoginFailure as e:
        logger.error(f"Échec de connexion Discord: {e}")
        raise
    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {e}")
        raise

def main():
    """Fonction principale"""
    print("🤖 Neuro-Bot - Version Corrigée")
    print("=" * 35)
    
    try:
        # Vérifications préliminaires comme dans start_bot.py
        print("🔍 Vérifications...")
        
        if not os.path.exists(config.MODEL_PATH):
            print(f"❌ Modèle non trouvé: {config.MODEL_PATH}")
            return
        
        print("✅ Toutes les vérifications passées")
        print("🚀 Démarrage du bot...")
        
        # Démarrer le bot
        asyncio.run(start_bot())
        
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt demandé par l'utilisateur")
        logger.info("Bot arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        logger.error(f"Erreur fatale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()