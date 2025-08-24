#!/usr/bin/env python3
"""
Script de test pour vérifier les améliorations apportées au bot
"""

import sys
import os
import traceback
from pathlib import Path

def test_imports():
    """Test des imports principaux"""
    print("🧪 Test des imports...")
    
    try:
        from config import config, logger
        print("✅ Config et logger importés")
        
        from database import init_database, get_db_connection
        print("✅ Database importé")
        
        from memory import get_history, save_fact, get_facts
        print("✅ Memory importé")
        
        from auth_decorators import require_2fa, require_authorized_role
        print("✅ Auth decorators importés")
        
        from model import ModelManager
        print("✅ Model manager importé")
        
        from web import load_web_state, save_web_state
        print("✅ Web functions importées")
        
        return True
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        traceback.print_exc()
        return False

def test_config():
    """Test de la configuration"""
    print("\n🧪 Test de la configuration...")
    
    try:
        from config import config, logger
        
        # Test des chemins
        assert hasattr(config, 'MODEL_PATH'), "MODEL_PATH manquant"
        assert hasattr(config, 'DB_PATH'), "DB_PATH manquant"
        assert hasattr(config, 'TOKEN'), "TOKEN manquant"
        
        # Test du logger
        logger.info("Test du logger")
        
        print("✅ Configuration valide")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def test_database():
    """Test de la base de données"""
    print("\n🧪 Test de la base de données...")
    
    try:
        from database import init_database, get_db_connection
        
        # Initialisation
        init_database()
        
        # Test de connexion
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
        print(f"✅ Base de données initialisée avec {len(tables)} tables")
        return True
    except Exception as e:
        print(f"❌ Erreur de base de données: {e}")
        return False

def test_memory():
    """Test du système de mémoire"""
    print("\n🧪 Test du système de mémoire...")
    
    try:
        from memory import save_fact, get_facts, clear_facts
        
        test_user = "test_user_123"
        test_fact = "Test fact for improvements"
        
        # Sauvegarde
        save_fact(test_user, test_fact)
        
        # Récupération
        facts = get_facts(test_user)
        assert test_fact in facts, "Fait non trouvé"
        
        # Nettoyage
        clear_facts(test_user)
        
        print("✅ Système de mémoire fonctionnel")
        return True
    except Exception as e:
        print(f"❌ Erreur de mémoire: {e}")
        return False

def test_web():
    """Test des fonctions web"""
    print("\n🧪 Test des fonctions web...")
    
    try:
        from web import load_web_state, save_web_state
        
        # Test de sauvegarde/chargement
        save_web_state(True)
        state = load_web_state()
        assert state == True, "État web incorrect"
        
        save_web_state(False)
        state = load_web_state()
        assert state == False, "État web incorrect"
        
        print("✅ Fonctions web opérationnelles")
        return True
    except Exception as e:
        print(f"❌ Erreur web: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test des améliorations du bot Neuro")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_database,
        test_memory,
        test_web
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} échoué: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Les améliorations sont fonctionnelles.")
        return 0
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main())