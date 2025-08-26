"""
Script de vérification rapide de l'état de santé de Neuro-Bot
"""
import os
import sys
import time
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from config import config, logger
from database import get_db_connection
from model import model_manager, generate_reply
import asyncio


def quick_database_check():
    """Vérification rapide de la base de données"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            if 'memory' not in tables or 'facts' not in tables:
                return False, "Tables manquantes"
            
            # Test d'intégrité rapide
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            
            if result != "ok":
                return False, f"Intégrité: {result}"
            
            # Compter les données
            cursor.execute("SELECT COUNT(*) FROM memory")
            memory_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM facts")
            facts_count = cursor.fetchone()[0]
            
            return True, f"Memory: {memory_count}, Facts: {facts_count}"
            
    except Exception as e:
        return False, str(e)


def quick_model_check():
    """Vérification rapide du modèle"""
    try:
        # Vérifier l'existence du fichier
        if not os.path.exists(config.MODEL_PATH):
            return False, "Fichier modèle manquant"
        
        # Vérifier l'initialisation
        if not model_manager.is_ready():
            return False, "Modèle non initialisé"
        
        # Test de génération rapide
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        start_time = time.time()
        response = loop.run_until_complete(
            generate_reply("health_check", "Test rapide", context_limit=1)
        )
        end_time = time.time()
        
        if response and not response.startswith("❌"):
            return True, f"Génération OK ({end_time - start_time:.1f}s)"
        else:
            return False, "Erreur de génération"
            
    except Exception as e:
        return False, str(e)


def main():
    """Vérification rapide de santé"""
    print("🏥 VÉRIFICATION RAPIDE DE SANTÉ - NEURO-BOT")
    print("=" * 50)
    
    # Base de données
    print("🗄️  Base de données...", end=" ")
    db_ok, db_msg = quick_database_check()
    print(f"{'✅' if db_ok else '❌'} {db_msg}")
    
    # Modèle
    print("🤖 Modèle LLM...", end=" ")
    model_ok, model_msg = quick_model_check()
    print(f"{'✅' if model_ok else '❌'} {model_msg}")
    
    # Résumé
    print("\n" + "=" * 50)
    if db_ok and model_ok:
        print("🎉 SYSTÈME EN BONNE SANTÉ")
    else:
        print("⚠️  PROBLÈMES DÉTECTÉS")
        if not db_ok:
            print(f"   - Base de données: {db_msg}")
        if not model_ok:
            print(f"   - Modèle: {model_msg}")
    
    print(f"📅 Vérification: {time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()