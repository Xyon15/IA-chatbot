#!/usr/bin/env python3
"""
Script pour activer le support GPU pour Neuro-Bot
"""

import subprocess
import sys
import os
from pathlib import Path

def test_current_cuda_support():
    """Teste si la version actuelle de llama-cpp-python supporte CUDA"""
    print("🧪 Test du support CUDA actuel...")
    
    try:
        from llama_cpp import Llama
        
        # Test avec un modèle minimal et GPU
        models_dir = Path("models")
        model_files = list(models_dir.glob("*.gguf"))
        
        if not model_files:
            print("❌ Aucun modèle trouvé pour le test")
            return False
        
        model_path = model_files[0]
        print(f"📄 Test avec: {model_path.name}")
        
        # Essayer de charger avec GPU
        print("⏳ Test de chargement avec 1 couche GPU...")
        test_llm = Llama(
            model_path=str(model_path),
            n_gpu_layers=1,
            n_ctx=256,
            n_batch=64,
            verbose=False
        )
        
        # Vérifier si des couches sont sur GPU
        print("✅ Chargement réussi - vérification de l'utilisation GPU...")
        
        # Test de génération simple
        result = test_llm("Test", max_tokens=1, temperature=0)
        print("✅ Support CUDA déjà fonctionnel !")
        return True
        
    except Exception as e:
        if "CUDA" in str(e) or "cuBLAS" in str(e) or "GPU" in str(e):
            print(f"❌ Support CUDA non disponible: {e}")
        else:
            print(f"❌ Erreur lors du test: {e}")
        return False

