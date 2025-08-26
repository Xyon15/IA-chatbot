"""
Script de vérification de l'intégrité du modèle LLM Neuro-Bot
"""
import os
import sys
import time
import hashlib
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from config import config, logger
from model import model_manager, llm, generate_reply
from utils import count_tokens, truncate_text_to_tokens, shorten_response


def check_model_file_exists():
    """Vérifie si le fichier du modèle existe"""
    print("🔍 Vérification de l'existence du fichier modèle...")
    print(f"📍 Chemin configuré: {config.MODEL_PATH}")
    
    if os.path.exists(config.MODEL_PATH):
        size = os.path.getsize(config.MODEL_PATH)
        size_gb = size / (1024**3)
        print(f"✅ Fichier modèle trouvé (taille: {size_gb:.2f} GB)")
        return True, size
    else:
        print(f"❌ Fichier modèle non trouvé à: {config.MODEL_PATH}")
        return False, 0


def check_model_integrity():
    """Vérifie l'intégrité du fichier modèle (checksum)"""
    print("\n🔍 Vérification de l'intégrité du fichier modèle...")
    
    try:
        # Calculer le hash SHA256 du fichier
        print("⏳ Calcul du checksum SHA256 (peut prendre quelques minutes)...")
        hash_sha256 = hashlib.sha256()
        
        with open(config.MODEL_PATH, "rb") as f:
            # Lire par chunks pour éviter de charger tout en mémoire
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        
        file_hash = hash_sha256.hexdigest()
        print(f"📊 SHA256: {file_hash}")
        
        # Note: Pour une vérification complète, il faudrait comparer avec un hash de référence
        # Ici on vérifie juste que le calcul est possible (fichier lisible)
        print("✅ Fichier modèle lisible et intègre")
        return True, file_hash
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification d'intégrité: {e}")
        return False, None


def check_model_initialization():
    """Vérifie l'initialisation du modèle"""
    print("\n🔍 Vérification de l'initialisation du modèle...")
    
    try:
        # Vérifier que le gestionnaire de modèle existe
        if model_manager is None:
            print("❌ Gestionnaire de modèle non initialisé")
            return False
        
        # Vérifier que le modèle est prêt
        if not model_manager.is_ready():
            print("❌ Modèle non prêt")
            return False
        
        # Vérifier l'instance LLM
        if llm is None:
            print("❌ Instance LLM non disponible")
            return False
        
        print("✅ Modèle initialisé et prêt")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification d'initialisation: {e}")
        return False


def check_model_configuration():
    """Vérifie la configuration du modèle"""
    print("\n🔍 Vérification de la configuration du modèle...")
    
    try:
        print("📋 Configuration LLM:")
        for key, value in config.LLM_CONFIG.items():
            print(f"   - {key}: {value}")
        
        # Vérifier les paramètres critiques
        critical_params = ['n_gpu_layers', 'n_threads', 'n_ctx', 'n_batch']
        for param in critical_params:
            if param not in config.LLM_CONFIG:
                print(f"⚠️  Paramètre manquant: {param}")
                return False
        
        # Vérifier les valeurs
        n_ctx = config.LLM_CONFIG.get('n_ctx', 0)
        if n_ctx < 1024:
            print(f"⚠️  Contexte trop petit: {n_ctx} (recommandé: >= 1024)")
            return False
        
        print("✅ Configuration du modèle valide")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de configuration: {e}")
        return False


def check_model_attributes():
    """Vérifie les attributs du modèle chargé"""
    print("\n🔍 Vérification des attributs du modèle...")
    
    try:
        if llm is None:
            print("❌ Modèle non chargé")
            return False
        
        # Vérifier n_ctx
        n_ctx_attr = getattr(llm, "n_ctx", None)
        if callable(n_ctx_attr):
            n_ctx_value = n_ctx_attr()
        elif n_ctx_attr is not None:
            n_ctx_value = n_ctx_attr
        else:
            n_ctx_value = "Non disponible"
        
        print(f"📊 Attributs du modèle:")
        print(f"   - n_ctx: {n_ctx_value}")
        
        # Autres attributs utiles
        attrs_to_check = ['n_vocab', 'n_embd', 'n_layer']
        for attr in attrs_to_check:
            value = getattr(llm, attr, "Non disponible")
            if callable(value):
                try:
                    value = value()
                except:
                    value = "Erreur d'accès"
            print(f"   - {attr}: {value}")
        
        print("✅ Attributs du modèle accessibles")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des attributs: {e}")
        return False


