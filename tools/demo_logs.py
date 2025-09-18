#!/usr/bin/env python3
"""
Démonstration du système de logs avancé de Kira-Bot
"""

import sys
import os
import time
import threading
from datetime import datetime

# Ajoute le répertoire du projet au path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def demo_basic_logging():
    """Démonstration du logging de base"""
    print("🎬 Démonstration du logging de base")
    print("-" * 50)
    
    from config import logger
    
    # Différents niveaux de logs
    logger.debug("🔍 Message de debug - détails techniques")
    logger.info("ℹ️ Bot démarré avec succès")
    logger.warning("⚠️ Mémoire faible détectée")
    logger.error("❌ Erreur de connexion à la base de données")
    logger.critical("🚨 Erreur critique - arrêt du système")
    
    print("✅ Logs de base générés")
    time.sleep(2)

def demo_advanced_features():
    """Démonstration des fonctionnalités avancées"""
    print("\n🎬 Démonstration des fonctionnalités avancées")
    print("-" * 50)
    
    try:
        from config import advanced_log_manager
        
        if not advanced_log_manager:
            print("⚠️ Système de logs avancé non disponible")
            return
        
        # Génère quelques logs avec contexte
        from config import logger
        
        logger.info("🤖 Initialisation du bot Discord")
        logger.info("🧠 Chargement du modèle LLM")
        logger.warning("⚠️ GPU température élevée: 75°C")
        logger.error("❌ Échec de connexion au serveur Discord")
        logger.info("🔄 Tentative de reconnexion...")
        logger.info("✅ Reconnexion réussie")
        
        # Récupère les statistiques
        stats = advanced_log_manager.get_stats(1)  # Dernière journée
        print(f"📊 Statistiques générées:")
        print(f"   - Total logs: {stats.get('total_logs', 0)}")
        print(f"   - Erreurs: {stats.get('error_count', 0)}")
        print(f"   - Warnings: {stats.get('warning_count', 0)}")
        
        # Récupère les logs récents
        recent_logs = advanced_log_manager.get_logs(limit=5)
        print(f"📋 {len(recent_logs)} logs récents récupérés")
        
        print("✅ Fonctionnalités avancées démontrées")
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")

def demo_concurrent_logging():
    """Démonstration du logging concurrent"""
    print("\n🎬 Démonstration du logging concurrent")
    print("-" * 50)
    
    from config import logger
    
    def worker_task(worker_id, task_count):
        """Tâche simulée avec logs"""
        for i in range(task_count):
            if i % 3 == 0:
                logger.info(f"🔧 Worker {worker_id} - Tâche {i} démarrée")
            elif i % 3 == 1:
                logger.warning(f"⚠️ Worker {worker_id} - Tâche {i} lente")
            else:
                logger.error(f"❌ Worker {worker_id} - Tâche {i} échouée")
            
            time.sleep(0.1)  # Simule du travail
    
    # Lance plusieurs workers
    threads = []
    for worker_id in range(3):
        thread = threading.Thread(
            target=worker_task, 
            args=(worker_id, 5)
        )
        threads.append(thread)
        thread.start()
    
    # Attend la fin
    for thread in threads:
        thread.join()
    
    print("✅ Logging concurrent démontré")

def demo_performance():
    """Démonstration des performances"""
    print("\n🎬 Test de performance")
    print("-" * 50)
    
    from config import logger
    
    # Test de performance
    start_time = time.time()
    log_count = 200
    
    print(f"🚀 Génération de {log_count} logs...")
    
    for i in range(log_count):
        level = ["info", "warning", "error"][i % 3]
        message = f"Message de test de performance #{i}"
        
        if level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        else:
            logger.error(message)
    
    end_time = time.time()
    duration = end_time - start_time
    rate = log_count / duration
    
    print(f"📊 Performance:")
    print(f"   - {log_count} logs en {duration:.3f} secondes")
    print(f"   - Débit: {rate:.1f} logs/seconde")
    
    if rate > 100:
        print("✅ Performance excellente")
    elif rate > 50:
        print("✅ Performance bonne")
    else:
        print("⚠️ Performance acceptable")

