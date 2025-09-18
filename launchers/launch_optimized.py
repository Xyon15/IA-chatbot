#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher principal optimisé avec architecture GUI modulaire
Support pour Kira-Bot avec interface moderne
"""

import sys
import os
import argparse
from pathlib import Path

def setup_environment():
    """Configure l'environnement Python et les paths"""
    # Ajouter le répertoire du projet au path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Variables d'environnement pour l'optimisation
    os.environ['PYTHONPATH'] = str(project_root)
    os.environ['GUI_ARCHITECTURE'] = 'modular'

def check_dependencies():
    """Vérifie les dépendances critiques"""
    required_packages = [
        'PySide6',
        'psutil', 
        'pynvml'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Dépendances manquantes: {', '.join(missing)}")
        print("📥 Installez avec: pip install " + " ".join(missing))
        return False
    return True

def launch_kira_gui():
    """Lance l'interface Kira-Bot avec architecture modulaire"""
    print("🚀 Lancement de Kira-Bot avec architecture GUI optimisée...")
    
    try:
        from gui.modules import show_success
        from gui.enhanced_main_gui import main as kira_main
        
        # Notification de lancement
        show_success("Kira-Bot", "Interface principale en cours de lancement...")
        
        # Configuration optimisée
        os.environ['KIRA_GUI_MODE'] = 'enhanced'
        os.environ['ENABLE_GPU_MONITORING'] = '1'
        
        return kira_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import Kira GUI: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def launch_kira_alt_gui():
    """Lance l'interface Kira-Bot alternative avec architecture modulaire"""
    print("🧠 Lancement de Kira-Bot (Interface Alternative) avec architecture GUI optimisée...")
    
    try:
        from gui.modules import show_info
        from start_kira_alt import main as kira_alt_main
        
        # Notification de lancement
        show_info("Kira-Bot Alt", "Interface alternative en cours de lancement...")
        
        # Configuration optimisée
        os.environ['KIRA_ALT_GUI_MODE'] = 'enhanced'
        os.environ['ENABLE_SYSTEM_MONITORING'] = '1'
        
        return kira_alt_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import Kira Alt GUI: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def launch_log_viewer():
    """Lance le visionneur de logs avec interface optimisée"""
    print("📊 Lancement du Visionneur de Logs optimisé...")
    
    try:
        from gui.modules import show_info
        from gui.tools.enhanced_log_viewer import main as log_main
        
        # Notification de lancement
        show_info("Log Viewer", "Visionneur de logs en cours de lancement...")
        
        return log_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import Log Viewer: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def run_integration_tests():
    """Lance les tests d'intégration de l'architecture GUI"""
    print("🧪 Lancement des tests d'intégration...")
    
    try:
        from test_integration import run_all_tests
        return run_all_tests()
    except ImportError:
        # Fallback - exécuter le script de test directement
        import subprocess
        import sys
        
        result = subprocess.run([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'test_integration.py')
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Erreurs:", result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        return False

def show_banner():
    """Affiche la bannière principale"""
    banner = """
    ===============================================
           🤖 IA-CHATBOT LAUNCHER v2.0
        Architecture GUI Modulaire Optimisée
    ===============================================
    
    Options disponibles:
    1️⃣  Kira-Bot GUI     - Interface principale
    2️⃣  Kira-Bot Alt     - Interface alternative
    3️⃣  Log Viewer       - Visionneur de logs
    4️⃣  Tests modules    - Tests intégration
    
    🔧 Mode ligne de commande avec --mode
    """
    print(banner)

def main():
    """Point d'entrée principal du launcher optimisé"""
    parser = argparse.ArgumentParser(description="Launcher IA-Chatbot avec architecture modulaire")
    parser.add_argument('--mode', choices=['kira', 'kira-alt', 'logs', 'test'], 
                       help='Mode de lancement direct')
    parser.add_argument('--fullscreen', action='store_true', 
                       help='Lancer en plein écran')
    parser.add_argument('--debug', action='store_true',
                       help='Mode debug avec informations détaillées')
    
    args = parser.parse_args()
    
    # Configuration debug
    if args.debug:
        os.environ['DEBUG_MODE'] = '1'
        print("🐛 Mode debug activé")
    
    # Configuration plein écran
    if args.fullscreen:
        os.environ['FULLSCREEN_MODE'] = '1'
        print("🖥️ Mode plein écran activé")
    
    # Configuration de l'environnement
    setup_environment()
    
    # Vérification des dépendances
    if not check_dependencies():
        return False
    
    # Lancement selon le mode
    if args.mode == 'kira':
        return launch_kira_gui()
    elif args.mode == 'kira-alt':
        return launch_kira_alt_gui()
    elif args.mode == 'logs':
        return launch_log_viewer()
    elif args.mode == 'test':
        return run_integration_tests()
    else:
        # Mode interactif
        show_banner()
        
        while True:
            try:
                choice = input("\n➤ Votre choix (1-4, q pour quitter): ").strip()
                
                if choice.lower() in ['q', 'quit', 'exit']:
                    print("👋 Au revoir !")
                    return True
                elif choice == '1':
                    return launch_kira_gui()
                elif choice == '2':
                    return launch_kira_alt_gui()
                elif choice == '3':
                    return launch_log_viewer()
                elif choice == '4':
                    return run_integration_tests()
                else:
                    print("❌ Choix invalide. Utilisez 1-4 ou q pour quitter.")
                    
            except KeyboardInterrupt:
                print("\n🛑 Interruption utilisateur")
                return True
            except Exception as e:
                print(f"❌ Erreur: {e}")
                continue

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        sys.exit(1)