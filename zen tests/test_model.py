#!/usr/bin/env python3
"""
Tests pour le module model.py - Focus sur la fonction generate_reply et le bug n_ctx
"""

import sys
import asyncio
import unittest.mock as mock
from pathlib import Path

# Test imports
def test_imports():
    """Test des imports du module model"""
    print("🧪 Test des imports du module model...")
    
    try:
        from model import ModelManager, model_manager, generate_reply
        from config import config, logger
        from utils import count_tokens, truncate_text_to_tokens, shorten_response
        from memory import save_interaction, get_history, get_facts
        print("✅ Imports du module model réussis")
        return True
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_generate_successful_response():
    """Test de génération d'une réponse réussie"""
    print("\n🧪 Test de génération d'une réponse réussie...")
    
    try:
        from model import generate_reply, model_manager
        
        # Mock du modèle et des dépendances
        with mock.patch.object(model_manager, 'is_ready', return_value=True):
            with mock.patch('model.llm') as mock_llm:
                # Configuration du mock llm avec n_ctx en tant qu'entier (cas normal)
                mock_llm.n_ctx = 4096
                mock_llm.return_value = {
                    "choices": [{"text": "Bonjour ! Comment ça va ?"}]
                }
                
                with mock.patch('model.get_history', return_value=[]):
                    with mock.patch('model.get_facts', return_value=[]):
                        with mock.patch('model.count_tokens', return_value=100):
                            with mock.patch('model.save_interaction'):
                                with mock.patch('model.shorten_response', return_value="Bonjour ! Comment ça va ?"):
                                    
                                    result = asyncio.run(generate_reply("user123", "Salut !", 5))
                                    
                                    assert isinstance(result, str), "La réponse doit être une chaîne"
                                    assert len(result) > 0, "La réponse ne doit pas être vide"
                                    assert "❌" not in result, "La réponse ne doit pas contenir d'erreur"
                                    
        print("✅ Test de génération réussie passé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test de génération réussie: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_handle_n_ctx_as_method():
    """Test de gestion de n_ctx en tant que méthode (BUG IDENTIFIÉ)"""
    print("\n🧪 Test de gestion de n_ctx en tant que méthode (BUG)...")
    
    try:
        from model import generate_reply, model_manager
        
        # Mock du modèle avec n_ctx comme méthode au lieu d'un entier
        with mock.patch.object(model_manager, 'is_ready', return_value=True):
            with mock.patch('model.llm') as mock_llm:
                # Simulation du bug: n_ctx est une méthode, pas un entier
                mock_llm.n_ctx = lambda: 4096  # Méthode au lieu d'entier
                mock_llm.return_value = {
                    "choices": [{"text": "Réponse de test"}]
                }
                
                with mock.patch('model.get_history', return_value=[]):
                    with mock.patch('model.get_facts', return_value=[]):
                        with mock.patch('model.count_tokens', return_value=100):
                            with mock.patch('model.save_interaction'):
                                with mock.patch('model.shorten_response', return_value="Réponse de test"):
                                    
                                    result = asyncio.run(generate_reply("user123", "Test", 5))
                                    
                                    # Ce test devrait échouer avec le bug actuel
                                    # Si on arrive ici sans erreur, le bug est corrigé
                                    if "❌ Erreur lors de la génération:" in result:
                                        print("🐛 Bug confirmé: n_ctx en tant que méthode cause une erreur")
                                        return False
                                    else:
                                        print("✅ Bug corrigé: n_ctx méthode gérée correctement")
                                        return True
                                    
    except TypeError as e:
        if "'<=' not supported between instances of 'int' and 'method'" in str(e):
            print("🐛 Bug confirmé: erreur de comparaison int/méthode détectée")
            return False
        else:
            print(f"❌ Erreur inattendue: {e}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test n_ctx méthode: {e}")
        return False

def test_handle_model_not_ready():
    """Test de gestion quand le modèle n'est pas prêt"""
    print("\n🧪 Test de gestion du modèle non prêt...")
    
    try:
        from model import generate_reply, model_manager
        
        # Mock du modèle non prêt
        with mock.patch.object(model_manager, 'is_ready', return_value=False):
            result = asyncio.run(generate_reply("user123", "Test", 5))
            
            assert "❌ Modèle non initialisé" == result, "Message d'erreur incorrect"
            
        print("✅ Test modèle non prêt passé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test modèle non prêt: {e}")
        return False

def test_handle_empty_prompt():
    """Test de gestion d'un prompt vide"""
    print("\n🧪 Test de gestion d'un prompt vide...")
    
    try:
        from model import generate_reply, model_manager
        
        with mock.patch.object(model_manager, 'is_ready', return_value=True):
            with mock.patch('model.llm') as mock_llm:
                mock_llm.n_ctx = 4096
                mock_llm.return_value = {
                    "choices": [{"text": "Je n'ai pas de question à traiter."}]
                }
                
                with mock.patch('model.get_history', return_value=[]):
                    with mock.patch('model.get_facts', return_value=[]):
                        with mock.patch('model.count_tokens', return_value=50):
                            with mock.patch('model.save_interaction'):
                                with mock.patch('model.shorten_response', return_value="Je n'ai pas de question à traiter."):
                                    
                                    result = asyncio.run(generate_reply("user123", "", 5))
                                    
                                    assert isinstance(result, str), "La réponse doit être une chaîne"
                                    assert len(result) > 0, "La réponse ne doit pas être vide"
                                    
        print("✅ Test prompt vide passé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test prompt vide: {e}")
        return False

def test_handle_token_limit_exceeded():
    """Test de gestion du dépassement de limite de tokens"""
    print("\n🧪 Test de gestion du dépassement de limite de tokens...")
    
    try:
        from model import generate_reply, model_manager
        
        with mock.patch.object(model_manager, 'is_ready', return_value=True):
            with mock.patch('model.llm') as mock_llm:
                mock_llm.n_ctx = 4096
                
                with mock.patch('model.get_history', return_value=[]):
                    with mock.patch('model.get_facts', return_value=[]):
                        # Simuler un prompt très long (plus de tokens que disponible)
                        with mock.patch('model.count_tokens', return_value=4500):  # > 4096
                            with mock.patch('model.truncate_text_to_tokens') as mock_truncate:
                                mock_truncate.return_value = "Prompt tronqué"
                                with mock.patch('model.count_tokens', return_value=100):  # Après troncature
                                    mock_llm.return_value = {
                                        "choices": [{"text": "Réponse après troncature"}]
                                    }
                                    
                                    with mock.patch('model.save_interaction'):
                                        with mock.patch('model.shorten_response', return_value="Réponse après troncature"):
                                            
                                            result = asyncio.run(generate_reply("user123", "Prompt très long", 5))
                                            
                                            # Vérifier que la troncature a été appelée
                                            mock_truncate.assert_called_once()
                                            assert "❌" not in result, "Ne devrait pas y avoir d'erreur après troncature"
                                            
        print("✅ Test dépassement tokens passé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test dépassement tokens: {e}")
        return False

def test_reduce_context_when_needed():
    """Test de réduction du contexte quand nécessaire"""
    print("\n🧪 Test de réduction du contexte...")
    
    try:
        from model import generate_reply, model_manager
        
        with mock.patch.object(model_manager, 'is_ready', return_value=True):
            with mock.patch('model.llm') as mock_llm:
                mock_llm.n_ctx = 1000  # Contexte limité
                mock_llm.return_value = {
                    "choices": [{"text": "Réponse avec contexte réduit"}]
                }
                
                # Simuler un historique qui force la réduction du contexte
                long_history = [("Message très long " * 50, "Réponse très longue " * 50)] * 10
                with mock.patch('model.get_history', return_value=long_history):
                    with mock.patch('model.get_facts', return_value=[]):
                        # Premier appel: tokens élevés, forçant la réduction
                        with mock.patch('model.count_tokens', side_effect=[900, 800, 700, 200]):
                            with mock.patch('model.save_interaction'):
                                with mock.patch('model.shorten_response', return_value="Réponse avec contexte réduit"):
                                    
                                    result = asyncio.run(generate_reply("user123", "Test", 10))
                                    
                                    assert "❌" not in result, "Ne devrait pas y avoir d'erreur"
                                    
        print("✅ Test réduction contexte passé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test réduction contexte: {e}")
        return False

def test_handle_llm_generation_error():
    """Test de gestion d'erreur lors de la génération LLM"""
    print("\n🧪 Test de gestion d'erreur lors de la génération...")
    
    try:
        from model import generate_reply, model_manager
        
        with mock.patch.object(model_manager, 'is_ready', return_value=True):
            with mock.patch('model.llm') as mock_llm:
                mock_llm.n_ctx = 4096
                # Simuler une erreur lors de la génération
                mock_llm.side_effect = RuntimeError("Erreur de génération du modèle")
                
                with mock.patch('model.get_history', return_value=[]):
                    with mock.patch('model.get_facts', return_value=[]):
                        with mock.patch('model.count_tokens', return_value=100):
                            
                            result = asyncio.run(generate_reply("user123", "Test", 5))
                            
                            assert "❌ Erreur lors de la génération:" in result, "Message d'erreur attendu"
                            
        print("✅ Test erreur génération passé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test erreur génération: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Tests du module model.py - Focus sur generate_reply")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_generate_successful_response,
        test_handle_n_ctx_as_method,  # Test du bug principal
        test_handle_model_not_ready,
        test_handle_empty_prompt,
        test_handle_token_limit_exceeded,
        test_reduce_context_when_needed,
        test_handle_llm_generation_error
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} échoué: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés !")
        return 0
    else:
        print("⚠️ Certains tests ont échoué.")
        print("💡 Le test 'test_handle_n_ctx_as_method' devrait échouer tant que le bug n'est pas corrigé.")
        return 1

if __name__ == "__main__":
    sys.exit(main())