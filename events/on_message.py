from model import generate_reply
from utils import shorten_response
from memory import get_history

def setup(bot):
    @bot.event
    async def on_message(message):
        # ignorer messages du bot
        if message.author == bot.user:
            return

        # initialisation safe
        if not hasattr(bot, "waiting_for_2fa"):
            bot.waiting_for_2fa = {}

        # Empêcher les réponses pendant la 2FA
        if bot.waiting_for_2fa.get(message.author.id, False):
            return

        is_command = message.content.startswith("!")
        is_mentioned = bot.user.mentioned_in(message)

        # Permettre les réponses automatiques si activées
        if is_mentioned or (getattr(bot, "auto_reply_enabled", False) and not is_command):
            prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
            user_id = str(message.author.id)
            await message.channel.typing()
            history = get_history(user_id, limit=bot.current_context_limit)
            reply = await generate_reply(user_id, prompt, context_limit=bot.current_context_limit)
            reply = shorten_response(reply)
            try:
                await message.reply(reply)
            except Exception as e:
                print(f"[ERR] failed to reply: {e}")
                try:
                    await message.author.send(reply)
                except Exception:
                    pass

        await bot.process_commands(message)