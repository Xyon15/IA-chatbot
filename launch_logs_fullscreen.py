#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur rapide Log Viewer en plein écran
"""

import sys
import os

# Ajouter le répertoire du projet au path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def launch_log_viewer_fullscreen():
    """Lance le visualiseur de logs en plein écran"""
    print("🚀 Lancement du Log Viewer en plein écran...")
    print("📊 Interface de monitoring des logs avancée")
    print("🔧 Raccourcis: F11=Plein écran, F5=Actualiser")
    print("=" * 60)
    
    try:
        # Import du log viewer
        from gui.tools.log_viewer_gui import main as viewer_main
        
        # Lancement
        return viewer_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que les modules de logging sont présents")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║              📊 LOG VIEWER FULLSCREEN                   ║
    ║             Visualiseur de Logs Unifié                  ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        success = launch_log_viewer_fullscreen()
        if success:
            print("\n✅ Log Viewer fermé proprement")
            sys.exit(0)
        else:
            print("\n❌ Problème lors du lancement")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Interruption utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)