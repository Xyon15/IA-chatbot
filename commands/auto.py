from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE, AUTO_REPLY_PATH
import json

def setup(bot):
    @bot.command()
    @has_role(AUTHORIZED_ROLE)
    async def auto(ctx, mode: str = None):
        if mode == "on":
            bot.auto_reply_enabled = True
            try:
                with open(AUTO_REPLY_PATH, "w", encoding="utf-8") as f:
                    json.dump({"enabled": True}, f, indent=2, ensure_ascii=False)
                await ctx.send("✅ Réponses automatiques activées.")
            except Exception as e:
                await ctx.send(f"❌ Impossible d'enregistrer la configuration : {e}")

        elif mode == "off":
            bot.auto_reply_enabled = False
            try:
                with open(AUTO_REPLY_PATH, "w", encoding="utf-8") as f:
                    json.dump({"enabled": False}, f, indent=2, ensure_ascii=False)
                await ctx.send("🚫 Réponses automatiques désactivées.")
            except Exception as e:
                await ctx.send(f"❌ Impossible d'enregistrer la configuration : {e}")

        else:
            status = "activées" if getattr(bot, "auto_reply_enabled", False) else "désactivées"
            await ctx.send(f"ℹ️ Réponses automatiques actuellement **{status}**.\nUtilise `!auto on` ou `!auto off`.")