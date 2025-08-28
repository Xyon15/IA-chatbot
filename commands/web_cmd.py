from auth_decorators import require_authorized_role
from config import config, logger
from web import save_web_state, duckduckgo_search

def setup(bot):
    @bot.command(name="web")
    @require_authorized_role
    async def web_toggle(ctx, state: str = None):
        """Active ou désactive la recherche web"""
        if state is None:
            current_state = "activée" if getattr(bot, 'web_enabled', False) else "désactivée"
            await ctx.send(f"🌐 Recherche web actuellement **{current_state}**.\nUtilise `!web on` ou `!web off` pour changer.")
            logger.debug(f"État web consulté par {ctx.author.id}: {current_state}")
            return

        try:
            if state.lower() == "on":
                bot.web_enabled = True
                save_web_state(True)
                await ctx.send("✅ Recherche web **activée**.")
                logger.info(f"Recherche web activée par {ctx.author.id}")
            elif state.lower() == "off":
                bot.web_enabled = False
                save_web_state(False)
                await ctx.send("❌ Recherche web **désactivée**.")
                logger.info(f"Recherche web désactivée par {ctx.author.id}")
            else:
                await ctx.send("❓ Utilise `!web on` ou `!web off`.")
        except Exception as e:
            await ctx.send("❌ Erreur lors de la modification de la recherche web.")
            logger.error(f"Erreur web par {ctx.author.id}: {e}")
    
    @bot.command(name="webtest")
    @require_authorized_role
    async def web_test(ctx, *, query: str = None):
        """Teste une recherche web manuellement"""
        if query is None:
            await ctx.send("❓ Utilise `!webtest <texte>` pour tester une recherche.")
            return
        
        try:
            await ctx.send(f"🔍 Recherche en cours pour : **{query}**...")
            
            # Effectuer la recherche
            results = await duckduckgo_search(query)
            
            if results:
                response = f"🌐 **Résultats pour '{query}' :**\n\n{results[:1500]}..."
                if len(results) > 1500:
                    response += "\n\n*(Résultats tronqués)*"
            else:
                response = f"❌ Aucun résultat trouvé pour : **{query}**"
            
            await ctx.send(response)
            logger.info(f"Test recherche web par {ctx.author.id}: {query}")
            
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de la recherche web : {e}")
            logger.error(f"Erreur webtest par {ctx.author.id}: {e}")