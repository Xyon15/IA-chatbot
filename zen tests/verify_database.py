#!/usr/bin/env python3
"""
Script pour vérifier l'état de la base de données
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import get_db_connection
from config import config

def verify_database():
    """Vérifie l'état de la base de données"""
    print(f"🗄️  Chemin de la base de données configuré: {config.DB_PATH}")
    print(f"📁 Existence du fichier: {os.path.exists(config.DB_PATH)}")
    
    if not os.path.exists(config.DB_PATH):
        print("❌ Le fichier de base de données n'existe pas!")
        return False
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📋 Tables trouvées: {tables}")
            
            # Vérifier les données dans les tables
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"📊 Table '{table}': {count} enregistrements")
        
        print("✅ Base de données vérifiée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la base de données: {e}")
        return False

if __name__ == "__main__":
    verify_database()