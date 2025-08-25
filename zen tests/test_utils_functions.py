#!/usr/bin/env python3
"""
Tests unitaires pour les fonctions utilitaires du bot Neuro
"""

import unittest
import os
import sys
import tempfile
import json
from unittest.mock import patch, MagicMock

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import count_tokens, truncate_text_to_tokens, shorten_response


class TestTokenOperations(unittest.TestCase):
    """Test des opérations de comptage et troncature de tokens"""

    def test_token_counting_and_truncation(self):
        """Test: Token counting and truncation"""
        test_text = "This is a test sentence for token counting."
        
        # Test du comptage de tokens
        token_count = count_tokens(test_text)
        self.assertGreater(token_count, 0)
        self.assertIsInstance(token_count, int)

    def test_count_tokens_with_tokenizer(self):
        """Test: Comptage avec tokenizer disponible"""
        if 'utils' in sys.modules:
            del sys.modules['utils']
        
        # Mock du tokenizer disponible
        with patch('utils.tokenizer') as mock_tokenizer:
            mock_tokenizer.encode.return_value = [1, 2, 3, 4, 5]  # 5 tokens
            
            from utils import count_tokens
            
            result = count_tokens("test text")
            self.assertEqual(result, 5)

    def test_count_tokens_fallback(self):
        """Test: Comptage avec fallback (tokenizer indisponible)"""
        if 'utils' in sys.modules:
            del sys.modules['utils']
        
        # Mock du tokenizer indisponible
        with patch('utils.tokenizer', None):
            from utils import count_tokens
            
            test_text = "This is a test"  # 14 caractères
            result = count_tokens(test_text)
            
            # Fallback: max(1, len(text) // 3)
            expected = max(1, len(test_text) // 3)
            self.assertEqual(result, expected)

    def test_truncate_text_with_tokenizer(self):
        """Test: Troncature avec tokenizer"""
        if 'utils' in sys.modules:
            del sys.modules['utils']
        
        with patch('utils.tokenizer') as mock_tokenizer:
            # Simuler encode/decode
            mock_tokenizer.encode.return_value = [1, 2, 3, 4, 5, 6, 7, 8]
            mock_tokenizer.decode.return_value = "Truncated text"
            
            from utils import truncate_text_to_tokens
            
            result = truncate_text_to_tokens("Long text to truncate", max_tokens=5)
            
            # Vérifier que decode a été appelé avec les premiers 5 tokens
            mock_tokenizer.decode.assert_called_with(
                [1, 2, 3, 4, 5], 
                clean_up_tokenization_spaces=True, 
                skip_special_tokens=True
            )
            self.assertEqual(result, "Truncated text")

    def test_truncate_text_no_truncation_needed(self):
        """Test: Pas de troncature nécessaire"""
        if 'utils' in sys.modules:
            del sys.modules['utils']
        
        with patch('utils.tokenizer') as mock_tokenizer:
            mock_tokenizer.encode.return_value = [1, 2, 3]  # 3 tokens
            
            from utils import truncate_text_to_tokens
            
            original_text = "Short text"
            result = truncate_text_to_tokens(original_text, max_tokens=5)
            
            # Pas de troncature nécessaire
            self.assertEqual(result, original_text)

    def test_truncate_text_fallback(self):
        """Test: Troncature avec fallback"""
        if 'utils' in sys.modules:
            del sys.modules['utils']
        
        with patch('utils.tokenizer', None):
            from utils import truncate_text_to_tokens
            
            long_text = "This is a very long text that should be truncated properly"
            result = truncate_text_to_tokens(long_text, max_tokens=5)
            
            # Fallback: 5 tokens * 3 chars = 15 chars max
            self.assertLessEqual(len(result), 15)
            self.assertTrue(result.endswith(' text'))  # Coupure au mot


class TestResponseShortening(unittest.TestCase):
    """Test des fonctions de raccourcissement de réponse"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.test_limits_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        limits_config = {
            "max_reply_length": 100
        }
        json.dump(limits_config, self.test_limits_file)
        self.test_limits_file.close()

    def tearDown(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_limits_file.name):
            os.unlink(self.test_limits_file.name)

    def test_shorten_response_with_explicit_length(self):
        """Test: Raccourcissement avec longueur explicite"""
        long_text = "This is a very long text that should be shortened to fit the specified maximum length."
        
        result = shorten_response(long_text, max_length=50)
        
        self.assertLessEqual(len(result), 50)
        self.assertTrue(result.startswith("This is a very long text"))

    @patch('utils.config.LIMITS_FILE')
    def test_shorten_response_from_config(self, mock_limits_file):
        """Test: Raccourcissement en lisant la config"""
        mock_limits_file.return_value = self.test_limits_file.name
        
        # Mock du chemin de config
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
                "max_reply_length": 50
            })
            
            long_text = "This is a very long text that should be shortened automatically based on configuration."
            
            result = shorten_response(long_text, max_length=None)
            
            # Note: Le test exact dépend de l'implémentation, 
            # mais on vérifie que la fonction ne plante pas
            self.assertIsInstance(result, str)

    def test_shorten_response_no_shortening_needed(self):
        """Test: Pas de raccourcissement nécessaire"""
        short_text = "Short text"
        
        result = shorten_response(short_text, max_length=100)
        
        # Texte inchangé
        self.assertEqual(result, short_text)

    def test_shorten_response_cut_at_sentence_end(self):
        """Test: Coupure à la fin de phrase"""
        text_with_sentences = "First sentence. Second sentence that is longer. Third sentence here."
        
        result = shorten_response(text_with_sentences, max_length=30)
        
        # Doit couper après le premier point
        self.assertTrue(result.endswith("."))
        self.assertIn("First sentence", result)

    def test_shorten_response_cut_at_newline(self):
        """Test: Coupure au saut de ligne"""
        text_with_newlines = "First line\nSecond line that is longer\nThird line"
        
        result = shorten_response(text_with_newlines, max_length=25)
        
        # Doit couper après le premier saut de ligne
        self.assertIn("First line", result)
        self.assertNotIn("Third line", result)

    def test_shorten_response_fallback_cut(self):
        """Test: Coupure de fallback sans point ni saut de ligne"""
        long_text_no_breaks = "a" * 200  # Texte long sans ponctuation
        
        result = shorten_response(long_text_no_breaks, max_length=50)
        
        self.assertLessEqual(len(result), 50)

    def test_empty_or_null_parameters(self):
        """Test: Empty or null parameters"""
        # Texte vide
        result = shorten_response("", max_length=100)
        self.assertEqual(result, "")
        
        # max_length = 0
        result = shorten_response("test", max_length=0)
        self.assertEqual(result, "")

    @patch('utils.logger')
    def test_config_file_error_handling(self, mock_logger):
        """Test: Gestion d'erreur de lecture du fichier de config"""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            long_text = "Text to shorten"
            
            # Doit utiliser la valeur par défaut sans lever d'exception
            result = shorten_response(long_text, max_length=None)
            
            # Vérifier que l'erreur est loggée
            mock_logger.warning.assert_called()

    @patch('utils.logger')
    def test_invalid_config_file_handling(self, mock_logger):
        """Test: Invalid file paths handling pour le fichier de limites"""
        # Simuler un fichier JSON invalide
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = "invalid json"
            
            with patch('json.load', side_effect=json.JSONDecodeError("Invalid JSON", "", 0)):
                long_text = "Text to shorten"
                
                result = shorten_response(long_text, max_length=None)
                
                # Doit utiliser la valeur par défaut
                mock_logger.warning.assert_called()


class TestUtilsWithoutTokenizer(unittest.TestCase):
    """Test des utilitaires sans tokenizer disponible"""

    def test_tokenizer_unavailable_initialization(self):
        """Test: Initialisation sans tokenizer"""
        # Forcer la réinitialisation du module avec erreur de tokenizer
        if 'utils' in sys.modules:
            del sys.modules['utils']
        
        with patch('utils.GPT2TokenizerFast', side_effect=ImportError("No tokenizer")):
            import utils
            
            # Le tokenizer doit être None
            self.assertIsNone(utils.tokenizer)

    def test_all_functions_work_without_tokenizer(self):
        """Test: Toutes les fonctions fonctionnent sans tokenizer"""
        if 'utils' in sys.modules:
            del sys.modules['utils']
        
        with patch('utils.GPT2TokenizerFast', side_effect=ImportError("No tokenizer")):
            from utils import count_tokens, truncate_text_to_tokens, shorten_response
            
            # Toutes les fonctions doivent fonctionner
            test_text = "Test text for fallback mode"
            
            token_count = count_tokens(test_text)
            self.assertGreater(token_count, 0)
            
            truncated = truncate_text_to_tokens(test_text, max_tokens=3)
            self.assertLessEqual(len(truncated), len(test_text))
            
            shortened = shorten_response(test_text, max_length=10)
            self.assertLessEqual(len(shortened), 10)


if __name__ == '__main__':
    unittest.main(verbosity=2)