#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur pour l'interface GUI principale améliorée de Neuro-Bot
Interface moderne avec indicateurs circulaires et design optimisé
"""

import sys
import os
import subprocess

def main():
    """Lance l'interface GUI améliorée"""
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
            return 1
        
        print("🚀 Lancement de l'interface GUI améliorée...")
        print("✨ Fonctionnalités: Indicateurs circulaires, design moderne, raccourcis clavier")
        print()
        
        # Lancement direct du module
        subprocess.run([sys.executable, gui_path], check=True)
        
        print("✅ Interface fermée proprement")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de l'interface: Code {e.returncode}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n👋 Interruption utilisateur")
        return 0
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())