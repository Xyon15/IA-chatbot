#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sélecteur d'interface graphique pour Neuro-Bot
Permet de choisir entre les différentes interfaces disponibles
"""

import sys
import os
import subprocess
from pathlib import Path

def print_banner():
    """Affiche la bannière de sélection"""
    print("=" * 60)
    print("🤖 NEURO-BOT - SÉLECTEUR D'INTERFACE")
    print("=" * 60)
    print()

def print_interfaces():
    """Affiche les interfaces disponibles"""
    interfaces = [
        {
            "num": "1",
            "name": "Interface Principale Améliorée",
            "file": "launch_enhanced_gui.py",
            "description": "🚀 Moderne avec indicateurs circulaires, logs optimisés",
            "features": ["Indicateurs circulaires temps réel", "Design moderne sombre", "Raccourcis clavier", "Logs avec limite intelligente"]
        },
        {
            "num": "2", 
            "name": "Interface Complète (Neuro GUI)",
            "file": "gui/neuro_gui.py",
            "description": "🔧 Interface complète avec toutes les fonctionnalités",
            "features": ["Gestion mémoire avancée", "Graphiques détaillés", "Configuration étendue", "Historique complet"]
        },
        {
            "num": "3",
            "name": "Interface Simple (Bot GUI)", 
            "file": "gui/bot_gui.py",
            "description": "💡 Interface basique et légère",
            "features": ["Contrôles de base", "Logs simples", "Faible utilisation ressources", "Démarrage rapide"]
        }
    ]
    
    for interface in interfaces:
        print(f"[{interface['num']}] {interface['name']}")
        print(f"    {interface['description']}")
        for feature in interface['features']:
            print(f"    • {feature}")
        print(f"    📁 Fichier: {interface['file']}")
        print()
    
    return interfaces

def launch_interface(file_path):
    """Lance l'interface sélectionnée"""
    try:
        # Vérification de l'existence du fichier
        if not os.path.exists(file_path):
            print(f"❌ Erreur: Le fichier '{file_path}' n'existe pas")
            return False
        
        print(f"🚀 Lancement de {file_path}...")
        
        # Lancement dans un nouveau processus
        if file_path.startswith("gui/"):
            # Pour les fichiers dans le dossier gui
            subprocess.Popen([sys.executable, file_path], 
                           cwd=os.path.dirname(os.path.abspath(__file__)))
        else:
            # Pour les fichiers à la racine
            subprocess.Popen([sys.executable, file_path])
        
        print("✅ Interface lancée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False

def check_dependencies():
    """Vérifie les dépendances nécessaires"""
    print("🔍 Vérification des dépendances...")
    
    dependencies = {
        "PySide6": "Interface graphique",
        "psutil": "Monitoring système", 
        "pynvml": "Monitoring GPU NVIDIA"
    }
    
    missing = []
    for dep, desc in dependencies.items():
        try:
            __import__(dep.lower() if dep == "PySide6" else dep)
            print(f"  ✅ {dep} - {desc}")
        except ImportError:
            print(f"  ❌ {dep} - {desc} (MANQUANT)")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Dépendances manquantes: {', '.join(missing)}")
        print("📦 Installation requise:")
        for dep in missing:
            if dep == "PySide6":
                print(f"   pip install PySide6")
            else:
                print(f"   pip install {dep}")
        print()
        return False
    
    print("✅ Toutes les dépendances sont disponibles!")
    print()
    return True

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérification des dépendances
    if not check_dependencies():
        choice = input("Continuer malgré les dépendances manquantes ? (o/N): ").lower()
        if choice not in ['o', 'oui', 'y', 'yes']:
            print("❌ Installation annulée")
            return 1
        print()
    
    # Affichage des interfaces
    interfaces = print_interfaces()
    
    print("📝 RECOMMANDATIONS:")
    print("  • Première utilisation: Interface Simple (3)")
    print("  • Utilisation quotidienne: Interface Améliorée (1)")  
    print("  • Configuration avancée: Interface Complète (2)")
    print()
    
    # Boucle de sélection
    while True:
        try:
            choice = input("Choisissez une interface (1-3) ou 'q' pour quitter: ").strip()
            
            if choice.lower() in ['q', 'quit', 'quitter']:
                print("👋 Au revoir!")
                return 0
            
            if choice in ['1', '2', '3']:
                selected_interface = interfaces[int(choice) - 1]
                print(f"\n🎯 Interface sélectionnée: {selected_interface['name']}")
                
                # Confirmation
                confirm = input("Confirmer le lancement ? (O/n): ").lower()
                if confirm in ['', 'o', 'oui', 'y', 'yes']:
                    if launch_interface(selected_interface['file']):
                        return 0
                    else:
                        print("\n❌ Échec du lancement")
                        continue
                else:
                    print("❌ Lancement annulé")
                    continue
            else:
                print("❌ Choix invalide. Veuillez entrer 1, 2, 3 ou 'q'")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interruption utilisateur. Au revoir!")
            return 0
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    sys.exit(main())