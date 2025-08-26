"""
Script de vérification de l'intégrité de la base de données Neuro-Bot
"""
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from config import config, logger
from database import get_db_connection, db_manager


def check_database_exists():
    """Vérifie si la base de données existe"""
    print(f"🔍 Vérification de l'existence de la base de données...")
    print(f"📍 Chemin configuré: {config.DB_PATH}")
    
    if os.path.exists(config.DB_PATH):
        size = os.path.getsize(config.DB_PATH)
        print(f"✅ Base de données trouvée (taille: {size} bytes)")
        return True
    else:
        print(f"❌ Base de données non trouvée à: {config.DB_PATH}")
        return False


def check_database_structure():
    """Vérifie la structure de la base de données"""
    print(f"\n🔍 Vérification de la structure de la base de données...")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier les tables existantes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📋 Tables trouvées: {tables}")
            
            expected_tables = ['memory', 'facts']
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Tables manquantes: {missing_tables}")
                return False
            else:
                print(f"✅ Toutes les tables requises sont présentes")
            
            # Vérifier la structure de chaque table
            for table in expected_tables:
                print(f"\n📊 Structure de la table '{table}':")
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                for col in columns:
                    print(f"  - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'} {'PRIMARY KEY' if col[5] else ''}")
            
            # Vérifier les index
            print(f"\n🔗 Index disponibles:")
            cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
            indexes = cursor.fetchall()
            for idx in indexes:
                print(f"  - {idx[0]} sur table {idx[1]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la structure: {e}")
        return False


def check_database_integrity():
    """Vérifie l'intégrité de la base de données avec PRAGMA integrity_check"""
    print(f"\n🔍 Vérification de l'intégrité de la base de données...")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            
            if result == "ok":
                print(f"✅ Intégrité de la base de données: OK")
                return True
            else:
                print(f"❌ Problème d'intégrité détecté: {result}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur lors de la vérification d'intégrité: {e}")
        return False


def get_database_statistics():
    """Affiche les statistiques de la base de données"""
    print(f"\n📊 Statistiques de la base de données...")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Statistiques de la table memory
            cursor.execute("SELECT COUNT(*) FROM memory")
            memory_count = cursor.fetchone()[0]
            print(f"💭 Entrées dans 'memory': {memory_count}")
            
            if memory_count > 0:
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM memory")
                unique_users_memory = cursor.fetchone()[0]
                print(f"👥 Utilisateurs uniques dans 'memory': {unique_users_memory}")
                
                cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM memory")
                min_date, max_date = cursor.fetchone()
                print(f"📅 Période couverte (memory): {min_date} → {max_date}")
            
            # Statistiques de la table facts
            cursor.execute("SELECT COUNT(*) FROM facts")
            facts_count = cursor.fetchone()[0]
            print(f"📝 Entrées dans 'facts': {facts_count}")
            
            if facts_count > 0:
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM facts")
                unique_users_facts = cursor.fetchone()[0]
                print(f"👥 Utilisateurs uniques dans 'facts': {unique_users_facts}")
                
                cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM facts")
                min_date, max_date = cursor.fetchone()
                print(f"📅 Période couverte (facts): {min_date} → {max_date}")
            
            # Taille de la base de données
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            db_size = page_count * page_size
            print(f"💾 Taille de la base: {db_size} bytes ({db_size / 1024:.2f} KB)")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des statistiques: {e}")


def check_data_consistency():
    """Vérifie la cohérence des données"""
    print(f"\n🔍 Vérification de la cohérence des données...")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier les entrées avec des champs vides
            cursor.execute("SELECT COUNT(*) FROM memory WHERE user_id = '' OR user_input = '' OR bot_response = ''")
            empty_memory = cursor.fetchone()[0]
            if empty_memory > 0:
                print(f"⚠️  Entrées 'memory' avec champs vides: {empty_memory}")
            else:
                print(f"✅ Aucune entrée 'memory' avec champs vides")
            
            cursor.execute("SELECT COUNT(*) FROM facts WHERE user_id = '' OR fact = ''")
            empty_facts = cursor.fetchone()[0]
            if empty_facts > 0:
                print(f"⚠️  Entrées 'facts' avec champs vides: {empty_facts}")
            else:
                print(f"✅ Aucune entrée 'facts' avec champs vides")
            
            # Vérifier les timestamps invalides
            cursor.execute("SELECT COUNT(*) FROM memory WHERE timestamp IS NULL")
            null_timestamps_memory = cursor.fetchone()[0]
            if null_timestamps_memory > 0:
                print(f"⚠️  Entrées 'memory' avec timestamp NULL: {null_timestamps_memory}")
            else:
                print(f"✅ Tous les timestamps 'memory' sont valides")
            
            cursor.execute("SELECT COUNT(*) FROM facts WHERE timestamp IS NULL")
            null_timestamps_facts = cursor.fetchone()[0]
            if null_timestamps_facts > 0:
                print(f"⚠️  Entrées 'facts' avec timestamp NULL: {null_timestamps_facts}")
            else:
                print(f"✅ Tous les timestamps 'facts' sont valides")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de cohérence: {e}")


def test_database_operations():
    """Teste les opérations de base sur la base de données"""
    print(f"\n🔍 Test des opérations de base de données...")
    
    test_user_id = "test_integrity_check"
    test_input = "Test d'intégrité"
    test_response = "Réponse de test"
    test_fact = "Fait de test pour vérification"
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Test d'insertion dans memory
            cursor.execute("""
                INSERT INTO memory (user_id, user_input, bot_response)
                VALUES (?, ?, ?)
            """, (test_user_id, test_input, test_response))
            
            # Test de lecture
            cursor.execute("SELECT * FROM memory WHERE user_id = ?", (test_user_id,))
            result = cursor.fetchone()
            if result:
                print(f"✅ Test d'insertion/lecture 'memory': OK")
            else:
                print(f"❌ Test d'insertion/lecture 'memory': ÉCHEC")
            
            # Test d'insertion dans facts
            cursor.execute("""
                INSERT INTO facts (user_id, fact)
                VALUES (?, ?)
            """, (test_user_id, test_fact))
            
            # Test de lecture facts
            cursor.execute("SELECT * FROM facts WHERE user_id = ?", (test_user_id,))
            result = cursor.fetchone()
            if result:
                print(f"✅ Test d'insertion/lecture 'facts': OK")
            else:
                print(f"❌ Test d'insertion/lecture 'facts': ÉCHEC")
            
            # Nettoyage des données de test
            cursor.execute("DELETE FROM memory WHERE user_id = ?", (test_user_id,))
            cursor.execute("DELETE FROM facts WHERE user_id = ?", (test_user_id,))
            conn.commit()
            
            print(f"✅ Données de test nettoyées")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des opérations: {e}")


def main():
    """Fonction principale de vérification"""
    print("=" * 60)
    print("🤖 VÉRIFICATION DE L'INTÉGRITÉ DE LA BASE DE DONNÉES NEURO-BOT")
    print("=" * 60)
    
    # Vérifications séquentielles
    checks = [
        check_database_exists,
        check_database_structure,
        check_database_integrity,
        check_data_consistency,
        test_database_operations
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur inattendue dans {check.__name__}: {e}")
            results.append(False)
    
    # Affichage des statistiques
    get_database_statistics()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    if passed == total:
        print(f"✅ Toutes les vérifications sont passées ({passed}/{total})")
        print("🎉 La base de données est en bon état !")
    else:
        print(f"⚠️  {total - passed} vérification(s) ont échoué sur {total}")
        print("🔧 Des actions correctives peuvent être nécessaires")
    
    print(f"\n📅 Vérification effectuée le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()