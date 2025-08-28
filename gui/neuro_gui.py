#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeuroBot - Interface GUI Moderne
Utilise la palette de couleurs personnalisée pour une interface moderne et élégante
"""

import sys
import os
import time
import threading
import asyncio
import sqlite3
import psutil
import pynvml
import json
from datetime import datetime
from typing import Dict, List, Optional
import traceback

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QPushButton, QTextEdit, QFrame, QProgressBar,
    QTabWidget, QScrollArea, QListWidget, QSplitter, QGroupBox,
    QLineEdit, QSpinBox, QCheckBox, QComboBox, QSystemTrayIcon,
    QMenu, QMessageBox, QDialog, QDialogButtonBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QStackedWidget
)
from PySide6.QtCore import (
    QTimer, QThread, Signal, Qt, QPropertyAnimation, QEasingCurve,
    QRect, QSize, QPoint
)
from PySide6.QtGui import (
    QFont, QPixmap, QPainter, QColor, QBrush, QPen, QLinearGradient,
    QIcon, QAction, QPalette
)

# Ajout du répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import des modules du bot
try:
    from bot import start_bot, stop_bot
    from config import advanced_log_manager
    from memory import get_conversation_history, get_user_facts, clear_user_memory
    from model import get_model_info
    BOT_AVAILABLE = True
except ImportError as e:
    print(f"Certains modules du bot ne sont pas disponibles : {e}")
    BOT_AVAILABLE = False

# Import des widgets personnalisés
try:
    from gui.chart_widgets import DashboardWidget, CircularProgressWidget
    from gui.notification_system import notification_manager, show_info, show_success, show_warning, show_error
    ENHANCED_FEATURES = True
except ImportError as e:
    print(f"Widgets avancés non disponibles : {e}")
    ENHANCED_FEATURES = False

# Configuration de la palette de couleurs sombres
COLOR_PALETTE = {
    'primary_dark': '#1a1a1a',      # Noir profond
    'secondary_dark': '#2d2d2d',    # Gris très foncé
    'neutral_light': '#3a3a3a',     # Gris moyen
    'accent_light': '#4a4a4a',      # Gris clair
    'accent_warm': '#555555',       # Gris plus clair
    'accent_orange': '#4a9eff',     # Bleu accent moderne
    'text_dark': '#ffffff',         # Texte blanc
    'text_light': '#d1d5db',        # Texte gris clair
    'success': '#4ade80',           # Vert moderne
    'warning': '#fbbf24',           # Jaune moderne
    'error': '#ef4444'              # Rouge moderne
}

# Styles CSS pour l'interface
STYLES = f"""
QMainWindow {{
    background: {COLOR_PALETTE['primary_dark']};
    color: {COLOR_PALETTE['text_light']};
}}

QWidget#sidebar {{
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLOR_PALETTE['primary_dark']}, 
                stop:1 {COLOR_PALETTE['secondary_dark']});
    border-radius: 10px;
}}

QPushButton#nav_button {{
    background: transparent;
    color: {COLOR_PALETTE['text_light']};
    border: none;
    padding: 15px;
    text-align: left;
    font-size: 14px;
    font-weight: bold;
    border-radius: 8px;
}}

QPushButton#nav_button:hover {{
    background: {COLOR_PALETTE['accent_orange']};
    color: white;
}}

QPushButton#nav_button:checked {{
    background: {COLOR_PALETTE['accent_orange']};
    color: white;
}}

QPushButton#action_button {{
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLOR_PALETTE['primary_dark']}, 
                stop:1 {COLOR_PALETTE['secondary_dark']});
    color: {COLOR_PALETTE['text_light']};
    border: none;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: bold;
    border-radius: 6px;
}}

QPushButton#action_button:hover {{
    background: {COLOR_PALETTE['accent_orange']};
}}

QPushButton#action_button:pressed {{
    background: {COLOR_PALETTE['secondary_dark']};
}}

QLabel#title {{
    color: {COLOR_PALETTE['text_dark']};
    font-size: 24px;
    font-weight: bold;
    margin: 10px 0;
}}

QLabel#subtitle {{
    color: {COLOR_PALETTE['text_light']};
    font-size: 16px;
    font-weight: 600;
}}

QLabel#stat_label {{
    color: {COLOR_PALETTE['text_light']};
    font-size: 12px;
    font-weight: 500;
}}

QFrame#card {{
    background: {COLOR_PALETTE['secondary_dark']};
    border: 1px solid {COLOR_PALETTE['accent_light']};
    border-radius: 12px;
    padding: 15px;
}}

QProgressBar {{
    border: 1px solid {COLOR_PALETTE['accent_light']};
    border-radius: 8px;
    background: {COLOR_PALETTE['neutral_light']};
    height: 25px;
    color: {COLOR_PALETTE['text_light']};
}}

