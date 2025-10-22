#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur principal unifié pour toutes les interfaces GUI de Kira-Bot
Gère le lancement de l'interface moderne et de l'interface améliorée
"""

import sys
import os
import argparse
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
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
        print("❌ Dépendances manquantes :")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n💡 Pour installer les dépendances :")
        print("pip install PySide6 psutil pynvml")
        return False
    
    return True

def launch_legacy_gui():
    """Lance l'ancienne interface graphique (kira_gui) - Legacy"""
    if not check_dependencies():
        return False
    
    try:
        print("🚀 Lancement de KiraBot GUI Legacy...")

        # Créer l'application Qt d'abord pour éviter les conflits
        from PySide6.QtWidgets import QApplication
        
        # Vérifier si une application Qt existe déjà
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # S'assurer que nous avons une QApplication (pas QCoreApplication)
        if not isinstance(app, QApplication):
            app = QApplication(sys.argv)
            app_created = True
        else:
            app_created = False
        
        # Ajout du répertoire parent au path
        parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_path not in sys.path:
            sys.path.insert(0, parent_path)

        # Vérification du chemin d'import et importation du module
        try:
            from gui.kira_gui import MainWindow, STYLES
        except ModuleNotFoundError:
            # Tentative d'import absolu si l'import relatif échoue
            import importlib
            kira_gui = importlib.import_module("gui.kira_gui")
            MainWindow = getattr(kira_gui, "MainWindow")
            STYLES = getattr(kira_gui, "STYLES")
        
        # Application du style global
        app.setStyleSheet(STYLES)
        
        # Création et affichage de la fenêtre
        window = MainWindow()
        window.show()
        
        print("✅ Interface legacy lancée avec succès !")
        
        # Exécuter l'application seulement si elle a été créée ici
        if app_created:
            return app.exec()
        else:
            # Si l'app existait déjà, juste afficher la fenêtre
            return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'interface legacy : {e}")
        import traceback
        traceback.print_exc()
        return False

def launch_main_gui():
    """Lance l'interface graphique principale moderne (enhanced_main_gui)"""
    if not check_dependencies():
        return False
    
    try:
        print("🚀 Lancement de KiraBot GUI Moderne...")
        
        # Ajout du répertoire parent au path
        parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_path not in sys.path:
            sys.path.append(parent_path)
        
        from gui.enhanced_main_gui import main as enhanced_main
        return enhanced_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que PySide6 est installé: pip install PySide6")
        return 1
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'interface moderne: {e}")
        import traceback
        traceback.print_exc()
        return 1

def show_banner():
    """Affiche la bannière de bienvenue"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                    🤖 Kira GUI                           ║
    ║                   Lanceur Unifié                         ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                          ║
    ║  📋 Interface Principale (Nouvelle) :                   ║
    ║     🚀 Moderne    : Interface enhanced_main_gui          ║
    ║                     avec indicateurs circulaires        ║
    ║                                                          ║
    ║  📋 Interface Alternative :                              ║
    ║     🎨 Legacy     : Ancienne interface kira_gui        ║
    ║                                                          ║
    ║  ✨ Fonctionnalités :                                    ║
    ║     📊 Monitoring temps réel (CPU, RAM, GPU, VRAM)      ║
    ║     🎮 Contrôle complet du bot Discord                  ║
    ║     🧠 Gestionnaire de mémoire conversationnelle        ║
    ║     📈 Dashboard avec graphiques modernes               ║
    ║     📋 Visualiseur de logs avancé                       ║
    ║     🔔 Système de notifications                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Fonction principale avec sélection d'interface"""
    parser = argparse.ArgumentParser(
        description="Lanceur unifié pour les interfaces GUI de Kira-Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python launch_gui.py                    # Nouvelle interface moderne (défaut)
  python launch_gui.py --modern           # Nouvelle interface moderne (explicite)
  python launch_gui.py --legacy           # Ancienne interface legacy
  python launch_gui.py --select           # Sélection interactive
        """
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--modern', action='store_true', 
                      help='Lance la nouvelle interface moderne (défaut)')
    group.add_argument('--legacy', action='store_true', 
                      help='Lance l\'ancienne interface legacy')
    group.add_argument('--select', action='store_true', 
                      help='Sélection interactive de l\'interface')
    
    args = parser.parse_args()
    
    show_banner()
    
    # Génère les icônes si nécessaire
    assets_path = os.path.join(os.path.dirname(__file__), "assets", "icons")
    if not os.path.exists(assets_path):
        print("🎨 Génération des icônes...")
        try:
            from gui.icons_generator import create_icons_directory
            create_icons_directory()
            print("✅ Icônes générées avec succès.")
        except Exception as e:
            print(f"⚠️  Impossible de générer les icônes : {e}")
    
    # Déterminer quelle interface lancer
    if args.legacy:
        interface_type = 'legacy'
    elif args.select:
        print("\n🎯 Sélection de l'interface :")
        print("  1. Interface Moderne (enhanced_main_gui) - RECOMMANDÉE")
        print("  2. Interface Legacy (kira_gui)")
        
        while True:
            try:
                choice = input("\nChoisissez une interface (1-2) : ").strip()
                if choice == '1':
                    interface_type = 'modern'
                    break
                elif choice == '2':
                    interface_type = 'legacy'
                    break
                else:
                    print("❌ Choix invalide. Veuillez choisir 1 ou 2.")
            except KeyboardInterrupt:
                print("\n\n👋 Annulé par l'utilisateur.")
                return 0
    else:
        # Défaut : nouvelle interface moderne
        interface_type = 'modern'
    
    print(f"\n🔍 Vérification des dépendances...")
    if not check_dependencies():
        print("\n❌ Impossible de lancer l'interface.")
        print("💡 Veuillez installer les dépendances manquantes.")
        return 1
    
    print("✅ Toutes les dépendances sont présentes.")
    
    # Lancer l'interface appropriée
    if interface_type == 'legacy':
        print("\n🎉 Lancement de l'interface legacy...")
        success = launch_legacy_gui()
    else:  # modern
        print("\n🎉 Lancement de la nouvelle interface moderne...")
        success = launch_main_gui()
    
    if success:
        print("✅ Interface fermée proprement.")
        return 0
    else:
        print("❌ L'interface a rencontré un problème.")
        return 1

if __name__ == "__main__":
    sys.exit(main())