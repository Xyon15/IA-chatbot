#!/usr/bin/env python3
"""
Test et correction de la configuration GPU pour le bot Neuro
"""

import os
import sys
from pathlib import Path

def test_pynvml():
    """Teste pynvml avec gestion des erreurs"""
    print("🔧 Test détaillé de pynvml...")
    
    try:
        import pynvml
        print("✅ pynvml importé")
        
        # Initialisation
        pynvml.nvmlInit()
        print("✅ pynvml initialisé")
        
        # Obtenir le nombre de GPUs
        gpu_count = pynvml.nvmlDeviceGetCount()
        print(f"✅ {gpu_count} GPU(s) détecté(s)")
        
        # Pour chaque GPU
        for i in range(gpu_count):
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                print(f"✅ Handle GPU {i} obtenu")
                
                # Nom du GPU (correction du bug decode)
                try:
                    name = pynvml.nvmlDeviceGetName(handle)
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    elif isinstance(name, str):
                        pass  # Déjà une chaîne
                    else:
                        name = str(name)
                    print(f"✅ GPU {i}: {name}")
                except Exception as e:
                    print(f"⚠️ Impossible d'obtenir le nom du GPU {i}: {e}")
                    name = f"GPU {i} (nom inconnu)"
                
                # Informations mémoire
                try:
                    memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    total_mb = memory.total // 1024**2
                    free_mb = memory.free // 1024**2
                    used_mb = memory.used // 1024**2
                    print(f"   Mémoire: {used_mb}/{total_mb} MB utilisés ({free_mb} MB libres)")
                except Exception as e:
                    print(f"⚠️ Impossible d'obtenir les infos mémoire du GPU {i}: {e}")
                
                # Température
                try:
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    print(f"   Température: {temp}°C")
                except Exception as e:
                    print(f"⚠️ Impossible d'obtenir la température du GPU {i}: {e}")
                
            except Exception as e:
                print(f"❌ Erreur pour GPU {i}: {e}")
        
        return True
        
    except ImportError:
        print("❌ pynvml non installé")
        print("🔧 Installation: pip install pynvml")
        return False
    except Exception as e:
        print(f"❌ Erreur pynvml: {e}")
        return False

def test_cuda_availability():
    """Teste la disponibilité de CUDA"""
    print("\n🔧 Test de disponibilité CUDA...")
    
    # Test via llama-cpp-python
    try:
        from llama_cpp import Llama
        
        # Créer une instance de test avec 1 couche GPU
        print("🧪 Test avec 1 couche GPU...")
        models_dir = Path("models")
        model_files = list(models_dir.glob("*.gguf"))
        
        if not model_files:
            print("❌ Aucun modèle trouvé pour le test")
            return False
        
        model_path = model_files[0]  # Premier modèle trouvé
        print(f"📄 Utilisation du modèle: {model_path.name}")
        
        # Configuration de test avec GPU
        test_config = {
            'model_path': str(model_path),
            'n_gpu_layers': 1,  # Une seule couche pour test rapide
            'n_ctx': 512,       # Contexte réduit
            'n_batch': 64,      # Batch réduit
            'verbose': True     # Pour voir les messages CUDA
        }
        
        print("⏳ Chargement du modèle avec GPU (peut prendre 1-2 minutes)...")
        llm = Llama(**test_config)
        print("✅ Modèle chargé avec GPU activé")
        
        # Test de génération très simple
        print("🧪 Test de génération...")
        result = llm("Hello", max_tokens=5, temperature=0)
        print("✅ Génération réussie avec GPU")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur CUDA: {e}")
        
        if "CUDA" in str(e) or "cuBLAS" in str(e):
            print("🔧 Problème CUDA détecté. Solutions:")
            print("   1. Vérifiez que CUDA est installé")
            print("   2. Réinstallez llama-cpp-python avec support CUDA")
            print("   3. Ou utilisez N_GPU_LAYERS=0 pour CPU uniquement")
        
        return False

def fix_config_for_cpu():
    """Configure le bot pour utiliser uniquement le CPU"""
    print("\n🔧 Configuration pour CPU uniquement...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Fichier .env manquant")
        return False
    
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Modifier N_GPU_LAYERS
    modified = False
    for i, line in enumerate(lines):
        if line.strip().startswith('N_GPU_LAYERS='):
            lines[i] = 'N_GPU_LAYERS=0  # CPU uniquement\n'
            modified = True
            break
    
    if not modified:
        lines.append('\nN_GPU_LAYERS=0  # CPU uniquement\n')
    
    # Sauvegarder
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print("✅ Configuration mise à jour pour CPU uniquement")
    return True

def test_final_config():
    """Test final de la configuration"""
    print("\n🧪 Test de la configuration finale...")
    
    try:
        from config import config
        print(f"✅ Configuration chargée")
        print(f"   TOKEN: {'✅ Présent' if config.TOKEN else '❌ Manquant'}")
        print(f"   N_GPU_LAYERS: {config.LLM_CONFIG.get('n_gpu_layers', 'Non défini')}")
        print(f"   Modèle: {Path(config.MODEL_PATH).name}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 Test et Correction GPU - Neuro-Bot")
    print("=" * 50)
    
    # Test 1: pynvml
    gpu_ok = test_pynvml()
    
    # Test 2: CUDA uniquement si GPU détecté
    cuda_ok = False
    if gpu_ok:
        cuda_ok = test_cuda_availability()
    
    # Si CUDA ne fonctionne pas, configurer pour CPU
    if not cuda_ok:
        print("\n⚠️ GPU/CUDA non fonctionnel - configuration pour CPU")
        fix_config_for_cpu()
    
    # Test final
    test_final_config()
    
    # Recommandations finales
    print("\n" + "=" * 50)
    print("📋 RECOMMANDATIONS FINALES:")
    
    if cuda_ok:
        print("✅ Configuration GPU fonctionnelle")
        print("🚀 Le bot peut utiliser votre GPU NVIDIA")
    else:
        print("⚠️ Configuration CPU activée")
        print("🐌 Le bot sera plus lent mais fonctionnel")
        print("🔧 Pour activer GPU plus tard:")
        print("   1. Installez CUDA Toolkit")
        print("   2. pip uninstall llama-cpp-python")
        print("   3. pip install llama-cpp-python --force-reinstall --no-cache-dir")
        print("   4. Changez N_GPU_LAYERS=32 dans .env")
    
    print("\n🚀 Vous pouvez maintenant lancer: python start_bot.py")

if __name__ == "__main__":
    main()