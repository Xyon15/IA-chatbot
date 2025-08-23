from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE
import psutil
import time
import sqlite3
import pynvml

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

            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            gpu_name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(gpu_name, bytes):
                gpu_name = gpu_name.decode()
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            gpu_util = util.gpu
            vram_used = round(mem_info.used / (1024**2), 1)
            vram_total = round(mem_info.total / (1024**2), 1)
            vram_percent = round((mem_info.used / mem_info.total) * 100, 1)
            pynvml.nvmlShutdown()

            conn = sqlite3.connect(bot.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory")
            total_msgs = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM memory")
            user_count = cursor.fetchone()[0]
            conn.close()

            msg = (
                "```\n"
                "📊 STATISTIQUES SYSTÈME\n"
                "────────────────────────────\n"
                f"🧠 CPU             :{cpu_percent:>5}%\n"
                f"💾 RAM             : {ram_used:.2f} Go / {ram_total:.2f} Go ({ram_percent}%)\n"
                f"🕒 Uptime PC       : {uptime_str}\n"
                f"🤖 Uptime Neuro    : {bot_uptime_str}\n"
                f"🌐 Accès Web       : {'Activé ✅' if bot.web_enabled else 'Désactivé ❌'}\n"
                "\n"
                f"🖥️ GPU    : {gpu_name}\n"
                f"   📈 Utilisation   : {gpu_util}%\n"
                f"   🌡️ Température   : {temp}°C\n"
                f"   🧮 VRAM     : {vram_used} MiB / {vram_total} MiB ({vram_percent}%)\n"
                "\n"
                "🧠 MÉMOIRE DE NEURO\n"
                "────────────────────────────\n"
                f"🗂️ Disque mémoire  : {disk_used:.2f} Go / {disk_total:.2f} Go ({disk_percent}%)\n"
                f"💬 Messages db     : {total_msgs}\n"
                f"👤 Utilisateurs db : {user_count}\n"
                "```"
            )
            await ctx.send(msg)

        except Exception as e:
            await ctx.send(f"❌ Erreur lors de la récupération des stats : {e}")