#!/usr/bin/env python3
"""
Test du support GPU après réinstallation de llama-cpp-python
"""

import sys
from pathlib import Path

def test_gpu_support():
    """Teste le support GPU après réinstallation"""
    print("🧪 Test du Support GPU - Après Réinstallation")
    print("=" * 50)
    
    try:
        from llama_cpp import Llama
        print("✅ llama-cpp-python importé avec succès")
        
        # Trouver un modèle de test
        models_dir = Path("models")
        model_files = list(models_dir.glob("*.gguf"))
        
        if not model_files:
            print("❌ Aucun modèle .gguf trouvé")
            return False
        
        model_path = model_files[0]  # Premier modèle trouvé
        print(f"📄 Test avec: {model_path.name}")
        
        # Test avec 4 couches GPU pour commencer
        print("\n🔧 Test avec 4 couches sur GPU...")
        print("⏳ Chargement du modèle (peut prendre 1-2 minutes)...")
        
        llm = Llama(
            model_path=str(model_path),
            n_gpu_layers=4,  # Commencer avec quelques couches
            n_ctx=512,       # Contexte réduit pour test rapide
            n_batch=64,      # Batch réduit
            verbose=True     # Voir les messages de chargement
        )
        
        print("\n🎉 Modèle chargé avec succès !")
        
        # Test de génération simple
        print("\n🧪 Test de génération...")
        response = llm("Hello", max_tokens=5, temperature=0)
        print(f"✅ Génération réussie: {response['choices'][0]['text'].strip()}")
        
        # Vérifier si des couches sont sur GPU dans les logs
        print("\n📊 Recherche des messages GPU dans les logs ci-dessus...")
        print("Cherchez des lignes contenant 'GPU' ou 'CUDA' dans la sortie verbose")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        
        if "CUDA" in str(e) or "cuBLAS" in str(e):
            print("\n🔧 Problème CUDA détecté:")
            print("- Vérifiez que CUDA Toolkit est bien installé")
            print("- La réinstallation de llama-cpp-python pourrait être nécessaire")
            print("- Ou utilisez N_GPU_LAYERS=0 pour CPU uniquement")
        
        return False

def check_gpu_assignment():
    """Vérifie l'assignation des couches GPU dans les logs"""
    print("\n🔍 Guide de Vérification GPU:")
    print("Dans les logs ci-dessus, cherchez:")
    print("✅ 'layer X assigned to device GPU' = Couches sur GPU")
    print("❌ 'layer X assigned to device CPU' = Couches sur CPU")
    print("✅ Messages contenant 'CUDA' ou 'cuBLAS' = Support GPU actif")
    print("✅ 'GPU KV buffer size' = Mémoire GPU utilisée")

if __name__ == "__main__":
    success = test_gpu_support()
    check_gpu_assignment()
    
    if success:
        print("\n🎉 Test réussi ! Le GPU semble fonctionnel.")
        print("💡 Vous pouvez maintenant augmenter N_GPU_LAYERS dans .env")
    else:
        print("\n❌ Test échoué. Le bot utilisera le CPU.")
        print("💡 Changez N_GPU_LAYERS=0 dans .env pour CPU uniquement")