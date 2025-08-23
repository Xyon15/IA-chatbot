import sys
import time
import threading
import asyncio
import sqlite3
import psutil
import traceback
import pynvml
import json

from bot import start_bot, stop_bot  # Utilise les vraies fonctions du bot

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit)
from PySide6.QtCore import QTimer

DB_PATH = "D:/neuro_memory/neuro.db"  # adapte à ta config

# ----- THREAD ET BOUCLE ASYNC -----

class DiscordBotThread(threading.Thread):
    def __init__(self, log_callback=None):
        super().__init__()
        self.loop = None
        self.running = False
        self.log_callback = log_callback

    def run(self):
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.running = True
            # Appelle directement bot.start dans la bonne boucle
            self.loop.run_until_complete(start_bot(self.loop))
        except asyncio.CancelledError:
            pass
        except Exception:
            msg = "[Erreur dans le bot]\n" + traceback.format_exc()
            print(msg)
            if self.log_callback:
                self.log_callback(msg)
        finally:
            try:
                self.loop.run_until_complete(stop_bot())
            except Exception:
                pass
            self.loop.close()
            self.running = False

    def stop(self):
        if self.loop and self.running:
            try:
                # Demande d'abord l'arrêt du bot Discord
                fut = asyncio.run_coroutine_threadsafe(stop_bot(), self.loop)
                try:
                    fut.result(timeout=10)  # attend la fermeture propre du bot
                except Exception as e:
                    if self.log_callback:
                        self.log_callback(f"[Thread] Erreur lors de l'arrêt du bot Discord : {e}")
                # Puis annule les tâches restantes
                for task in asyncio.all_tasks(loop=self.loop):
                    try:
                        task.cancel()
                    except Exception as e:
                        if self.log_callback:
                            self.log_callback(f"[Thread] Erreur lors de l'annulation d'une tâche : {e}")
                self.loop.call_soon_threadsafe(self.loop.stop)
            except Exception as e:
                if self.log_callback:
                    self.log_callback(f"[Thread] Erreur lors de l'arrêt du loop : {e}")
            self.running = False

# ----- FONCTION STATS -----

def get_stats(bot_start_time, web_enabled=True):
    try:
        # CPU, RAM, disque
        cpu_percent = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory()
        ram_used = ram.used / (1024**3)
        ram_total = ram.total / (1024**3)
        ram_percent = ram.percent

        boot_time = psutil.boot_time()
        uptime_sec = int(time.time() - boot_time)
        days = uptime_sec // 86400
        hours = (uptime_sec % 86400) // 3600
        minutes = (uptime_sec % 3600) // 60
        uptime_pc_str = f"{days}j {hours}h {minutes}m"

        # Uptime bot
        if bot_start_time:
            uptime_bot_sec = int(time.time() - bot_start_time)
            d = uptime_bot_sec // 86400
            h = (uptime_bot_sec % 86400) // 3600
            m = (uptime_bot_sec % 3600) // 60
            uptime_bot_str = f"{d}j {h}h {m}m"
        else:
            uptime_bot_str = "N/A"

        disk = psutil.disk_usage('D:')
        disk_used = disk.used / (1024**3)
        disk_total = disk.total / (1024**3)
        disk_percent = disk.percent

        # GPU stats avec pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        if isinstance(gpu_name, bytes):
            gpu_name = gpu_name.decode()
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        pynvml.nvmlShutdown()

        gpu_util = util.gpu
        vram_used = mem_info.used / (1024**2)
        vram_total = mem_info.total / (1024**2)
        vram_percent = (mem_info.used / mem_info.total) * 100

        # Base SQLite (exemple, adapte à ta vraie table memory)
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory")
            total_msgs = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM memory")
            user_count = cursor.fetchone()[0]
            conn.close()
        except Exception:
            total_msgs = -1
            user_count = -1

        stats_text = (
            "📊 STATISTIQUES SYSTÈME\n"
            "────────────────────────────\n"
            f"🧠 CPU              :{cpu_percent:>5}%\n"
            f"💾 RAM             : {ram_used:.2f} Go / {ram_total:.2f} Go ({ram_percent}%)\n"
            f"🕒 Uptime PC       : {uptime_pc_str}\n"
            f"🤖 Uptime Bot      : {uptime_bot_str}\n"
            f"🌐 Accès Web       : {'Activé ✅' if web_enabled else 'Désactivé ❌'}\n\n"
            f"🖥️ GPU             : {gpu_name}\n"
            f"   📈 Utilisation       : {gpu_util}%\n"
            f"   🌡️ Température   : {temp}°C\n"
            f"   🧮 VRAM             : {vram_used:.1f} MiB / {vram_total:.1f} MiB ({vram_percent:.1f}%)\n\n"
            "🧠 MÉMOIRE DE NEURO\n"
            "────────────────────────────\n"
            f"🗂️ Disque mémoire   :{disk_used:.2f} Go / {disk_total:.2f} Go ({disk_percent}%)\n"
            f"💬 Messages db        : {total_msgs if total_msgs>=0 else 'Erreur'}\n"
            f"👤 Utilisateurs db      : {user_count if user_count>=0 else 'Erreur'}\n"
        )

        return stats_text
    except Exception as e:
        return f"Erreur récupération stats : {e}"

