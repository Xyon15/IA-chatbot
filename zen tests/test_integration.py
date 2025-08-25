#!/usr/bin/env python3
"""
Tests d'intégration pour le bot Neuro - Test complet du système
"""

import unittest
import os
import sys
import tempfile
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSystemIntegration(unittest.TestCase):
    """Tests d'intégration du système complet"""

    def setUp(self):
        """Configuration avant chaque test"""
        # Créer des fichiers temporaires pour les tests
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        self.test_web_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.test_web_file.write('{"enabled": false}')
        self.test_web_file.close()
        
        self.test_auto_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.test_auto_file.write('{"enabled": true}')
        self.test_auto_file.close()
        
        self.test_limits_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.test_limits_file.write('{"max_reply_length": 1500}')
        self.test_limits_file.close()

    def tearDown(self):
        """Nettoyage après chaque test"""
        files_to_clean = [
            self.test_db.name,
            self.test_web_file.name,
            self.test_auto_file.name,
            self.test_limits_file.name
        ]
        
        for file_path in files_to_clean:
            if os.path.exists(file_path):
                os.unlink(file_path)

    @patch.dict(os.environ, {
        'DISCORD_TOKEN': 'test_token',
        'AUTH_SECRET': 'test_secret'
    })
    def test_complete_memory_workflow(self):
        """Test: Workflow complet de mémoire"""
        # Mock des chemins de fichiers
        with patch('database.config.DB_PATH', self.test_db.name):
            with patch('memory.config.AUTO_REPLY_PATH', self.test_auto_file.name):
                # Réinitialiser les modules pour prendre en compte les nouveaux paths
                modules_to_reset = ['database', 'memory']
                for module in modules_to_reset:
                    if module in sys.modules:
                        del sys.modules[module]
                
                from database import DatabaseManager
                from memory import (
                    save_interaction, get_history, save_fact, 
                    get_facts, clear_memory, clear_facts
                )
                
                # Créer le gestionnaire de DB
                db_manager = DatabaseManager(self.test_db.name)
                
                test_user_id = "integration_test_user"
                
                # 1. Sauvegarder une interaction
                save_interaction(test_user_id, "Bonjour", "Salut ! Comment ça va ?")
                
                # 2. Vérifier l'historique
                history = get_history(test_user_id)
                self.assertEqual(len(history), 1)
                self.assertEqual(history[0][0], "Bonjour")
                
                # 3. Sauvegarder un fait
                save_fact(test_user_id, "Préfère le thé au café")
                
                # 4. Vérifier les faits
                facts = get_facts(test_user_id)
                self.assertEqual(len(facts), 1)
                self.assertIn("Préfère le thé au café", facts)
                
                # 5. Nettoyer la mémoire conversationnelle
                deleted_count = clear_memory(test_user_id)
                self.assertEqual(deleted_count, 1)
                
                # 6. Vérifier que l'historique est vide mais les faits restent
                history = get_history(test_user_id)
                self.assertEqual(len(history), 0)
                
                facts = get_facts(test_user_id)
                self.assertEqual(len(facts), 1)
                
                # 7. Nettoyer les faits
                clear_facts(test_user_id)
                facts = get_facts(test_user_id)
                self.assertEqual(len(facts), 0)
                
                # Nettoyer
                db_manager.close_connections()

    def test_web_and_utils_integration(self):
        """Test: Intégration web et utilitaires"""
        with patch('web.config.WEB_STATE_FILE', self.test_web_file.name):
            with patch('utils.config.LIMITS_FILE', self.test_limits_file.name):
                # Réinitialiser les modules
                modules_to_reset = ['web', 'utils']
                for module in modules_to_reset:
                    if module in sys.modules:
                        del sys.modules[module]
                
                from web import load_web_state, save_web_state
                from utils import shorten_response
                
                # 1. Tester l'état web
                initial_state = load_web_state()
                self.assertFalse(initial_state)
                
                # 2. Changer l'état
                save_web_state(True)
                new_state = load_web_state()
                self.assertTrue(new_state)
                
                # 3. Tester le raccourcissement de réponse
                long_text = "Ce texte est très long " * 100  # Texte très long
                shortened = shorten_response(long_text)
                
                # Doit être raccourci selon la config (1500 caractères)
                self.assertLessEqual(len(shortened), 1500)

    @patch('web.aiohttp.ClientSession')
    def test_web_search_integration(self, mock_session):
        """Test: Intégration de la recherche web complète"""
        # Mock de la réponse DuckDuckGo
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            'Abstract': 'Résultat de test pour intégration'
        })
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        with patch('web.config.WEB_STATE_FILE', self.test_web_file.name):
            if 'web' in sys.modules:
                del sys.modules['web']
            
            from web import duckduckgo_search, load_web_state, save_web_state
            
            # 1. Activer la recherche web
            save_web_state(True)
            self.assertTrue(load_web_state())
            
            # 2. Effectuer une recherche
            async def run_search():
                return await duckduckgo_search("test query")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(run_search())
                self.assertEqual(result, 'Résultat de test pour intégration')
            finally:
                loop.close()

    @patch.dict(os.environ, {
        'DISCORD_TOKEN': 'test_token',
        'AUTH_SECRET': 'test_secret'
    })
    def test_configuration_and_database_integration(self):
        """Test: Intégration configuration et base de données"""
        # Mock du modèle existant
        with patch('os.path.exists', return_value=True):
            # Réinitialiser le module config
            if 'config' in sys.modules:
                del sys.modules['config']
            
            from config import config, logger
            
            # Vérifier que la configuration est chargée
            self.assertEqual(config.TOKEN, 'test_token')
            self.assertEqual(config.AUTH_SECRET, 'test_secret')
            
            # Test du logger
            logger.info("Test d'intégration du logger")
            
            # Test avec base de données
            with patch('database.config.DB_PATH', self.test_db.name):
                if 'database' in sys.modules:
                    del sys.modules['database']
                
                from database import get_db_connection, init_database
                
                # Initialiser et tester la base de données
                init_database()
                
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                    table_count = cursor.fetchone()[0]
                    
                    # Doit avoir au moins les tables memory et facts
                    self.assertGreaterEqual(table_count, 2)

    def test_complete_system_error_handling(self):
        """Test: Gestion d'erreur du système complet"""
        # Test avec chemins de fichiers invalides
        invalid_db = "/invalid/path/test.db"
        invalid_config = "/invalid/path/config.json"
        
        # Test de récupération gracieuse des erreurs
        with patch('database.config.DB_PATH', invalid_db):
            modules_to_reset = ['memory']
            for module in modules_to_reset:
                if module in sys.modules:
                    del sys.modules[module]
            
            from memory import get_history, get_facts
            
            # Les fonctions doivent retourner des listes vides au lieu de planter
            history = get_history("test_user")
            self.assertEqual(len(history), 0)
            
            facts = get_facts("test_user")
            self.assertEqual(len(facts), 0)

    def test_multi_user_scenario(self):
        """Test: Scénario multi-utilisateurs"""
        with patch('database.config.DB_PATH', self.test_db.name):
            if 'database' in sys.modules:
                del sys.modules['database']
            if 'memory' in sys.modules:
                del sys.modules['memory']
            
            from database import DatabaseManager
            from memory import save_interaction, save_fact, get_history, get_facts
            
            db_manager = DatabaseManager(self.test_db.name)
            
            # Simulation de 3 utilisateurs
            users = ["user1", "user2", "user3"]
            
            # Chaque utilisateur a des interactions et des faits
            for i, user in enumerate(users):
                save_interaction(user, f"Message {i}", f"Réponse {i}")
                save_fact(user, f"Fait {i} pour {user}")
            
            # Vérifier l'isolation des données
            for i, user in enumerate(users):
                history = get_history(user)
                self.assertEqual(len(history), 1)
                self.assertIn(f"Message {i}", history[0][0])
                
                facts = get_facts(user)
                self.assertEqual(len(facts), 1)
                self.assertIn(f"Fait {i}", facts[0])
            
            # Vérifier qu'un utilisateur ne voit pas les données d'un autre
            user1_history = get_history("user1")
            self.assertNotIn("Message 2", str(user1_history))
            
            db_manager.close_connections()

    def test_concurrent_database_access(self):
        """Test: Accès concurrent à la base de données"""
        import threading
        import time
        
        with patch('database.config.DB_PATH', self.test_db.name):
            modules_to_reset = ['database', 'memory']
            for module in modules_to_reset:
                if module in sys.modules:
                    del sys.modules[module]
            
            from database import DatabaseManager
            from memory import save_interaction, get_history
            
            db_manager = DatabaseManager(self.test_db.name)
            results = {}
            errors = {}
            
            def worker(thread_id):
                """Fonction worker pour test concurrent"""
                try:
                    user_id = f"thread_user_{thread_id}"
                    
                    # Chaque thread sauvegarde et récupère des données
                    for i in range(5):
                        save_interaction(user_id, f"Message {i}", f"Response {i}")
                        time.sleep(0.01)  # Petit délai pour simuler l'activité
                    
                    # Récupérer l'historique
                    history = get_history(user_id)
                    results[thread_id] = len(history)
                    
                except Exception as e:
                    errors[thread_id] = str(e)
            
            # Créer et lancer 3 threads
            threads = []
            for i in range(3):
                t = threading.Thread(target=worker, args=(i,))
                threads.append(t)
                t.start()
            
            # Attendre la fin de tous les threads
            for t in threads:
                t.join()
            
            # Vérifications
            self.assertEqual(len(errors), 0, f"Erreurs dans les threads: {errors}")
            self.assertEqual(len(results), 3)
            
            # Chaque thread doit avoir sauvegardé 5 interactions
            for thread_id, count in results.items():
                self.assertEqual(count, 5, f"Thread {thread_id} a {count} interactions au lieu de 5")
            
            db_manager.close_connections()


if __name__ == '__main__':
    unittest.main(verbosity=2)