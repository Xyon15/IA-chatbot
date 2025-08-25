#!/usr/bin/env python3
"""
Script principal pour exécuter tous les tests unitaires du bot Neuro
"""

import sys
import os
import unittest
import time
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import des modules de test
from test_memory_operations import TestMemoryOperations, TestAutoReplyOperations, TestDatabaseConnectionFailures
from test_web_operations import TestWebStateOperations, TestDuckDuckGoSearch, TestHTMLFallback
from test_configuration import TestConfigurationLoading, TestLoggingSetup
from test_database_manager import TestDatabaseManager, TestGlobalDatabaseFunctions
from test_utils_functions import TestTokenOperations, TestResponseShortening, TestUtilsWithoutTokenizer


def create_test_suite():
    """Créer la suite de tests complète"""
    suite = unittest.TestSuite()
    
    # Tests de mémoire
    suite.addTest(unittest.makeSuite(TestMemoryOperations))
    suite.addTest(unittest.makeSuite(TestAutoReplyOperations))
    suite.addTest(unittest.makeSuite(TestDatabaseConnectionFailures))
    
    # Tests web
    suite.addTest(unittest.makeSuite(TestWebStateOperations))
    suite.addTest(unittest.makeSuite(TestDuckDuckGoSearch))
    suite.addTest(unittest.makeSuite(TestHTMLFallback))
    
    # Tests de configuration
    suite.addTest(unittest.makeSuite(TestConfigurationLoading))
    suite.addTest(unittest.makeSuite(TestLoggingSetup))
    
    # Tests de base de données
    suite.addTest(unittest.makeSuite(TestDatabaseManager))
    suite.addTest(unittest.makeSuite(TestGlobalDatabaseFunctions))
    
    # Tests des utilitaires
    suite.addTest(unittest.makeSuite(TestTokenOperations))
    suite.addTest(unittest.makeSuite(TestResponseShortening))
    suite.addTest(unittest.makeSuite(TestUtilsWithoutTokenizer))
    
    return suite


def run_test_category(category_name, test_classes):
    """Exécuter une catégorie de tests"""
    print(f"\n{'='*60}")
    print(f"🧪 CATÉGORIE: {category_name}")
    print(f"{'='*60}")
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        suite.addTest(unittest.makeSuite(test_class))
    
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    return result.wasSuccessful(), result.testsRun, len(result.failures), len(result.errors)


def main():
    """Fonction principale"""
    print("🚀 LANCEMENT DES TESTS UNITAIRES - BOT NEURO")
    print("="*70)
    
    start_time = time.time()
    
    # Définir les catégories de tests
    test_categories = {
        "MÉMOIRE ET STOCKAGE": [
            TestMemoryOperations,
            TestAutoReplyOperations,
            TestDatabaseConnectionFailures
        ],
        "RECHERCHE WEB": [
            TestWebStateOperations,
            TestDuckDuckGoSearch,
            TestHTMLFallback
        ],
        "CONFIGURATION": [
            TestConfigurationLoading,
            TestLoggingSetup
        ],
        "BASE DE DONNÉES": [
            TestDatabaseManager,
            TestGlobalDatabaseFunctions
        ],
        "UTILITAIRES": [
            TestTokenOperations,
            TestResponseShortening,
            TestUtilsWithoutTokenizer
        ]
    }
    
    # Variables de suivi
    total_success = True
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    # Exécuter chaque catégorie
    for category_name, test_classes in test_categories.items():
        success, tests, failures, errors = run_test_category(category_name, test_classes)
        
        total_success = total_success and success
        total_tests += tests
        total_failures += failures
        total_errors += errors
        
        # Affichage du résumé de la catégorie
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"\n📊 {category_name}: {status}")
        print(f"   Tests: {tests} | Échecs: {failures} | Erreurs: {errors}")
    
    # Résumé final
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*70}")
    print("📈 RÉSUMÉ GLOBAL")
    print(f"{'='*70}")
    print(f"⏱️  Durée d'exécution: {duration:.2f} secondes")
    print(f"🧪 Total des tests: {total_tests}")
    print(f"✅ Tests réussis: {total_tests - total_failures - total_errors}")
    print(f"❌ Échecs: {total_failures}")
    print(f"💥 Erreurs: {total_errors}")
    
    if total_success:
        print(f"\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        print("✨ Le bot Neuro est prêt à fonctionner!")
        return_code = 0
    else:
        print(f"\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Veuillez vérifier les erreurs ci-dessus avant de déployer")
        return_code = 1
    
    print(f"\n{'='*70}")
    return return_code


def run_specific_test(test_name):
    """Exécuter un test spécifique"""
    print(f"🎯 Exécution du test spécifique: {test_name}")
    
    # Mapping des noms de tests
    test_mapping = {
        'memory': [TestMemoryOperations, TestAutoReplyOperations],
        'web': [TestWebStateOperations, TestDuckDuckGoSearch, TestHTMLFallback],
        'config': [TestConfigurationLoading, TestLoggingSetup],
        'database': [TestDatabaseManager, TestGlobalDatabaseFunctions],
        'utils': [TestTokenOperations, TestResponseShortening, TestUtilsWithoutTokenizer]
    }
    
    if test_name.lower() in test_mapping:
        test_classes = test_mapping[test_name.lower()]
        success, tests, failures, errors = run_test_category(test_name.upper(), test_classes)
        return 0 if success else 1
    else:
        print(f"❌ Test '{test_name}' non trouvé")
        print("Tests disponibles: memory, web, config, database, utils")
        return 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Exécuter un test spécifique
        test_name = sys.argv[1]
        sys.exit(run_specific_test(test_name))
    else:
        # Exécuter tous les tests
        sys.exit(main())