# ----- INTERFACE QT -----

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neuro Bot GUI")
        self.resize(600, 600)

        self.bot_thread = None
        self.bot_start_time = None
        self.web_enabled = True  # configure si accès web activé

        layout = QVBoxLayout(self)

        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        layout.addWidget(self.stats_text)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(220)  # Limite la hauteur à 220px (ajuste selon ton goût)
        layout.addWidget(self.log_text)

        self.toggle_btn = QPushButton("Démarrer le bot")
        self.toggle_btn.clicked.connect(self.toggle_bot)
        layout.addWidget(self.toggle_btn)

        self.timer = QTimer()
        self.timer.setInterval(2000)  # mise à jour toutes les 2s
        self.timer.timeout.connect(self.update_stats)
        self.timer.start()

        self.status_timer = QTimer()
        self.status_timer.setInterval(1000)
        self.status_timer.timeout.connect(self.check_bot_status)
        self.status_timer.start()

    def append_log(self, text):
        self.log_text.append(text)

    def toggle_bot(self):
        if self.bot_thread and self.bot_thread.running:
            self.append_log("[INFO] Arrêt du bot demandé...")
            self.bot_thread.stop()
            self.bot_thread.join()
            self.bot_thread = None
            self.bot_start_time = None
            self.toggle_btn.setText("Démarrer le bot")
            self.append_log("[INFO] Bot arrêté.")
        else:
            self.append_log("[INFO] Démarrage du bot demandé...")
            self.bot_thread = DiscordBotThread(log_callback=self.append_log)
            self.bot_thread.start()
            self.bot_start_time = time.time()
            self.toggle_btn.setText("Arrêter le bot")
            self.append_log("[INFO] Bot démarré.")

    def update_stats(self):
        # Recharge l'état web_enabled depuis le fichier à chaque tick
        try:
            with open("JSON/web.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.web_enabled = data.get("enabled", False)
        except Exception:
            self.web_enabled = False
        stats = get_stats(self.bot_start_time, self.web_enabled)
        self.stats_text.setPlainText(stats)

    def check_bot_status(self):
        # Si le thread n'est plus running mais le bouton affiche "Arrêter le bot", on remet à jour l'UI
        if self.bot_thread and not self.bot_thread.running and self.toggle_btn.text() == "Arrêter le bot":
            self.append_log("[INFO] Bot arrêté (détecté automatiquement).")
            self.bot_thread = None
            self.bot_start_time = None
            self.toggle_btn.setText("Démarrer le bot")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
