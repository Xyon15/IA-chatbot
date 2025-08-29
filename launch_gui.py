#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raccourci vers le lanceur GUI unifié dans le dossier gui/
"""

import sys
import os

def main():
    """Redirige vers le lanceur unifié dans gui/"""
    print("🔄 Redirection vers le lanceur GUI unifié...")
    
    # Ajouter le répertoire gui au path
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui')
    sys.path.insert(0, gui_path)
    
    try:
        from gui.launch_gui import main as gui_main
        return gui_main()
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        print("💡 Assurez-vous que tous les modules GUI sont présents dans le dossier gui/")
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return 1

if __name__ == "__main__":
    # Transmettre les arguments à l'interface unifiée
    sys.exit(main())