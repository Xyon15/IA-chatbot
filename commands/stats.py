from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE
import psutil
import time
import sqlite3
from gpu_utils import get_gpu_info, is_gpu_available
from model import model_manager

def setup(bot):
    @bot.command()
    @has_role(AUTHORIZED_ROLE)
    async def stats(ctx):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            ram_used = round(ram.used / (1024**3), 2)
            ram_total = round(ram.total / (1024**3), 2)
            ram_percent = ram.percent

            boot_time = psutil.boot_time()
            uptime_sec = int(time.time() - boot_time)
            days = uptime_sec // 86400
            hours = (uptime_sec % 86400) // 3600
            minutes = (uptime_sec % 3600) // 60
            uptime_str = f"{days}j {hours}h {minutes}m"

            uptime_bot = int(time.time() - bot.bot_start_time)
            bot_days = uptime_bot // 86400
            bot_hours = (uptime_bot % 86400) // 3600
            bot_minutes = (uptime_bot % 3600) // 60
            bot_uptime_str = f"{bot_days}j {bot_hours}h {bot_minutes}m"

            disk = psutil.disk_usage('D:')
            disk_used = round(disk.used / (1024**3), 2)
            disk_total = round(disk.total / (1024**3), 2)
            disk_percent = disk.percent

            # GPU Info
            gpu_info = get_gpu_info()
            if gpu_info:
                gpu_name = gpu_info.name
                gpu_util = gpu_info.utilization_gpu
                vram_used = round(gpu_info.vram_used_mb / 1024, 1)  # GB
                vram_total = round(gpu_info.vram_total_mb / 1024, 1)  # GB
                vram_percent = round(gpu_info.vram_usage_percent, 1)
                temp = gpu_info.temperature_c
            else:
                gpu_name = "Non disponible"
                gpu_util = 0
                vram_used = 0
                vram_total = 0
                vram_percent = 0
                temp = 0

            # Informations sur le modèle LLM
            llm_status = "✅ Initialisé" if model_manager.is_ready() else "❌ Non initialisé"
            
            # Informations sur le profil et le contexte
            current_profile = model_manager.get_current_profile()
            context_info = model_manager.get_context_info()
            
            if current_profile and context_info:
                profile_name = current_profile['config']['name']
                configured_ctx = context_info['configured_ctx']
                actual_ctx = context_info['actual_ctx']
                ctx_efficiency = f"{context_info['efficiency_percent']:.1f}%"
                # Tenter de lire le nombre réel de couches offloadées si exposé par llama.cpp
                # Sinon, retomber sur la config du profil
                gpu_layers = current_profile['config'].get('n_gpu_layers', 'N/A')
                try:
                    # Dans certaines versions, on peut lire n_gpu_layers depuis l’objet interne
                    ngl_attr = getattr(getattr(model_manager, 'llm', None), 'model_params', None)
                    if ngl_attr is not None:
                        real_ngl = getattr(ngl_attr, 'n_gpu_layers', None)
                        if isinstance(real_ngl, int) and real_ngl > 0:
                            gpu_layers = real_ngl if real_ngl != 0x7FFFFFFF else 'ALL'
                except Exception:
                    pass
                batch_size = current_profile['config']['n_batch']
            else:
                profile_name = "N/A"
                configured_ctx = "N/A"
                actual_ctx = "N/A"
                ctx_efficiency = "N/A"
                gpu_layers = "N/A"
                batch_size = "N/A"

            conn = sqlite3.connect(bot.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory")
            total_msgs = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM memory")
            user_count = cursor.fetchone()[0]
            conn.close()

            # Statut VRAM avec recommandations
            vram_status = "🟢 Optimal"
            if vram_percent > 90:
                vram_status = "🔴 Critique"
            elif vram_percent > 80:
                vram_status = "🟠 Élevé"
            elif vram_percent > 60:
                vram_status = "🟡 Modéré"

            msg = (
                "```\n"
                "📊 STATISTIQUES SYSTÈME\n"
                "────────────────────────────\n"
                f"🧠 CPU             :{cpu_percent:>5}%\n"
                f"💾 RAM             : {ram_used:.2f} Go / {ram_total:.2f} Go ({ram_percent}%)\n"
                f"🕒 Uptime PC       : {uptime_str}\n"
                f"🤖 Uptime Kira      : {bot_uptime_str}\n"
                f"🌐 Accès Web       : {'Activé ✅' if bot.web_enabled else 'Désactivé ❌'}\n"
                "\n"
                f"🖥️ GPU    : {gpu_name}\n"
                f"   📈 Utilisation   : {gpu_util}%\n"
                f"   🌡️ Température   : {temp}°C\n"
                f"   🧮 VRAM     : {vram_used} MiB / {vram_total} MiB ({vram_percent}%) {vram_status}\n"
                "\n"
                "🤖 MODÈLE LLM\n"
                "────────────────────────────\n"
                f"📊 Statut          : {llm_status}\n"
                f"🎯 Profil actuel   : {profile_name}\n"
                f"🧮 Contexte config : {configured_ctx:,} tokens\n"
                f"🧮 Contexte réel   : {actual_ctx:,} tokens\n"
                f"⚡ Efficacité ctx  : {ctx_efficiency}\n"
                f"🔧 Couches GPU     : {gpu_layers}\n"
                f"📦 Batch size      : {batch_size}\n"
            )

            # Ajout d’un état backend (CUDA oui/non) si dispo
            try:
                runtime = current_profile.get('runtime') if current_profile else None
                if runtime is not None:
                    cuda_state = runtime.get('cuda')
                    module_path = runtime.get('module_path')
                    if cuda_state is True:
                        msg += f"   ⚙️ Backend       : CUDA ✅\n"
                    elif cuda_state is False:
                        msg += f"   ⚙️ Backend       : CUDA ❌\n"
                    # Optionnel: montrer le chemin du module pour détecter conflit import
                    if module_path:
                        msg += f"   📦 Module        : {module_path}\n"
            except Exception:
                pass

            msg += (
                "\n"
                "🧠 MÉMOIRE DE KIRA\n"
                "────────────────────────────\n"
                f"🗂️ Disque mémoire  : {disk_used:.2f} Go / {disk_total:.2f} Go ({disk_percent}%)\n"
                f"💬 Messages db     : {total_msgs}\n"
                f"👤 Utilisateurs db : {user_count}\n"
                "```"
            )
            await ctx.send(msg)

        except Exception as e:
            await ctx.send(f"❌ Erreur lors de la récupération des stats : {e}")