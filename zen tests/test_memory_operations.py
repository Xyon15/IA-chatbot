#!/usr/bin/env python3
"""
Tests unitaires pour les opérations de mémoire du bot Neuro
"""

import unittest
import os
import sys
import tempfile
import sqlite3
from unittest.mock import patch, MagicMock

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory import (
    get_history, save_fact, save_interaction, clear_memory, 
    clear_all_memory, get_facts, clear_facts,
    load_auto_reply, save_auto_reply
)
from database import DatabaseManager, get_db_connection


class TestMemoryOperations(unittest.TestCase):
    """Test des opérations de mémoire de base"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        # Créer un gestionnaire de base de données de test
        self.db_manager = DatabaseManager(self.test_db.name)
        
        # Mock pour le gestionnaire global
        self.db_patcher = patch('memory.get_db_connection')
        self.mock_get_db = self.db_patcher.start()
        self.mock_get_db.return_value = self.db_manager.get_connection()
        
        self.test_user_id = "123456789"
        self.test_fact = "Aime le café noir"
        self.test_input = "Bonjour !"
        self.test_response = "Salut ! Comment ça va ?"

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.db_patcher.stop()
        self.db_manager.close_connections()
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)

    def test_basic_fact_operations(self):
        """Test: Basic memory operations work"""
        # Sauvegarder un fait
        save_fact(self.test_user_id, self.test_fact)
        
        # Récupérer les faits
        facts = get_facts(self.test_user_id)
        
        # Vérifications
        self.assertEqual(len(facts), 1)
        self.assertIn(self.test_fact, facts)

    def test_interaction_storage_and_retrieval(self):
        """Test: Sauvegarde et récupération des interactions"""
        # Sauvegarder une interaction
        save_interaction(self.test_user_id, self.test_input, self.test_response)
        
        # Récupérer l'historique
        history = get_history(self.test_user_id, limit=1)
        
        # Vérifications
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][0], self.test_input)
        self.assertEqual(history[0][1], self.test_response)

    def test_memory_clearing(self):
        """Test: Nettoyage de la mémoire"""
        # Ajouter des données
        save_interaction(self.test_user_id, self.test_input, self.test_response)
        save_fact(self.test_user_id, self.test_fact)
        
        # Vérifier que les données sont là
        self.assertEqual(len(get_history(self.test_user_id)), 1)
        self.assertEqual(len(get_facts(self.test_user_id)), 1)
        
        # Nettoyer la mémoire conversationnelle
        deleted_count = clear_memory(self.test_user_id)
        self.assertEqual(deleted_count, 1)
        self.assertEqual(len(get_history(self.test_user_id)), 0)
        
        # Les faits doivent rester
        self.assertEqual(len(get_facts(self.test_user_id)), 1)
        
        # Nettoyer les faits
        deleted_facts = clear_facts(self.test_user_id)
        self.assertEqual(deleted_facts, 1)
        self.assertEqual(len(get_facts(self.test_user_id)), 0)

    def test_history_limit(self):
        """Test: Limite de l'historique"""
        # Ajouter plusieurs interactions
        for i in range(5):
            save_interaction(self.test_user_id, f"Input {i}", f"Response {i}")
        
        # Récupérer avec limite
        history = get_history(self.test_user_id, limit=3)
        
        # Vérifications
        self.assertEqual(len(history), 3)
        # L'ordre doit être chronologique (plus ancien en premier)
        self.assertEqual(history[0][0], "Input 2")  # Plus ancien affiché
        self.assertEqual(history[2][0], "Input 4")  # Plus récent affiché

    def test_clear_all_memory(self):
        """Test: Nettoyage de toute la mémoire"""
        # Ajouter des données pour plusieurs utilisateurs
        user1, user2 = "user1", "user2"
        save_interaction(user1, "Hello", "Hi")
        save_interaction(user2, "Bonjour", "Salut")
        
        # Nettoyer tout
        deleted_count = clear_all_memory()
        self.assertEqual(deleted_count, 2)
        
        # Vérifier que tout est vide
        self.assertEqual(len(get_history(user1)), 0)
        self.assertEqual(len(get_history(user2)), 0)

    def test_empty_parameters(self):
        """Test: Empty or null parameters"""
        # Test avec user_id vide
        facts = get_facts("")
        self.assertEqual(len(facts), 0)
        
        history = get_history("", limit=10)
        self.assertEqual(len(history), 0)
        
        # Test avec fait vide
        with self.assertRaises(Exception):
            save_fact(self.test_user_id, "")

    def test_nonexistent_user(self):
        """Test: Utilisateur inexistant"""
        nonexistent_user = "999999999"
        
        # Récupérer données d'un utilisateur inexistant
        facts = get_facts(nonexistent_user)
        self.assertEqual(len(facts), 0)
        
        history = get_history(nonexistent_user)
        self.assertEqual(len(history), 0)
        
        # Nettoyer un utilisateur inexistant
        deleted_count = clear_memory(nonexistent_user)
        self.assertEqual(deleted_count, 0)


class TestAutoReplyOperations(unittest.TestCase):
    """Test des opérations de réponse automatique"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.test_file.close()
        
        # Mock le chemin du fichier de configuration
        self.config_patcher = patch('memory.config.AUTO_REPLY_PATH', self.test_file.name)
        self.config_patcher.start()

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.config_patcher.stop()
        if os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)

    def test_auto_reply_state_persistence(self):
        """Test: Web search state persistence (adapté pour auto-reply)"""
        # Sauvegarder état activé
        save_auto_reply(True)
        
        # Charger et vérifier
        state = load_auto_reply()
        self.assertTrue(state)
        
        # Sauvegarder état désactivé
        save_auto_reply(False)
        
        # Charger et vérifier
        state = load_auto_reply()
        self.assertFalse(state)

    def test_auto_reply_file_not_found(self):
        """Test: Fichier de configuration manquant"""
        # Supprimer le fichier
        os.unlink(self.test_file.name)
        
        # Charger doit retourner False par défaut
        state = load_auto_reply()
        self.assertFalse(state)

    def test_invalid_file_handling(self):
        """Test: Invalid file paths handling"""
        # Écrire un JSON invalide
        with open(self.test_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Doit retourner False sans lever d'exception
        state = load_auto_reply()
        self.assertFalse(state)


class TestDatabaseConnectionFailures(unittest.TestCase):
    """Test des échecs de connexion à la base de données"""

    def test_database_connection_failures(self):
        """Test: Database connection failures"""
        # Tester avec un chemin de base de données invalide
        with patch('memory.get_db_connection') as mock_conn:
            # Simuler une erreur de connexion
            mock_conn.side_effect = sqlite3.Error("Connection failed")
            
            # Les fonctions doivent gérer l'erreur gracieusement
            history = get_history("test_user")
            self.assertEqual(len(history), 0)
            
            facts = get_facts("test_user")
            self.assertEqual(len(facts), 0)

    @patch('memory.logger')
    def test_error_logging(self, mock_logger):
        """Test: Les erreurs sont bien loggées"""
        with patch('memory.get_db_connection') as mock_conn:
            mock_conn.side_effect = Exception("Test error")
            
            # Appeler une fonction qui doit logger l'erreur
            get_history("test_user")
            
            # Vérifier que l'erreur a été loggée
            mock_logger.error.assert_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)