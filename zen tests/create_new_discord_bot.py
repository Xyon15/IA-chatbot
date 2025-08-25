#!/usr/bin/env python3
"""
Guide interactif pour créer un nouveau bot Discord
"""

import webbrowser
import time

def create_new_discord_bot():
    """Guide pas à pas pour créer un nouveau bot Discord"""
    print("🤖 Création d'un Nouveau Bot Discord")
    print("=" * 40)
    
    print("🚀 Ce script va vous guider étape par étape!")
    print()
    
    # Étape 1: Ouvrir le portail développeur
    print("📝 ÉTAPE 1: Accès au Portail Développeur")
    print("Je vais ouvrir le portail Discord Developer...")
    
    if input("Appuyez sur Entrée pour continuer..."):
        pass
    
    webbrowser.open("https://discord.com/developers/applications")
    print("✅ Portail ouvert dans votre navigateur")
    
    print("\n📋 ÉTAPE 2: Création de l'Application")
    print("Dans le navigateur:")
    print("1. Cliquez sur 'New Application' (en haut à droite)")
    print("2. Nom suggéré: 'Neuro-Bot' ou 'Mon-ChatBot'")
    print("3. Acceptez les conditions et cliquez 'Create'")
    
    input("\n✅ Appuyez sur Entrée une fois l'application créée...")
    
    print("\n🤖 ÉTAPE 3: Configuration du Bot")
    print("1. Cliquez sur l'onglet 'Bot' (dans le menu de gauche)")
    print("2. Cliquez sur 'Reset Token' (ou 'Add Bot' si c'est la première fois)")
    print("3. Confirmez en cliquant 'Yes, do it!'")
    print("4. ⚠️ IMPORTANT: Copiez immédiatement le token affiché!")
    print("   (Il ne sera plus visible après avoir quitté la page)")
    
    input("\n✅ Appuyez sur Entrée une fois le token copié...")
    
    print("\n🎯 ÉTAPE 4: Permissions du Bot")
    print("1. Toujours sur la page 'Bot', descendez jusqu'à 'Bot Permissions'")
    print("2. Activez ces permissions:")
    print("   ☑️ Send Messages")
    print("   ☑️ Send Messages in Threads") 
    print("   ☑️ Read Message History")
    print("   ☑️ Use Slash Commands")
    print("   ☑️ Add Reactions")
    
    input("\n✅ Appuyez sur Entrée une fois les permissions configurées...")
    
    print("\n🔗 ÉTAPE 5: Invitation du Bot")
    print("1. Cliquez sur l'onglet 'OAuth2' > 'URL Generator'")
    print("2. Dans 'Scopes', cochez: 'bot'")
    print("3. Dans 'Bot Permissions', les permissions s'affichent automatiquement")
    print("4. Copiez l'URL générée en bas")
    print("5. Collez l'URL dans un nouvel onglet pour inviter le bot sur votre serveur")
    
    input("\n✅ Appuyez sur Entrée une fois le bot invité sur votre serveur...")
    
    # Configuration du token
    print("\n⚙️ ÉTAPE 6: Configuration du Token")
    new_token = input("🔑 Collez votre nouveau token ici: ").strip()
    
    if not new_token:
        print("❌ Token vide! Relancez le script et collez le token.")
        return False
    
    if len(new_token) < 50:
        print("⚠️ Token semble trop court. Vérifiez que vous avez copié le token complet.")
        if input("Continuer quand même? (y/n): ").lower() != 'y':
            return False
    
    # Sauvegarder le token
    try:
        env_path = "../.env"
        
        # Lire le fichier actuel
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer le token
        lines = content.split('\n')
        updated_lines = []
        token_updated = False
        
        for line in lines:
            if line.startswith('DISCORD_TOKEN='):
                updated_lines.append(f'DISCORD_TOKEN={new_token}')
                token_updated = True
                print(f"🔄 Token mis à jour dans .env")
            else:
                updated_lines.append(line)
        
        if not token_updated:
            updated_lines.insert(0, f'DISCORD_TOKEN={new_token}')
            print(f"➕ Token ajouté à .env")
        
        # Sauvegarder
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        
        print("✅ Fichier .env mis à jour avec succès!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        print(f"💡 Modifiez manuellement le fichier .env avec:")
        print(f"DISCORD_TOKEN={new_token}")
        return False

def create_discord_role_guide():
    """Guide pour créer le rôle NeuroMaster"""
    print("\n🏷️ ÉTAPE 7: Création du Rôle 'NeuroMaster'")
    print("=" * 45)
    print("Sur votre serveur Discord:")
    print("1. Clic droit sur le nom du serveur > 'Paramètres du serveur'")
    print("2. Cliquez sur 'Rôles' dans le menu de gauche")
    print("3. Cliquez sur 'Créer un rôle'")
    print("4. Nom du rôle: 'NeuroMaster'")
    print("5. Couleur: Au choix (ex: Bleu ou Vert)")
    print("6. Cliquez 'Sauvegarder les modifications'")
    print("7. Assignez-vous ce rôle (Clic droit sur votre nom > Rôles)")
    print()
    print("💡 Seuls les utilisateurs avec le rôle 'NeuroMaster' peuvent utiliser le bot!")

def final_test():
    """Guide pour le test final"""
    print("\n🧪 ÉTAPE 8: Test Final")
    print("=" * 25)
    print("1. Ouvrez un terminal dans c:\\Dev\\IA-chatbot")
    print("2. Lancez: python start_bot.py")
    print("3. Si tout va bien, vous verrez:")
    print("   ✅ GPU RTX 4050 détecté")
    print("   ✅ Modèle LLM chargé")
    print("   ✅ Bot Discord connecté")
    print()
    print("4. Testez sur Discord:")
    print("   - !helpme")
    print("   - @Neuro-Bot Bonjour!")
    print()
    print("🎉 Si ça marche, félicitations! Votre bot IA est opérationnel!")

if __name__ == "__main__":
    print("🎬 Bienvenue dans l'Assistant de Création de Bot Discord!")
    print("🎯 Objectif: Créer un token Discord valide pour Neuro-Bot")
    print()
    
    if input("🚀 Commencer la création du bot? (y/n): ").lower() == 'y':
        success = create_new_discord_bot()
        
        if success:
            create_discord_role_guide()
            final_test()
            print("\n🎊 Configuration terminée!")
            print("🚀 Lancez maintenant: python start_bot.py")
        else:
            print("\n❌ Configuration échouée. Réessayez ou configurez manuellement.")
    else:
        print("👋 Au revoir! Lancez le script quand vous serez prêt.")