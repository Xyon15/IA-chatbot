#!/usr/bin/env python3
"""
Test final du support GPU après installation CUDA
"""

def test_gpu_support():
    """Teste le support GPU après installation CUDA"""
    print("🧪 Test Final du Support GPU")
    print("=" * 40)
    
    try:
        from llama_cpp import Llama
        from pathlib import Path
        
        # Trouver un modèle
        models_dir = Path("../models")
        model_files = list(models_dir.glob("*.gguf"))
        
        if not model_files:
            print("❌ Aucun modèle .gguf trouvé")
            return False
        
        model_path = model_files[0]
        print(f"📄 Test avec: {model_path.name}")
        
        # Test avec 4 couches GPU
        print("\n🔧 Chargement avec 4 couches sur GPU...")
        print("⏳ Si CUDA fonctionne, vous verrez 'layer X assigned to device GPU'...")
        
        llm = Llama(
            model_path=str(model_path),
            n_gpu_layers=4,
            n_ctx=512,
            verbose=True
        )
        
        print("\n🧪 Test de génération...")
        response = llm("Hello", max_tokens=5, temperature=0)
        print(f"✅ Génération réussie: {response['choices'][0]['text'].strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def analyze_gpu_usage():
    """Analyse les logs pour vérifier l'utilisation GPU"""
    print("\n🔍 Comment Vérifier l'Utilisation GPU:")
    print("Dans les logs ci-dessus, cherchez:")
    print("✅ 'layer X assigned to device GPU' = Couches sur GPU")
    print("✅ 'GPU KV buffer size' = Cache GPU utilisé")
    print("✅ Messages contenant 'CUDA' = Support GPU actif")
    print("❌ 'layer X assigned to device CPU' = Couches sur CPU (pas de GPU)")

if __name__ == "__main__":
    success = test_gpu_support()
    analyze_gpu_usage()
    
    if success:
        print("\n🎉 Test terminé !")
        print("Si vous voyez 'layer X assigned to device GPU', le GPU fonctionne !")
    else:
        print("\n❌ Test échoué.")
        print("Le bot utilisera le CPU.") 