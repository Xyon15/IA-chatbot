#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur rapide Neuro-Bot en plein écran
"""

import sys
import os

# Ajouter le répertoire du projet au path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def launch_neuro_bot_fullscreen():
    """Lance l'interface principale Neuro-Bot en plein écran"""
    print("🚀 Lancement de Neuro-Bot en plein écran...")
    print("📍 Interface principale avec monitoring avancé")
    print("🔧 Raccourcis: F11=Plein écran, F5=Bot ON/OFF, F1=Aide")
    print("=" * 60)
    
    try:
        # Import de l'interface principale
        from gui.enhanced_main_gui import main as neuro_main
        
        # Lancement
        return neuro_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que les modules GUI sont présents")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                🤖 NEURO-BOT FULLSCREEN                   ║
    ║               Interface Principale                       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        success = launch_neuro_bot_fullscreen()
        if success:
            print("\n✅ Interface fermée proprement")
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