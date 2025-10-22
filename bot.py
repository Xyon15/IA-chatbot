# --- Imports ---
from config import config, logger, advanced_log_manager
from model import generate_reply
from web import load_web_state
from gpu_utils import gpu_manager, get_gpu_info

import os
import json
import discord
from discord.ext import commands
from typing import Optional, Dict, Any, Union
import time
import asyncio

# --- Classes personnalisées ---
class KiraBot(commands.Bot):
    """Bot Discord personnalisé avec attributs supplémentaires"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Attributs personnalisés
        self.waiting_for_2fa: Dict[int, Dict[str, Any]] = {}
        self.current_context_limit: int = 10
        self.auto_reply_enabled: bool = False
        self.web_enabled: bool = False
        self.DB_PATH: Optional[str] = None
        self.bot_start_time: float = time.time()
import time
import asyncio
from commands import setup_all_commands
from events import setup_all_events

# Initialisation du logging
logger.info("Démarrage du bot Kira...")

# Vérification du système de logs avancé
if advanced_log_manager:
    logger.info("Système de logs avancé activé")
else:
    logger.warning("Système de logs avancé non disponible - mode standard")

web_enabled = load_web_state()

# Configuration déjà chargée via config.py

# --- Intents Discord ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Nécessaire pour lire le contenu des messages


# --- Limite de charactère ---
def get_max_reply_length() -> int:
    """Récupère la limite maximale de réponse"""
    try:
        with open(config.LIMITS_FILE, "r", encoding="utf-8") as f:
            limits_config = json.load(f)
            return limits_config.get("max_reply_length", 1900)
    except Exception as e:
        logger.warning(f"Erreur lecture limits: {e}")
        return 1900   # Valeur par défaut

def set_max_reply_length(length: int):
    """Définit la limite maximale de réponse"""
    try:
        with open(config.LIMITS_FILE, "w", encoding="utf-8") as f:
            json.dump({"max_reply_length": length}, f, indent=2)
        logger.info(f"Limite de réponse définie à {length}")
    except Exception as e:
        logger.error(f"Erreur sauvegarde limits: {e}")
        raise



# --- Configuration du bot Discord ---
bot_start_time = time.time()  # ← Enregistre l'heure de démarrage du bot

# Configuration des rôles déjà dans config.py


# --- Démarrage du bot ---

bot = None
_bot_task = None
_bot_loop = None

def create_bot():
    """Crée et configure l'instance du bot Discord"""
    logger.info("Création de l'instance du bot Discord...")
    
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    bot = KiraBot(command_prefix="!", intents=intents, help_command=None)

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

def start_bot(loop=None):
    """Démarre le bot Discord"""
    global bot, _bot_task, _bot_loop
    if bot is not None:
        logger.warning("Bot déjà démarré")
        if _bot_task is not None:
            return _bot_task
        else:
            # Si bot existe mais pas de task, on redémarre
            bot = None
    if loop is None:
        loop = asyncio.get_event_loop()
    _bot_loop = loop
    bot = create_bot()
    logger.info("Démarrage du bot Discord...")
    
    # Vérification du token
    if config.TOKEN is None:
        raise ValueError("Token Discord non configuré")
        
    return bot.start(config.TOKEN)

async def stop_bot():
    """Arrête le bot Discord proprement"""
    global bot, _bot_task, _bot_loop
    if bot:
        logger.info("Arrêt du bot Discord...")
        await bot.close()
        bot = None
        _bot_task = None
        _bot_loop = None
        logger.info("Bot Discord arrêté")

if __name__ == "__main__":
    asyncio.run(start_bot())

async def some_function(user_id, prompt):
    if bot is None:
        raise RuntimeError("Bot non initialisé")
    reply = await generate_reply(user_id, prompt, context_limit=bot.current_context_limit)