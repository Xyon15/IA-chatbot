#!/usr/bin/env python3
"""
Tests unitaires pour les opérations web du bot Neuro
"""

import unittest
import os
import sys
import tempfile
import json
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import aiohttp

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web import (
    load_web_state, save_web_state, 
    duckduckgo_search, duckduckgo_html_fallback
)


class TestWebStateOperations(unittest.TestCase):
    """Test des opérations d'état web"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.test_file.close()
        
        # Mock le chemin du fichier de configuration
        self.config_patcher = patch('web.config.WEB_STATE_FILE', self.test_file.name)
        self.config_patcher.start()

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.config_patcher.stop()
        if os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)

    def test_web_search_state_persistence(self):
        """Test: Web search state persistence"""
        # Sauvegarder état activé
        save_web_state(True)
        
        # Charger et vérifier
        state = load_web_state()
        self.assertTrue(state)
        
        # Sauvegarder état désactivé
        save_web_state(False)
        
        # Charger et vérifier
        state = load_web_state()
        self.assertFalse(state)

    def test_web_state_file_not_found(self):
        """Test: Fichier de configuration manquant"""
        # Supprimer le fichier
        os.unlink(self.test_file.name)
        
        # Charger doit retourner False par défaut
        state = load_web_state()
        self.assertFalse(state)

    def test_invalid_web_file_handling(self):
        """Test: Invalid file paths handling"""
        # Écrire un JSON invalide
        with open(self.test_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Doit retourner False sans lever d'exception
        state = load_web_state()
        self.assertFalse(state)

    def test_web_state_json_structure(self):
        """Test: Structure JSON correcte"""
        # Sauvegarder et vérifier la structure
        save_web_state(True)
        
        with open(self.test_file.name, 'r') as f:
            data = json.load(f)
        
        self.assertIn('enabled', data)
        self.assertTrue(data['enabled'])

    @patch('web.logger')
    def test_web_state_save_error_handling(self, mock_logger):
        """Test: Gestion des erreurs de sauvegarde"""
        # Simuler une erreur de sauvegarde en rendant le fichier en lecture seule
        os.chmod(self.test_file.name, 0o444)  # Lecture seule
        
        with self.assertRaises(Exception):
            save_web_state(True)
        
        # Vérifier que l'erreur a été loggée
        mock_logger.error.assert_called()
        
        # Restaurer les permissions
        os.chmod(self.test_file.name, 0o644)


class TestDuckDuckGoSearch(unittest.TestCase):
    """Test des fonctions de recherche DuckDuckGo"""

    @patch('web.aiohttp.ClientSession')
    async def test_successful_json_search(self, mock_session):
        """Test: Recherche JSON réussie"""
        # Mock de la réponse JSON
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            'Abstract': 'Test abstract result'
        })
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Tester la recherche
        result = await duckduckgo_search("test query")
        
        self.assertEqual(result, 'Test abstract result')

    @patch('web.aiohttp.ClientSession')
    async def test_json_with_answer(self, mock_session):
        """Test: Réponse JSON avec Answer"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            'Answer': 'Test answer result'
        })
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        result = await duckduckgo_search("test query")
        self.assertEqual(result, 'Test answer result')

    @patch('web.aiohttp.ClientSession')
    async def test_json_with_definition(self, mock_session):
        """Test: Réponse JSON avec Definition"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            'Definition': 'Test definition result'
        })
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        result = await duckduckgo_search("test query")
        self.assertEqual(result, 'Test definition result')

    @patch('web.duckduckgo_html_fallback')
    @patch('web.aiohttp.ClientSession')
    async def test_fallback_on_content_error(self, mock_session, mock_fallback):
        """Test: Fallback HTML sur erreur de contenu JSON"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(side_effect=aiohttp.ContentTypeError(
            request_info=MagicMock(), history=[]
        ))
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        mock_fallback.return_value = "Fallback result"
        
        result = await duckduckgo_search("test query")
        
        mock_fallback.assert_called_once_with("test query")
        self.assertEqual(result, "Fallback result")

    @patch('web.aiohttp.ClientSession')
    async def test_http_error_handling(self, mock_session):
        """Test: Gestion des erreurs HTTP"""
        mock_response = AsyncMock()
        mock_response.status = 404
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        result = await duckduckgo_search("test query")
        
        self.assertIn("❌ Erreur HTTP 404", result)

    @patch('web.aiohttp.ClientSession')
    async def test_timeout_handling(self, mock_session):
        """Test: Gestion du timeout"""
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.side_effect = asyncio.TimeoutError()
        
        result = await duckduckgo_search("test query")
        
        self.assertIn("❌ Temps de réponse trop long", result)


