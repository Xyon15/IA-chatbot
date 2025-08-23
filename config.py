import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
AUTH_SECRET = os.getenv("AUTH_SECRET")
AUTHORIZED_ROLE = "NeuroMaster"
LIMITS_FILE = os.path.join("JSON", "character_limits.json")
WEB_STATE_FILE = os.path.join("JSON", "web.json")
CONFIG_PATH = os.path.join("JSON", "context.json")
AUTO_REPLY_PATH = os.path.join("JSON", "autoreply.json")
DB_PATH = "D:/neuro_memory/neuro.db"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "zephyr-7b-beta.Q5_K_M.gguf")