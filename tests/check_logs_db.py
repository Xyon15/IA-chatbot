#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier la structure et contenu de la base de données logs
"""

import sqlite3
import os
from datetime import datetime

def check_logs_database():
    """Vérifie la structure et le contenu de logs.db"""
    db_path = "c:/Dev/IA-chatbot/data/logs.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} n'existe pas")
        return
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Vérifie les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Tables trouvées: {[table[0] for table in tables]}")
            
            # Vérifie la structure de la table logs si elle existe
            if ('logs',) in tables:
                cursor.execute("PRAGMA table_info(logs);")
                columns = cursor.fetchall()
                print("\n📝 Structure de la table 'logs':")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
                
                # Compte les enregistrements
                cursor.execute("SELECT COUNT(*) FROM logs;")
                count = cursor.fetchone()[0]
                print(f"\n📊 Nombre total de logs: {count}")
                
                if count > 0:
                    # Statistiques par niveau
                    cursor.execute("SELECT level, COUNT(*) FROM logs GROUP BY level ORDER BY COUNT(*) DESC;")
                    level_stats = cursor.fetchall()
                    print("\n📈 Répartition par niveau:")
                    for level, cnt in level_stats:
                        print(f"  - {level}: {cnt}")
                    
                    # Derniers logs
                    cursor.execute("SELECT timestamp, level, logger_name, message FROM logs ORDER BY timestamp DESC LIMIT 5;")
                    recent_logs = cursor.fetchall()
                    print("\n🕒 5 derniers logs:")
                    for log in recent_logs:
                        print(f"  [{log[0]}] {log[1]} - {log[2]}: {log[3][:50]}{'...' if len(log[3]) > 50 else ''}")
            else:
                print("\n⚠️ Table 'logs' n'existe pas")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    print("🔍 Vérification de la base de données des logs...\n")
    check_logs_database()