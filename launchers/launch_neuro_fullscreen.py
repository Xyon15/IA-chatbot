#!/usr/bin/env python3#!/usr/bin/env python3#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

Lanceur rapide Neuro-Bot en plein écran avec architecture modulaire

"""""""""



import sysLanceur rapide Neuro-Bot en plein écran avec architecture modulaireLancif __name__ == "__main__":

import os

"""    print("""

# Ajouter le répertoire du projet au path

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    ╔══════════════════════════════════════════════════════════╗

sys.path.insert(0, project_root)

import sys    ║                🧠 NEURO-BOT FULLSCREEN                  ║

def launch_neuro_bot_fullscreen():

    """Lance l'interface Neuro-Bot en plein écran avec nouvelle architecture"""import os    ║               Interface Neuro Optimisée                 ║

    print("🚀 Lancement de Neuro-Bot en plein écran...")

    print("🧠 Interface Neuro avec monitoring système optimisé")    ╚══════════════════════════════════════════════════════════╝

    print("🔧 Raccourcis: F11=Plein écran, F5=Bot ON/OFF, F1=Aide")

    print("=" * 60)# Ajouter le répertoire du projet au path    """)

    

    try:project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    

        # Configuration plein écran pour Neuro

        os.environ['NEURO_FULLSCREEN'] = '1'sys.path.insert(0, project_root)    try:

        os.environ['NEURO_GUI_MODE'] = 'enhanced'

                success = launch_neuro_bot_fullscreen()

        # Import de l'interface principale Neuro

        from start_neuro import main as neuro_maindef launch_neuro_bot_fullscreen():        if success:

        

        # Lancement    """Lance l'interface Neuro-Bot en plein écran avec nouvelle architecture"""            print("\n✅ Interface Neuro fermée proprement")

        return neuro_main()

            print("🚀 Lancement de Neuro-Bot en plein écran...")            sys.exit(0)

    except ImportError as e:

        print(f"❌ Erreur d'import: {e}")    print("🧠 Interface Neuro avec monitoring système optimisé")        else:

        print("💡 Vérifiez que les modules Neuro sont présents")

        return False    print("🔧 Raccourcis: F11=Plein écran, F5=Bot ON/OFF, F1=Aide")            print("\n❌ Problème lors du lancement")

    except Exception as e:

        print(f"❌ Erreur lors du lancement: {e}")    print("=" * 60)            sys.exit(1)

        return False

        except KeyboardInterrupt:

if __name__ == "__main__":

    print("""    try:        print("\n🛑 Interruption utilisateur")

    ===============================================

               NEURO-BOT FULLSCREEN        # Configuration plein écran pour Neuro        sys.exit(0)t en plein écran avec architecture modulaire

            Interface Neuro Optimisée

    ===============================================        os.environ['NEURO_FULLSCREEN'] = '1'"""

    """)

            os.environ['NEURO_GUI_MODE'] = 'enhanced'

    try:

        success = launch_neuro_bot_fullscreen()        import sys

        if success:

            print("\n✅ Interface Neuro fermée proprement")        # Import de l'interface principale Neuroimport os

            sys.exit(0)

        else:        from start_neuro import main as neuro_main

            print("\n❌ Problème lors du lancement")

            sys.exit(1)        # Ajouter le répertoire du projet au path

    except KeyboardInterrupt:

        print("\n🛑 Interruption utilisateur")        # Lancementproject_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        sys.exit(0)
        return neuro_main()sys.path.insert(0, project_root)

        

    except ImportError as e:def launch_neuro_bot_fullscreen():

        print(f"❌ Erreur d'import: {e}")    """Lance l'interface Neuro-Bot en plein écran avec nouvelle architecture"""

        print("💡 Vérifiez que les modules Neuro sont présents")    print("🚀 Lancement de Neuro-Bot en plein écran...")

        return False    print("🧠 Interface Neuro avec monitoring système optimisé")

    except Exception as e:    print("🔧 Raccourcis: F11=Plein écran, F5=Bot ON/OFF, F1=Aide")

        print(f"❌ Erreur lors du lancement: {e}")    print("=" * 60)

        return False    

    try:

if __name__ == "__main__":        # Import de l'interface Neuro avec nouvelle architecture

    print("""        from gui.modules import show_info

    ╔══════════════════════════════════════════════════════════╗        from gui.core import QApplication

    ║                🧠 NEURO-BOT FULLSCREEN                  ║        

    ║               Interface Neuro Optimisée                 ║        # Créer l'application si nécessaire

    ╚══════════════════════════════════════════════════════════╝        app = QApplication.instance()

    """)        if app is None:

                app = QApplication(sys.argv)

    try:        

        success = launch_neuro_bot_fullscreen()        # Notification de lancement

        if success:        show_info("Neuro-Bot", "Interface Neuro en cours de lancement...")

            print("\n✅ Interface Neuro fermée proprement")        

            sys.exit(0)        # Import de l'interface principale Neuro

        else:        from start_neuro import main as neuro_main

            print("\n❌ Problème lors du lancement")        

            sys.exit(1)        # Configuration plein écran pour Neuro

    except KeyboardInterrupt:        os.environ['NEURO_FULLSCREEN'] = '1'

        print("\n🛑 Interruption utilisateur")        os.environ['NEURO_GUI_MODE'] = 'enhanced'

        sys.exit(0)        
        # Lancement
        return neuro_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import GUI modulaire: {e}")
        print("💡 Tentative avec l'ancienne architecture...")
        
        # Fallback vers start_neuro classique
        try:
            from start_neuro import main as neuro_main
            return neuro_main()
        except ImportError:
            print("💡 Vérifiez que les modules Neuro sont présents")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                🤖 KIRA-BOT FULLSCREEN                   ║
    ║               Interface Principale                       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        success = launch_kira_bot_fullscreen()
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