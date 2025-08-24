"""
Décorateurs d'authentification pour les commandes Discord
"""
import asyncio
import pyotp
from functools import wraps
from discord.ext.commands import has_role
from config import config, logger


def require_2fa(func):
    """Décorateur pour exiger une authentification 2FA avant l'exécution d'une commande"""
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        try:
            # Demander le code 2FA
            await ctx.send("🔒 Envoie-moi ton code d'authentification 2FA pour confirmer l'opération (valide 30s).")
            
            # Marquer l'utilisateur comme en attente de 2FA
            if not hasattr(ctx.bot, 'waiting_for_2fa'):
                ctx.bot.waiting_for_2fa = {}
            ctx.bot.waiting_for_2fa[ctx.author.id] = True

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                # Attendre le message avec le code 2FA
                msg = await ctx.bot.wait_for("message", check=check, timeout=30)
                user_code = msg.content.strip()

                # Vérifier le code 2FA
                totp = pyotp.TOTP(config.AUTH_SECRET)
                if not totp.verify(user_code):
                    await ctx.send("❌ Code 2FA invalide. Opération annulée.")
                    logger.warning(f"Code 2FA invalide pour {ctx.author.id}")
                    return

                logger.info(f"Authentification 2FA réussie pour {ctx.author.id}")
                # Exécuter la fonction originale si l'authentification réussit
                return await func(ctx, *args, **kwargs)

            except asyncio.TimeoutError:
                await ctx.send("⏱️ Temps écoulé. Veuillez réessayer.")
                logger.warning(f"Timeout 2FA pour {ctx.author.id}")
                return

        except Exception as e:
            await ctx.send("❌ Erreur lors de l'authentification. Veuillez réessayer.")
            logger.error(f"Erreur 2FA pour {ctx.author.id}: {e}")
            return
        finally:
            # Nettoyer l'état d'attente 2FA
            if hasattr(ctx.bot, 'waiting_for_2fa'):
                ctx.bot.waiting_for_2fa[ctx.author.id] = False

    return wrapper


def require_role_and_2fa(role_name: str = None):
    """Décorateur combiné pour exiger un rôle ET une authentification 2FA"""
    def decorator(func):
        @has_role(role_name or config.AUTHORIZED_ROLE)
        @require_2fa
        @wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            return await func(ctx, *args, **kwargs)
        return wrapper
    return decorator


def require_authorized_role(func):
    """Décorateur pour exiger le rôle autorisé configuré"""
    @has_role(config.AUTHORIZED_ROLE)
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        logger.debug(f"Commande autorisée exécutée par {ctx.author.id}: {func.__name__}")
        return await func(ctx, *args, **kwargs)
    return wrapper