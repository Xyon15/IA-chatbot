#!/usr/bin/env python3
"""
Tests unitaires pour le système de configuration du bot Neuro
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfigurationLoading(unittest.TestCase):
    """Test du chargement de configuration"""

    def setUp(self):
        """Configuration avant chaque test"""
        # Créer des fichiers temporaires pour les tests
        self.temp_env = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env')
        self.temp_model = tempfile.NamedTemporaryFile(delete=False, suffix='.gguf')
        
        # Écrire un fichier .env de test
        self.temp_env.write("DISCORD_TOKEN=test_token_123\n")
        self.temp_env.write("AUTH_SECRET=test_secret_456\n")
        self.temp_env.write("AUTHORIZED_ROLE=TestRole\n")
        self.temp_env.close()
        self.temp_model.close()

    def tearDown(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.temp_env.name):
            os.unlink(self.temp_env.name)
        if os.path.exists(self.temp_model.name):
            os.unlink(self.temp_model.name)

    @patch.dict(os.environ, {}, clear=True)
    def test_configuration_loading_works(self):
        """Test: Configuration loading works"""
        with patch('config.load_dotenv') as mock_load_dotenv:
            with patch('os.getenv') as mock_getenv:
                mock_getenv.side_effect = lambda key, default=None: {
                    'DISCORD_TOKEN': 'test_token',
                    'AUTH_SECRET': 'test_secret',
                    'AUTHORIZED_ROLE': 'NeuroMaster',
                    'N_GPU_LAYERS': '32',
                    'N_THREADS': '6',
                    'N_CTX': '4096',
                    'N_BATCH': '256',
                    'LLM_VERBOSE': 'True'
                }.get(key, default)
                
                with patch('os.path.exists', return_value=True):
                    # Réimporter le module config pour déclencher le chargement
                    if 'config' in sys.modules:
                        del sys.modules['config']
                    
                    import config
                    
                    # Vérifications
                    self.assertEqual(config.config.TOKEN, 'test_token')
                    self.assertEqual(config.config.AUTH_SECRET, 'test_secret')
                    self.assertEqual(config.config.AUTHORIZED_ROLE, 'NeuroMaster')
                    self.assertEqual(config.config.LLM_CONFIG['n_gpu_layers'], 32)
                    self.assertEqual(config.config.LLM_CONFIG['n_threads'], 6)

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_token_validation(self):
        """Test: Validation des tokens manquants"""
        with patch('config.load_dotenv'):
            with patch('os.getenv') as mock_getenv:
                # Simuler un token manquant
                mock_getenv.side_effect = lambda key, default=None: {
                    'DISCORD_TOKEN': None,  # Token manquant
                    'AUTH_SECRET': 'test_secret',
                }.get(key, default)
                
                with patch('os.path.exists', return_value=True):
                    # Doit lever ValueError
                    if 'config' in sys.modules:
                        del sys.modules['config']
                    
                    with self.assertRaises(ValueError) as cm:
                        import config
                    
                    self.assertIn("DISCORD_TOKEN manquant", str(cm.exception))

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_auth_secret_validation(self):
        """Test: Validation du secret d'auth manquant"""
        with patch('config.load_dotenv'):
            with patch('os.getenv') as mock_getenv:
                mock_getenv.side_effect = lambda key, default=None: {
                    'DISCORD_TOKEN': 'test_token',
                    'AUTH_SECRET': None,  # Secret manquant
                }.get(key, default)
                
                with patch('os.path.exists', return_value=True):
                    if 'config' in sys.modules:
                        del sys.modules['config']
                    
                    with self.assertRaises(ValueError) as cm:
                        import config
                    
                    self.assertIn("AUTH_SECRET manquant", str(cm.exception))

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_model_validation(self):
        """Test: Validation du modèle manquant"""
        with patch('config.load_dotenv'):
            with patch('os.getenv') as mock_getenv:
                mock_getenv.side_effect = lambda key, default=None: {
                    'DISCORD_TOKEN': 'test_token',
                    'AUTH_SECRET': 'test_secret',
                    'MODEL_PATH': '/non/existent/model.gguf'
                }.get(key, default)
                
                with patch('os.path.exists', return_value=False):
                    if 'config' in sys.modules:
                        del sys.modules['config']
                    
                    with self.assertRaises(FileNotFoundError) as cm:
                        import config
                    
                    self.assertIn("Modèle non trouvé", str(cm.exception))

    def test_llm_config_defaults(self):
        """Test: Valeurs par défaut de la configuration LLM"""
        with patch('config.load_dotenv'):
            with patch('os.getenv') as mock_getenv:
                # Simuler des variables d'environnement minimales
                mock_getenv.side_effect = lambda key, default=None: {
                    'DISCORD_TOKEN': 'test_token',
                    'AUTH_SECRET': 'test_secret',
                }.get(key, default)
                
                with patch('os.path.exists', return_value=True):
                    if 'config' in sys.modules:
                        del sys.modules['config']
                    
                    import config
                    
                    # Vérifier les valeurs par défaut
                    self.assertEqual(config.config.LLM_CONFIG['n_gpu_layers'], 32)
                    self.assertEqual(config.config.LLM_CONFIG['n_threads'], 6)
                    self.assertEqual(config.config.LLM_CONFIG['n_ctx'], 4096)
                    self.assertEqual(config.config.LLM_CONFIG['n_batch'], 256)
                    self.assertTrue(config.config.LLM_CONFIG['verbose'])

    def test_directory_creation(self):
        """Test: Création des dossiers nécessaires"""
        with patch('config.load_dotenv'):
            with patch('os.getenv') as mock_getenv:
                mock_getenv.side_effect = lambda key, default=None: {
                    'DISCORD_TOKEN': 'test_token',
                    'AUTH_SECRET': 'test_secret',
                }.get(key, default)
                
                with patch('os.path.exists', return_value=True):
                    with patch('os.makedirs') as mock_makedirs:
                        if 'config' in sys.modules:
                            del sys.modules['config']
                        
                        import config
                        
                        # Vérifier que makedirs a été appelé pour les dossiers nécessaires
                        mock_makedirs.assert_any_call(config.config.json_dir, exist_ok=True)
                        mock_makedirs.assert_any_call(config.config.models_dir, exist_ok=True)
                        mock_makedirs.assert_any_call(config.config.data_dir, exist_ok=True)

    def test_path_construction(self):
        """Test: Construction des chemins de fichiers"""
        with patch('config.load_dotenv'):
            with patch('os.getenv') as mock_getenv:
                mock_getenv.side_effect = lambda key, default=None: {
                    'DISCORD_TOKEN': 'test_token',
                    'AUTH_SECRET': 'test_secret',
                }.get(key, default)
                
                with patch('os.path.exists', return_value=True):
                    if 'config' in sys.modules:
                        del sys.modules['config']
                    
                    import config
                    
                    # Vérifier la construction des chemins
                    self.assertTrue(config.config.LIMITS_FILE.endswith('character_limits.json'))
                    self.assertTrue(config.config.WEB_STATE_FILE.endswith('web.json'))
                    self.assertTrue(config.config.CONFIG_PATH.endswith('context.json'))
                    self.assertTrue(config.config.AUTO_REPLY_PATH.endswith('autoreply.json'))
                    self.assertTrue(config.config.DB_PATH.endswith('neuro.db'))

    def test_backward_compatibility_variables(self):
        """Test: Variables de compatibilité avec l'ancien code"""
        with patch('config.load_dotenv'):
            with patch('os.getenv') as mock_getenv:
                mock_getenv.side_effect = lambda key, default=None: {
                    'DISCORD_TOKEN': 'test_token',
                    'AUTH_SECRET': 'test_secret',
                }.get(key, default)
                
                with patch('os.path.exists', return_value=True):
                    if 'config' in sys.modules:
                        del sys.modules['config']
                    
                    import config
                    
                    # Vérifier que les variables globales existent pour compatibilité
                    self.assertEqual(config.TOKEN, config.config.TOKEN)
                    self.assertEqual(config.AUTH_SECRET, config.config.AUTH_SECRET)
                    self.assertEqual(config.AUTHORIZED_ROLE, config.config.AUTHORIZED_ROLE)
                    self.assertEqual(config.DB_PATH, config.config.DB_PATH)
                    self.assertEqual(config.MODEL_PATH, config.config.MODEL_PATH)


class TestLoggingSetup(unittest.TestCase):
    """Test de la configuration du logging"""

    @patch('config.os.makedirs')
    @patch('config.logging.basicConfig')
    def test_logging_setup(self, mock_basic_config, mock_makedirs):
        """Test: Configuration du système de logging"""
        from config import setup_logging
        
        logger = setup_logging()
        
        # Vérifier que le dossier logs est créé
        mock_makedirs.assert_called_once()
        
        # Vérifier que la configuration de base est appelée
        mock_basic_config.assert_called_once()
        
        # Vérifier les paramètres de configuration
        args, kwargs = mock_basic_config.call_args
        self.assertIn('level', kwargs)
        self.assertIn('format', kwargs)
        self.assertIn('handlers', kwargs)
        
        # Vérifier que le logger est retourné
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, 'neuro_bot')

    @patch('config.os.makedirs')
    def test_log_directory_creation(self, mock_makedirs):
        """Test: Création du dossier de logs"""
        from config import setup_logging
        
        setup_logging()
        
        # Vérifier que makedirs a été appelé avec exist_ok=True
        call_args = mock_makedirs.call_args
        self.assertTrue(call_args[1]['exist_ok'])


if __name__ == '__main__':
    unittest.main(verbosity=2)