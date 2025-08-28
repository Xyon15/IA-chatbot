#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur principal GUI pour NeuroBot
Redirige vers l'interface moderne dans le dossier gui/
"""

import sys
import os

def main():
    """Lance l'interface graphique moderne"""
    print("Lancement de NeuroBot GUI...")
    
    # Ajouter le répertoire gui au path
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui')
    sys.path.insert(0, gui_path)
    
    try:
        from gui.launch_neuro_gui import launch_gui
        success = launch_gui()
        
        if not success:
            print("Echec du lancement de l'interface")
            return 1
            
    except ImportError as e:
        print(f"Erreur d'import : {e}")
        print("Assurez-vous que tous les modules GUI sont présents dans le dossier gui/")
        return 1
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())