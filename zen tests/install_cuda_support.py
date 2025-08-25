#!/usr/bin/env python3
"""
Script pour installer llama-cpp-python avec support CUDA
"""

import subprocess
import sys
import os
from pathlib import Path

def check_cuda_installed():
    """Vérifie si CUDA est installé sur le système"""
    print("🔍 Vérification de CUDA...")
    
    # Vérifier nvcc
    try:
        result = subprocess.run(['nvcc', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ CUDA Toolkit détecté")
            print(f"   Version: {result.stdout}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Vérifier les variables d'environnement CUDA
    cuda_path = os.environ.get('CUDA_PATH')
    if cuda_path and Path(cuda_path).exists():
        print(f"✅ CUDA_PATH trouvé: {cuda_path}")
        return True
    
    print("❌ CUDA Toolkit non détecté")
    return False

def install_cuda_llama():
    """Installe llama-cpp-python avec support CUDA"""
    print("📦 Installation de llama-cpp-python avec CUDA...")
    
    # Commandes d'installation
    commands = [
        # Désinstaller la version actuelle
        [sys.executable, '-m', 'pip', 'uninstall', 'llama-cpp-python', '-y'],
        
        # Réinstaller avec CUDA (force les variables d'environnement)
        [sys.executable, '-m', 'pip', 'install', 'llama-cpp-python', 
         '--force-reinstall', '--no-cache-dir']
    ]
    
    # Variables d'environnement pour forcer CUDA
    env = os.environ.copy()
    env['CMAKE_ARGS'] = '-DLLAMA_CUBLAS=on'
    env['FORCE_CMAKE'] = '1'
    
    for i, cmd in enumerate(commands, 1):
        print(f"🔄 Étape {i}/{len(commands)}: {' '.join(cmd)}")
        
        try:
            if i == 2:  # Deuxième commande avec variables d'environnement
                result = subprocess.run(cmd, env=env, check=True, timeout=600)
            else:
                result = subprocess.run(cmd, check=True, timeout=600)
            
            print(f"✅ Étape {i} réussie")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'étape {i}: {e}")
            return False
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout lors de l'étape {i}")
            return False
    
    return True

def test_cuda_support():
    """Teste si CUDA fonctionne avec llama-cpp-python"""
    print("🧪 Test du support CUDA...")
    
    try:
        from llama_cpp import Llama
        
        # Trouver un modèle de test
        models_dir = Path("models")
        model_files = list(models_dir.glob("*.gguf")) if models_dir.exists() else []
        
        if not model_files:
            print("❌ Aucun modèle .gguf trouvé pour le test")
            return False
        
        model_path = model_files[0]
        print(f"📄 Test avec: {model_path.name}")
        
        # Test avec GPU
        print("⏳ Chargement avec GPU (peut prendre quelques minutes)...")
        test_llm = Llama(
            model_path=str(model_path),
            n_gpu_layers=1,  # Une couche sur GPU
            n_ctx=256,       # Contexte réduit pour test rapide
            verbose=True
        )
        
        print("✅ CUDA fonctionne!")
        
        # Test de génération
        result = test_llm("Test", max_tokens=1)
        print("✅ Génération avec GPU réussie")
        
        return True
        
    except Exception as e:
        print(f"❌ Test CUDA échoué: {e}")
        return False

def update_env_for_gpu():
    """Met à jour .env pour utiliser le GPU"""
    print("⚙️ Configuration pour utiliser le GPU...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Fichier .env non trouvé")
        return False
    
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Modifier N_GPU_LAYERS
    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith('N_GPU_LAYERS='):
            lines[i] = 'N_GPU_LAYERS=32  # GPU NVIDIA activé\n'
            updated = True
            break
    
    if not updated:
        lines.append('\nN_GPU_LAYERS=32  # GPU NVIDIA activé\n')
    
    # Sauvegarder
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print("✅ Configuration GPU activée dans .env")
    return True

def show_cuda_installation_guide():
    """Affiche le guide d'installation CUDA"""
    print("📖 Guide d'Installation CUDA")
    print("=" * 40)
    print()
    print("Pour installer CUDA Toolkit:")
    print("1. Allez sur: https://developer.nvidia.com/cuda-downloads")
    print("2. Sélectionnez: Windows > x86_64 > 11 > exe (local)")
    print("3. Téléchargez et installez CUDA Toolkit")
    print("4. Redémarrez votre ordinateur")
    print("5. Relancez ce script pour installer llama-cpp-python")
    print()
    print("⚠️ ATTENTION:")
    print("- L'installation CUDA prend ~3GB d'espace disque")
    print("- Nécessite un redémarrage")
    print("- Compatible uniquement avec GPU NVIDIA")

def main():
    """Fonction principale"""
    print("🚀 Installation Support CUDA - Neuro-Bot")
    print("=" * 50)
    
    # Vérifier CUDA
    if not check_cuda_installed():
        print()
        show_cuda_installation_guide()
        
        install_cuda = input("\n❓ CUDA n'est pas installé. Voulez-vous voir le guide d'installation ? (y/N): ").lower()
        if install_cuda == 'y':
            show_cuda_installation_guide()
        return
    
    # CUDA est installé, procéder à l'installation
    print("\n🔧 CUDA détecté. Installation de llama-cpp-python avec support GPU...")
    proceed = input("Continuer ? Cela va réinstaller llama-cpp-python (y/N): ").lower()
    
    if proceed != 'y':
        print("❌ Installation annulée")
        return
    
    # Installation
    if install_cuda_llama():
        print("\n✅ Installation terminée!")
        
        # Test
        test_cuda = input("\n🧪 Tester le support CUDA ? (y/N): ").lower()
        if test_cuda == 'y':
            if test_cuda_support():
                print("\n🎉 Support CUDA fonctionnel!")
                
                # Mettre à jour .env
                update_gpu = input("\n⚙️ Activer le GPU dans la configuration ? (y/N): ").lower()
                if update_gpu == 'y':
                    update_env_for_gpu()
                    print("\n🚀 Configuration complète! Vous pouvez lancer: python start_bot.py")
                else:
                    print("\n💡 Pour activer le GPU plus tard, changez N_GPU_LAYERS=32 dans .env")
            else:
                print("\n❌ Problème avec CUDA. Le bot utilisera le CPU.")
        else:
            print("\n💡 Pour tester plus tard, relancez ce script")
    else:
        print("\n❌ Échec de l'installation. Le bot continuera à utiliser le CPU.")

if __name__ == "__main__":
    main()