#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeuroBot - Interface GUI Principale Améliorée
Interface moderne avec indicateurs circulaires pour les performances
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
import math
from datetime import datetime
from typing import Dict, List, Optional
import traceback

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QPushButton, QTextEdit, QFrame, QProgressBar,
    QSplitter, QGroupBox, QSystemTrayIcon, QMenu, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import (
    QTimer, QThread, Signal, Qt, QPropertyAnimation, QEasingCurve,
    QRect, QSize, QPoint
)
from PySide6.QtGui import (
    QFont, QPixmap, QPainter, QColor, QBrush, QPen, QLinearGradient,
    QIcon, QAction, QPalette, QRadialGradient, QKeySequence, QShortcut
)

# Ajout du répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import des modules du bot
try:
    from bot import start_bot, stop_bot
    BOT_AVAILABLE = True
except ImportError as e:
    print(f"Modules du bot non disponibles : {e}")
    BOT_AVAILABLE = False

# Configuration des couleurs
COLOR_PALETTE = {
    'bg_primary': '#0f0f0f',       # Noir très profond
    'bg_secondary': '#1a1a1a',     # Noir profond
    'bg_tertiary': '#2a2a2a',      # Gris très sombre
    'accent_blue': '#00d4ff',      # Bleu néon
    'accent_green': '#00ff88',     # Vert néon
    'accent_orange': '#ff6b35',    # Orange vif
    'accent_purple': '#8b5cf6',    # Violet
    'text_primary': '#ffffff',     # Blanc pur
    'text_secondary': '#b0b0b0',   # Gris clair
    'text_accent': '#00d4ff',      # Bleu pour accents
    'success': '#00ff88',          # Vert succès
    'warning': '#ffaa00',          # Orange avertissement
    'error': '#ff4444',            # Rouge erreur
    'neutral': '#666666'           # Gris neutre
}

DB_PATH = "D:/neuro_memory/neuro.db"