def demo_export():
    """Démonstration de l'export"""
    print("\n🎬 Démonstration de l'export")
    print("-" * 50)
    
    try:
        from config import advanced_log_manager
        
        if not advanced_log_manager:
            print("⚠️ Export non disponible sans système avancé")
            return
        
        # Crée un fichier d'export temporaire
        export_path = os.path.join(
            os.path.dirname(__file__), 
            f"demo_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        print(f"💾 Export vers: {export_path}")
        
        success = advanced_log_manager.export_logs(
            export_path, 
            "json", 
            limit=50
        )
        
        if success and os.path.exists(export_path):
            file_size = os.path.getsize(export_path)
            print(f"✅ Export réussi ({file_size} bytes)")
            
            # Nettoie le fichier de test
            os.remove(export_path)
            print("🗑️ Fichier de test nettoyé")
        else:
            print("❌ Échec de l'export")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")

def demo_gui_integration():
    """Démonstration de l'intégration GUI"""
    print("\n🎬 Démonstration de l'intégration GUI")
    print("-" * 50)
    
    try:
        # Test d'import des composants GUI
        from gui.tools.log_viewer_gui import (
            LogTableWidget, LogStatsWidget, 
            LogFilterWidget, LogViewerMainWindow
        )
        
        print("✅ Composants GUI importés avec succès")
        
        # Test de l'interface principale
        from gui.enhanced_main_gui import MainInterface
        print("✅ Interface principale disponible")
        
        print("🎨 Interfaces disponibles:")
        print("   - Interface complète: start_enhanced_gui.py")
        print("   - Visualiseur logs: launch_log_viewer.py")
        print("   - Scripts batch: launch_gui.bat, launch_log_viewer.bat")
        
    except ImportError as e:
        print(f"⚠️ Composants GUI non disponibles: {e}")
        print("   Installez PySide6: pip install PySide6")
    except Exception as e:
        print(f"❌ Erreur GUI: {e}")

def interactive_demo():
    """Démonstration interactive"""
    print("\n🎮 Mode interactif")
    print("-" * 50)
    print("Tapez des commandes pour générer des logs:")
    print("  'info <message>' - Log d'information")
    print("  'warn <message>' - Log d'avertissement") 
    print("  'error <message>' - Log d'erreur")
    print("  'stats' - Affiche les statistiques")
    print("  'export' - Exporte les logs")
    print("  'quit' - Quitte le mode interactif")
    print()
    
    from config import logger, advanced_log_manager
    
    while True:
        try:
            command = input("📝 Commande: ").strip()
            
            if command.lower() == 'quit':
                break
            elif command.lower() == 'stats':
                if advanced_log_manager:
                    stats = advanced_log_manager.get_stats(1)
                    print(f"📊 Stats: {stats.get('total_logs', 0)} logs, "
                          f"{stats.get('error_count', 0)} erreurs")
                else:
                    print("⚠️ Statistiques non disponibles")
            elif command.lower() == 'export':
                if advanced_log_manager:
                    export_path = f"interactive_export_{int(time.time())}.json"
                    success = advanced_log_manager.export_logs(export_path, "json", limit=20)
                    if success:
                        print(f"✅ Export réussi: {export_path}")
                    else:
                        print("❌ Échec de l'export")
                else:
                    print("⚠️ Export non disponible")
            elif command.startswith('info '):
                message = command[5:]
                logger.info(f"📝 {message}")
                print("✅ Log d'info généré")
            elif command.startswith('warn '):
                message = command[5:]
                logger.warning(f"⚠️ {message}")
                print("✅ Log d'avertissement généré")
            elif command.startswith('error '):
                message = command[6:]
                logger.error(f"❌ {message}")
                print("✅ Log d'erreur généré")
            else:
                print("❓ Commande inconnue")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    print("👋 Mode interactif terminé")

def main():
    """Fonction principale de démonstration"""
    print("🎬 DÉMONSTRATION DU SYSTÈME DE LOGS AVANCÉ")
    print("=" * 60)
    print("Cette démonstration présente toutes les fonctionnalités")
    print("du nouveau système de logs de Kira-Bot")
    print("=" * 60)
    
    try:
        # Initialise le système
        from config import config, logger, advanced_log_manager
        
        print(f"⚙️ Configuration chargée")
        print(f"📋 Logger initialisé: {logger.name}")
        
        if advanced_log_manager:
            print(f"✅ Système de logs avancé: ACTIVÉ")
        else:
            print(f"⚠️ Système de logs avancé: NON DISPONIBLE")
        
        print()
        
        # Exécute les démonstrations
        demo_basic_logging()
        demo_advanced_features()
        demo_concurrent_logging()
        demo_performance()
        demo_export()
        demo_gui_integration()
        
        # Mode interactif optionnel
        print("\n" + "=" * 60)
        response = input("🎮 Voulez-vous essayer le mode interactif ? (o/N): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            interactive_demo()
        
        print("\n🎉 Démonstration terminée avec succès!")
        print("\n📚 Pour plus d'informations:")
        print("   - Guide: GUIDE_LOGS.md")
        print("   - Documentation: LOGS_SYSTEM.md")
        print("   - Tests: python 'zen tests/test_advanced_logging.py'")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())