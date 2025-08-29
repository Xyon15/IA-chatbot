#!/usr/bin/env python3
"""
Test du support GPU pour Neuro-Bot
Vérifie que llama-cpp-python utilise bien CUDA
"""

import os
import sys

# Ajouter le répertoire du projet au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_llama_cpp_cuda():
    """Test le support CUDA de llama-cpp-python"""
    print("========================================")
    print("Test du support GPU - Neuro Bot")
    print("========================================")
    
    try:
        from llama_cpp import Llama
        from llama_cpp import llama_cpp as _llama_cpp
        
        # Obtenir les informations système
        sys_info = _llama_cpp.llama_print_system_info().decode("utf-8")
        print("Informations système llama.cpp:")
        print(sys_info)
        print()
        
        # Vérifier la présence de CUDA
        cuda_supported = any(term in sys_info for term in ["CUDA", "cuBLAS", "ggml-cuda"])
        
        if cuda_supported:
            print("✅ CUDA Support détecté !")
            print("Le GPU sera utilisé pour l'accélération.")
        else:
            print("❌ CUDA Support NON détecté")
            print("Le bot fonctionnera en mode CPU uniquement.")
        
        print()
        return cuda_supported
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_gpu_detection():
    """Test la détection GPU avec pynvml"""
    print("Test de détection GPU:")
    
    try:
        import pynvml
        pynvml.nvmlInit()
        
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        if isinstance(gpu_name, bytes):
            gpu_name = gpu_name.decode()
        
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        vram_total_mb = mem_info.total // (1024**2)
        vram_free_mb = mem_info.free // (1024**2)
        
        print(f"✅ GPU détectée: {gpu_name}")
        print(f"   VRAM: {vram_free_mb} MB libre / {vram_total_mb} MB total")
        
        pynvml.nvmlShutdown()
        return True
        
    except ImportError:
        print("❌ pynvml non disponible")
        return False
    except Exception as e:
        print(f"❌ Erreur détection GPU: {e}")
        return False

def main():
    """Fonction principale de test"""
    cuda_ok = test_llama_cpp_cuda()
    print()
    gpu_ok = test_gpu_detection()
    
    print()
    print("========================================")
    if cuda_ok and gpu_ok:
        print("✅ Tous les tests GPU ont réussi !")
        print("Le bot peut utiliser l'accélération GPU.")
    else:
        print("❌ Des problèmes ont été détectés.")
        if not cuda_ok:
            print("- llama-cpp-python n'a pas le support CUDA")
        if not gpu_ok:
            print("- La détection GPU a échoué")
    print("========================================")

if __name__ == "__main__":
    main()