"""
Module de gestion de base de données avec context manager et pool de connexions
"""
import sqlite3
import threading
from contextlib import contextmanager
from typing import Generator
from config import config, logger


class DatabaseManager:
    """Gestionnaire de base de données avec pool de connexions"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._local = threading.local()
        self._init_database()
    
    def _init_database(self):
        """Initialise la base de données avec les tables nécessaires"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Table mémoire conversationnelle
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        user_input TEXT NOT NULL,
                        bot_response TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Index pour la table memory
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_memory_user_id ON memory(user_id)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_memory_timestamp ON memory(timestamp)
                """)
                
                # Table mémoire longue durée (faits)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS facts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        fact TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Index pour la table facts
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_facts_user_id ON facts(user_id)
                """)
                
                conn.commit()
                logger.info("Base de données initialisée avec succès")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
            raise
    
    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager pour obtenir une connexion à la base de données"""
        # Utilise une connexion par thread pour éviter les conflits
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )
            # Configuration pour de meilleures performances
            self._local.connection.execute("PRAGMA journal_mode=WAL")
            self._local.connection.execute("PRAGMA synchronous=NORMAL")
            self._local.connection.execute("PRAGMA cache_size=10000")
            self._local.connection.execute("PRAGMA temp_store=MEMORY")
        
        conn = self._local.connection
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"Erreur de base de données: {e}")
            raise
        finally:
            # La connexion reste ouverte pour réutilisation dans le même thread
            pass
    
    def close_connections(self):
        """Ferme toutes les connexions ouvertes"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')


# Instance globale du gestionnaire de base de données
db_manager = DatabaseManager(config.DB_PATH)

# Context manager pour compatibilité
@contextmanager
def get_db_connection():
    """Context manager pour obtenir une connexion à la base de données"""
    with db_manager.get_connection() as conn:
        yield conn

def init_database():
    """Fonction utilitaire pour initialiser la base de données"""
    return db_manager._init_database()