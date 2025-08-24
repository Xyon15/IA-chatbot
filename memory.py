import json
from database import get_db_connection
from config import config, logger

# --- Réponse automatique ---
def load_auto_reply():
    """Charge l'état des réponses automatiques"""
    try:
        with open(config.AUTO_REPLY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("enabled", False)
    except FileNotFoundError:
        logger.warning("Fichier autoreply.json non trouvé, utilisation de la valeur par défaut")
        return False
    except Exception as e:
        logger.error(f"Erreur lors du chargement de autoreply.json: {e}")
        return False

def save_auto_reply(enabled: bool):
    """Sauvegarde l'état des réponses automatiques"""
    try:
        with open(config.AUTO_REPLY_PATH, "w", encoding="utf-8") as f:
            json.dump({"enabled": enabled}, f, indent=2)
        logger.info(f"État auto-reply sauvegardé: {enabled}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde de autoreply.json: {e}")
        raise

auto_reply_enabled = load_auto_reply()



def get_history(user_id: str, limit: int = 10) -> list:
    """Récupère l'historique des conversations pour un utilisateur"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_input, bot_response FROM memory
                WHERE user_id = ? ORDER BY id DESC LIMIT ?
            """, (user_id, limit))
            rows = cursor.fetchall()
            logger.debug(f"Historique récupéré pour {user_id}: {len(rows)} entrées")
            return list(reversed(rows))
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'historique pour {user_id}: {e}")
        return []

def save_fact(user_id: str, fact: str):
    """Sauvegarde un fait dans la mémoire longue durée"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO facts (user_id, fact) VALUES (?, ?)", (user_id, fact))
            conn.commit()
            logger.info(f"Fait sauvegardé pour {user_id}: {fact[:50]}...")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du fait pour {user_id}: {e}")
        raise

def save_interaction(user_id: str, user_input: str, bot_response: str):
    """Sauvegarde une interaction dans la mémoire conversationnelle"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memory (user_id, user_input, bot_response)
                VALUES (?, ?, ?)
            """, (user_id, user_input, bot_response))
            conn.commit()
            logger.debug(f"Interaction sauvegardée pour {user_id}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde de l'interaction pour {user_id}: {e}")
        raise

def clear_memory(user_id: str):
    """Efface la mémoire conversationnelle d'un utilisateur"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memory WHERE user_id = ?", (user_id,))
            deleted_count = cursor.rowcount
            conn.commit()
            logger.info(f"Mémoire effacée pour {user_id}: {deleted_count} entrées supprimées")
            return deleted_count
    except Exception as e:
        logger.error(f"Erreur lors de l'effacement de la mémoire pour {user_id}: {e}")
        raise

def clear_all_memory():
    """Efface toute la mémoire conversationnelle"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memory")
            deleted_count = cursor.rowcount
            conn.commit()
            logger.warning(f"Toute la mémoire effacée: {deleted_count} entrées supprimées")
            return deleted_count
    except Exception as e:
        logger.error(f"Erreur lors de l'effacement de toute la mémoire: {e}")
        raise

def get_facts(user_id: str) -> list:
    """Récupère les faits mémorisés pour un utilisateur"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT fact FROM facts WHERE user_id = ?", (user_id,))
            facts = [row[0] for row in cursor.fetchall()]
            logger.debug(f"Faits récupérés pour {user_id}: {len(facts)} faits")
            return facts
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des faits pour {user_id}: {e}")
        return []

def clear_facts(user_id: str = None):
    """Efface les faits d'un utilisateur ou tous les faits"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute("DELETE FROM facts WHERE user_id = ?", (user_id,))
                logger.info(f"Faits effacés pour {user_id}")
            else:
                cursor.execute("DELETE FROM facts")
                logger.warning("Tous les faits effacés")
            
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
    except Exception as e:
        logger.error(f"Erreur lors de l'effacement des faits: {e}")
        raise