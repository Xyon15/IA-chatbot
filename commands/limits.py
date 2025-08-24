from auth_decorators import require_authorized_role
from config import config, logger
import json

def setup(bot):
    @bot.command()
    @require_authorized_role
    async def limits(ctx, length: int = None):
        """Définit ou affiche la limite de longueur des réponses"""
        if length is None:
            try:
                with open(config.LIMITS_FILE, "r", encoding="utf-8") as f:
                    limits_config = json.load(f)
                    current_limit = limits_config.get("max_reply_length", 1900)
                await ctx.send(f"📏 Limite actuelle : **{current_limit}** caractères.\nUtilise `!limits <valeur>` pour changer.")
                logger.debug(f"Limites consultées par {ctx.author.id}: {current_limit}")
            except Exception as e:
                await ctx.send("❌ Erreur lors de la lecture de la configuration.")
                logger.error(f"Erreur lecture limits par {ctx.author.id}: {e}")
            return

        if not (100 <= length <= 2000):
            await ctx.send("❌ La limite doit être entre 100 et 2000 caractères.")
            return

        try:
            with open(config.LIMITS_FILE, "w", encoding="utf-8") as f:
                json.dump({"max_reply_length": length}, f, indent=2, ensure_ascii=False)
            
            await ctx.send(f"✅ Limite de réponse définie à **{length}** caractères.")
            logger.info(f"Limite de réponse modifiée à {length} par {ctx.author.id}")
            
        except Exception as e:
            await ctx.send("❌ Erreur lors de la sauvegarde de la configuration.")
            logger.error(f"Erreur limits par {ctx.author.id}: {e}")