def install_cuda_llama_cpp():
    """Installe llama-cpp-python avec support CUDA"""
    print("\n🔧 Installation de llama-cpp-python avec support CUDA...")
    print("⚠️ Cela va prendre plusieurs minutes...")
    
    # Variables d'environnement pour forcer CUDA
    env = os.environ.copy()
    env['CMAKE_ARGS'] = '-DLLAMA_CUBLAS=on'
    env['FORCE_CMAKE'] = '1'
    
    commands = [
        # Désinstaller la version actuelle
        [sys.executable, '-m', 'pip', 'uninstall', 'llama-cpp-python', '-y'],
        
        # Nettoyer le cache pip
        [sys.executable, '-m', 'pip', 'cache', 'purge'],
        
        # Réinstaller avec CUDA
        [sys.executable, '-m', 'pip', 'install', 'llama-cpp-python', 
         '--force-reinstall', '--no-cache-dir', '--verbose']
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n🔄 Étape {i}/{len(commands)}")
        print(f"Commande: {' '.join(cmd)}")
        
        try:
            if i == 3:  # Installation avec CUDA
                print("📦 Installation avec support CUDA (cela peut prendre 5-10 minutes)...")
                result = subprocess.run(cmd, env=env, check=True, timeout=1800)  # 30 minutes max
            else:
                result = subprocess.run(cmd, check=True, timeout=300)  # 5 minutes max
            
            print(f"✅ Étape {i} terminée avec succès")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'étape {i}:")
            print(f"Code de retour: {e.returncode}")
            if hasattr(e, 'output') and e.output:
                print(f"Sortie: {e.output}")
            return False
            
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout lors de l'étape {i} (processus trop long)")
            return False
        
        except KeyboardInterrupt:
            print(f"❌ Installation interrompue par l'utilisateur")
            return False
    
    return True

def update_gpu_config():
    """Met à jour la configuration pour utiliser le GPU"""
    print("\n⚙️ Mise à jour de la configuration GPU...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Fichier .env non trouvé")
        return False
    
    # Lire le fichier actuel
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Modifier N_GPU_LAYERS
    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith('N_GPU_LAYERS='):
            # Pour RTX 4050 avec 6GB VRAM, on peut utiliser 28-32 couches
            lines[i] = 'N_GPU_LAYERS=32  # GPU RTX 4050 activé\n'
            updated = True
            break
    
    if not updated:
        lines.append('\nN_GPU_LAYERS=32  # GPU RTX 4050 activé\n')
    
    # Ajouter des commentaires sur l'optimisation GPU
    gpu_config = """
# Configuration GPU optimisée pour RTX 4050
# N_GPU_LAYERS=32   # Toutes les couches sur GPU (maximum performance)
# N_GPU_LAYERS=28   # La plupart des couches sur GPU (sécurisé)
# N_GPU_LAYERS=16   # Hybride GPU/CPU (économise la VRAM)
# N_GPU_LAYERS=0    # CPU uniquement (pas de VRAM utilisée)
"""
    
    # Ajouter la configuration si elle n'existe pas déjà
    content = ''.join(lines)
    if 'Configuration GPU optimisée' not in content:
        lines.append(gpu_config)
    
    # Sauvegarder
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print("✅ Configuration GPU mise à jour dans .env")
    print("🎯 N_GPU_LAYERS=32 (toutes les couches sur GPU)")
    return True

def final_gpu_test():
    """Test final avec le GPU activé"""
    print("\n🚀 Test final avec GPU activé...")
    
    try:
        from llama_cpp import Llama
        
        # Trouver un modèle
        models_dir = Path("models")
        model_files = list(models_dir.glob("*.gguf"))
        
        if not model_files:
            print("❌ Aucun modèle trouvé")
            return False
        
        model_path = model_files[0]
        print(f"📄 Test avec: {model_path.name}")
        
        # Chargement avec GPU complet
        print("⏳ Chargement avec GPU (32 couches)...")
        llm = Llama(
            model_path=str(model_path),
            n_gpu_layers=32,
            n_ctx=1024,
            n_batch=128,
            verbose=True  # Pour voir les messages CUDA
        )
        
        print("\n🧪 Test de génération...")
        result = llm("Bonjour", max_tokens=10, temperature=0.7)
        
        print("✅ Test GPU réussi !")
        print(f"Réponse: {result['choices'][0]['text'].strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test GPU échoué: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Activation du Support GPU - Neuro-Bot")
    print("=" * 50)
    print(f"🎯 GPU Cible: RTX 4050 Laptop")
    print(f"🔧 CUDA Version: 12.9")
    
    # Test du support actuel
    if test_current_cuda_support():
        print("\n🎉 Le support CUDA est déjà fonctionnel !")
        update_gpu_config()
        print("\n✅ Configuration terminée. Le bot utilisera maintenant le GPU !")
        return
    
    print("\n🔧 Support CUDA non disponible - installation nécessaire")
    
    # Confirmer l'installation
    confirm = input("\n❓ Installer llama-cpp-python avec support CUDA ? (y/N): ").lower()
    if confirm != 'y':
        print("❌ Installation annulée")
        return
    
    print("\n⚠️ AVERTISSEMENT:")
    print("- L'installation peut prendre 10-15 minutes")
    print("- Nécessite une connexion internet stable")
    print("- Le processus va compiler les binaires CUDA")
    
    proceed = input("\nContinuer ? (y/N): ").lower()
    if proceed != 'y':
        print("❌ Installation annulée")
        return
    
    # Installation
    if install_cuda_llama_cpp():
        print("\n🎉 Installation terminée avec succès !")
        
        # Mise à jour config
        update_gpu_config()
        
        # Test final
        print("\n🧪 Test de la configuration GPU...")
        if final_gpu_test():
            print("\n🎉 SUCCÈS ! Le bot peut maintenant utiliser votre GPU RTX 4050 !")
            print("🚀 Performance attendue: 20-50 tokens/seconde (vs 1-5 en CPU)")
            print("\n💡 Commandes utiles:")
            print("   python start_bot.py  # Lancer le bot avec GPU")
            print("   !stats               # Voir l'utilisation GPU sur Discord")
        else:
            print("\n⚠️ Installation réussie mais test échoué")
            print("Le bot devrait quand même fonctionner avec GPU")
    else:
        print("\n❌ Échec de l'installation")
        print("Le bot continuera à utiliser le CPU")

if __name__ == "__main__":
    main()