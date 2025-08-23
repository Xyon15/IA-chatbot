from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE, LIMITS_FILE
import json

def setup(bot):
    @bot.command(name="limits")
    @has_role(AUTHORIZED_ROLE)
    async def limits(ctx, length: int = None):
        path = LIMITS_FILE

        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {"max_reply_length": 1900}

        if length is None:
            await ctx.send(f"📏 Limite actuelle des réponses : `{config.get('max_reply_length', 1900)}` caractères.")
            return

        if length < 100 or length > 2000:
            await ctx.send("❌ La limite doit être comprise entre 100 et 2000 caractères.")
            return

        config["max_reply_length"] = length
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

        await ctx.send(
            f"✅ Nouvelle limite de réponse enregistrée : `{length}` caractères.\n"
            f"🔧 Utilise `!resetlimits` pour revenir à la valeur par défaut."
        )

    @bot.command(name="resetlimits")
    @has_role(AUTHORIZED_ROLE)
    async def resetlimits(ctx):
        path = LIMITS_FILE
        default_limit = 1900

        config = {"max_reply_length": default_limit}
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            await ctx.send(f"🔄 Limite réinitialisée à `{default_limit}` caractères.")
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de la réinitialisation : {e}")