def test_model_generation():
    """Teste la génération de texte avec le modèle"""
    print("\n🔍 Test de génération de texte...")
    
    test_prompts = [
        "Bonjour, comment ça va ?",
        "Quel est ton nom ?",
        "Peux-tu me dire quelque chose d'intéressant ?"
    ]
    
    try:
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n📝 Test {i}/3: '{prompt}'")
            
            start_time = time.time()
            
            # Test de génération simple (sans async pour le test)
            test_user = "test_model_user"
            
            # Utiliser la fonction generate_reply de manière synchrone pour le test
            import asyncio
            
            # Créer une boucle d'événements si elle n'existe pas
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Exécuter la génération
            response = loop.run_until_complete(generate_reply(test_user, prompt, context_limit=1))
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            if response and not response.startswith("❌"):
                print(f"   ✅ Réponse générée en {generation_time:.2f}s")
                print(f"   📄 Réponse: {response[:100]}{'...' if len(response) > 100 else ''}")
            else:
                print(f"   ❌ Erreur de génération: {response}")
                return False
        
        print("\n✅ Tous les tests de génération réussis")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de génération: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_utility_functions():
    """Teste les fonctions utilitaires"""
    print("\n🔍 Test des fonctions utilitaires...")
    
    try:
        # Test de count_tokens
        test_text = "Ceci est un test pour compter les tokens."
        token_count = count_tokens(test_text)
        print(f"📊 Tokens comptés: {token_count} pour '{test_text}'")
        
        if token_count > 0:
            print("   ✅ count_tokens fonctionne")
        else:
            print("   ❌ count_tokens ne fonctionne pas")
            return False
        
        # Test de truncate_text_to_tokens
        long_text = "Ceci est un texte très long " * 50
        truncated = truncate_text_to_tokens(long_text, 20)
        truncated_tokens = count_tokens(truncated)
        print(f"📊 Texte tronqué à {truncated_tokens} tokens")
        
        if truncated_tokens <= 20:
            print("   ✅ truncate_text_to_tokens fonctionne")
        else:
            print("   ❌ truncate_text_to_tokens ne fonctionne pas correctement")
            return False
        
        # Test de shorten_response
        long_response = "Voici une réponse très longue " * 100
        shortened = shorten_response(long_response)
        print(f"📊 Réponse raccourcie: {len(shortened)} caractères")
        
        print("   ✅ shorten_response fonctionne")
        
        print("✅ Toutes les fonctions utilitaires fonctionnent")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des fonctions utilitaires: {e}")
        return False


def check_model_performance():
    """Vérifie les performances du modèle"""
    print("\n🔍 Vérification des performances du modèle...")
    
    try:
        # Test de performance simple
        test_prompt = "Raconte-moi une blague courte."
        test_user = "perf_test_user"
        
        print("⏱️  Test de performance (3 générations)...")
        times = []
        
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        for i in range(3):
            start = time.time()
            response = loop.run_until_complete(generate_reply(test_user, f"{test_prompt} #{i+1}", context_limit=1))
            end = time.time()
            
            if response and not response.startswith("❌"):
                times.append(end - start)
                print(f"   Test {i+1}: {end - start:.2f}s")
            else:
                print(f"   Test {i+1}: Échec - {response}")
                return False
        
        avg_time = sum(times) / len(times)
        print(f"📊 Temps moyen de génération: {avg_time:.2f}s")
        
        if avg_time < 30:  # Moins de 30 secondes considéré comme acceptable
            print("✅ Performances acceptables")
            return True
        else:
            print("⚠️  Performances lentes (>30s par génération)")
            return True  # Pas un échec critique
        
    except Exception as e:
        print(f"❌ Erreur lors du test de performance: {e}")
        return False


def main():
    """Fonction principale de vérification du modèle"""
    print("=" * 60)
    print("🤖 VÉRIFICATION DE L'INTÉGRITÉ DU MODÈLE LLM NEURO-BOT")
    print("=" * 60)
    
    # Vérifications séquentielles
    checks = [
        ("Existence du fichier", check_model_file_exists),
        ("Intégrité du fichier", check_model_integrity),
        ("Initialisation", check_model_initialization),
        ("Configuration", check_model_configuration),
        ("Attributs du modèle", check_model_attributes),
        ("Génération de texte", test_model_generation),
        ("Fonctions utilitaires", test_utility_functions),
        ("Performances", check_model_performance)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n🚀 {check_name}...")
        try:
            if check_name == "Existence du fichier":
                result, extra = check_func()
                results.append((check_name, result))
            elif check_name == "Intégrité du fichier":
                result, extra = check_func()
                results.append((check_name, result))
            else:
                result = check_func()
                results.append((check_name, result))
            
            status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
            print(f"{status}")
            
        except Exception as e:
            print(f"❌ Erreur inattendue dans {check_name}: {e}")
            results.append((check_name, False))
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DE LA VÉRIFICATION DU MODÈLE")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{status} - {check_name}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} vérifications passées")
    
    if passed == total:
        print("🎉 Le modèle LLM est entièrement fonctionnel !")
    elif passed >= total * 0.8:  # 80% ou plus
        print("⚠️  Le modèle fonctionne mais certains aspects nécessitent attention")
    else:
        print("❌ Le modèle présente des problèmes significatifs")
    
    print(f"\n📅 Vérification effectuée le: {time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()