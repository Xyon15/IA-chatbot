from auth_decorators import require_authorized_role
from config import config, logger
import json

def setup(bot):
    @bot.command()
    @require_authorized_role
    async def auto(ctx, mode: str = None):
        """Active ou désactive les réponses automatiques"""
        if mode == "on":
            bot.auto_reply_enabled = True
            try:
                with open(config.AUTO_REPLY_PATH, "w", encoding="utf-8") as f:
                    json.dump({"enabled": True}, f, indent=2, ensure_ascii=False)
                await ctx.send("✅ Réponses automatiques activées.")
                logger.info(f"Auto-reply activé par {ctx.author.id}")
            except Exception as e:
                await ctx.send(f"❌ Impossible d'enregistrer la configuration : {e}")
                logger.error(f"Erreur auto on par {ctx.author.id}: {e}")

        elif mode == "off":
            bot.auto_reply_enabled = False
            try:
                with open(config.AUTO_REPLY_PATH, "w", encoding="utf-8") as f:
                    json.dump({"enabled": False}, f, indent=2, ensure_ascii=False)
                await ctx.send("🚫 Réponses automatiques désactivées.")
                logger.info(f"Auto-reply désactivé par {ctx.author.id}")
            except Exception as e:
                await ctx.send(f"❌ Impossible d'enregistrer la configuration : {e}")
                logger.error(f"Erreur auto off par {ctx.author.id}: {e}")

        else:
            status = "activées" if getattr(bot, "auto_reply_enabled", False) else "désactivées"
            await ctx.send(f"ℹ️ Réponses automatiques actuellement **{status}**.\nUtilise `!auto on` ou `!auto off`.")
            logger.debug(f"Statut auto-reply consulté par {ctx.author.id}: {status}")