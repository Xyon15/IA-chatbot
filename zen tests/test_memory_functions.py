"""
Test complet des fonctions du module memory.py
"""
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from config import config, logger
from memory import (
    save_fact, get_facts, clear_facts,
    save_interaction, get_history, clear_memory, clear_all_memory,
    load_auto_reply, save_auto_reply
)


def test_auto_reply_functions():
    """Test des fonctions de réponse automatique"""
    print("🔍 Test des fonctions auto-reply...")
    
    try:
        # Test de sauvegarde et chargement
        original_state = load_auto_reply()
        print(f"   État initial: {original_state}")
        
        # Changer l'état
        save_auto_reply(True)
        new_state = load_auto_reply()
        print(f"   Après activation: {new_state}")
        
        # Remettre l'état original
        save_auto_reply(original_state)
        final_state = load_auto_reply()
        print(f"   État restauré: {final_state}")
        
        if final_state == original_state:
            print("   ✅ Fonctions auto-reply OK")
            return True
        else:
            print("   ❌ Problème avec les fonctions auto-reply")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur dans test auto-reply: {e}")
        return False


def test_memory_functions():
    """Test des fonctions de mémoire conversationnelle"""
    print("\n🔍 Test des fonctions de mémoire conversationnelle...")
    
    test_user = "test_memory_user"
    test_input = "Bonjour, comment ça va ?"
    test_response = "Ça va bien, merci !"
    
    try:
        # Nettoyer d'abord au cas où
        clear_memory(test_user)
        
        # Test de sauvegarde d'interaction
        save_interaction(test_user, test_input, test_response)
        print("   ✅ Interaction sauvegardée")
        
        # Test de récupération d'historique
        history = get_history(test_user, limit=5)
        print(f"   📚 Historique récupéré: {len(history)} entrées")
        
        if len(history) > 0:
            print(f"   📝 Dernière entrée: {history[-1]}")
            print("   ✅ Récupération d'historique OK")
        else:
            print("   ❌ Aucun historique récupéré")
            return False
        
        # Test de suppression
        deleted_count = clear_memory(test_user)
        print(f"   🗑️  {deleted_count} entrées supprimées")
        
        # Vérifier que c'est bien supprimé
        history_after = get_history(test_user, limit=5)
        if len(history_after) == 0:
            print("   ✅ Suppression OK")
            return True
        else:
            print("   ❌ Suppression incomplète")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur dans test mémoire: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_facts_functions():
    """Test des fonctions de faits"""
    print("\n🔍 Test des fonctions de faits...")
    
    test_user = "test_facts_user"
    test_facts = [
        "J'aime le café",
        "Je travaille dans l'informatique",
        "Mon langage préféré est Python"
    ]
    
    try:
        # Nettoyer d'abord
        clear_facts(test_user)
        
        # Test de sauvegarde de faits
        for fact in test_facts:
            save_fact(test_user, fact)
        print(f"   ✅ {len(test_facts)} faits sauvegardés")
        
        # Test de récupération de faits
        retrieved_facts = get_facts(test_user)
        print(f"   📚 Faits récupérés: {len(retrieved_facts)}")
        
        if len(retrieved_facts) == len(test_facts):
            print("   ✅ Tous les faits récupérés")
            for i, fact in enumerate(retrieved_facts):
                print(f"      {i+1}. {fact}")
        else:
            print(f"   ⚠️  Nombre de faits différent: attendu {len(test_facts)}, reçu {len(retrieved_facts)}")
        
        # Test de suppression de faits
        deleted_count = clear_facts(test_user)
        print(f"   🗑️  {deleted_count} faits supprimés")
        
        # Vérifier que c'est bien supprimé
        facts_after = get_facts(test_user)
        if len(facts_after) == 0:
            print("   ✅ Suppression des faits OK")
            return True
        else:
            print("   ❌ Suppression des faits incomplète")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur dans test faits: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_clear_all_functions():
    """Test des fonctions de suppression globale"""
    print("\n🔍 Test des fonctions de suppression globale...")
    
    test_users = ["user1", "user2", "user3"]
    
    try:
        # Ajouter quelques données de test
        for user in test_users:
            save_interaction(user, "Test input", "Test response")
            save_fact(user, f"Fait pour {user}")
        
        print(f"   📝 Données de test ajoutées pour {len(test_users)} utilisateurs")
        
        # Test de suppression globale de la mémoire (optionnel, commenté pour sécurité)
        # deleted_memory = clear_all_memory()
        # print(f"   🗑️  {deleted_memory} entrées de mémoire supprimées")
        
        # Test de suppression globale des faits
        deleted_facts = clear_facts()  # Sans paramètre = tous les faits
        print(f"   🗑️  {deleted_facts} faits supprimés")
        
        # Nettoyer les données de test restantes
        for user in test_users:
            clear_memory(user)
        
        print("   ✅ Nettoyage terminé")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur dans test suppression globale: {e}")
        return False


def main():
    """Fonction principale de test"""
    print("=" * 60)
    print("🧪 TEST COMPLET DES FONCTIONS MEMORY.PY")
    print("=" * 60)
    
    tests = [
        ("Auto-reply", test_auto_reply_functions),
        ("Mémoire conversationnelle", test_memory_functions),
        ("Faits", test_facts_functions),
        ("Suppression globale", test_clear_all_functions)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🚀 Lancement du test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n🎯 Résultat global: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Le module memory.py fonctionne correctement.")
    else:
        print("⚠️  Certains tests ont échoué. Vérification nécessaire.")


if __name__ == "__main__":
    main()