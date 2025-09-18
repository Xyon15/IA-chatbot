#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur rapide Kira-Bot secondaire en plein écran avec architecture modulaire
"""

import sys
import os

# Ajouter le répertoire du projet au path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def launch_kira_secondary_fullscreen():
    """Lance une interface Kira-Bot secondaire en plein écran"""
    print("🚀 Lancement de Kira-Bot (Interface Secondaire) en plein écran...")
    print("🧠 Interface alternative avec monitoring système optimisé")
    print("🔧 Raccourcis: F11=Plein écran, F5=Bot ON/OFF, F1=Aide")
    print("=" * 60)
    
    try:
        # Configuration plein écran pour l'interface secondaire
        os.environ['KIRA_SECONDARY_FULLSCREEN'] = '1'
        os.environ['KIRA_SECONDARY_GUI_MODE'] = 'enhanced'
        
        # Import de l'interface alternative
        from start_kira_alt import main as kira_alt_main
        
        # Lancement
        return kira_alt_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que les modules Kira sont présents")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False

if __name__ == "__main__":
    print("""
    ===============================================
            KIRA-BOT SECONDARY FULLSCREEN
          Interface Alternative Optimisée
    ===============================================
    """)
    
    try:
        success = launch_kira_secondary_fullscreen()
        if success:
            print("\n✅ Interface Kira secondaire fermée proprement")
            sys.exit(0)
        else:
            print("\n❌ Problème lors du lancement")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Interruption utilisateur")
        sys.exit(0)