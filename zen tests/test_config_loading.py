#!/usr/bin/env python3
"""
Test de chargement de la configuration du bot
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent pour les imports
sys.path.append(str(Path("..").absolute()))

def test_config_direct():
    """Test direct de la configuration du bot"""
    print("🔧 Test de Chargement de Configuration")
    print("=" * 45)
    
    try:
        # Nettoyer le cache Python
        modules_to_remove = [name for name in sys.modules if 'config' in name.lower() or 'dotenv' in name.lower()]
        for module in modules_to_remove:
            if module in sys.modules:
                del sys.modules[module]
                print(f"🧹 Module {module} supprimé du cache")
        
        # Nettoyer les variables d'environnement
        env_vars = ['DISCORD_TOKEN', 'AUTH_SECRET']
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]
                print(f"🧹 Variable {var} supprimée")
        
        # Changer vers le bon répertoire
        os.chdir("..")
        print(f"📂 Répertoire: {os.getcwd()}")
        
        # Importer la configuration APRÈS le nettoyage
        from config import Config
        
        # Créer une nouvelle instance
        config = Config()
        
        print(f"\n📋 Configuration chargée:")
        print(f"🔑 Token: {config.TOKEN[:20] if config.TOKEN else 'None'}...{config.TOKEN[-10:] if config.TOKEN else ''}")
        print(f"📏 Longueur token: {len(config.TOKEN) if config.TOKEN else 0}")
        print(f"🔐 Secret: {config.AUTH_SECRET[:10] if config.AUTH_SECRET else 'None'}...")
        print(f"📏 Longueur secret: {len(config.AUTH_SECRET) if config.AUTH_SECRET else 0}")
        
        # Validation
        if not config.TOKEN:
            print("❌ Token manquant!")
            return False
        elif len(config.TOKEN) < 50:
            print("❌ Token trop court!")
            return False
        else:
            print("✅ Token présent et valide")
        
        if not config.AUTH_SECRET:
            print("❌ Secret manquant!")
            return False
        else:
            print("✅ Secret présent")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def manual_env_check():
    """Vérification manuelle du fichier .env"""
    print("\n📄 Lecture Manuelle du Fichier .env")
    print("=" * 35)
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Fichier .env introuvable!")
        return
    
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        line = line.rstrip('\n\r')
        if line.startswith('DISCORD_TOKEN='):
            token = line.split('=', 1)[1]
            print(f"Ligne {i}: DISCORD_TOKEN={token[:20]}...{token[-10:]} (len: {len(token)})")
            
            # Vérifier les caractères invisibles
            if len(token) != len(token.strip()):
                print(f"   ⚠️ ATTENTION: Espaces détectés!")
                print(f"   Avant: '{token}'")
                print(f"   Après: '{token.strip()}'")
            
        elif line.startswith('AUTH_SECRET='):
            secret = line.split('=', 1)[1]
            print(f"Ligne {i}: AUTH_SECRET={secret[:10]}... (len: {len(secret)})")

if __name__ == "__main__":
    print("🔍 Diagnostic de Configuration Neuro-Bot")
    print("=" * 45)
    
    # Vérification manuelle d'abord
    manual_env_check()
    
    # Test de configuration
    success = test_config_direct()
    
    if success:
        print("\n🎉 Configuration chargée correctement!")
        print("🚀 Le bot devrait maintenant démarrer sans problème")
    else:
        print("\n❌ Problème de configuration détecté")
        print("🔧 Vérifiez le fichier .env")