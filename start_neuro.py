#!/usr/bin/env python3
"""
Script de démarrage unifié pour Kira-Bot
Combine validation, optimisation GPU et démarrage sécurisé
"""

import sys
import os
import time
import asyncio
from pathlib import Path

def clean_environment():
    """Nettoie l'environnement des variables en cache - SOLUTION AU PROBLÈME TOKEN"""
    print("🧹 Nettoyage de l'environnement...")
    
    # Supprimer les variables d'environnement en cache
    cache_vars_removed = 0
    for var in ['DISCORD_TOKEN', 'AUTH_SECRET']:
        if var in os.environ:
            del os.environ[var]
            cache_vars_removed += 1
    
    # Supprimer les modules Python en cache liés à la config
    modules_to_remove = []
    for name in sys.modules:
        if any(keyword in name.lower() for keyword in ['config', 'dotenv']):
            modules_to_remove.append(name)
    
    for name in modules_to_remove:
        del sys.modules[name]
    
    if cache_vars_removed > 0 or modules_to_remove:
        print(f"✅ Cache nettoyé: {cache_vars_removed} variables, {len(modules_to_remove)} modules")
    else:
        print("✅ Environnement déjà propre")
    
    # Forcer le rechargement du .env
    from dotenv import load_dotenv
    load_dotenv(override=True)

def check_requirements():
    """Vérifie que tous les prérequis sont installés"""
    print("🔍 Vérification des prérequis...")
    
    # Packages essentiels (obligatoires)
    essential_packages = {
        'discord.py': 'discord',
        'llama-cpp-python': 'llama_cpp', 
        'python-dotenv': 'dotenv',
        'pynvml': 'pynvml',
        'aiohttp': 'aiohttp',
        'selectolax': 'selectolax',
        'transformers': 'transformers',
        'pyotp': 'pyotp'
    }
    
    # Packages optionnels (pour fonctionnalités spécifiques)
    optional_packages = {
        'pyside6': ('PySide6', 'Interface graphique')
    }
    
    missing_essential = []
    missing_optional = []
    
    # Vérification packages essentiels
    for package_name, import_name in essential_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_essential.append(package_name)
    
    # Vérification packages optionnels
    for package_name, (import_name, description) in optional_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_optional.append((package_name, description))
    
    # Rapport des packages manquants
    if missing_essential:
        print(f"❌ Packages essentiels manquants: {', '.join(missing_essential)}")
        print("Installez-les avec: pip install " + " ".join(missing_essential))
        return False
    
    if missing_optional:
        print(f"⚠️  Packages optionnels manquants:")
        for package, desc in missing_optional:
            print(f"   - {package} ({desc})")
        print("💡 Installez-les avec: pip install " + " ".join([p[0] for p in missing_optional]))
    
    print("✅ Tous les packages essentiels sont installés")
    return True

