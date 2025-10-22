#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lanceur rapide Neuro-Bot en plein écran avec architecture modulaire
"""

import sys
import os

# Ajouter le répertoire du projet au path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def launch_neuro_bot_fullscreen():
    """Lance l'interface Neuro-Bot en plein écran avec nouvelle architecture"""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                🧠 NEURO-BOT FULLSCREEN                  ║
    ║               Interface Neuro Optimisée                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("🧠 Interface Neuro avec monitoring système optimisé")
    print("🔧 Raccourcis: F11=Plein écran, F5=Bot ON/OFF, F1=Aide")
    
    try:
        # Configuration des variables d'environnement
        os.environ['NEURO_FULLSCREEN'] = '1'
        os.environ['NEURO_GUI_MODE'] = 'enhanced'
        
        # Tentative d'import et lancement du module Neuro-Bot
        try:
            # Essayer d'importer start_neuro si disponible
            import start_neuro
            print("🚀 Lancement de Neuro-Bot en plein écran...")
            success = start_neuro.main()
            if success:
                sys.exit(0)
            else:
                print("\n❌ Problème lors du lancement")
                return False
        except ImportError as e:
            print(f"❌ start_neuro non disponible: {e}")
            print("🔄 Tentative de lancement via GUI alternative...")
            
            # Fallback vers interface GUI standard
            try:
                from gui.launch_gui import main as gui_main
                # Appeler sans arguments car la fonction ne les accepte pas
                return gui_main()
            except ImportError:
                print("❌ Aucune interface disponible")
                return False
                
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        return False

def main():
    """Point d'entrée principal"""
    try:
        success = launch_neuro_bot_fullscreen()
        if not success:
            print("\n❌ Échec du lancement de Neuro-Bot")
            input("Appuyez sur Entrée pour fermer...")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)

if __name__ == "__main__":
    main()