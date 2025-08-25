#!/usr/bin/env python3
"""
Monitore l'installation de llama-cpp-python et teste le GPU
"""

import time
import subprocess
import sys

def check_installation():
    """Vérifie si llama-cpp-python est installé"""
    try:
        import llama_cpp
        return True
    except ImportError:
        return False

def test_gpu_immediately():
    """Test GPU immédiatement après installation"""
    print("🧪 Test GPU immédiatement après installation...")
    
    try:
        from llama_cpp import Llama
        from pathlib import Path
        
        # Trouver un modèle
        models_dir = Path("models")
        model_files = list(models_dir.glob("*.gguf"))
        
        if not model_files:
            print("❌ Aucun modèle trouvé")
            return False
        
        model_path = model_files[0]
        print(f"📄 Test avec: {model_path.name}")
        
        # Test avec 2 couches GPU
        print("🔧 Test avec 2 couches sur GPU...")
        llm = Llama(
            model_path=str(model_path),
            n_gpu_layers=2,
            n_ctx=256,
            verbose=True
        )
        
        print("✅ Test réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def monitor_and_test():
    """Surveille l'installation et teste le GPU"""
    print("🔍 Surveillance de l'Installation llama-cpp-python")
    print("=" * 55)
    
    max_attempts = 60  # 60 tentatives = 5 minutes
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        
        print(f"🔄 Vérification {attempt}/{max_attempts}...")
        
        if check_installation():
            print("🎉 llama-cpp-python installé !")
            
            # Attendre quelques secondes pour que tout soit stabilisé
            print("⏳ Attente de stabilisation (5 secondes)...")
            time.sleep(5)
            
            # Test GPU
            if test_gpu_immediately():
                print("\n✅ SUCCÈS ! Le GPU est fonctionnel")
                print("💡 Vous pouvez maintenant changer N_GPU_LAYERS=32 dans .env")
                return True
            else:
                print("\n⚠️ Installation réussie mais GPU non fonctionnel")
                print("💡 Gardez N_GPU_LAYERS=0 pour CPU uniquement")
                return False
        
        # Attendre 5 secondes avant la prochaine vérification
        time.sleep(5)
    
    print("❌ Timeout - Installation non détectée après 5 minutes")
    return False

if __name__ == "__main__":
    monitor_and_test()