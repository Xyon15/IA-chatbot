#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur GUI principal unifié pour Kira-Bot
Fusion intelligente des lanceurs avec sélection automatique de l'interface optimale
"""

import sys
import os
import argparse
import subprocess
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

def launch_enhanced_gui_direct():
    """Lance l'interface GUI améliorée directement via subprocess (méthode enhanced)"""
    try:
        # Chemin vers le GUI amélioré
        gui_path = os.path.join("gui", "enhanced_main_gui.py")
        
        # Vérification de l'existence du fichier
        if not os.path.exists(gui_path):
            print(f"❌ Erreur: Le fichier GUI amélioré '{gui_path}' n'existe pas")
            print("🔍 Fichiers GUI disponibles:")
            gui_dir = "gui"
            if os.path.exists(gui_dir):
                for file in os.listdir(gui_dir):
                    if file.endswith('.py'):
                        print(f"  • {file}")
            return False
        
        print("🚀 Lancement de l'interface GUI améliorée...")
        print("✨ Fonctionnalités: Indicateurs circulaires, design moderne, raccourcis clavier")
        print()
        
        # Lancement direct du module
        result = subprocess.run([sys.executable, gui_path], check=True)
        
        print("✅ Interface fermée proprement")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de l'interface: Code {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def launch_unified_gui():
    """Lance l'interface via le lanceur unifié dans gui/"""
    print("🔄 Lancement de l'interface GUI optimisée...")
    
    # Ajouter le répertoire parent au path pour l'importation
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    try:
        # Import de la nouvelle architecture GUI modulaire
        from gui.enhanced_main_gui import main as gui_main
        return gui_main()
    except ImportError as e:
        print(f"❌ Erreur d'import GUI modulaire : {e}")
        # Fallback vers l'ancien système si nécessaire
        try:
            from gui.launch_gui import main as fallback_gui
            print("🔄 Utilisation du système GUI de fallback...")
            return fallback_gui()
        except ImportError:
            print("💡 Assurez-vous que tous les modules GUI sont présents dans le dossier gui/")
            return False
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return False

def show_main_banner():
    """Affiche la bannière principale fusionnée"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                    🤖 KIRABOT GUI                       ║
    ║                  Lanceur Principal                       ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                          ║
    ║  🚀 Méthodes de lancement disponibles :                 ║
    ║                                                          ║
    ║  1️⃣  Enhanced (Recommandé) : Subprocess optimisé        ║
    ║      • Interface moderne enhanced_main_gui              ║
    ║      • Indicateurs circulaires et design optimisé       ║
    ║      • Raccourcis clavier                               ║
    ║                                                          ║
    ║  2️⃣  Unified : Lanceur unifié avec sélection           ║
    ║      • Interface moderne ET legacy disponibles         ║
    ║      • Sélection interactive                            ║
    ║      • Vérification des dépendances                     ║
    ║                                                          ║
    ║  ✨ Auto : Sélection automatique optimale               ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def auto_select_best_method():
    """Sélectionne automatiquement la meilleure méthode de lancement"""
    print("🔍 Détection automatique de la meilleure méthode...")
    
    # Vérifier la disponibilité du GUI amélioré
    enhanced_path = os.path.join("gui", "enhanced_main_gui.py")
    unified_launcher_path = os.path.join("gui", "launch_gui.py")
    
    if os.path.exists(enhanced_path):
        print("✅ Interface améliorée détectée - Utilisation du mode Enhanced")
        return 'enhanced'
    elif os.path.exists(unified_launcher_path):
        print("✅ Lanceur unifié détecté - Utilisation du mode Unified")
        return 'unified'
    else:
        print("⚠️ Aucune interface détectée - Fallback vers mode Unified")
        return 'unified'

def main():
    """Fonction principale fusionnée avec sélection intelligente"""
    parser = argparse.ArgumentParser(
        description="Lanceur GUI principal unifié pour Kira-Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python launch_gui.py                    # Sélection automatique (recommandé)
  python launch_gui.py --enhanced         # Interface améliorée directe
  python launch_gui.py --unified          # Lanceur unifié avec sélection
  python launch_gui.py --select           # Sélection interactive
        """
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--enhanced', action='store_true', 
                      help='Lance directement l\'interface améliorée (subprocess)')
    group.add_argument('--unified', action='store_true', 
                      help='Lance le lanceur unifié avec sélection')
    group.add_argument('--select', action='store_true', 
                      help='Sélection interactive de la méthode')
    group.add_argument('--auto', action='store_true', default=True,
                      help='Sélection automatique optimale (défaut)')
    
    args = parser.parse_args()
    
    show_main_banner()
    
    # Déterminer la méthode de lancement
    if args.enhanced:
        method = 'enhanced'
    elif args.unified:
        method = 'unified'
    elif args.select:
        print("\n🎯 Sélection de la méthode de lancement :")
        print("  1. Enhanced - Interface améliorée directe (Recommandé)")
        print("  2. Unified - Lanceur unifié avec sélection")
        
        while True:
            try:
                choice = input("\nChoisissez une méthode (1-2) : ").strip()
                if choice == '1':
                    method = 'enhanced'
                    break
                elif choice == '2':
                    method = 'unified'
                    break
                else:
                    print("❌ Choix invalide. Veuillez choisir 1 ou 2.")
            except KeyboardInterrupt:
                print("\n\n👋 Annulé par l'utilisateur.")
                return 0
    else:
        # Mode auto (défaut)
        method = auto_select_best_method()
    
    # Vérification des dépendances avant lancement
    print(f"\n🔍 Vérification des dépendances...")
    if not check_dependencies():
        print("\n❌ Impossible de lancer l'interface.")
        print("💡 Veuillez installer les dépendances manquantes.")
        return 1
    
    print("✅ Toutes les dépendances sont présentes.")
    
    # Lancer avec la méthode appropriée
    success = False
    if method == 'enhanced':
        print("\n🎉 Lancement via méthode Enhanced...")
        success = launch_enhanced_gui_direct()
    elif method == 'unified':
        print("\n🎉 Lancement via méthode Unified...")
        success = launch_unified_gui()
    
    if success:
        print("\n✅ Interface fermée proprement.")
        return 0
    else:
        print("\n❌ L'interface a rencontré un problème.")
        # Fallback automatique
        if method == 'enhanced':
            print("🔄 Tentative de fallback vers la méthode Unified...")
            success = launch_unified_gui()
            if success:
                print("✅ Fallback réussi - Interface fermée proprement.")
                return 0
        
        return 1

if __name__ == "__main__":
    # Transmettre les arguments au système unifié
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 Interruption utilisateur - Arrêt propre")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)