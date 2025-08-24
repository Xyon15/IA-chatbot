#!/usr/bin/env python3
"""
Script de démarrage amélioré pour le bot Neuro
Inclut la validation de la configuration et l'initialisation complète
"""

import sys
import os
import asyncio
from pathlib import Path

def check_requirements():
    """Vérifie que tous les prérequis sont installés"""
    print("🔍 Vérification des prérequis...")
    
    # Mapping des noms de packages vers leurs noms d'import
    required_packages = {
        'discord.py': 'discord',
        'llama-cpp-python': 'llama_cpp', 
        'python-dotenv': 'dotenv',
        'pyside6': 'PySide6',
        'pynvml': 'pynvml',
        'aiohttp': 'aiohttp',
        'selectolax': 'selectolax',
        'transformers': 'transformers',
        'pyotp': 'pyotp'
    }
    
    missing = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print(f"❌ Packages manquants: {', '.join(missing)}")
        print("Installez-les avec: pip install " + " ".join(missing))
        return False
    
    print("✅ Tous les packages requis sont installés")
    return True

def check_files():
    """Vérifie que tous les fichiers nécessaires existent"""
    print("📁 Vérification des fichiers...")
    
    required_files = [
        '.env',
        'JSON/config.json',
        'JSON/context.json', 
        'JSON/character_limits.json',
        'JSON/web.json',
        'JSON/autoreply.json'
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"❌ Fichiers manquants: {', '.join(missing)}")
        return False
    
    print("✅ Tous les fichiers requis sont présents")
    return True

def check_model():
    """Vérifie que le modèle LLM existe"""
    print("🤖 Vérification du modèle...")
    
    try:
        from config import config
        model_path = Path(config.MODEL_PATH)
        
        if not model_path.exists():
            print(f"❌ Modèle non trouvé: {model_path}")
            print("Téléchargez un modèle GGUF dans le dossier models/")
            return False
        
        print(f"✅ Modèle trouvé: {model_path.name}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du modèle: {e}")
        return False

def check_database():
    """Initialise et vérifie la base de données"""
    print("🗄️ Initialisation de la base de données...")
    
    try:
        from database import init_database
        init_database()
        print("✅ Base de données initialisée")
        return True
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def check_config():
    """Vérifie la configuration"""
    print("⚙️ Vérification de la configuration...")
    
    try:
        from config import config, logger
        
        # Vérifier les variables critiques
        if not config.TOKEN:
            print("❌ DISCORD_TOKEN manquant dans .env")
            return False
        
        if not config.AUTH_SECRET:
            print("⚠️ AUTH_SECRET manquant dans .env (2FA désactivé)")
        
        print("✅ Configuration valide")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

async def start_bot_safe():
    """Démarre le bot avec gestion d'erreurs"""
    try:
        from bot import start_bot
        from config import logger
        
        logger.info("Démarrage du bot Neuro...")
        print("🚀 Démarrage du bot Discord...")
        
        await start_bot()
        
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("👋 Bot arrêté")

def main():
    """Fonction principale"""
    print("🤖 Neuro-Bot - Démarrage Sécurisé")
    print("=" * 40)
    
    # Vérifications préalables
    checks = [
        check_requirements,
        check_files,
        check_config,
        check_model,
        check_database
    ]
    
    for check in checks:
        if not check():
            print("\n❌ Échec des vérifications préalables")
            print("Corrigez les erreurs ci-dessus avant de redémarrer")
            return 1
    
    print("\n✅ Toutes les vérifications sont passées")
    print("🚀 Lancement du bot...\n")
    
    # Démarrage du bot
    try:
        asyncio.run(start_bot_safe())
        return 0
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())