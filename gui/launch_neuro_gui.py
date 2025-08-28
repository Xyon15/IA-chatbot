#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur principal pour NeuroBot GUI
Lance l'interface moderne avec toutes les fonctionnalités
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    required_packages = [
        'PySide6',
        'psutil',
        'pynvml'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Dépendances manquantes :")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Pour installer les dépendances :")
        print("pip install PySide6 psutil pynvml")
        return False
    
    return True

def launch_gui():
    """Lance l'interface graphique moderne"""
    if not check_dependencies():
        return False
    
    try:
        print("🚀 Lancement de NeuroBot GUI Moderne...")
        
        # Créer l'application Qt d'abord pour éviter les conflits
        from PySide6.QtWidgets import QApplication
        
        # Vérifier si une application Qt existe déjà
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app_created = True
        else:
            app_created = False
        
        # Ajout du répertoire parent au path
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Import et configuration après création de l'app
        from gui.neuro_gui import MainWindow, STYLES
        
        # Application du style global
        app.setStyleSheet(STYLES)
        
        # Création et affichage de la fenêtre
        window = MainWindow()
        window.show()
        
        print("✅ Interface lancée avec succès !")
        
        # Exécuter l'application seulement si elle a été créée ici
        if app_created:
            return app.exec()
        else:
            # Si l'app existait déjà, juste afficher la fenêtre
            return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        import traceback
        traceback.print_exc()
        return False

def show_banner():
    """Affiche la bannière de bienvenue"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                    🤖 NEUROBOT GUI                       ║
    ║                  Interface Moderne                       ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                          ║
    ║  ✨ Fonctionnalités :                                    ║
    ║     📊 Monitoring temps réel (CPU, RAM, GPU, VRAM)      ║
    ║     🎮 Contrôle complet du bot Discord                  ║
    ║     🧠 Gestionnaire de mémoire conversationnelle        ║
    ║     📈 Dashboard avec graphiques animés                 ║
    ║     📋 Visualiseur de logs avancé                       ║
    ║     🔔 Système de notifications                         ║
    ║     🎨 Interface moderne avec palette personnalisée     ║
    ║                                                          ║
    ║  🎯 Couleurs : Vert emeraude, Orange accent, Rose pâle  ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Fonction principale"""
    show_banner()
    
    print("🔍 Vérification des dépendances...")
    if not check_dependencies():
        print("\n❌ Impossible de lancer l'interface.")
        print("💡 Veuillez installer les dépendances manquantes.")
        return False
    
    print("✅ Toutes les dépendances sont présentes.")
    
    # Génère les icônes si nécessaire
    if not os.path.exists("assets/icons"):
        print("🎨 Génération des icônes...")
        try:
            from icons_generator import create_icons_directory
            create_icons_directory()
        except Exception as e:
            print(f"⚠️  Impossible de générer les icônes : {e}")
    
    print("🎉 Lancement de l'interface...")
    success = launch_gui()
    
    if success:
        print("✅ Interface fermée proprement.")
    else:
        print("❌ L'interface a rencontré un problème.")
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)