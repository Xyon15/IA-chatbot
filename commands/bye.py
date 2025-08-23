from discord.ext.commands import has_role, CheckFailure
from config import AUTHORIZED_ROLE

def setup(bot):
    @bot.command()
    @has_role(AUTHORIZED_ROLE)
    async def bye(ctx):
        await ctx.send("👋 Au revoir ! Neuro se déconnecte...")
        await bot.close()

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("🚫 Tu n'as pas l'autorisation d'utiliser cette commande.")