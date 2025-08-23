import sqlite3
import os
import json
from config import DB_PATH, AUTO_REPLY_PATH

# Table mémoire globale (prompt/réponse)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        user_input TEXT,
        bot_response TEXT
    )
""")

# Table mémoire longue durée (faits)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        fact TEXT
    )
""")

conn.commit()
conn.close()

# --- Réponse automatique ---
AUTO_REPLY_PATH = os.path.join("JSON", "autoreply.json")

def load_auto_reply():
    try:
        with open(AUTO_REPLY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("enabled", False)
    except FileNotFoundError:
        return False

def save_auto_reply(enabled):
    with open(AUTO_REPLY_PATH, "w", encoding="utf-8") as f:
        json.dump({"enabled": enabled}, f, indent=2)

auto_reply_enabled = load_auto_reply()



def get_history(user_id, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_input, bot_response FROM memory
        WHERE user_id = ? ORDER BY id DESC LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return list(reversed(rows))

def save_fact(user_id: str, fact: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO facts (user_id, fact) VALUES (?, ?)", (user_id, fact))
    conn.commit()
    conn.close()

def save_interaction(user_id, user_input, bot_response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memory (user_id, user_input, bot_response)
        VALUES (?, ?, ?)
    """, (user_id, user_input, bot_response))
    conn.commit()
    conn.close()

def clear_memory(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memory WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_facts(user_id: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fact FROM facts WHERE user_id = ?", (user_id,))
    facts = [row[0] for row in cursor.fetchall()]
    conn.close()
    return facts