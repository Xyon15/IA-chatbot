#!/usr/bin/env python3
"""
Tests unitaires pour le gestionnaire de base de données du bot Neuro
"""

import unittest
import os
import sys
import tempfile
import sqlite3
import threading
import time
from unittest.mock import patch, MagicMock

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager, get_db_connection


class TestDatabaseManager(unittest.TestCase):
    """Test du gestionnaire de base de données"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        self.db_manager = DatabaseManager(self.test_db.name)

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.db_manager.close_connections()
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)

    def test_database_connection_context_manager(self):
        """Test: Database connection context manager"""
        # Tester le context manager
        with self.db_manager.get_connection() as conn:
            self.assertIsInstance(conn, sqlite3.Connection)
            
            # Tester une requête simple
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

    def test_database_initialization(self):
        """Test: Initialisation de la base de données"""
        # Vérifier que les tables ont été créées
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier l'existence de la table memory
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='memory'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Vérifier l'existence de la table facts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='facts'")
            self.assertIsNotNone(cursor.fetchone())

    def test_indexes_creation(self):
        """Test: Création des index"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier les index sur la table memory
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='memory'")
            indexes = [row[0] for row in cursor.fetchall()]
            
            self.assertIn('idx_memory_user_id', indexes)
            self.assertIn('idx_memory_timestamp', indexes)
            
            # Vérifier l'index sur la table facts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='facts'")
            indexes = [row[0] for row in cursor.fetchall()]
            
            self.assertIn('idx_facts_user_id', indexes)

    def test_pragma_settings(self):
        """Test: Configuration PRAGMA pour les performances"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier le mode WAL
            cursor.execute("PRAGMA journal_mode")
            self.assertEqual(cursor.fetchone()[0].upper(), 'WAL')
            
            # Vérifier le mode synchronous
            cursor.execute("PRAGMA synchronous")
            result = cursor.fetchone()[0]
            self.assertIn(result, [1, 2])  # NORMAL ou FULL
            
            # Vérifier cache_size
            cursor.execute("PRAGMA cache_size")
            cache_size = cursor.fetchone()[0]
            self.assertGreater(abs(cache_size), 0)

    def test_thread_local_connections(self):
        """Test: Connexions par thread (thread-local)"""
        connections = {}
        
        def get_connection_id(thread_id):
            """Fonction pour récupérer l'ID de connexion depuis un thread"""
            with self.db_manager.get_connection() as conn:
                connections[thread_id] = id(conn)
        
        # Créer deux threads
        thread1 = threading.Thread(target=get_connection_id, args=(1,))
        thread2 = threading.Thread(target=get_connection_id, args=(2,))
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
        # Les connexions doivent être différentes pour chaque thread
        self.assertNotEqual(connections[1], connections[2])

    def test_connection_reuse_in_same_thread(self):
        """Test: Réutilisation des connexions dans le même thread"""
        conn_id1 = None
        conn_id2 = None
        
        # Première connexion
        with self.db_manager.get_connection() as conn:
            conn_id1 = id(conn)
        
        # Deuxième connexion (doit être la même)
        with self.db_manager.get_connection() as conn:
            conn_id2 = id(conn)
        
        self.assertEqual(conn_id1, conn_id2)

    def test_transaction_rollback_on_error(self):
        """Test: Rollback automatique en cas d'erreur"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Insérer une donnée valide
            cursor.execute("INSERT INTO memory (user_id, user_input, bot_response) VALUES (?, ?, ?)",
                         ('user1', 'test', 'response'))
            conn.commit()
        
        # Tenter une transaction qui échoue
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO memory (user_id, user_input, bot_response) VALUES (?, ?, ?)",
                             ('user2', 'test2', 'response2'))
                # Simuler une erreur
                raise Exception("Test error")
        except Exception:
            pass
        
        # Vérifier que seule la première insertion a été conservée
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 1)

    def test_connection_timeout(self):
        """Test: Configuration du timeout de connexion"""
        # Créer un nouveau gestionnaire avec un chemin invalide pour forcer un timeout
        invalid_db = "/invalid/path/test.db"
        
        with self.assertRaises(sqlite3.OperationalError):
            invalid_manager = DatabaseManager(invalid_db)

    def test_close_connections(self):
        """Test: Fermeture des connexions"""
        # Obtenir une connexion
        with self.db_manager.get_connection() as conn:
            pass
        
        # Fermer les connexions
        self.db_manager.close_connections()
        
        # Vérifier qu'une nouvelle connexion est créée après fermeture
        with self.db_manager.get_connection() as conn:
            self.assertIsInstance(conn, sqlite3.Connection)

    @patch('database.logger')
    def test_error_logging(self, mock_logger):
        """Test: Logging des erreurs de base de données"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                # Exécuter une requête invalide
                cursor.execute("INVALID SQL QUERY")
        except Exception:
            pass
        
        # Vérifier que l'erreur a été loggée
        mock_logger.error.assert_called()

    def test_database_connection_failures(self):
        """Test: Database connection failures"""
        # Tester avec un chemin de fichier en lecture seule
        readonly_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        readonly_db.close()
        
        # Créer la base de données d'abord
        temp_manager = DatabaseManager(readonly_db.name)
        temp_manager.close_connections()
        
        # Rendre le fichier en lecture seule
        os.chmod(readonly_db.name, 0o444)
        
        try:
            # Essayer d'écrire dans une base de données en lecture seule
            with self.assertRaises(sqlite3.OperationalError):
                readonly_manager = DatabaseManager(readonly_db.name)
                with readonly_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO memory (user_id, user_input, bot_response) VALUES (?, ?, ?)",
                                 ('test', 'test', 'test'))
                    conn.commit()
        finally:
            # Restaurer les permissions et nettoyer
            os.chmod(readonly_db.name, 0o644)
            if os.path.exists(readonly_db.name):
                os.unlink(readonly_db.name)


class TestGlobalDatabaseFunctions(unittest.TestCase):
    """Test des fonctions globales de base de données"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        # Mock le chemin de la base de données
        self.config_patcher = patch('database.config.DB_PATH', self.test_db.name)
        self.config_patcher.start()

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.config_patcher.stop()
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)

    def test_global_get_db_connection(self):
        """Test: Context manager global get_db_connection"""
        # Réimporter le module pour utiliser le nouveau chemin
        if 'database' in sys.modules:
            del sys.modules['database']
        
        from database import get_db_connection
        
        # Tester le context manager global
        with get_db_connection() as conn:
            self.assertIsInstance(conn, sqlite3.Connection)
            
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

    def test_init_database_function(self):
        """Test: Fonction utilitaire init_database"""
        if 'database' in sys.modules:
            del sys.modules['database']
        
        from database import init_database
        
        # Appeler la fonction d'initialisation
        init_database()
        
        # Vérifier que la base de données a été initialisée
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('memory', tables)
        self.assertIn('facts', tables)
        
        conn.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)