QProgressBar::chunk {{
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLOR_PALETTE['accent_orange']}, 
                stop:1 {COLOR_PALETTE['success']});
    border-radius: 6px;
}}

QTextEdit {{
    background: {COLOR_PALETTE['secondary_dark']};
    border: 1px solid {COLOR_PALETTE['accent_light']};
    border-radius: 8px;
    padding: 8px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11px;
    color: {COLOR_PALETTE['text_light']};
    selection-background-color: {COLOR_PALETTE['accent_orange']};
}}

QTabWidget::pane {{
    border: 1px solid {COLOR_PALETTE['accent_light']};
    border-radius: 8px;
    background: {COLOR_PALETTE['secondary_dark']};
}}

QTabBar::tab {{
    background: {COLOR_PALETTE['neutral_light']};
    color: {COLOR_PALETTE['text_light']};
    padding: 12px 20px;
    margin-right: 2px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: 1px solid {COLOR_PALETTE['accent_light']};
}}

QTabBar::tab:selected {{
    background: {COLOR_PALETTE['accent_orange']};
    color: {COLOR_PALETTE['text_dark']};
}}

QTabBar::tab:hover {{
    background: {COLOR_PALETTE['accent_light']};
}}
"""

DB_PATH = "D:/neuro_memory/neuro.db"

class DiscordBotThread(QThread):
    log_signal = Signal(str)
    status_signal = Signal(bool)
    
    def __init__(self):
        super().__init__()
        self.loop = None
        self.running = False
        
    def run(self):
        try:
            if not BOT_AVAILABLE:
                self.log_signal.emit("[ERREUR] Modules du bot non disponibles")
                return
                
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.running = True
            self.status_signal.emit(True)
            self.log_signal.emit("[INFO] Bot Discord démarré")
            self.loop.run_until_complete(start_bot(self.loop))
        except Exception as e:
            self.log_signal.emit(f"[ERREUR] {traceback.format_exc()}")
        finally:
            self.running = False
            self.status_signal.emit(False)
            if self.loop:
                try:
                    self.loop.run_until_complete(stop_bot())
                except:
                    pass
                self.loop.close()

class SystemStatsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.bot_start_time = None
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("📊 MONITORING SYSTÈME")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Grille de statistiques
        stats_layout = QGridLayout()
        
        # CPU
        self.cpu_card = self.create_stat_card("🧠 CPU", "0%")
        self.cpu_progress = QProgressBar()
        stats_layout.addWidget(self.cpu_card, 0, 0)
        
        # RAM
        self.ram_card = self.create_stat_card("💾 RAM", "0/0 GB")
        self.ram_progress = QProgressBar()
        stats_layout.addWidget(self.ram_card, 0, 1)
        
        # GPU
        self.gpu_card = self.create_stat_card("🖥️ GPU", "Non détecté")
        stats_layout.addWidget(self.gpu_card, 1, 0)
        
        # VRAM
        self.vram_card = self.create_stat_card("🧮 VRAM", "0/0 MB")
        stats_layout.addWidget(self.vram_card, 1, 1)
        
        # Bot Status
        self.bot_card = self.create_stat_card("🤖 BOT", "Arrêté")
        stats_layout.addWidget(self.bot_card, 2, 0)
        
        # Database
        self.db_card = self.create_stat_card("💬 MESSAGES", "0")
        stats_layout.addWidget(self.db_card, 2, 1)
        
        layout.addLayout(stats_layout)
        
    def create_stat_card(self, title: str, value: str) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card.setFixedHeight(100)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setObjectName("subtitle")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("stat_label")
        value_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FF8128;")
        layout.addWidget(value_label)
        
        return card
    
    def update_stats(self):
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.update_card_value(self.cpu_card, f"{cpu_percent:.1f}%")
            
            # RAM
            ram = psutil.virtual_memory()
            ram_used = ram.used / (1024**3)
            ram_total = ram.total / (1024**3)
            self.update_card_value(self.ram_card, f"{ram_used:.1f}/{ram_total:.1f} GB")
            
            # GPU
            try:
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu_name = pynvml.nvmlDeviceGetName(handle)
                if isinstance(gpu_name, bytes):
                    gpu_name = gpu_name.decode()
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                
                self.update_card_value(self.gpu_card, f"{gpu_name[:20]}...")
                
                vram_used = mem_info.used / (1024**2)
                vram_total = mem_info.total / (1024**2)
                self.update_card_value(self.vram_card, f"{vram_used:.0f}/{vram_total:.0f} MB")
                
                pynvml.nvmlShutdown()
            except Exception:
                self.update_card_value(self.gpu_card, "Non disponible")
                self.update_card_value(self.vram_card, "N/A")
            
            # Database
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM memory")
                total_msgs = cursor.fetchone()[0]
                conn.close()
                self.update_card_value(self.db_card, f"{total_msgs}")
            except Exception:
                self.update_card_value(self.db_card, "Erreur")
                
        except Exception as e:
            print(f"Erreur update stats: {e}")
    
    def update_card_value(self, card: QFrame, value: str):
        # Trouve le label de valeur (le deuxième label dans le card)
        for child in card.children():
            if isinstance(child, QVBoxLayout):
                if child.count() >= 2:
                    value_label = child.itemAt(1).widget()
                    if isinstance(value_label, QLabel):
                        value_label.setText(value)
                        break

class BotControlWidget(QWidget):
    bot_start_signal = Signal()
    bot_stop_signal = Signal()
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.bot_thread = None
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("🎮 CONTRÔLE DU BOT")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Status du bot
        self.status_label = QLabel("🔴 Bot arrêté")
        self.status_label.setObjectName("subtitle")
        layout.addWidget(self.status_label)
        
        # Boutons de contrôle
        buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Démarrer")
        self.start_btn.setObjectName("action_button")
        self.start_btn.clicked.connect(self.start_bot)
        buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Arrêter")
        self.stop_btn.setObjectName("action_button")
        self.stop_btn.clicked.connect(self.stop_bot)
        self.stop_btn.setEnabled(False)
        buttons_layout.addWidget(self.stop_btn)
        
        layout.addLayout(buttons_layout)
        
        # Configuration rapide
        config_group = QGroupBox("Configuration")
        config_layout = QGridLayout(config_group)
        
        # Auto reply
        self.auto_reply_check = QCheckBox("Réponses automatiques")
        config_layout.addWidget(self.auto_reply_check, 0, 0)
        
        # Web search
        self.web_search_check = QCheckBox("Recherche web")
        config_layout.addWidget(self.web_search_check, 0, 1)
        
        # Context length
        config_layout.addWidget(QLabel("Longueur contexte:"), 1, 0)
        self.context_spin = QSpinBox()
        self.context_spin.setRange(1, 50)
        self.context_spin.setValue(10)
        config_layout.addWidget(self.context_spin, 1, 1)
        
        layout.addWidget(config_group)
        
    def start_bot(self):
        if self.bot_thread is None or not self.bot_thread.isRunning():
            self.bot_thread = DiscordBotThread()
            self.bot_thread.log_signal.connect(self.on_bot_log)
            self.bot_thread.status_signal.connect(self.on_bot_status)
            self.bot_thread.start()
            self.bot_start_signal.emit()
            
    def stop_bot(self):
        if self.bot_thread and self.bot_thread.isRunning():
            self.bot_thread.terminate()
            self.bot_thread.wait()
            self.bot_stop_signal.emit()
            
    def on_bot_log(self, message: str):
        # Signal vers le widget de logs principal
        pass
        
    def on_bot_status(self, running: bool):
        if running:
            self.status_label.setText("🟢 Bot en marche")
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        else:
            self.status_label.setText("🔴 Bot arrêté")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

class MemoryManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("🧠 GESTION MÉMOIRE")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Table des conversations
        self.conversation_table = QTableWidget()
        self.conversation_table.setColumnCount(4)
        self.conversation_table.setHorizontalHeaderLabels(["Utilisateur", "Dernier message", "Messages", "Date"])
        
        header = self.conversation_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.conversation_table)
        
        # Boutons d'actions
        actions_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setObjectName("action_button")
        refresh_btn.clicked.connect(self.refresh_conversations)
        actions_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton("🗑️ Effacer sélection")
        clear_btn.setObjectName("action_button")
        clear_btn.clicked.connect(self.clear_selected)
        actions_layout.addWidget(clear_btn)
        
        layout.addLayout(actions_layout)
        
    def refresh_conversations(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Récupère les conversations groupées par utilisateur
            cursor.execute("""
                SELECT user_id, 
                       COUNT(*) as message_count,
                       MAX(timestamp) as last_message,
                       substr(content, 1, 50) as preview
                FROM memory 
                WHERE role = 'user'
                GROUP BY user_id 
                ORDER BY last_message DESC
            """)
            
            conversations = cursor.fetchall()
            conn.close()
            
            self.conversation_table.setRowCount(len(conversations))
            
            for row, (user_id, count, timestamp, preview) in enumerate(conversations):
                self.conversation_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
                self.conversation_table.setItem(row, 1, QTableWidgetItem(preview + "..."))
                self.conversation_table.setItem(row, 2, QTableWidgetItem(str(count)))
                
                # Format de la date
                try:
                    dt = datetime.fromtimestamp(timestamp)
                    date_str = dt.strftime("%d/%m/%Y %H:%M")
                except:
                    date_str = "N/A"
                self.conversation_table.setItem(row, 3, QTableWidgetItem(date_str))
                
        except Exception as e:
            print(f"Erreur refresh conversations: {e}")
            
    def clear_selected(self):
        current_row = self.conversation_table.currentRow()
        if current_row >= 0:
            user_id = self.conversation_table.item(current_row, 0).text()
            
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                f"Effacer toutes les conversations de l'utilisateur {user_id} ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    clear_user_memory(user_id)
                    self.refresh_conversations()
                except Exception as e:
                    QMessageBox.warning(self, "Erreur", f"Impossible d'effacer: {e}")

class LogsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("📋 LOGS SYSTÈME")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Zone de logs
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        layout.addWidget(self.logs_text)
        
        # Contrôles
        controls_layout = QHBoxLayout()
        
        clear_btn = QPushButton("🗑️ Effacer")
        clear_btn.setObjectName("action_button")
        clear_btn.clicked.connect(self.clear_logs)
        controls_layout.addWidget(clear_btn)
        
        save_btn = QPushButton("💾 Sauvegarder")
        save_btn.setObjectName("action_button") 
        save_btn.clicked.connect(self.save_logs)
        controls_layout.addWidget(save_btn)
        
        layout.addLayout(controls_layout)
        
    def add_log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs_text.append(f"[{timestamp}] {message}")
        
    def clear_logs(self):
        self.logs_text.clear()
        
    def save_logs(self):
        # TODO: Implémenter la sauvegarde des logs
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupTimers()
        
    def initUI(self):
        self.setWindowTitle("NeuroBot - Interface Moderne")
        self.setMinimumSize(1400, 900)
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Zone de contenu principal avec StackedWidget
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)
        
        # Widgets de contenu
        self.stats_widget = SystemStatsWidget()
        self.control_widget = BotControlWidget() 
        self.memory_widget = MemoryManagerWidget()
        self.logs_widget = LogsWidget()
        
        # Ajouter les widgets au stack
        self.content_area.addWidget(self.stats_widget)
        self.content_area.addWidget(self.control_widget)
        self.content_area.addWidget(self.memory_widget)
        self.content_area.addWidget(self.logs_widget)
        
        # Dashboard avancé si disponible
        if ENHANCED_FEATURES:
            self.dashboard_widget = DashboardWidget()
            self.content_area.addWidget(self.dashboard_widget)
            
        # Système de notifications
        if ENHANCED_FEATURES:
            # Connecte les signaux aux notifications
            self.control_widget.bot_start_signal.connect(
                lambda: show_success("Bot Discord", "Bot démarré avec succès"))
            self.control_widget.bot_stop_signal.connect(
                lambda: show_info("Bot Discord", "Bot arrêté"))
        
        # Affichage initial
        self.show_stats()
        
    def create_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 30, 20, 30)
        
        # Logo/Titre
        title = QLabel("NEUROBOT")
        title.setStyleSheet(f"color: {COLOR_PALETTE['text_light']}; font-size: 24px; font-weight: bold; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Boutons de navigation
        nav_buttons = [
            ("📊 Monitoring", self.show_stats),
            ("🎮 Contrôles", self.show_controls),
            ("🧠 Mémoire", self.show_memory),
            ("📋 Logs", self.show_logs),
        ]
        
        # Ajoute le dashboard si disponible
        if ENHANCED_FEATURES:
            nav_buttons.insert(1, ("📈 Dashboard", self.show_dashboard))
        
        for text, callback in nav_buttons:
            btn = QPushButton(text)
            btn.setObjectName("nav_button")
            btn.clicked.connect(callback)
            layout.addWidget(btn)
            
        layout.addStretch()
        
        # Bouton de fermeture
        quit_btn = QPushButton("🚪 Quitter")
        quit_btn.setObjectName("nav_button")
        quit_btn.clicked.connect(self.close)
        layout.addWidget(quit_btn)
        
        return sidebar
        
    def show_stats(self):
        self.switch_content(self.stats_widget)
        
    def show_controls(self):
        self.switch_content(self.control_widget)
        
    def show_memory(self):
        self.switch_content(self.memory_widget)
        self.memory_widget.refresh_conversations()
        
    def show_logs(self):
        self.switch_content(self.logs_widget)
        
    def show_dashboard(self):
        """Affiche le dashboard avancé si disponible"""
        if ENHANCED_FEATURES:
            self.switch_content(self.dashboard_widget)
        
    def switch_content(self, widget: QWidget):
        # Utilise QStackedWidget pour basculer de manière sécurisée
        self.content_area.setCurrentWidget(widget)
        
    def setupTimers(self):
        # Timer pour les stats système
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.stats_widget.update_stats)
        self.stats_timer.start(2000)  # 2 secondes

def main():
    app = QApplication(sys.argv)
    
    # Application du style
    app.setStyleSheet(STYLES)
    
    # Fenêtre principale
    window = MainWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())