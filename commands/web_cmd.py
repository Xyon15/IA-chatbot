from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE
from web import duckduckgo_search, save_web_state
from utils import count_tokens, truncate_text_to_tokens, shorten_response

def setup(bot):
    @bot.command(name="web")
    @has_role(AUTHORIZED_ROLE)
    async def web(ctx, state: str = None, *, arg: str = None):
        if state is None:
            status = "activé ✅" if bot.web_enabled else "désactivé ❌"
            await ctx.send(f"🌐 L’accès web est actuellement **{status}**.\nUtilisation : `!web on/off/test <terme>`")
            return

        if state.lower() == "on":
            save_web_state(True)
            bot.web_enabled = True
            await ctx.send("🌐 L’accès web est maintenant **activé**.")
            return

        elif state.lower() == "off":
            save_web_state(False)
            bot.web_enabled = False
            await ctx.send("🌐 L’accès web est maintenant **désactivé**.")
            return

        elif state.lower() == "test":
            if not arg:
                await ctx.send("🔎 Utilisation : `!web test <terme>`")
                return

            web_result = await duckduckgo_search(arg)

            if web_result.startswith("❌") or web_result.startswith("😶"):
                await ctx.send(web_result)
                return

            intro = f"{arg}\n\nVoici ce que tu sais à propos du sujet (sans mentionner que c'est une recherche) :\n"
            outro = (
                "\nUtilise ce que tu viens d’apprendre pour répondre naturellement et en français, "
                "comme si tu le savais toi-même. Ne donne aucun lien ni source. Résume avec tes propres mots.\n"
            )

            max_total = 2048
            reserved_for_response = 400
            available_for_prompt = max_total - reserved_for_response
            intro_outro_tokens = count_tokens(intro + outro)
            remaining_tokens = max(0, available_for_prompt - intro_outro_tokens)
            truncated_result = truncate_text_to_tokens(web_result, remaining_tokens)
            prompt = intro + truncated_result + outro
            prompt_tokens = count_tokens(prompt)
            if prompt_tokens + reserved_for_response > max_total:
                await ctx.send(f"❌ Erreur : le prompt généré ({prompt_tokens}) dépasse la limite autorisée.")
                return

            user_id = str(ctx.author.id)
            from model import generate_reply
            reply = await generate_reply(user_id, prompt)
            await ctx.send(shorten_response(reply))
            return

        else:
            await ctx.send("❌ Option inconnue. Utilisation : `!web on/off/test <terme>`")