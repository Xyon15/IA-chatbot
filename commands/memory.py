from memory import save_fact, get_facts, clear_all_memory, clear_facts, clear_memory
from auth_decorators import require_role_and_2fa, require_authorized_role
from config import config, logger

def setup(bot):
    @bot.command()
    @require_role_and_2fa()
    async def reset(ctx, target: str = None):
        """Réinitialise la mémoire conversationnelle"""
        if target is None:
            await ctx.send("📋 Utilisation : `!reset @utilisateur` ou `!reset all`")
            return

        try:
            if target.lower() == "all":
                deleted_count = clear_all_memory()
                await ctx.send(f"🧠 Toute la mémoire a été supprimée ({deleted_count} entrées).")
                logger.info(f"Mémoire complète réinitialisée par {ctx.author.id}")
            elif ctx.message.mentions:
                user_id = str(ctx.message.mentions[0].id)
                deleted_count = clear_memory(user_id)
                await ctx.send(f"🧠 Mémoire de <@{user_id}> supprimée ({deleted_count} entrées).")
                logger.info(f"Mémoire de {user_id} réinitialisée par {ctx.author.id}")
            else:
                await ctx.send("❌ Veuillez mentionner un utilisateur valide ou utiliser `!reset all`.")
        except Exception as e:
            await ctx.send("❌ Erreur lors de la réinitialisation de la mémoire.")
            logger.error(f"Erreur reset par {ctx.author.id}: {e}")

    @bot.command(name="remember")
    @require_authorized_role
    async def remember_fact(ctx, *, fact: str):
        """Mémorise un fait sur l'utilisateur"""
        try:
            user_id = str(ctx.author.id)
            save_fact(user_id, fact)
            await ctx.send("🧠 Noté ! Je m'en souviendrai.")
            logger.info(f"Fait mémorisé par {ctx.author.id}: {fact[:50]}...")
        except Exception as e:
            await ctx.send("❌ Erreur lors de la sauvegarde du fait.")
            logger.error(f"Erreur remember par {ctx.author.id}: {e}")

    @bot.command(name="facts")
    @require_authorized_role
    async def facts(ctx, member=None):
        """Affiche les faits mémorisés sur un utilisateur"""
        try:
            target = member or ctx.author
            user_id = str(target.id)
            facts_list = get_facts(user_id)
            
            if not facts_list:
                await ctx.send(f"😶 Je n'ai encore rien noté sur {target.display_name}.")
                return
                
            facts_str = "\n".join([f"📝 {fact}" for fact in facts_list])
            message = f"🧾 **Faits mémorisés pour {target.display_name} :**\n```\n{facts_str}\n```"
            await ctx.send(message)
            logger.info(f"Faits consultés pour {user_id} par {ctx.author.id}")
        except Exception as e:
            await ctx.send("❌ Erreur lors de la récupération des faits.")
            logger.error(f"Erreur facts par {ctx.author.id}: {e}")

    @bot.command()
    @require_role_and_2fa()
    async def forget(ctx, *, target: str = None):
        """Efface les faits mémorisés"""
        if not target:
            await ctx.send(
                "🧹 **Utilisation de `!forget` :**\n"
                "- `!forget me` → Efface ta propre mémoire\n"
                "- `!forget @utilisateur` → Efface la mémoire d'un utilisateur\n"
                "- `!forget all` → Efface toute la mémoire"
            )
            return

        try:
            if target.lower() == "all":
                deleted_count = clear_facts()
                await ctx.send(f"💥 Toute la mémoire a été effacée ({deleted_count} faits supprimés).")
                logger.warning(f"Tous les faits effacés par {ctx.author.id}")

            elif target.lower() == "me":
                user_id = str(ctx.author.id)
                deleted_count = clear_facts(user_id)
                if deleted_count:
                    await ctx.send(f"🧠 J'ai tout oublié à ton sujet ({deleted_count} faits supprimés).")
                else:
                    await ctx.send("😶 Il n'y avait rien à oublier sur toi.")
                logger.info(f"Faits personnels effacés par {ctx.author.id}")

            elif ctx.message.mentions:
                member = ctx.message.mentions[0]
                user_id = str(member.id)
                deleted_count = clear_facts(user_id)
                if deleted_count:
                    await ctx.send(f"🧹 Mémoire de {member.display_name} effacée ({deleted_count} faits supprimés).")
                else:
                    await ctx.send(f"ℹ️ Je n'avais rien mémorisé pour {member.display_name}.")
                logger.info(f"Faits de {user_id} effacés par {ctx.author.id}")
            else:
                await ctx.send("❌ Utilisation incorrecte. Mentionne un utilisateur ou utilise `me` ou `all`.")

        except Exception as e:
            await ctx.send("❌ Erreur lors de l'effacement des faits.")
            logger.error(f"Erreur forget par {ctx.author.id}: {e}")