class TestHTMLFallback(unittest.TestCase):
    """Test du fallback HTML"""

    @patch('web.shorten_response')
    @patch('web.aiohttp.ClientSession')
    async def test_successful_html_parsing(self, mock_session, mock_shorten):
        """Test: Parsing HTML réussi"""
        # HTML fictif avec résultats
        mock_html = """
        <div class="result">
            <div class="result__snippet">Premier résultat de test</div>
        </div>
        <div class="result">
            <div class="result__snippet">Deuxième résultat de test</div>
        </div>
        """
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value=mock_html)
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        mock_shorten.return_value = "Shortened result"
        
        result = await duckduckgo_html_fallback("test query")
        
        # Vérifier que shorten_response a été appelé
        mock_shorten.assert_called_once()
        self.assertEqual(result, "Shortened result")

    @patch('web.aiohttp.ClientSession')
    async def test_html_no_results(self, mock_session):
        """Test: Aucun résultat trouvé dans HTML"""
        mock_html = "<html><body>No results here</body></html>"
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value=mock_html)
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        result = await duckduckgo_html_fallback("test query")
        
        self.assertIn("😶 Aucun résultat trouvé", result)

    @patch('web.aiohttp.ClientSession')
    async def test_html_http_error(self, mock_session):
        """Test: Erreur HTTP dans fallback HTML"""
        mock_response = AsyncMock()
        mock_response.status = 500
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        result = await duckduckgo_html_fallback("test query")
        
        self.assertIn("❌ Erreur HTTP 500", result)

    @patch('web.aiohttp.ClientSession')
    async def test_html_timeout_error(self, mock_session):
        """Test: Timeout dans fallback HTML"""
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.side_effect = asyncio.TimeoutError()
        
        result = await duckduckgo_html_fallback("test query")
        
        self.assertIn("❌ Timeout lors de la recherche HTML", result)

    @patch('web.aiohttp.ClientSession')
    async def test_html_parsing_error(self, mock_session):
        """Test: Erreur de parsing HTML"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(side_effect=Exception("Parsing error"))
        
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.return_value.get.return_value.__aexit__ = AsyncMock(return_value=None)
        
        result = await duckduckgo_html_fallback("test query")
        
        self.assertIn("❌ Erreur parsing HTML", result)


# Fonction helper pour exécuter les tests asyncio
def run_async_test(coro):
    """Execute une coroutine de test"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


if __name__ == '__main__':
    # Configurer asyncio pour les tests
    class AsyncTestCase(unittest.TestCase):
        def run_async(self, coro):
            return run_async_test(coro)
    
    # Patch les méthodes de test async pour qu'elles fonctionnent
    for test_class in [TestDuckDuckGoSearch, TestHTMLFallback]:
        for attr_name in dir(test_class):
            if attr_name.startswith('test_'):
                attr = getattr(test_class, attr_name)
                if asyncio.iscoroutinefunction(attr):
                    # Wrapper pour exécuter les tests async
                    def make_sync_test(async_test):
                        def sync_test(self):
                            return run_async_test(async_test(self))
                        return sync_test
                    
                    setattr(test_class, attr_name, make_sync_test(attr))
    
    unittest.main(verbosity=2)