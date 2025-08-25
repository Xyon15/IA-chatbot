#!/usr/bin/env python3
"""
Script de diagnostic pour identifier et corriger les problèmes du bot Neuro
"""

import os
import sys
from pathlib import Path
import json

def check_discord_token():
    """Vérifie et valide le token Discord"""
    print("🔐 Vérification du token Discord...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Fichier .env manquant")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Vérifier si le token est présent
    if 'DISCORD_TOKEN=' not in content:
        print("❌ DISCORD_TOKEN manquant dans .env")
        return False
    
    # Extraire le token
    for line in content.split('\n'):
        if line.startswith('DISCORD_TOKEN='):
            token = line.split('=', 1)[1].strip()
            if not token or token == 'votre_token_discord_ici':
                print("❌ Token Discord vide ou exemple")
                print("🔧 Solution: Remplacez par un vrai token Discord")
                print("   1. Allez sur https://discord.com/developers/applications")
                print("   2. Créez une nouvelle application")
                print("   3. Dans Bot > Token, copiez le token")
                print("   4. Remplacez la valeur dans .env")
                return False
            
            # Vérifier le format basique du token
            if len(token) < 50:
                print(f"❌ Token trop court: {len(token)} caractères")
                print("🔧 Un token Discord valide fait généralement 70+ caractères")
                return False
            
            print(f"✅ Token présent ({len(token)} caractères)")
            return True
    
    return False

