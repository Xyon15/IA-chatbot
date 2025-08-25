#!/usr/bin/env python3
"""
Redémarrage propre du bot avec cache nettoyé
"""

import os
import sys
import subprocess
import time

def clear_environment():
    """Nettoie complètement l'environnement"""
    print("🧹 Nettoyage complet de l'environnement...")
    
    # Variables à nettoyer
    env_vars = ['DISCORD_TOKEN', 'AUTH_SECRET', 'N_GPU_LAYERS']
    
    for var in env_vars:
        if var in os.environ:
            del os.environ[var]
            print(f"   ✅ {var} supprimé du cache")
    
    # Nettoyer le cache Python
    if hasattr(sys, 'modules'):
        modules_to_remove = []
        for module_name in sys.modules:
            if any(name in module_name.lower() for name in ['config', 'dotenv']):
                modules_to_remove.append(module_name)
        
        for module_name in modules_to_remove:
            if module_name in sys.modules:
                del sys.modules[module_name]
                print(f"   ✅ Module {module_name} supprimé du cache")

def verify_env_file():
    """Vérifie le contenu actuel du fichier .env"""
    env_path = "../.env"
    
    print("🔍 Vérification du fichier .env:")
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for i, line in enumerate(content.split('\n'), 1):
        if line.startswith('DISCORD_TOKEN='):
            token = line.split('=', 1)[1]
            print(f"   Ligne {i}: Token {token[:20]}...{token[-10:]} (longueur: {len(token)})")
        elif line.startswith('AUTH_SECRET='):
            secret = line.split('=', 1)[1]
            print(f"   Ligne {i}: Secret {secret[:10]}... (longueur: {len(secret)})")

def restart_bot_subprocess():
    """Redémarre le bot dans un sous-processus complètement neuf"""
    print("\n🚀 Redémarrage du bot dans un environnement propre...")
    
    # Se placer dans le répertoire parent
    parent_dir = os.path.abspath("..")
    os.chdir(parent_dir)
    
    print(f"📂 Répertoire de travail: {os.getcwd()}")
    
    # Lancer le bot avec un environnement neuf
    try:
        # Utiliser PowerShell pour un redémarrage complet
        cmd = "python start_bot.py"
        
        print(f"🔄 Commande: {cmd}")
        print("⏳ Démarrage du bot (Ctrl+C pour arrêter)...")
        print("=" * 50)
        
        # Exécuter dans un nouveau processus
        result = subprocess.run(
            cmd,
            shell=True,
            text=True,
            capture_output=False,  # Afficher la sortie en temps réel
            timeout=300  # 5 minutes max
        )
        
        if result.returncode == 0:
            print("\n✅ Bot démarré avec succès!")
        else:
            print(f"\n❌ Échec du démarrage (code: {result.returncode})")
            
    except subprocess.TimeoutExpired:
        print("\n⏱️ Timeout - Le bot prend trop de temps à démarrer")
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du redémarrage: {e}")

if __name__ == "__main__":
    print("🔄 Redémarrage Propre de Neuro-Bot")
    print("=" * 40)
    
    # Nettoyer l'environnement
    clear_environment()
    
    # Vérifier le fichier .env
    verify_env_file()
    
    # Redémarrer proprement
    restart_bot_subprocess()