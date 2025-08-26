"""
Script de migration automatique pour corriger la structure de la base de données Neuro-Bot
"""
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from config import config, logger


def backup_database():
    """Crée une sauvegarde de la base de données avant migration"""
    backup_path = f"{config.DB_PATH}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        import shutil
        shutil.copy2(config.DB_PATH, backup_path)
        print(f"✅ Sauvegarde créée: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return None


def check_facts_table_structure():
    """Vérifie la structure actuelle de la table facts"""
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(facts)")
        columns = cursor.fetchall()
        
        print("📊 Structure actuelle de la table 'facts':")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'} {'PRIMARY KEY' if col[5] else ''}")
        
        # Vérifier si les colonnes requises existent
        column_names = [col[1] for col in columns]
        required_columns = ['id', 'user_id', 'fact', 'timestamp']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        conn.close()
        return missing_columns
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return None


def migrate_facts_table():
    """Migre la table facts vers la nouvelle structure"""
    print("\n🔄 Migration de la table 'facts'...")
    
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        
        # Vérifier s'il y a des données existantes
        cursor.execute("SELECT COUNT(*) FROM facts")
        existing_count = cursor.fetchone()[0]
        print(f"📊 Données existantes dans 'facts': {existing_count}")
        
        # Sauvegarder les données existantes si elles existent
        existing_data = []
        if existing_count > 0:
            cursor.execute("SELECT user_id, fact FROM facts")
            existing_data = cursor.fetchall()
            print(f"💾 Sauvegarde de {len(existing_data)} entrées existantes")
        
        # Supprimer l'ancienne table
        cursor.execute("DROP TABLE IF EXISTS facts")
        print("🗑️  Ancienne table 'facts' supprimée")
        
        # Créer la nouvelle table avec la structure correcte
        cursor.execute("""
            CREATE TABLE facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                fact TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("🆕 Nouvelle table 'facts' créée")
        
        # Créer l'index
        cursor.execute("CREATE INDEX idx_facts_user_id ON facts(user_id)")
        print("🔗 Index créé sur user_id")
        
        # Restaurer les données existantes
        if existing_data:
            for user_id, fact in existing_data:
                cursor.execute("""
                    INSERT INTO facts (user_id, fact, timestamp)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (user_id, fact))
            print(f"📥 {len(existing_data)} entrées restaurées")
        
        conn.commit()
        conn.close()
        
        print("✅ Migration de la table 'facts' terminée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        return False


def verify_migration():
    """Vérifie que la migration s'est bien déroulée"""
    print("\n🔍 Vérification de la migration...")
    
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        
        # Vérifier la structure de la table facts
        cursor.execute("PRAGMA table_info(facts)")
        columns = cursor.fetchall()
        
        expected_columns = ['id', 'user_id', 'fact', 'timestamp']
        actual_columns = [col[1] for col in columns]
        
        missing = [col for col in expected_columns if col not in actual_columns]
        if missing:
            print(f"❌ Colonnes manquantes: {missing}")
            return False
        
        print("✅ Structure de la table 'facts' correcte")
        
        # Vérifier les index
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='facts'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        if 'idx_facts_user_id' in indexes:
            print("✅ Index sur user_id présent")
        else:
            print("⚠️  Index sur user_id manquant")
        
        # Test d'insertion
        test_user = "migration_test"
        test_fact = "Test de migration"
        
        cursor.execute("INSERT INTO facts (user_id, fact) VALUES (?, ?)", (test_user, test_fact))
        cursor.execute("SELECT * FROM facts WHERE user_id = ?", (test_user,))
        result = cursor.fetchone()
        
        if result:
            print("✅ Test d'insertion réussi")
            # Nettoyer le test
            cursor.execute("DELETE FROM facts WHERE user_id = ?", (test_user,))
            conn.commit()
        else:
            print("❌ Test d'insertion échoué")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False


def main():
    """Fonction principale de migration automatique"""
    print("=" * 60)
    print("🔧 MIGRATION AUTOMATIQUE DE LA BASE DE DONNÉES NEURO-BOT")
    print("=" * 60)
    
    # Vérifier l'existence de la base de données
    if not os.path.exists(config.DB_PATH):
        print(f"❌ Base de données non trouvée: {config.DB_PATH}")
        return
    
    # Créer une sauvegarde
    backup_path = backup_database()
    if not backup_path:
        print("❌ Impossible de créer une sauvegarde. Migration annulée.")
        return
    
    # Vérifier la structure actuelle
    missing_columns = check_facts_table_structure()
    if missing_columns is None:
        print("❌ Impossible de vérifier la structure. Migration annulée.")
        return
    
    if not missing_columns:
        print("✅ La table 'facts' a déjà la structure correcte")
        return
    
    print(f"⚠️  Colonnes manquantes dans 'facts': {missing_columns}")
    print("🚀 Procédure de migration automatique...")
    
    # Effectuer la migration
    if migrate_facts_table():
        if verify_migration():
            print("\n🎉 Migration terminée avec succès !")
            print(f"💾 Sauvegarde disponible: {backup_path}")
        else:
            print("\n❌ La vérification post-migration a échoué")
            print(f"🔄 Vous pouvez restaurer depuis: {backup_path}")
    else:
        print("\n❌ La migration a échoué")
        print(f"🔄 Vous pouvez restaurer depuis: {backup_path}")


if __name__ == "__main__":
    main()