def check_gpu_configuration():
    """Vérifie la configuration GPU"""
    print("🖥️ Vérification de la configuration GPU...")
    
    try:
        import pynvml
        pynvml.nvmlInit()
        gpu_count = pynvml.nvmlDeviceGetCount()
        print(f"✅ {gpu_count} GPU(s) NVIDIA détecté(s)")
        
        # Afficher les informations des GPUs
        for i in range(gpu_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')
            memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
            print(f"   GPU {i}: {name} - Mémoire: {memory.total // 1024**2} MB")
        
        return True
        
    except ImportError:
        print("⚠️ pynvml non installé - impossible de détecter les GPUs")
        print("   Installation: pip install pynvml")
        return False
    except Exception as e:
        print(f"⚠️ Erreur GPU: {e}")
        print("   Le bot utilisera le CPU")
        return False

def check_llama_cpp_gpu():
    """Vérifie que llama-cpp-python supporte CUDA"""
    print("🔧 Vérification de llama-cpp-python avec support CUDA...")
    
    try:
        from llama_cpp import Llama
        print("✅ llama-cpp-python installé")
        
        # Tenter de créer un modèle minimal avec GPU
        print("🧪 Test de configuration GPU...")
        
        # Vérifier si nous avons un modèle de test
        models_dir = Path("models")
        model_files = list(models_dir.glob("*.gguf")) if models_dir.exists() else []
        
        if model_files:
            print(f"📄 Modèles trouvés: {[m.name for m in model_files]}")
            return True
        else:
            print("❌ Aucun modèle .gguf trouvé dans le dossier models/")
            print("🔧 Solution: Téléchargez un modèle GGUF compatible")
            return False
            
    except ImportError:
        print("❌ llama-cpp-python non installé")
        print("🔧 Installation avec support CUDA:")
        print("   pip uninstall llama-cpp-python")
        print("   pip install llama-cpp-python --force-reinstall --no-cache-dir")
        return False
    except Exception as e:
        print(f"❌ Erreur llama-cpp: {e}")
        return False

def create_env_template():
    """Crée un fichier .env template avec de vraies instructions"""
    print("📝 Création du fichier .env template...")
    
    env_content = """# Configuration du bot Neuro-Bot
# IMPORTANT: Remplacez les valeurs ci-dessous par vos vraies valeurs

# Token de votre bot Discord (obligatoire)
# 1. Allez sur https://discord.com/developers/applications
# 2. Créez une nouvelle application
# 3. Dans Bot > Token, copiez le token
# 4. Remplacez la ligne ci-dessous:
DISCORD_TOKEN=VOTRE_VRAI_TOKEN_ICI

# Secret pour l'authentification 2FA (optionnel mais recommandé)
# Générez une clé secrète de 32 caractères
# Vous pouvez utiliser: https://www.allkeysgenerator.com/Random/Security-Encryption-Key-Generator.aspx
AUTH_SECRET=VOTRE_SECRET_2FA_ICI

# Configuration avancée (optionnel)
# N_GPU_LAYERS=32  # Nombre de couches sur GPU (0 = CPU uniquement)
# N_THREADS=6      # Nombre de threads CPU
# N_CTX=4096       # Taille du contexte
# N_BATCH=256      # Taille des batches
"""
    
    # Sauvegarder le template
    with open('.env.template', 'w') as f:
        f.write(env_content)
    
    print("✅ Template créé: .env.template")
    print("🔧 Copiez .env.template vers .env et modifiez les valeurs")

def fix_gpu_config():
    """Propose des corrections pour la configuration GPU"""
    print("🔧 Correction de la configuration GPU...")
    
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Vérifier si N_GPU_LAYERS est défini
        if 'N_GPU_LAYERS=' not in content:
            print("⚙️ Ajout de N_GPU_LAYERS à .env...")
            with open(env_file, 'a') as f:
                f.write('\n# Configuration GPU\n')
                f.write('N_GPU_LAYERS=32  # Utilisez 0 pour CPU uniquement\n')
            print("✅ N_GPU_LAYERS ajouté")
        
        print("📋 Configuration GPU recommandée:")
        print("   N_GPU_LAYERS=32   # Pour GPU NVIDIA")
        print("   N_GPU_LAYERS=0    # Pour CPU uniquement")

def test_model_loading():
    """Teste le chargement d'un modèle"""
    print("🧪 Test de chargement de modèle...")
    
    try:
        from config import config
        model_path = Path(config.MODEL_PATH)
        
        if not model_path.exists():
            print(f"❌ Modèle non trouvé: {model_path}")
            return False
        
        print(f"📄 Modèle trouvé: {model_path.name}")
        print(f"📏 Taille: {model_path.stat().st_size // 1024**2} MB")
        
        # Test de chargement minimal
        from llama_cpp import Llama
        
        print("🔄 Test de chargement (peut prendre quelques minutes)...")
        test_config = {
            'n_gpu_layers': 1,  # Test avec 1 couche seulement
            'n_ctx': 512,       # Contexte réduit pour test
            'verbose': False
        }
        
        try:
            llm = Llama(model_path=str(model_path), **test_config)
            print("✅ Modèle chargé avec succès")
            
            # Test de génération simple
            result = llm("Test", max_tokens=1)
            print("✅ Génération de texte fonctionnelle")
            return True
            
        except Exception as e:
            print(f"❌ Erreur de chargement: {e}")
            if "CUDA" in str(e):
                print("🔧 Problème CUDA détecté - essayez N_GPU_LAYERS=0")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("🔍 Neuro-Bot - Diagnostic des Problèmes")
    print("=" * 50)
    
    # Vérifications par ordre de priorité
    issues_found = []
    
    # 1. Token Discord
    if not check_discord_token():
        issues_found.append("Token Discord invalide")
        create_env_template()
    
    # 2. Configuration GPU
    if not check_gpu_configuration():
        issues_found.append("Problème de détection GPU")
    
    # 3. llama-cpp-python avec CUDA
    if not check_llama_cpp_gpu():
        issues_found.append("Problème llama-cpp-python")
    
    # 4. Configuration
    fix_gpu_config()
    
    # 5. Test de modèle (optionnel)
    print("\n" + "="*50)
    test_model = input("🤔 Voulez-vous tester le chargement du modèle ? (y/N): ").lower()
    if test_model == 'y':
        test_model_loading()
    
    # Résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    
    if issues_found:
        print("❌ Problèmes détectés:")
        for issue in issues_found:
            print(f"   • {issue}")
        
        print("\n🔧 ACTIONS RECOMMANDÉES:")
        print("1. Corrigez le token Discord dans .env")
        print("2. Si pas de GPU: ajoutez N_GPU_LAYERS=0 dans .env")  
        print("3. Réinstallez llama-cpp-python si nécessaire")
        print("4. Relancez le diagnostic après corrections")
    else:
        print("✅ Configuration semble correcte")
        print("🚀 Vous pouvez essayer de lancer le bot")

if __name__ == "__main__":
    main()