from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE, AUTH_SECRET
from memory import save_fact, get_facts
import pyotp
import sqlite3
import asyncio

def setup(bot):
    @bot.command()
    @has_role(AUTHORIZED_ROLE)
    async def reset(ctx, target: str = None):
        if target is None:
            await ctx.send(" Utilisation : `!reset @utilisateur` ou `!reset all`")
            return

        await ctx.send("🔒 Envoie-moi ton code d’authentification 2FA pour confirmer l’opération (valide 30s).")
        bot.waiting_for_2fa[ctx.author.id] = True

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            user_code = msg.content.strip()

            totp = pyotp.TOTP(AUTH_SECRET)
            if not totp.verify(user_code):
                await ctx.send("❌ Code 2FA invalide. Opération annulée.")
                return

            conn = sqlite3.connect(bot.DB_PATH)
            cursor = conn.cursor()

            if target.lower() == "all":
                cursor.execute("DELETE FROM memory")
                conn.commit()
                conn.close()
                await ctx.send("🧠 Toute la mémoire a été supprimée.")
            elif ctx.message.mentions:
                user_id = str(ctx.message.mentions[0].id)
                cursor.execute("DELETE FROM memory WHERE user_id = ?", (user_id,))
                conn.commit()
                conn.close()
                await ctx.send(f"🧠 Mémoire de <@{user_id}> supprimée.")
            else:
                await ctx.send("❌ Veuillez mentionner un utilisateur valide ou utiliser `!reset all`.")

        except asyncio.TimeoutError:
            await ctx.send("⏱️ Temps écoulé. Veuillez réessayer.")
        finally:
            bot.waiting_for_2fa[ctx.author.id] = False

    @bot.command(name="remember")
    @has_role(AUTHORIZED_ROLE)
    async def remember_fact(ctx, *, fact: str):
        user_id = str(ctx.author.id)
        save_fact(user_id, fact)
        await ctx.send("🧠 Noté ! Je m’en souviendrai.")

    @bot.command(name="facts")
    @has_role(AUTHORIZED_ROLE)
    async def facts(ctx, member=None):
        target = member or ctx.author
        user_id = str(target.id)
        facts_list = get_facts(user_id)
        if not facts_list:
            await ctx.send(f"😶 Je n’ai encore rien noté sur {target.display_name}.")
            return
        facts_str = "\n".join([f"📝 {fact}" for fact in facts_list])
        message = f"🧾 **Faits mémorisés pour {target.display_name} :**\n```\n{facts_str}\n```"
        await ctx.send(message)

    @bot.command()
    @has_role(AUTHORIZED_ROLE)
    async def forget(ctx, *, target: str = None):
        if not target:
            await ctx.send(
                "🧹 **Utilisation de `!forget` :**\n"
                "- `!forget me` → Efface ta propre mémoire\n"
                "- `!forget @utilisateur` → Efface la mémoire d’un utilisateur\n"
                "- `!forget all` → Efface toute la mémoire"
            )
            return

        await ctx.send("🔒 Envoie-moi ton code d’authentification 2FA pour confirmer l’opération (valide 30s).")
        bot.waiting_for_2fa[ctx.author.id] = True

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            user_code = msg.content.strip()

            totp = pyotp.TOTP(AUTH_SECRET)
            if not totp.verify(user_code):
                await ctx.send("❌ Code 2FA invalide. Opération annulée.")
                return

            conn = sqlite3.connect(bot.DB_PATH)
            cursor = conn.cursor()

            if target.lower() == "all":
                cursor.execute("DELETE FROM facts")
                deleted = cursor.rowcount
                await ctx.send(f"💥 Toute la mémoire a été effacée ({deleted} faits supprimés).")

            elif target.lower() == "me":
                user_id = str(ctx.author.id)
                cursor.execute("DELETE FROM facts WHERE user_id = ?", (user_id,))
                deleted = cursor.rowcount
                if deleted:
                    await ctx.send(f"🧠 J’ai tout oublié à ton sujet ({deleted} faits supprimés).")
                else:
                    await ctx.send("😶 Il n’y avait rien à oublier sur toi.")

            elif ctx.message.mentions:
                member = ctx.message.mentions[0]
                user_id = str(member.id)
                cursor.execute("DELETE FROM facts WHERE user_id = ?", (user_id,))
                deleted = cursor.rowcount
                if deleted:
                    await ctx.send(f"🧹 Mémoire de {member.display_name} effacée ({deleted} faits supprimés).")
                else:
                    await ctx.send(f"ℹ️ Je n'avais rien mémorisé pour {member.display_name}.")
            else:
                await ctx.send("❌ Utilisation incorrecte. Mentionne un utilisateur ou utilise `me` ou `all`.")

            conn.commit()
            conn.close()

        except Exception:
            await ctx.send("⏱️ Temps écoulé ou erreur. Veuillez réessayer.")
        finally:
            bot.waiting_for_2fa[ctx.author.id] = False