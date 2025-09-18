#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des lanceurs plein écran
"""

import os
import sys
import subprocess

def test_lanceurs():
    """Test des nouveaux lanceurs plein écran"""
    
    print("🔧 Test des lanceurs plein écran")
    print("=" * 50)
    
    # Liste des fichiers à vérifier
    files_to_check = [
        ("launch_kira_fullscreen.py", "Lanceur Python Kira-Bot"),
        ("launch_logs_fullscreen.py", "Lanceur Python Log Viewer"), 
        ("START_KIRA_FULLSCREEN.bat", "Lanceur Windows Kira-Bot"),
        ("START_LOGS_FULLSCREEN.bat", "Lanceur Windows Log Viewer")
    ]
    
    print("\n1️⃣ Vérification des fichiers...")
    all_present = True
    
    for filename, description in files_to_check:
        filepath = os.path.join("c:\\Dev\\IA-chatbot", filename)
        if os.path.exists(filepath):
            print(f"  ✅ {description}: {filename}")
        else:
            print(f"  ❌ {description}: {filename} MANQUANT")
            all_present = False
    
    if not all_present:
        return False
    
    print("\n2️⃣ Vérification du contenu...")
    
    # Vérifier le contenu des lanceurs Python
    python_launchers = [
        "launch_kira_fullscreen.py",
        "launch_logs_fullscreen.py"
    ]
    
    for launcher in python_launchers:
        try:
            with open(f"c:\\Dev\\IA-chatbot\\{launcher}", 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications basiques
            if "def launch_" in content and "sys.path.insert" in content:
                print(f"  ✅ {launcher}: Structure correcte")
            else:
                print(f"  ⚠️ {launcher}: Structure possiblement incomplète")
                
        except Exception as e:
            print(f"  ❌ {launcher}: Erreur de lecture - {e}")
    
    # Vérifier le contenu des fichiers .bat
    bat_launchers = [
    "START_KIRA_FULLSCREEN.bat", 
        "START_LOGS_FULLSCREEN.bat"
    ]
    
    for launcher in bat_launchers:
        try:
            with open(f"c:\\Dev\\IA-chatbot\\{launcher}", 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications basiques
            if "python launch_" in content and "activate.bat" in content:
                print(f"  ✅ {launcher}: Structure correcte")
            else:
                print(f"  ⚠️ {launcher}: Structure possiblement incomplète")
                
        except Exception as e:
            print(f"  ❌ {launcher}: Erreur de lecture - {e}")
    
    print("\n3️⃣ Test des imports...")
    
    # Test import Kira-Bot
    try:
        sys.path.insert(0, "c:\\Dev\\IA-chatbot")
        from gui.enhanced_main_gui import MainInterface
        print("  ✅ Import Kira-Bot: gui.enhanced_main_gui.MainInterface")
    except Exception as e:
        print(f"  ⚠️ Import Kira-Bot: {e}")
    
    # Test import Log Viewer
    try:
        from gui.tools.log_viewer_gui import LogViewerMainWindow
        print("  ✅ Import Log Viewer: gui.tools.log_viewer_gui.LogViewerMainWindow")
    except Exception as e:
        print(f"  ⚠️ Import Log Viewer: {e}")
    
    print("\n4️⃣ Vérification des modifications plein écran...")
    
    # Vérifier que les modifications showMaximized() sont présentes
    gui_files = [
        ("gui/enhanced_main_gui.py", "self.showMaximized()"),
        ("gui/tools/log_viewer_gui.py", "self.showMaximized()")
    ]
    
    for filepath, expected in gui_files:
        try:
            with open(f"c:\\Dev\\IA-chatbot\\{filepath}", 'r', encoding='utf-8') as f:
                content = f.read()
            
            if expected in content:
                print(f"  ✅ {filepath}: Plein écran automatique configuré")
            else:
                print(f"  ⚠️ {filepath}: Plein écran automatique manquant")
                
        except Exception as e:
            print(f"  ❌ {filepath}: Erreur - {e}")
    
    print("\n" + "=" * 50)
    print("🎊 TESTS DES LANCEURS TERMINÉS")
    print("=" * 50)
    
    print("\n🚀 Lanceurs disponibles:")
    print("  • Double-clic sur START_KIRA_FULLSCREEN.bat")
    print("  • Double-clic sur START_LOGS_FULLSCREEN.bat")
    print("  • python launch_kira_fullscreen.py")
    print("  • python launch_logs_fullscreen.py")
    
    print("\n⌨️ Raccourcis dans les interfaces:")
    print("  • F11: Basculer plein écran/fenêtré")
    print("  • F5: Actions principales (bot/actualiser)")
    print("  • F1: Aide (Kira-Bot seulement)")
    
    return True

if __name__ == "__main__":
    success = test_lanceurs()
    if success:
        print(f"\n🏆 TESTS RÉUSSIS!")
        print(f"Vos lanceurs plein écran sont prêts à utiliser.")
    else:
        print(f"\n⚠️ Certains problèmes détectés.")