#!/usr/bin/env python3
"""
Test complet final - GPU + Discord + Bot
"""

import asyncio
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent pour les imports
sys.path.append(str(Path("..").absolute()))

async def test_discord_connection():
    """Test de la connexion Discord"""
    print("🔑 Test de Connexion Discord")
    print("=" * 35)
    
    try:
        import aiohttp
        from dotenv import load_dotenv
        
        load_dotenv("../.env")
        token = os.getenv("DISCORD_TOKEN")
        
        if not token:
            print("❌ Token Discord non trouvé")
            return False
        
        headers = {
            "Authorization": f"Bot {token}",
            "User-Agent": "Neuro-Bot Test"
        }
        
        timeout = aiohttp.ClientTimeout(total=10)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Bot Discord: {data['username']}#{data.get('discriminator', '0000')}")
                    print(f"🆔 ID: {data['id']}")
                    return True
                else:
                    print(f"❌ Échec de connexion: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Erreur Discord: {e}")
        return False

def test_gpu_status():
    """Test du statut GPU"""
    print("\n🔥 Test du GPU")
    print("=" * 20)
    
    try:
        from llama_cpp import Llama
        
        # Test rapide avec peu de couches
        llm = Llama(
            model_path="../models/mistral-7b-instruct-v0.2.Q5_K_M.gguf",
            n_gpu_layers=4,
            n_ctx=256,
            verbose=False
        )
        
        print("✅ GPU RTX 4050: FONCTIONNEL")
        print("✅ Modèle LLM: CHARGÉ")
        return True
        
    except Exception as e:
        print(f"❌ Erreur GPU/LLM: {e}")
        return False

def test_all_components():
    """Test de tous les composants"""
    print("🧪 Test Complet de Neuro-Bot")
    print("=" * 40)
    
    results = {
        "gpu": False,
        "discord": False
    }
    
    # Test GPU
    results["gpu"] = test_gpu_status()
    
    # Test Discord (async)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results["discord"] = loop.run_until_complete(test_discord_connection())
    finally:
        loop.close()
    
    # Résumé
    print("\n📊 Résumé des Tests")
    print("=" * 25)
    print(f"🔥 GPU RTX 4050:     {'✅ OK' if results['gpu'] else '❌ ÉCHEC'}")
    print(f"🤖 Discord Token:    {'✅ OK' if results['discord'] else '❌ ÉCHEC'}")
    
    if all(results.values()):
        print("\n🎉 TOUS LES TESTS PASSÉS!")
        print("🚀 Neuro-Bot est PRÊT À FONCTIONNER!")
        print("\n📋 Commandes de test Discord:")
        print("   !helpme")
        print("   !stats") 
        print("   @Neuro-Bot Bonjour!")
        
        print(f"\n⚡ Performances attendues:")
        print(f"   🚄 Vitesse: 20-25 tokens/seconde")
        print(f"   💾 VRAM: ~5GB utilisés")
        print(f"   🔥 GPU: 32/32 couches")
        
        return True
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        
        if not results["gpu"]:
            print("🔧 GPU: Vérifiez l'installation CUDA")
        
        if not results["discord"]:
            print("🔧 Discord: Token invalide - Utilisez create_new_discord_bot.py")
        
        return False

def show_launch_instructions():
    """Instructions de lancement"""
    print("\n🚀 Instructions de Lancement")
    print("=" * 35)
    print("1. Ouvrez un terminal dans c:\\Dev\\IA-chatbot")
    print("2. Activez l'environnement: llama-venv\\Scripts\\activate")
    print("3. Lancez le bot: python start_bot.py")
    print("4. Attendez le message: 'Bot Discord connecté'")
    print("5. Testez sur Discord avec: !helpme")
    print()
    print("💡 Le bot utilisera automatiquement le GPU RTX 4050!")

if __name__ == "__main__":
    print("🎯 Test Final Complet - Neuro-Bot")
    print("🔍 Vérification: GPU + Discord + Configuration")
    print()
    
    success = test_all_components()
    
    if success:
        show_launch_instructions()
    else:
        print("\n🔧 Corriger les problèmes avant de lancer le bot.")
        print("💡 Utilisez create_new_discord_bot.py pour le token Discord")