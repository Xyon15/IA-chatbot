#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement pour le Visionneur de Logs Avancé Neuro-Bot
"""

import sys
import os

# Ajouter le répertoire du projet au path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def main():
    """Lance le visionneur de logs avancé"""
    try:
        from gui.tools.enhanced_log_viewer import main as log_viewer_main
        print("🚀 Lancement du Visionneur de Logs Avancé Neuro-Bot...")
        log_viewer_main()
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Assurez-vous que tous les modules requis sont installés.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()