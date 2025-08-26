"""
Script de debug pour identifier les problèmes de la base de données
"""
import os
import sqlite3
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from config import config, logger
from database import get_db_connection


def debug_database():
    """Debug détaillé de la base de données"""
    print("🔍 DEBUG DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Test 1: Vérifier les tables
            print("1️⃣ Tables disponibles:")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for table in tables:
                print(f"   - {table[0]}")
            
            # Test 2: Structure de memory
            print("\n2️⃣ Structure de la table 'memory':")
            cursor.execute("PRAGMA table_info(memory)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'}")
            
            # Test 3: Structure de facts
            print("\n3️⃣ Structure de la table 'facts':")
            cursor.execute("PRAGMA table_info(facts)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'}")
            
            # Test 4: Compter les données
            print("\n4️⃣ Données présentes:")
            cursor.execute("SELECT COUNT(*) FROM memory")
            memory_count = cursor.fetchone()[0]
            print(f"   - memory: {memory_count} entrées")
            
            cursor.execute("SELECT COUNT(*) FROM facts")
            facts_count = cursor.fetchone()[0]
            print(f"   - facts: {facts_count} entrées")
            
            # Test 5: Vérifier les timestamps NULL dans memory
            print("\n5️⃣ Vérification des timestamps NULL dans memory:")
            cursor.execute("SELECT COUNT(*) FROM memory WHERE timestamp IS NULL")
            null_memory = cursor.fetchone()[0]
            print(f"   - Timestamps NULL dans memory: {null_memory}")
            
            # Test 6: Vérifier les timestamps NULL dans facts
            print("\n6️⃣ Vérification des timestamps NULL dans facts:")
            cursor.execute("SELECT COUNT(*) FROM facts WHERE timestamp IS NULL")
            null_facts = cursor.fetchone()[0]
            print(f"   - Timestamps NULL dans facts: {null_facts}")
            
            # Test 7: Échantillon de données memory
            print("\n7️⃣ Échantillon de données memory:")
            cursor.execute("SELECT id, user_id, timestamp FROM memory LIMIT 3")
            samples = cursor.fetchall()
            for sample in samples:
                print(f"   - ID: {sample[0]}, User: {sample[1]}, Time: {sample[2]}")
            
            # Test 8: Test d'insertion dans facts
            print("\n8️⃣ Test d'insertion dans facts:")
            test_user = "debug_test"
            test_fact = "Test de debug"
            
            cursor.execute("INSERT INTO facts (user_id, fact) VALUES (?, ?)", (test_user, test_fact))
            cursor.execute("SELECT * FROM facts WHERE user_id = ?", (test_user,))
            result = cursor.fetchone()
            
            if result:
                print(f"   ✅ Insertion réussie: {result}")
                # Nettoyer
                cursor.execute("DELETE FROM facts WHERE user_id = ?", (test_user,))
                conn.commit()
            else:
                print("   ❌ Insertion échouée")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    debug_database()