class CircularIndicator(QWidget):
    """Widget indicateur circulaire personnalisé"""
    
    def __init__(self, title: str, color: str, size: int = 120):
        super().__init__()
        self.title = title
        self.color = color
        self.value = 0
        self.max_value = 100
        self.text_value = "0%"
        self.setFixedSize(size, size)
        
    def setValue(self, value: float, text_value: str = None):
        self.value = max(0, min(value, self.max_value))
        if text_value:
            self.text_value = text_value
        else:
            self.text_value = f"{value:.1f}%"
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Configuration
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 10
        
        # Fond du cercle
        painter.setPen(QPen(QColor(COLOR_PALETTE['bg_tertiary']), 6))
        painter.drawEllipse(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        
        # Arc de progression
        if self.value > 0:
            # Calcul de l'angle (départ à 12h)
            start_angle = 90 * 16  # 90 degrés en unités Qt
            span_angle = int(-(self.value / self.max_value) * 360 * 16)
            
            # Couleur avec gradient
            pen_color = QColor(self.color)
            painter.setPen(QPen(pen_color, 6, Qt.SolidLine, Qt.RoundCap))
            painter.drawArc(center.x() - radius, center.y() - radius, 
                          radius * 2, radius * 2, start_angle, span_angle)
        
        # Texte central - valeur
        painter.setPen(QColor(COLOR_PALETTE['text_primary']))
        font = QFont("Segoe UI", 12, QFont.Bold)
        painter.setFont(font)
        
        text_rect = QRect(center.x() - radius//2, center.y() - 10, radius, 20)
        painter.drawText(text_rect, Qt.AlignCenter, self.text_value)
        
        # Titre en bas
        painter.setPen(QColor(COLOR_PALETTE['text_secondary']))
        font = QFont("Segoe UI", 9)
        painter.setFont(font)
        
        title_rect = QRect(center.x() - radius, center.y() + 15, radius * 2, 20)
        painter.drawText(title_rect, Qt.AlignCenter, self.title)

class TemperatureCircularIndicator(QWidget):
    """Widget indicateur circulaire pour la température GPU"""
    
    def __init__(self, title: str, max_temp: float = 90.0, size: int = 120):
        super().__init__()
        self.title = title
        self.max_temp = max_temp  # Température maximale pour la progression (90°C)
        self.temperature = 0.0
        self.utilization = 0.0
        self.text_value = "N/A"
        self.setFixedSize(size, size)
        
        # Seuils de température
        self.temp_thresholds = {
            'cool': 40,      # < 40°C : vert
            'warm': 65,      # 40-65°C : orange  
            'hot': 80,       # 65-80°C : rouge
            'critical': 85   # > 80°C : rouge clignotant
        }
        
    def setValue(self, utilization: float, temp_text: str):
        """Met à jour l'utilisation GPU et la température"""
        self.utilization = max(0, min(utilization, 100))
        self.text_value = temp_text
        
        # Extraire la température du texte (format: "75°C")
        try:
            if "°C" in temp_text:
                self.temperature = float(temp_text.replace("°C", ""))
            else:
                self.temperature = 0.0
        except:
            self.temperature = 0.0
            
        self.update()
        
    def get_temp_color(self):
        """Retourne la couleur selon la température"""
        if self.temperature < self.temp_thresholds['cool']:
            return QColor(COLOR_PALETTE['success'])      # Vert
        elif self.temperature < self.temp_thresholds['warm']:
            return QColor(COLOR_PALETTE['accent_blue'])  # Bleu
        elif self.temperature < self.temp_thresholds['hot']:
            return QColor(COLOR_PALETTE['warning'])      # Orange
        else:
            return QColor(COLOR_PALETTE['error'])        # Rouge
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Configuration
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 10
        
        # Fond du cercle
        painter.setPen(QPen(QColor(COLOR_PALETTE['bg_tertiary']), 6))
        painter.drawEllipse(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        
        # Arc de progression basé sur la température
        if self.temperature > 0:
            # Calcul de l'angle basé sur la température (départ à 12h)
            start_angle = 90 * 16  # 90 degrés en unités Qt
            # Progression basée sur la température avec une échelle adaptée
            temp_ratio = min(self.temperature / self.max_temp, 1.0)
            span_angle = int(-temp_ratio * 360 * 16)
            
            # Couleur dynamique selon la température
            pen_color = self.get_temp_color()
            
            # Effet de clignotement pour températures critiques
            if self.temperature > self.temp_thresholds['critical']:
                import time
                # Modulation de l'alpha pour effet de clignotement
                alpha = int(155 + 100 * abs(time.time() * 2 % 1 - 0.5))
                pen_color.setAlpha(alpha)
            
            painter.setPen(QPen(pen_color, 8, Qt.SolidLine, Qt.RoundCap))
            painter.drawArc(center.x() - radius, center.y() - radius, 
                          radius * 2, radius * 2, start_angle, span_angle)
            
            # Arc secondaire pour l'utilisation (plus fin)
            if self.utilization > 0:
                util_ratio = self.utilization / 100.0
                util_span = int(-util_ratio * 360 * 16)
                
                # Couleur plus discrète pour l'utilisation
                util_color = QColor(COLOR_PALETTE['text_secondary'])
                util_color.setAlpha(120)
                painter.setPen(QPen(util_color, 3, Qt.SolidLine, Qt.RoundCap))
                painter.drawArc(center.x() - radius + 6, center.y() - radius + 6, 
                              (radius - 6) * 2, (radius - 6) * 2, start_angle, util_span)
        
        # Texte central - température
        painter.setPen(QColor(COLOR_PALETTE['text_primary']))
        font = QFont("Segoe UI", 11, QFont.Bold)
        painter.setFont(font)
        
        text_rect = QRect(center.x() - radius//2, center.y() - 15, radius, 20)
        painter.drawText(text_rect, Qt.AlignCenter, self.text_value)
        
        # Utilisation en petit texte
        if self.utilization > 0:
            painter.setPen(QColor(COLOR_PALETTE['text_secondary']))
            font = QFont("Segoe UI", 8)
            painter.setFont(font)
            util_rect = QRect(center.x() - radius//2, center.y() + 2, radius, 15)
            painter.drawText(util_rect, Qt.AlignCenter, f"{self.utilization:.0f}%")
        
        # Titre en bas
        painter.setPen(QColor(COLOR_PALETTE['text_secondary']))
        font = QFont("Segoe UI", 9)
        painter.setFont(font)
        
        title_rect = QRect(center.x() - radius, center.y() + 20, radius * 2, 20)
        painter.drawText(title_rect, Qt.AlignCenter, self.title)

class StatusCard(QFrame):
    """Widget carte de statut"""
    
    def __init__(self, icon: str, title: str, value: str = "N/A"):
        super().__init__()
        self.setObjectName("status_card")
        self.setFixedHeight(80)
        self.setFrameStyle(QFrame.Box)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Icône
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 24px; color: {COLOR_PALETTE['accent_blue']};")
        icon_label.setFixedWidth(40)
        layout.addWidget(icon_label)
        
        # Contenu
        content_layout = QVBoxLayout()
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"color: {COLOR_PALETTE['text_secondary']}; font-size: 12px; font-weight: 600;")
        content_layout.addWidget(self.title_label)
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-size: 16px; font-weight: bold;")
        content_layout.addWidget(self.value_label)
        
        layout.addLayout(content_layout)
        
    def setValue(self, value: str):
        self.value_label.setText(value)

class DiscordBotThread(QThread):
    """Thread pour le bot Discord"""
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
    
    def stop(self):
        if self.loop and self.running:
            try:
                # Arrêt propre du bot
                fut = asyncio.run_coroutine_threadsafe(stop_bot(), self.loop)
                fut.result(timeout=10)
                
                # Annulation des tâches
                for task in asyncio.all_tasks(loop=self.loop):
                    try:
                        task.cancel()
                    except Exception:
                        pass
                        
                self.loop.call_soon_threadsafe(self.loop.stop)
            except Exception:
                pass
            self.running = False

class MainInterface(QMainWindow):
    """Interface principale améliorée"""
    
    def __init__(self):
        super().__init__()
        self.bot_thread = None
        self.bot_start_time = None
        self.web_enabled = True
        
        self.initUI()
        self.initTimers()
        self.initShortcuts()
        self.load_config()
        
    def initUI(self):
        self.setWindowTitle("Neuro-Bot - Interface Principale")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Panel gauche - Indicateurs de performance
        self.setupPerformancePanel(main_layout)
        
        # Panel droit - Contrôles et logs
        self.setupControlPanel(main_layout)
        
        self.applyStyles()
        
    def setupPerformancePanel(self, main_layout):
        """Configuration du panel de performance avec indicateurs circulaires"""
        perf_frame = QFrame()
        perf_frame.setObjectName("performance_panel")
        perf_layout = QVBoxLayout(perf_frame)
        perf_layout.setSpacing(20)
        
        # Titre
        title = QLabel("📊 PERFORMANCES SYSTÈME")
        title.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        perf_layout.addWidget(title)
        
        # Grille d'indicateurs circulaires
        indicators_layout = QGridLayout()
        indicators_layout.setSpacing(20)
        
        # Indicateurs principaux
        self.cpu_indicator = CircularIndicator("CPU", COLOR_PALETTE['accent_blue'])
        self.ram_indicator = CircularIndicator("RAM", COLOR_PALETTE['accent_green'])
        self.gpu_indicator = TemperatureCircularIndicator("GPU", max_temp=90.0)
        self.vram_indicator = CircularIndicator("VRAM", COLOR_PALETTE['accent_purple'])
        
        indicators_layout.addWidget(self.cpu_indicator, 0, 0)
        indicators_layout.addWidget(self.ram_indicator, 0, 1)
        indicators_layout.addWidget(self.gpu_indicator, 1, 0)
        indicators_layout.addWidget(self.vram_indicator, 1, 1)
        
        perf_layout.addLayout(indicators_layout)
        
        # Cartes de statut
        status_layout = QVBoxLayout()
        status_layout.setSpacing(10)
        
        self.bot_status_card = StatusCard("🤖", "Bot Status", "Arrêté")
        self.uptime_card = StatusCard("⏱️", "Uptime", "0j 0h 0m")
        self.messages_card = StatusCard("💬", "Messages", "0")
        self.users_card = StatusCard("👥", "Utilisateurs", "0")
        
        status_layout.addWidget(self.bot_status_card)
        status_layout.addWidget(self.uptime_card)
        status_layout.addWidget(self.messages_card)
        status_layout.addWidget(self.users_card)
        
        perf_layout.addLayout(status_layout)
        perf_layout.addStretch()
        
        main_layout.addWidget(perf_frame, 1)
        
    def setupControlPanel(self, main_layout):
        """Configuration du panel de contrôle et logs"""
        control_frame = QFrame()
        control_frame.setObjectName("control_panel")
        control_layout = QVBoxLayout(control_frame)
        control_layout.setSpacing(20)
        
        # Titre et contrôles du bot
        header_layout = QVBoxLayout()
        
        title = QLabel("🎮 CONTRÔLE DU BOT")
        title.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)
        
        # Status du bot
        self.status_display = QLabel("🔴 Bot arrêté")
        self.status_display.setStyleSheet(f"color: {COLOR_PALETTE['error']}; font-size: 14px; font-weight: 600; padding: 10px;")
        header_layout.addWidget(self.status_display)
        
        # Boutons de contrôle
        buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Démarrer Bot")
        self.start_btn.clicked.connect(self.start_bot)
        buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Arrêter Bot")
        self.stop_btn.clicked.connect(self.stop_bot)
        self.stop_btn.setEnabled(False)
        buttons_layout.addWidget(self.stop_btn)
        
        header_layout.addLayout(buttons_layout)
        control_layout.addLayout(header_layout)
        
        # Boutons utilitaires
        utils_layout = QHBoxLayout()
        
        config_btn = QPushButton("⚙️ Configuration")
        config_btn.clicked.connect(self.open_config)
        utils_layout.addWidget(config_btn)
        
        logs_btn = QPushButton("📋 Logs Avancés")
        logs_btn.clicked.connect(self.open_log_viewer)
        utils_layout.addWidget(logs_btn)
        
        restart_btn = QPushButton("🔄 Redémarrage")
        restart_btn.clicked.connect(self.restart_bot)
        utils_layout.addWidget(restart_btn)
        
        control_layout.addLayout(utils_layout)
        
        # Zone de logs
        logs_title = QLabel("📝 LOGS EN TEMPS RÉEL")
        logs_title.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-size: 14px; font-weight: bold;")
        control_layout.addWidget(logs_title)
        
        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(250)
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet(f"""
            QTextEdit {{
                background: {COLOR_PALETTE['bg_tertiary']};
                border: 1px solid {COLOR_PALETTE['neutral']};
                border-radius: 8px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
                color: {COLOR_PALETTE['text_secondary']};
            }}
        """)
        control_layout.addWidget(self.log_display)
        
        # Informations rapides
        info_layout = QVBoxLayout()
        
        info_title = QLabel("ℹ️ INFORMATIONS RAPIDES")
        info_title.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-size: 14px; font-weight: bold;")
        info_layout.addWidget(info_title)
        
        self.quick_info = QLabel()
        self.quick_info.setStyleSheet(f"color: {COLOR_PALETTE['text_secondary']}; font-size: 11px; padding: 10px;")
        self.quick_info.setWordWrap(True)
        info_layout.addWidget(self.quick_info)
        
        # Raccourcis clavier
        shortcuts_title = QLabel("⌨️ RACCOURCIS")
        shortcuts_title.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-size: 14px; font-weight: bold;")
        info_layout.addWidget(shortcuts_title)
        
        shortcuts_info = QLabel("F5: Start/Stop • Ctrl+R: Restart • Ctrl+L: Clear • F1: Help")
        shortcuts_info.setStyleSheet(f"color: {COLOR_PALETTE['text_accent']}; font-size: 10px; padding: 5px;")
        shortcuts_info.setWordWrap(True)
        info_layout.addWidget(shortcuts_info)
        
        control_layout.addLayout(info_layout)
        control_layout.addStretch()
        
        main_layout.addWidget(control_frame, 1)
        
    def initTimers(self):
        """Initialisation des timers"""
        # Timer pour les statistiques
        self.stats_timer = QTimer()
        self.stats_timer.setInterval(2000)  # 2 secondes
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start()
        
        # Timer pour le statut du bot
        self.status_timer = QTimer()
        self.status_timer.setInterval(1000)  # 1 seconde
        self.status_timer.timeout.connect(self.check_bot_status)
        self.status_timer.start()
        
    def initShortcuts(self):
        """Initialisation des raccourcis clavier"""
        # F5: Démarrer/Arrêter le bot
        self.toggle_shortcut = QShortcut(QKeySequence("F5"), self)
        self.toggle_shortcut.activated.connect(self.toggle_bot_shortcut)
        
        # Ctrl+R: Redémarrer le bot
        self.restart_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.restart_shortcut.activated.connect(self.restart_bot)
        
        # Ctrl+L: Effacer les logs
        self.clear_logs_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        self.clear_logs_shortcut.activated.connect(self.clear_logs)
        
        # F1: Aide
        self.help_shortcut = QShortcut(QKeySequence("F1"), self)
        self.help_shortcut.activated.connect(self.show_help)
        
    def applyStyles(self):
        """Application des styles CSS"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background: {COLOR_PALETTE['bg_primary']};
                color: {COLOR_PALETTE['text_primary']};
            }}
            
            QFrame#performance_panel {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_secondary']}, 
                    stop:1 {COLOR_PALETTE['bg_tertiary']});
                border-radius: 15px;
                border: 1px solid {COLOR_PALETTE['neutral']};
            }}
            
            QFrame#control_panel {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_secondary']}, 
                    stop:1 {COLOR_PALETTE['bg_tertiary']});
                border-radius: 15px;
                border: 1px solid {COLOR_PALETTE['neutral']};
            }}
            
            QFrame#status_card {{
                background: {COLOR_PALETTE['bg_tertiary']};
                border: 1px solid {COLOR_PALETTE['neutral']};
                border-radius: 8px;
            }}
            
            QPushButton {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_tertiary']}, 
                    stop:1 {COLOR_PALETTE['bg_secondary']});
                color: {COLOR_PALETTE['text_primary']};
                border: 1px solid {COLOR_PALETTE['neutral']};
                padding: 10px 15px;
                font-size: 12px;
                font-weight: 600;
                border-radius: 8px;
            }}
            
            QPushButton:hover {{
                background: {COLOR_PALETTE['accent_blue']};
                border-color: {COLOR_PALETTE['accent_blue']};
            }}
            
            QPushButton:pressed {{
                background: {COLOR_PALETTE['bg_secondary']};
            }}
            
            QPushButton:disabled {{
                background: {COLOR_PALETTE['neutral']};
                color: {COLOR_PALETTE['text_secondary']};
            }}
        """)
        
    def load_config(self):
        """Chargement de la configuration"""
        try:
            with open("JSON/web.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.web_enabled = data.get("enabled", False)
        except Exception:
            self.web_enabled = False
    
    def get_current_model_name(self):
        """Obtient le nom du modèle actuellement utilisé"""
        try:
            with open("JSON/config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                model_path = data.get("model_path", "models/zephyr-7b-beta.Q5_K_M.gguf")
                model_name = os.path.basename(model_path)
                # Simplification du nom pour l'affichage
                if "zephyr" in model_name.lower():
                    return "Zephyr-7B"
                elif "mistral" in model_name.lower():
                    return "Mistral-7B"
                elif "phi" in model_name.lower():
                    return "Phi-2"
                else:
                    return model_name[:20] + "..." if len(model_name) > 20 else model_name
        except Exception:
            return "Zephyr-7B (défaut)"
            
    def update_stats(self):
        """Mise à jour des statistiques"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_indicator.setValue(cpu_percent)
            
            # RAM
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_used = ram.used / (1024**3)
            ram_total = ram.total / (1024**3)
            self.ram_indicator.setValue(ram_percent, f"{ram_used:.1f}G")
            
            # GPU & VRAM
            try:
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu_name = pynvml.nvmlDeviceGetName(handle)
                if isinstance(gpu_name, bytes):
                    gpu_name = gpu_name.decode()
                    
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                
                self.gpu_indicator.setValue(util.gpu, f"{temp}°C")
                
                vram_used = mem_info.used / (1024**2)
                vram_total = mem_info.total / (1024**2)
                vram_percent = (mem_info.used / mem_info.total) * 100
                self.vram_indicator.setValue(vram_percent, f"{vram_used:.0f}M")
                
                pynvml.nvmlShutdown()
            except Exception:
                self.gpu_indicator.setValue(0, "N/A")
                self.vram_indicator.setValue(0, "N/A")
            
            # Uptime
            if self.bot_start_time:
                uptime_sec = int(time.time() - self.bot_start_time)
                days = uptime_sec // 86400
                hours = (uptime_sec % 86400) // 3600
                minutes = (uptime_sec % 3600) // 60
                self.uptime_card.setValue(f"{days}j {hours}h {minutes}m")
            
            # Base de données
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM memory")
                total_msgs = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM memory")
                user_count = cursor.fetchone()[0]
                conn.close()
                
                self.messages_card.setValue(str(total_msgs))
                self.users_card.setValue(str(user_count))
            except Exception:
                self.messages_card.setValue("Erreur")
                self.users_card.setValue("Erreur")
            
            # Informations rapides
            model_name = self.get_current_model_name()
            db_name = DB_PATH.split('/')[-1] if '/' in DB_PATH else DB_PATH.split('\\')[-1]
            
            info_text = f"""
• Web Search: {'Activé' if self.web_enabled else 'Désactivé'}
• Modèle: {model_name}
• Base: SQLite ({db_name})
• GPU: RTX 4050 (6GB VRAM)
• Profil: Équilibré Adaptatif
            """.strip()
            self.quick_info.setText(info_text)
            
        except Exception as e:
            self.append_log(f"[ERREUR] Mise à jour stats: {e}")
    
    def start_bot(self):
        """Démarrage du bot"""
        if not self.bot_thread or not self.bot_thread.running:
            self.append_log("[INFO] Démarrage du bot demandé...")
            self.bot_thread = DiscordBotThread()
            self.bot_thread.log_signal.connect(self.append_log)
            self.bot_thread.status_signal.connect(self.update_bot_status)
            self.bot_thread.start()
            self.bot_start_time = time.time()
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
    
    def stop_bot(self):
        """Arrêt du bot"""
        if self.bot_thread and self.bot_thread.running:
            self.append_log("[INFO] Arrêt du bot demandé...")
            self.bot_thread.stop()
            self.bot_thread.wait()
            self.bot_thread = None
            self.bot_start_time = None
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
    
    def restart_bot(self):
        """Redémarrage du bot"""
        self.append_log("[INFO] Redémarrage du bot...")
        self.stop_bot()
        QTimer.singleShot(2000, self.start_bot)  # Redémarre après 2s
    
    def update_bot_status(self, running: bool):
        """Mise à jour du statut du bot"""
        if running:
            self.status_display.setText("🟢 Bot en ligne")
            self.status_display.setStyleSheet(f"color: {COLOR_PALETTE['success']}; font-size: 14px; font-weight: 600; padding: 10px;")
            self.bot_status_card.setValue("En ligne")
        else:
            self.status_display.setText("🔴 Bot arrêté")
            self.status_display.setStyleSheet(f"color: {COLOR_PALETTE['error']}; font-size: 14px; font-weight: 600; padding: 10px;")
            self.bot_status_card.setValue("Arrêté")
    
    def check_bot_status(self):
        """Vérification périodique du statut du bot"""
        if self.bot_thread and not self.bot_thread.running and not self.start_btn.isEnabled():
            self.append_log("[INFO] Bot arrêté (détecté automatiquement)")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.bot_start_time = None
    
    def append_log(self, message: str):
        """Ajout d'un message aux logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_display.append(formatted_message)
        
        # Limite le nombre de lignes
        if self.log_display.document().lineCount() > 100:
            cursor = self.log_display.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.select(cursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()  # Supprime le saut de ligne
    
    def open_config(self):
        """Ouverture de la configuration"""
        self.append_log("[INFO] Ouverture des fichiers de configuration...")
        try:
            os.startfile("JSON")
        except Exception as e:
            self.append_log(f"[ERREUR] Impossible d'ouvrir le dossier config: {e}")
    
    def open_log_viewer(self):
        """Ouverture du visualiseur de logs avancé"""
        try:
            import subprocess
            subprocess.Popen([sys.executable, "gui/tools/log_viewer_gui.py"], 
                           cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.append_log("[INFO] Visualiseur de logs ouvert")
        except Exception as e:
            self.append_log(f"[ERREUR] Erreur ouverture visualiseur: {e}")
    
    def toggle_bot_shortcut(self):
        """Basculer le statut du bot via raccourci clavier"""
        if self.bot_thread and self.bot_thread.running:
            self.stop_bot()
        else:
            self.start_bot()
    
    def clear_logs(self):
        """Effacer les logs"""
        self.log_display.clear()
        self.append_log("[INFO] Logs effacés")
    
    def show_help(self):
        """Afficher l'aide"""
        help_text = """
🚀 RACCOURCIS CLAVIER

F5        - Démarrer/Arrêter le bot
Ctrl+R    - Redémarrer le bot
Ctrl+L    - Effacer les logs
F1        - Afficher cette aide

🎮 FONCTIONNALITÉS

• Indicateurs circulaires temps réel
• Contrôle complet du bot Discord
• Logs avec horodatage
• Monitoring GPU/CPU/RAM
• Configuration rapide
        """.strip()
        
        QMessageBox.information(self, "Aide - Neuro-Bot Interface", help_text)
    
    def closeEvent(self, event):
        """Gestion de la fermeture de l'application"""
        if self.bot_thread and self.bot_thread.running:
            reply = QMessageBox.question(self, 'Fermeture', 
                                       'Le bot est en cours d\'exécution. Voulez-vous l\'arrêter et fermer ?',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.stop_bot()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("Neuro-Bot")
    app.setApplicationVersion("1.0")
    
    # Style global sombre
    app.setStyle('Fusion')
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(COLOR_PALETTE['bg_primary']))
    dark_palette.setColor(QPalette.WindowText, QColor(COLOR_PALETTE['text_primary']))
    app.setPalette(dark_palette)
    
    window = MainInterface()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())