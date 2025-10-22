#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'architecture GUI modulaire
Vérifie l'intégrité de tous les composants du système
"""

import sys
import os
from pathlib import Path

def test_core_imports():
    """Test des imports core"""
    try:
        from gui.core.qt_imports import (
            QApplication, QWidget, QMainWindow, QVBoxLayout, 
            COLOR_PALETTE, FONTS
        )
        print("[OK] Imports core reussis")
        return True
    except Exception as e:
        print(f"[ERREUR] Erreur import core: {e}")
        return False

def test_modules_imports():
    """Test des imports modules"""
    try:
        from gui.modules import (
            show_success, show_error, show_warning, show_info,
            NotificationManager, SystemMonitorPanel
        )
        print("[OK] Imports modules reussis")
        return True
    except Exception as e:
        print(f"[ERREUR] Erreur import modules: {e}")
        return False

def test_gpu_utils():
    """Test des utilitaires GPU"""
    try:
        from tools import gpu_optimizer
        if hasattr(gpu_optimizer, 'gpu_manager'):
            print("[OK] GPU manager operationnel")
            return True
        else:
            print("[AVERTISSEMENT] GPU manager non disponible")
            return True  # Non critique
    except Exception as e:
        print(f"[ERREUR] Erreur import gpu_utils: {e}")
        return False

def test_widgets_creation():
    """Test création widgets sans affichage"""
    try:
        from gui.core.qt_imports import QApplication, QWidget
        from gui.modules.monitoring import SystemMonitorPanel
        
        # Test création widget (sans affichage)
        widget = QWidget()
        monitor = SystemMonitorPanel()
        
        # Vérification attributs essentiels
        assert hasattr(monitor, 'cpu_indicator')
        assert hasattr(monitor, 'ram_indicator')
        
        print("[OK] Test widgets termine")
        return True
    except Exception as e:
        print(f"[ERREUR] Erreur creation widgets: {e}")
        return False

def test_notifications():
    """Test système notifications"""
    try:
        from gui.modules.notifications import (
            show_success, show_error, show_warning, show_info,
            NotificationManager, NotificationType
        )
        
        # Vérifier que les fonctions existent
        assert callable(show_success)
        assert callable(show_error)
        assert callable(show_warning)
        assert callable(show_info)
        
        print("[OK] Fonctions notifications disponibles")
        return True
    except Exception as e:
        print(f"[ERREUR] Erreur test notifications: {e}")
        return False

def test_architecture_integrity():
    """Test intégrité architecture"""
    try:
        base_path = Path(__file__).parent.parent
        
        critical_files = [
            "gui/core/qt_imports.py",
            "gui/modules/__init__.py",
            "gui/modules/notifications.py",
            "gui/modules/monitoring.py",
            "gui/kira_gui.py",
            "launchers/launch_optimized.py"
        ]
        
        missing = []
        for file_path in critical_files:
            if not (base_path / file_path).exists():
                missing.append(file_path)
        
        if missing:
            print(f"[ERREUR] Fichiers manquants: {missing}")
            return False
        else:
            print("[OK] Structure architecture complete")
            return True
    except Exception as e:
        print(f"[ERREUR] Erreur test architecture: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print(">> Lancement des tests d'integration GUI modulaire")
    print("=" * 60)
    
    tests = [
        test_core_imports,
        test_modules_imports, 
        test_gpu_utils,
        test_architecture_integrity,
        test_widgets_creation,
        test_notifications
    ]
    
    results = {}
    
    for test in tests:
        test_name = test.__name__
        try:
            result = test()
            results[test_name] = result
        except Exception as e:
            print(f"[ERREUR] Erreur inattendue dans {test.__name__}: {e}")
            results[test_name] = False
    
    # Résumé
    passed = sum(results.values())
    total = len(results)
    
    print("\n" + "=" * 40)
    print(f"[OK] Tests reussis: {passed}/{total}")
    if passed != total:
        print(f"[ERREUR] Tests echoues: {total - passed}")
    
    success = passed == total
    return success, results

def main():
    """Point d'entrée principal"""
    if __name__ == "__main__":
        # Configuration du path
        script_dir = Path(__file__).parent.parent
        if str(script_dir) not in sys.path:
            sys.path.insert(0, str(script_dir))
        
        try:
            success, results = run_all_tests()
            
            if success:
                print("\n[OK] Tous les tests ont reussi!")
                print("Le systeme est pret pour utilisation.")
            else:
                print("\n[ERREUR] Certains tests ont echoue.")
                print("Verifiez les erreurs ci-dessus.")
                
        except Exception as e:
            print(f"\n[ERREUR] Erreur critique lors des tests: {e}")
            return False
            
        return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERREUR] Erreur fatale: {e}")
        sys.exit(1)