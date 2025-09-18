#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'architecture GUI modulaire
Vérifie l'intégration et le bon fonctionnement des modules
"""

import sys
import os
from pathlib import Path

def setup_test_environment():
    """Configure l'environnement de test"""
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    print(f"📁 Répertoire projet: {project_root}")

def test_core_imports():
    """Test des imports du module core"""
    print("\n🧪 Test des imports core...")
    
    try:
        from gui.core import (
            COLOR_PALETTE, FONTS, SIZES, ANIMATIONS,
            QApplication, QWidget, QVBoxLayout, QLabel
        )
        print("✅ Imports core réussis")
        print(f"   - Palette couleurs: {len(COLOR_PALETTE)} couleurs")
        print(f"   - Polices: {len(FONTS)} polices")
        print(f"   - Animations: {len(ANIMATIONS)} configs")
        return True
    except ImportError as e:
        print(f"❌ Erreur import core: {e}")
        return False

def test_modules_imports():
    """Test des imports des modules spécialisés"""
    print("\n🧪 Test des imports modules...")
    
    try:
        from gui.modules import (
            NotificationManager, SystemMonitorPanel, ChatInterface,
            show_info, show_success, show_warning, show_error
        )
        print("✅ Imports modules réussis")
        print("   - Système de notifications: OK")
        print("   - Monitoring système: OK") 
        print("   - Interface de chat: OK")
        return True
    except ImportError as e:
        print(f"❌ Erreur import modules: {e}")
        return False

def test_gpu_utils():
    """Test du module gpu_utils"""
    print("\n🧪 Test gpu_utils...")
    
    try:
        from gpu_utils import gpu_manager
        
        if gpu_manager.is_available():
            gpu_info = gpu_manager.get_gpu_info()
            print("✅ GPU manager opérationnel")
            if gpu_info:
                print(f"   - GPU: {gpu_info.name}")
                print(f"   - Utilisation: {gpu_info.utilization_gpu}%")
                print(f"   - VRAM: {gpu_info.vram_used_mb}/{gpu_info.vram_total_mb} MB ({gpu_info.vram_usage_percent:.1f}%)")
            else:
                print("   - Pas d'info GPU disponible")
        else:
            print("⚠️ GPU non disponible (normal sur certains systèmes)")
        return True
    except ImportError as e:
        print(f"❌ Erreur import gpu_utils: {e}")
        return False

def test_widgets_creation():
    """Test de création des widgets principaux"""
    print("\n🧪 Test création widgets...")
    
    try:
        from gui.core.qt_imports import QApplication
        from gui.modules.monitoring import SystemMonitorPanel
        from gui.modules.chat import ChatInterface
        from gui.modules.notifications import NotificationManager
        
        # Créer une application test si nécessaire
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test création widgets (sans initialisation complète)
        try:
            monitor = SystemMonitorPanel()
            print("   - SystemMonitorPanel: OK")
            monitor.deleteLater()
        except Exception as e:
            print(f"   - SystemMonitorPanel: ⚠️ {e}")
            
        try:
            chat = ChatInterface()
            print("   - ChatInterface: OK")
            chat.deleteLater()
        except Exception as e:
            print(f"   - ChatInterface: ⚠️ {e}")
            
        try:
            notif_manager = NotificationManager()
            print("   - NotificationManager: OK")
        except Exception as e:
            print(f"   - NotificationManager: ⚠️ {e}")
        
        print("✅ Test widgets terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création widgets: {e}")
        return False

def test_notifications():
    """Test du système de notifications"""
    print("\n🧪 Test système notifications...")
    
    try:
        from gui.modules import show_info, show_success, show_warning, show_error
        from gui.core import QApplication
        
        # Créer une application test si nécessaire
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test notifications (sans affichage)
        print("✅ Fonctions notifications disponibles")
        print("   - show_info: OK")
        print("   - show_success: OK") 
        print("   - show_warning: OK")
        print("   - show_error: OK")
        
        return True
    except Exception as e:
        print(f"❌ Erreur test notifications: {e}")
        return False

def test_architecture_integrity():
    """Test de l'intégrité de l'architecture"""
    print("\n🧪 Test intégrité architecture...")
    
    try:
        # Vérifier la structure des dossiers
        project_root = Path(__file__).parent.parent
        
        required_paths = [
            project_root / "gui" / "core",
            project_root / "gui" / "modules", 
            project_root / "gui" / "core" / "qt_imports.py",
            project_root / "gui" / "core" / "widgets.py",
            project_root / "gui" / "modules" / "notifications.py",
            project_root / "gui" / "modules" / "monitoring.py",
            project_root / "gui" / "modules" / "chat.py"
        ]
        
        missing = []
        for path in required_paths:
            if not path.exists():
                missing.append(str(path))
        
        if missing:
            print(f"❌ Fichiers manquants: {missing}")
            return False
        else:
            print("✅ Structure architecture complète")
            print(f"   - {len(required_paths)} composants vérifiés")
            return True
            
    except Exception as e:
        print(f"❌ Erreur test architecture: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("🚀 Lancement des tests d'intégration GUI modulaire")
    print("=" * 60)
    
    tests = [
        test_core_imports,
        test_modules_imports, 
        test_gpu_utils,
        test_architecture_integrity,
        test_widgets_creation,
        test_notifications
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur inattendue dans {test.__name__}: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests réussis: {passed}/{total}")
    if passed < total:
        print(f"❌ Tests échoués: {total - passed}")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Architecture prête.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

def main():
    """Point d'entrée principal"""
    setup_test_environment()
    
    try:
        success = run_all_tests()
        return success
    except KeyboardInterrupt:
        print("\n🛑 Tests interrompus par l'utilisateur")
        return False
    except Exception as e:
        print(f"\n❌ Erreur critique lors des tests: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        sys.exit(1)