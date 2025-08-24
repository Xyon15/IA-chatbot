from model import generate_reply
from utils import shorten_response
from memory import get_history
from web import duckduckgo_search
from config import logger
import re

def setup(bot):
    @bot.event
    async def on_message(message):
        """Gestionnaire principal des messages"""
        # Ignorer messages du bot
        if message.author == bot.user:
            return

        # Initialisation safe
        if not hasattr(bot, "waiting_for_2fa"):
            bot.waiting_for_2fa = {}

        # Empêcher les réponses pendant la 2FA
        if bot.waiting_for_2fa.get(message.author.id, False):
            return

        is_command = message.content.startswith("!")
        is_mentioned = bot.user.mentioned_in(message)

        # Permettre les réponses automatiques si activées
        if is_mentioned or (getattr(bot, "auto_reply_enabled", False) and not is_command):
            try:
                prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
                user_id = str(message.author.id)
                
                logger.debug(f"Traitement message de {user_id}: {prompt[:50]}...")
                
                await message.channel.typing()
                
                # Recherche web si activée et détectée
                web_info = ""
                if getattr(bot, 'web_enabled', False) and _should_search_web(prompt):
                    logger.info(f"Recherche web déclenchée pour: {prompt[:30]}...")
                    web_info = await duckduckgo_search(prompt)
                    if web_info and not web_info.startswith("❌"):
                        prompt += f"\n\nInformation trouvée : {web_info}"
                
                reply = await generate_reply(user_id, prompt, context_limit=bot.current_context_limit)
                reply = shorten_response(reply)
                
                await message.reply(reply)
                logger.info(f"Réponse envoyée à {user_id}")
                
            except Exception as e:
                logger.error(f"Erreur traitement message de {message.author.id}: {e}")
                try:
                    await message.reply("❌ Désolé, j'ai rencontré une erreur.")
                except Exception:
                    logger.error("Impossible d'envoyer le message d'erreur")

        await bot.process_commands(message)

def _should_search_web(prompt: str) -> bool:
    """Détermine si une recherche web est nécessaire"""
    web_keywords = [
        r'\b(?:quest-ce que|que sais-tu|dis-moi|explique|parle-moi de)\b',
        r'\b(?:actualité|news|nouveau|récent|dernière|info)\b',
        r'\b(?:météo|temps|température)\b',
        r'\b(?:prix|coût|combien)\b',
        r'\b(?:définition|cest quoi|signifie)\b'
    ]
    
    prompt_lower = prompt.lower()
    return any(re.search(pattern, prompt_lower) for pattern in web_keywords)