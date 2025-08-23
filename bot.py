# --- Imports ---
from config import (
    TOKEN, AUTH_SECRET, AUTHORIZED_ROLE,
    LIMITS_FILE, WEB_STATE_FILE, CONFIG_PATH, AUTO_REPLY_PATH, DB_PATH, MODEL_PATH
)
from utils import count_tokens, truncate_text_to_tokens, shorten_response
from memory import get_history, save_fact, save_interaction, clear_memory, get_facts
from model import generate_reply
from web import duckduckgo_search, duckduckgo_html_fallback, load_web_state, save_web_state


import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import asyncio
from commands import setup_all_commands
from events import setup_all_events

web_enabled = load_web_state()

# GPU Stats
nvml_path = r"C:\Program Files\NVIDIA Corporation\NVSMI"
if nvml_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + nvml_path

from pynvml import (
    nvmlInit, nvmlShutdown, nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetName, nvmlDeviceGetUtilizationRates,
    nvmlDeviceGetMemoryInfo, nvmlDeviceGetTemperature,
    NVML_TEMPERATURE_GPU, NVMLError
)



# --- Chargement du token discord ---
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Assure-toi que le token est dans le fichier .env

# --- Authentification 2FA pour !reset ---
AUTH_SECRET = os.getenv("AUTH_SECRET")

# --- Intents Discord ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Nécessaire pour lire le contenu des messages


# --- Limite de charactère ---
LIMITS_FILE = os.path.join("JSON", "character_limits.json")

def get_max_reply_length() -> int:
    try:
        with open(LIMITS_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("max_reply_length", 1900)
    except Exception:
        return 1900   # Valeur par défaut

def set_max_reply_length(length: int):
    with open(LIMITS_FILE, "w", encoding="utf-8") as f:
        json.dump({"max_reply_length": length}, f, indent=2)



# --- Configuration du bot Discord ---
bot_start_time = time.time()  # ← Enregistre l'heure de démarrage du bot

AUTHORIZED_ROLE = "NeuroMaster"  # ← Remplace par le nom exact du rôle autorisé


# --- Démarrage du bot ---

bot = None
_bot_task = None
_bot_loop = None

def create_bot():
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
    bot.waiting_for_2fa = {}

    # Charge dynamiquement le context_limit
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
            bot.current_context_limit = config.get("context_limit", 10)
    except Exception:
        bot.current_context_limit = 10

    # Charge dynamiquement l'état auto_reply
    try:
        with open(AUTO_REPLY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            bot.auto_reply_enabled = data.get("enabled", False)
    except Exception:
        bot.auto_reply_enabled = False

    bot.web_enabled = load_web_state()
    bot.DB_PATH = DB_PATH
    bot.bot_start_time = time.time()
    setup_all_commands(bot)
    setup_all_events(bot)
    return bot

def start_bot(loop=None):
    global bot, _bot_task, _bot_loop
    if bot is not None:
        return _bot_task
    if loop is None:
        loop = asyncio.get_event_loop()
    _bot_loop = loop
    bot = create_bot()
    return bot.start(TOKEN)

async def stop_bot():
    global bot, _bot_task, _bot_loop
    if bot:
        await bot.close()
        bot = None
        _bot_task = None
        _bot_loop = None

if __name__ == "__main__":
    asyncio.run(start_bot())

async def some_function(user_id, prompt):
    reply = await generate_reply(user_id, prompt, context_limit=bot.current_context_limit)