#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation complète du système de logs Neuro-Bot
"""

import sys
import os
import sqlite3
from datetime import datetime, timedelta
import json

# Ajouter le répertoire du projet au path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def check_database_health():
    """Vérifie l'état de santé de la base de données de logs"""
    print("🔍 Vérification de la base de données...")
    
    db_path = os.path.join(project_root, "data", "logs.db")
    
    if not os.path.exists(db_path):
        print(f"  ❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Vérifier la table logs
            cursor.execute("SELECT COUNT(*) FROM logs")
            total_logs = cursor.fetchone()[0]
            print(f"  ✅ Total des logs: {total_logs:,}")
            
            # Vérifier les logs récents
            cursor.execute("""
                SELECT COUNT(*) FROM logs 
                WHERE timestamp > datetime('now', '-24 hours')
            """)
            recent_logs = cursor.fetchone()[0]
            print(f"  ✅ Logs des 24h: {recent_logs:,}")
            
            # Vérifier la répartition par niveau
            cursor.execute("""
                SELECT level, COUNT(*) FROM logs 
                WHERE timestamp > datetime('now', '-7 days')
                GROUP BY level ORDER BY COUNT(*) DESC
            """)
            
            level_stats = cursor.fetchall()
            print("  📊 Répartition par niveau (7 jours):")
            for level, count in level_stats:
                print(f"     {level}: {count:,}")
            
            # Vérifier les index
            cursor.execute("PRAGMA index_list(logs)")
            indexes = cursor.fetchall()
            print(f"  ✅ Index disponibles: {len(indexes)}")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Erreur base de données: {e}")
        return False

def check_advanced_logging():
    """Vérifie le système de logs avancé"""
    print("\n🔧 Vérification du système de logs avancé...")
    
    try:
        from tools.advanced_logging import LogManager, LogDatabase, get_log_manager
        print("  ✅ Module advanced_logging importé")
        
        # Test du gestionnaire global
        global_manager = get_log_manager()
        if global_manager:
            print("  ✅ Gestionnaire global actif")
        else:
            print("  ⚠️  Gestionnaire global non initialisé")
        
        # Test de création d'un gestionnaire local
        db_path = os.path.join(project_root, "data", "logs.db")
        local_manager = LogManager(db_path)
        print("  ✅ Gestionnaire local créé")
        
        # Test de récupération de statistiques
        stats = local_manager.log_db.get_log_stats(days=1)
        print(f"  ✅ Statistiques récupérées: {stats.get('total_logs', 0)} logs")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur système logs: {e}")
        return False

def check_log_viewer():
    """Vérifie le visionneur de logs"""
    print("\n🎨 Vérification du visionneur de logs...")
    
    try:
        # Test d'import sans affichage
        from gui.tools.enhanced_log_viewer import EnhancedLogViewer, NeuroTheme, FilterPanel
        print("  ✅ Modules visionneur importés")
        
        # Test d'import des dépendances PySide6
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        print("  ✅ PySide6 disponible")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur visionneur: {e}")
        return False

def check_integration():
    """Vérifie l'intégration avec le GUI principal"""
    print("\n🖥️  Vérification de l'intégration GUI...")
    
    try:
        # Test d'import du GUI principal
        from gui.enhanced_main_gui import MainInterface
        print("  ✅ GUI principal importé")
        
        # Vérifier que la méthode open_log_viewer existe
        gui_methods = dir(MainInterface)
        if 'open_log_viewer' in gui_methods:
            print("  ✅ Méthode open_log_viewer présente")
        else:
            print("  ❌ Méthode open_log_viewer manquante")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur intégration: {e}")
        return False

def check_scripts():
    """Vérifie les scripts de lancement"""
    print("\n📱 Vérification des scripts...")
    
    scripts_to_check = [
        "launch_log_viewer.py",
        "demo_log_viewer.py", 
        "test_log_viewer_launch.py"
    ]
    
    all_ok = True
    for script in scripts_to_check:
        script_path = os.path.join(project_root, script)
        if os.path.exists(script_path):
            print(f"  ✅ {script}")
        else:
            print(f"  ❌ {script} manquant")
            all_ok = False
    
    return all_ok

def performance_benchmark():
    """Test de performance simple"""
    print("\n⚡ Test de performance...")
    
    try:
        from tools.advanced_logging import LogDatabase
        import time
        
        db_path = os.path.join(project_root, "data", "logs.db")
        log_db = LogDatabase(db_path)
        
        # Test de récupération de logs
        start_time = time.time()
        logs = log_db.get_logs(limit=100)
        end_time = time.time()
        
        print(f"  ✅ Récupération de 100 logs: {(end_time - start_time)*1000:.1f}ms")
        
        # Test de statistiques
        start_time = time.time()
        stats = log_db.get_log_stats(days=7)
        end_time = time.time()
        
        print(f"  ✅ Calcul statistiques 7j: {(end_time - start_time)*1000:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur performance: {e}")
        return False

def generate_report():
    """Génère un rapport de validation"""
    print("\n📋 Génération du rapport...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "system": "Neuro-Bot Log Viewer System",
        "version": "1.0.0",
        "validation_results": {}
    }
    
    # Exécuter tous les tests
    tests = [
        ("database_health", check_database_health),
        ("advanced_logging", check_advanced_logging),
        ("log_viewer", check_log_viewer),
        ("integration", check_integration),
        ("scripts", check_scripts),
        ("performance", performance_benchmark)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        try:
            result = test_func()
            report["validation_results"][test_name] = {
                "status": "PASS" if result else "FAIL",
                "timestamp": datetime.now().isoformat()
            }
            if not result:
                all_passed = False
        except Exception as e:
            report["validation_results"][test_name] = {
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            all_passed = False
    
    report["overall_status"] = "PASS" if all_passed else "FAIL"
    
    # Sauvegarder le rapport
    report_path = os.path.join(project_root, "zen rapports", "LOG_SYSTEM_VALIDATION.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Rapport sauvegardé: {report_path}")
    
    return all_passed, report

def main():
    """Fonction principale de validation"""
    print("🚀 Validation Complète du Système de Logs Neuro-Bot")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Répertoire: {project_root}")
    print()
    
    # Exécuter la validation et générer le rapport
    all_passed, report = generate_report()
    
    # Afficher le résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DE VALIDATION")
    print("=" * 70)
    
    for test_name, result in report["validation_results"].items():
        status = result["status"]
        if status == "PASS":
            icon = "✅"
            color = ""
        elif status == "FAIL":
            icon = "❌"
            color = ""
        else:
            icon = "⚠️"
            color = ""
        
        print(f"  {icon} {test_name.replace('_', ' ').title():<20} {status}")
    
    print("-" * 70)
    
    if all_passed:
        print("🎉 VALIDATION RÉUSSIE - Système prêt pour utilisation !")
        print("\n🚀 Méthodes de lancement disponibles:")
        print("   1. python launch_log_viewer.py")
        print("   2. python demo_log_viewer.py")
        print("   3. Via GUI principal -> bouton '📋 Logs Avancés'")
        print("   4. python gui/tools/enhanced_log_viewer.py")
    else:
        print("⚠️  VALIDATION ÉCHOUÉE - Certains composants nécessitent attention")
        print("   Consultez les détails ci-dessus et le rapport JSON généré")
    
    print(f"\n📄 Rapport détaillé: zen rapports/LOG_SYSTEM_VALIDATION.json")
    print(f"✨ Validation terminée à {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()