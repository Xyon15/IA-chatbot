from config import logger

def setup(bot):
    @bot.command(name="helpme")
    async def help_command(ctx):
        """Affiche l'aide des commandes disponibles"""
        try:
            help_text = """
```
📚 COMMANDES DE NEURO
────────────────────────────

💬 Parle à Neuro simplement en la mentionnant ou en envoyant un message sans préfixe (!).

🔧 Commandes disponibles :

📊 !stats → Affiche les stats système et mémoire de Neuro
🧠 !reset → Réinitialise la mémoire
🛠️ !auto on/off → Active ou désactive les réponses automatiques
🔢 !context <1-50> → Choisis le nombre d'échanges que neuro se souvient activement
🌐 !web on/off → Active ou désactive l'accès web (DuckDuckGo)
🧪 !webtest <texte> → Teste une recherche web manuellement
🧾 !remember [texte] → Ajoute un fait à la mémoire à long terme de Neuro
🔍 !facts [@user] → Affiche les faits connus (soi-même ou un autre utilisateur)
🧹 !forget me/@user/all → Oublie les faits
📏 !limits [valeur] → Définit ou affiche la longueur maximale des réponses
♻️ !resetlimits → Restaure la limite par défaut (1900 caractères)
🔧 !optimize → Gestion automatique de la configuration LLM
   • !optimize analyze → Analyser l'utilisation VRAM
   • !optimize apply → Appliquer l'optimisation recommandée
   • !optimize profiles → Afficher les profils disponibles
   • !optimize current → Afficher le profil actuel
   • !optimize set <profil> → Changer de profil
👋 !bye → Arrête proprement le bot
❓ !helpme → Affiche ce message d'aide

⚠️ Seuls les utilisateurs avec le rôle « NeuroMaster » peuvent utiliser ces commandes.
🔒 Certaines commandes nécessitent une authentification 2FA supplémentaire.
```
            """
            await ctx.send(help_text)
            logger.info(f"Aide consultée par {ctx.author.id}")
        except Exception as e:
            await ctx.send("❌ Erreur lors de l'affichage de l'aide.")
            logger.error(f"Erreur help par {ctx.author.id}: {e}")