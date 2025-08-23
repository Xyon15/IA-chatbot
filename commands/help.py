from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE

def setup(bot):
    @bot.command(name="helpme")
    @has_role(AUTHORIZED_ROLE)
    async def helpme(ctx):
        help_text = (
            "```\n"
            "📚 COMMANDES DE NEURO\n"
            "────────────────────────────\n"
            "💬 Parle à Neuro simplement en la mentionnant ou en envoyant un message sans préfixe (!).\n"
            "\n"
            "🔧 Commandes disponibles :\n"
            "🧠 !reset        → Réinitialise la mémoire\n"
            "📊 !stats        → Affiche les stats système et mémoire de Neuro\n"
            "🛠️ !auto on/off  → Active ou désactive les réponses automatiques\n"
            "🔢 !context <1-50>  → Choisis le nombre de d'échanges que neuro se souvient activement\n"
            "🌐 !web on/off         → Active ou désactive l’accès web (DuckDuckGo)\n"
            "🧪 !web test <texte>   → Teste une recherche web manuellement\n"
            "🧾 !remember [texte]   → Ajoute un fait à la mémoire à long terme de Neuro\n"
            "🔍 !facts [@user]      → Affiche les faits connus (soi-même ou un autre utilisateur)\n"
            "🧹 !forget me/@user/all → Oublie les faits \n"
            "📏 !limits [valeur]     → Définit ou affiche la longueur maximale des réponses\n"
            "♻️ !resetlimits         → Restaure la limite par défaut (1900 caractères)\n"
            "👋 !bye               → Arrête proprement le bot\n"
            "❓ !helpme         → Affiche ce message d’aide\n"
            "\n"
            "⚠️ Seuls les utilisateurs avec le rôle « NeuroMaster » peuvent utiliser ces commandes.\n"
            "```"
        )
        await ctx.send(help_text)