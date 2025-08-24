from config import logger

def setup(bot):
    @bot.command(name="helpme")
    async def help_command(ctx):
        """Affiche l'aide des commandes disponibles"""
        try:
            help_text = """
🤖 **Commandes Neuro-Bot** 🤖

**📋 Commandes générales :**
• `!helpme` → Affiche cette aide
• `!stats` → Statistiques système et GPU

**🧠 Gestion de la mémoire :**
• `!context <1-50>` → Définit le nombre d'échanges mémorisés
• `!remember <texte>` → Mémorise un fait personnel
• `!facts [@user]` → Affiche les faits mémorisés
• `!forget me/@user/all` → Efface les faits (🔒 2FA requis)
• `!reset @user/all` → Réinitialise la mémoire conversationnelle (🔒 2FA requis)

**🌐 Recherche web :**
• `!web on/off` → Active/désactive la recherche web

**⚙️ Configuration :**
• `!auto on/off` → Active/désactive les réponses automatiques
• `!limits [valeur]` → Définit la longueur max des réponses

**🔒 Commandes administrateur :**
• `!bye` → Arrêt sécurisé du bot (🔒 2FA requis)

*Les commandes marquées 🔒 nécessitent le rôle autorisé et une authentification 2FA.*
            """
            await ctx.send(help_text)
            logger.info(f"Aide consultée par {ctx.author.id}")
        except Exception as e:
            await ctx.send("❌ Erreur lors de l'affichage de l'aide.")
            logger.error(f"Erreur help par {ctx.author.id}: {e}")