#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement pour le Visionneur de Logs Avancé Kira-Bot
"""

import sys
import os

# Ajouter le répertoire du projet au path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def main():
    """Lance le visionneur de logs avancé avec architecture modulaire"""
    try:
        # Ajouter le répertoire parent au path
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, parent_dir)
        
        # Import des modules GUI optimisés
        from gui.modules import show_info
        from gui.core import QApplication
        
        # Créer l'application si nécessaire
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Notification de lancement
        show_info("Log Viewer", "Lancement du visionneur de logs optimisé...")
        
        # Import du visionneur de logs
        from gui.tools.enhanced_log_viewer import main as log_viewer_main
        print("🚀 Lancement du Visionneur de Logs Avancé avec architecture modulaire...")
        log_viewer_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import GUI modulaire: {e}")
        # Fallback vers l'ancienne version
        try:
            from gui.tools.enhanced_log_viewer import main as log_viewer_main
            print("🔄 Utilisation du visionneur de logs classique...")
            log_viewer_main()
        except ImportError:
            print("Assurez-vous que tous les modules requis sont installés.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()