from auth_decorators import require_role_and_2fa
from config import config, logger
from discord.ext.commands import CheckFailure

def setup(bot):
    @bot.command()
    @require_role_and_2fa()
    async def bye(ctx):
        """Arrête le bot de manière sécurisée"""
        try:
            await ctx.send("👋 Au revoir ! Neuro se déconnecte...")
            logger.info(f"Arrêt du bot demandé par {ctx.author.id}")
            await bot.close()
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt du bot: {e}")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("🚫 Tu n'as pas l'autorisation d'utiliser cette commande.")
            logger.warning(f"Tentative d'accès non autorisé par {ctx.author.id} à la commande {ctx.command}")