def check_files():
    """Vérifie que tous les fichiers nécessaires existent"""
    print("📁 Vérification des fichiers...")
    
    required_files = [
        '.env',
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

def check_vram_availability():
    """Vérifie la disponibilité VRAM et recommande une configuration"""
    try:
        import pynvml
        NVIDIA_AVAILABLE = True
    except ImportError:
        NVIDIA_AVAILABLE = False
        print("⚠️  GPU NVIDIA non détectée - utilisation CPU uniquement")
        return None
    
    if not NVIDIA_AVAILABLE:
        return None
    
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        if isinstance(gpu_name, bytes):
            gpu_name = gpu_name.decode()
        
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        vram_total = int(mem_info.total) // (1024**2)  # MB
        vram_free = int(mem_info.free) // (1024**2)   # MB
        vram_used = int(mem_info.used) // (1024**2)   # MB
        
        pynvml.nvmlShutdown()
        
        print(f"🖥️  GPU détectée: {gpu_name}")
        print(f"🧮 VRAM: {vram_used} MB utilisée / {vram_total} MB total ({vram_free} MB libre)")
        
        return {
            'gpu_name': gpu_name,
            'vram_total': vram_total,
            'vram_free': vram_free,
            'vram_used': vram_used
        }
        
    except Exception as e:
        print(f"⚠️  Erreur lors de la vérification GPU: {e}")
        return None

def get_optimal_config(vram_info):
    """Détermine la configuration optimale selon la VRAM disponible"""
    if not vram_info:
        return {
            'N_CTX': '4096',
            'N_GPU_LAYERS': '0',
            'N_BATCH': '64',
            'profile': 'CPU uniquement'
        }
    
    vram_free = vram_info['vram_free']
    
    if vram_free >= 2000:
        return {
            'N_CTX': '16384',
            'N_GPU_LAYERS': '32',
            'N_BATCH': '512',
            'profile': 'Performance maximale'
        }
    elif vram_free >= 1500:
        return {
            'N_CTX': '12288',
            'N_GPU_LAYERS': '28',
            'N_BATCH': '256',
            'profile': 'Équilibrée'
        }
    elif vram_free >= 1000:
        return {
            'N_CTX': '8192',
            'N_GPU_LAYERS': '24',
            'N_BATCH': '128',
            'profile': 'Économique'
        }
    else:
        return {
            'N_CTX': '4096',
            'N_GPU_LAYERS': '16',
            'N_BATCH': '64',
            'profile': 'Secours'
        }

def read_current_config():
    """Lit la configuration actuelle du fichier .env"""
    env_file = Path(__file__).parent / ".env"
    config = {}
    
    if not env_file.exists():
        return config
    
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config

def apply_config_if_needed(optimal_config, auto_apply=False):
    """Applique la configuration optimale si nécessaire"""
    current_config = read_current_config()
    
    # Vérification si des changements sont nécessaires
    changes_needed = []
    for key in ['N_CTX', 'N_GPU_LAYERS', 'N_BATCH']:
        current_value = current_config.get(key, 'non défini')
        optimal_value = optimal_config[key]
        if current_value != optimal_value:
            changes_needed.append((key, current_value, optimal_value))
    
    if not changes_needed:
        print("✅ Configuration GPU déjà optimale")
        return True
    
    print(f"\n🎯 Configuration recommandée: {optimal_config['profile']}")
    print("🔧 Changements proposés:")
    for key, old_val, new_val in changes_needed:
        print(f"   {key}: {old_val} → {new_val}")
    
    if not auto_apply:
        response = input("\n❓ Appliquer ces changements ? (o/N): ").lower().strip()
        if response not in ['o', 'oui', 'y', 'yes']:
            print("⚠️  Configuration non modifiée - démarrage avec les paramètres actuels")
            return False
    
    # Application des changements
    try:
        env_file = Path(__file__).parent / ".env"
        lines = []
        
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        
        # Mise à jour des lignes existantes
        updated_keys = set()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and '=' in stripped:
                key = stripped.split('=', 1)[0].strip()
                if key in optimal_config:
                    lines[i] = f"{key}={optimal_config[key]}\n"
                    updated_keys.add(key)
        
        # Ajout des nouvelles clés
        for key in ['N_CTX', 'N_GPU_LAYERS', 'N_BATCH']:
            if key not in updated_keys:
                lines.append(f"{key}={optimal_config[key]}\n")
        
        # Écriture du fichier
        with open(env_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("✅ Configuration GPU mise à jour avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

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
        
        logger.info("Démarrage du bot Kira...")
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

def start_gui():
    """Lance l'interface graphique"""
    # Vérifier d'abord PySide6
    try:
        import PySide6
    except ImportError:
        print("⚠️  PySide6 non installé - interface graphique indisponible")
        print("💡 Installez avec: pip install PySide6")
        return False
    
    # Essayer les différents modules GUI disponibles dans le bon ordre
    gui_modules = [
        ("gui.launch_kira_gui", "Interface moderne", "launch_gui"),
        ("gui.kira_gui", "Interface graphique", "main"),
        ("launch_gui", "Interface de redirection", "main")
    ]
    
    for module_name, description, function_name in gui_modules:
        try:
            print(f"🎨 {description}...")
            module = __import__(module_name, fromlist=[function_name])
            if hasattr(module, function_name):
                gui_function = getattr(module, function_name)
                result = gui_function()
                # Si c'est launch_gui qui retourne un booléen, vérifier le résultat
                if result is False:
                    continue
                return True
            else:
                print(f"⚠️  Fonction {function_name} non trouvée dans {module_name}")
        except ImportError as e:
            print(f"⚠️  Module {module_name} non trouvé: {e}")
            continue
        except Exception as e:
            print(f"❌ Erreur {module_name}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print("❌ Aucune interface graphique disponible")
    print("Solutions:")
    print("  - Installez PySide6: pip install PySide6")
    print("  - Vérifiez les logs d'erreur")
    return False

def main():
    """Fonction principale"""
    print("🤖 Kira-Bot - Démarrage Unifié")
    print("=" * 50)
    
    # Mode de fonctionnement
    mode = "bot"  # par défaut
    auto_gpu = False
    
    if "--gui" in sys.argv:
        mode = "gui"
    if "--auto" in sys.argv:
        auto_gpu = True
    
    # 1. NETTOYAGE DU CACHE EN PREMIER
    clean_environment()
    
    # 2. Vérifications préalables
    print("\n📋 Vérifications système...")
    checks = [
        ("Prérequis", check_requirements),
        ("Fichiers", check_files),
        ("Configuration", check_config),
        ("Modèle", check_model),
        ("Base de données", check_database)
    ]
    
    for name, check in checks:
        if not check():
            print(f"\n❌ Échec de vérification: {name}")
            print("Corrigez les erreurs ci-dessus avant de redémarrer")
            return 1
    
    # 3. Optimisation GPU
    print("\n🖥️ Optimisation GPU...")
    vram_info = check_vram_availability()
    optimal_config = get_optimal_config(vram_info)
    apply_config_if_needed(optimal_config, auto_gpu)
    
    print("\n✅ Toutes les vérifications sont passées")
    
    # 4. Démarrage selon le mode
    if mode == "gui":
        print("🎨 Mode interface graphique")
        return 0 if start_gui() else 1
    else:
        print("🤖 Mode bot Discord")
        try:
            asyncio.run(start_bot_safe())
            return 0
        except Exception as e:
            print(f"❌ Erreur fatale: {e}")
            return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️ Démarrage interrompu")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur fatale non gérée: {e}")
        sys.exit(1)