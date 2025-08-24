from auth_decorators import require_authorized_role
from config import config, logger
import json

def setup(bot):
    @bot.command()
    @require_authorized_role
    async def context(ctx, limit: int = None):
        """Définit ou affiche la limite du contexte conversationnel"""
        if limit is None:
            current_limit = getattr(bot, 'current_context_limit', 10)
            await ctx.send(f"🧠 Contexte actuel : **{current_limit}** échanges mémorisés.\nUtilise `!context <1-50>` pour changer.")
            logger.debug(f"Contexte consulté par {ctx.author.id}: {current_limit}")
            return

        if not (1 <= limit <= 50):
            await ctx.send("❌ La limite doit être entre 1 et 50.")
            return

        try:
            # Mise à jour en mémoire
            bot.current_context_limit = limit
            
            # Sauvegarde dans le fichier
            with open(config.CONFIG_PATH, "r", encoding="utf-8") as f:
                bot_config = json.load(f)
            
            bot_config["context_limit"] = limit
            
            with open(config.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(bot_config, f, indent=2, ensure_ascii=False)
            
            await ctx.send(f"✅ Contexte défini à **{limit}** échanges.")
            logger.info(f"Contexte modifié à {limit} par {ctx.author.id}")
            
        except Exception as e:
            await ctx.send("❌ Erreur lors de la sauvegarde de la configuration.")
            logger.error(f"Erreur context par {ctx.author.id}: {e}")