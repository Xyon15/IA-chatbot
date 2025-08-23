from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE, CONFIG_PATH
import json

def setup(bot):
    @bot.command()
    @has_role(AUTHORIZED_ROLE)
    async def context(ctx, count: int = None):
        try:
            if count is None:
                await ctx.send(f"🔍 Neuro utilise actuellement **{bot.current_context_limit}** derniers échanges en mémoire.")
                return

            if count < 1 or count > 50:
                await ctx.send("❌ Le nombre de messages doit être entre 1 et 50.")
                return

            bot.current_context_limit = count
            # Mets à jour le fichier JSON
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            config["context_limit"] = count
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            await ctx.send(f"✅ Contexte mis à jour : Neuro utilisera désormais les **{count}** derniers échanges.")
        except Exception as e:
            await ctx.send(f"❌ Une erreur est survenue lors de la mise à jour du contexte : `{e}`")