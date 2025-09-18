#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visionneur de Logs Avancé pour Kira-Bot
Interface moderne reprenant le thème du GUI principal
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import threading
from queue import Empty

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QComboBox, QLineEdit, QLabel, QSplitter,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QSpinBox,
    QDateTimeEdit, QGroupBox, QTabWidget, QProgressBar, QSystemTrayIcon,
    QMenu, QMessageBox, QFileDialog, QFrame, QScrollArea, QGridLayout,
    QInputDialog, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import (
    QTimer, Qt, QThread, Signal, QDateTime, QSize, QPropertyAnimation,
    QEasingCurve, QRect
)
from PySide6.QtGui import (
    QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush,
    QTextCharFormat, QTextCursor, QAction, QLinearGradient
)
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QLineSeries, QDateTimeAxis, QValueAxis

# Ajout du répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.advanced_logging import LogManager, LogEntry, LogLevel, get_log_manager

# Configuration des couleurs - reprend le thème du GUI principal
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

class KiraTheme:
    """Thème moderne reprenant le style du GUI principal"""
    
    @staticmethod
    def apply(app: QApplication):
        """Applique le thème Kira-Bot"""
        app.setStyle('Fusion')
        
        # Palette de couleurs
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(COLOR_PALETTE['bg_primary']))
        palette.setColor(QPalette.WindowText, QColor(COLOR_PALETTE['text_primary']))
        palette.setColor(QPalette.Base, QColor(COLOR_PALETTE['bg_secondary']))
        palette.setColor(QPalette.AlternateBase, QColor(COLOR_PALETTE['bg_tertiary']))
        palette.setColor(QPalette.ToolTipBase, QColor(COLOR_PALETTE['bg_secondary']))
        palette.setColor(QPalette.ToolTipText, QColor(COLOR_PALETTE['text_primary']))
        palette.setColor(QPalette.Text, QColor(COLOR_PALETTE['text_primary']))
        palette.setColor(QPalette.Button, QColor(COLOR_PALETTE['bg_tertiary']))
        palette.setColor(QPalette.ButtonText, QColor(COLOR_PALETTE['text_primary']))
        palette.setColor(QPalette.BrightText, QColor(COLOR_PALETTE['error']))
        palette.setColor(QPalette.Link, QColor(COLOR_PALETTE['accent_blue']))
        palette.setColor(QPalette.Highlight, QColor(COLOR_PALETTE['accent_blue']))
        palette.setColor(QPalette.HighlightedText, QColor(COLOR_PALETTE['bg_primary']))
        
        app.setPalette(palette)
        
        # Style CSS personnalisé
        app.setStyleSheet(f"""
            /* Fenêtre principale */
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_primary']}, 
                    stop:1 {COLOR_PALETTE['bg_secondary']});
                color: {COLOR_PALETTE['text_primary']};
                border: 1px solid {COLOR_PALETTE['bg_tertiary']};
            }}
            
            /* Widgets de base */
            QWidget {{
                background-color: transparent;
                color: {COLOR_PALETTE['text_primary']};
                selection-background-color: {COLOR_PALETTE['accent_blue']};
                selection-color: {COLOR_PALETTE['bg_primary']};
            }}
            
            /* Boutons */
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_tertiary']}, 
                    stop:1 {COLOR_PALETTE['bg_secondary']});
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                color: {COLOR_PALETTE['text_primary']};
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['accent_blue']}, 
                    stop:1 rgba(0, 212, 255, 0.7));
                border: 2px solid {COLOR_PALETTE['accent_blue']};
            }}
            QPushButton:pressed {{
                background: {COLOR_PALETTE['accent_blue']};
            }}
            QPushButton:disabled {{
                background: {COLOR_PALETTE['neutral']};
                border: 2px solid {COLOR_PALETTE['neutral']};
                color: {COLOR_PALETTE['text_secondary']};
            }}
            
            /* Zone de texte */
            QTextEdit, QPlainTextEdit {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_secondary']}, 
                    stop:1 {COLOR_PALETTE['bg_primary']});
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 8px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 10pt;
                color: {COLOR_PALETTE['text_primary']};
            }}
            
            /* Table */
            QTableWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_secondary']}, 
                    stop:1 {COLOR_PALETTE['bg_primary']});
                alternate-background-color: {COLOR_PALETTE['bg_tertiary']};
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 8px;
                gridline-color: {COLOR_PALETTE['neutral']};
                selection-background-color: {COLOR_PALETTE['accent_blue']};
                font-size: 10pt;
            }}
            QTableWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {COLOR_PALETTE['neutral']};
            }}
            QTableWidget::item:selected {{
                background: {COLOR_PALETTE['accent_blue']};
                color: {COLOR_PALETTE['bg_primary']};
            }}
            QHeaderView::section {{
                background: {COLOR_PALETTE['bg_tertiary']};
                color: {COLOR_PALETTE['text_primary']};
                padding: 8px;
                border: 1px solid {COLOR_PALETTE['neutral']};
                font-weight: bold;
            }}
            
            /* Combobox et Line Edit */
            QComboBox, QLineEdit, QSpinBox, QDateTimeEdit {{
                background: {COLOR_PALETTE['bg_tertiary']};
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 6px;
                padding: 6px;
                color: {COLOR_PALETTE['text_primary']};
                font-size: 10pt;
            }}
            QComboBox::drop-down {{
                border: none;
                background: {COLOR_PALETTE['accent_blue']};
                border-radius: 4px;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid {COLOR_PALETTE['text_primary']};
            }}
            QComboBox QAbstractItemView {{
                background: {COLOR_PALETTE['bg_tertiary']};
                border: 1px solid {COLOR_PALETTE['accent_blue']};
                selection-background-color: {COLOR_PALETTE['accent_blue']};
            }}
            
            /* GroupBox */
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
                color: {COLOR_PALETTE['text_primary']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: {COLOR_PALETTE['accent_blue']};
            }}
            
            /* Onglets */
            QTabWidget::pane {{
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 8px;
                background: {COLOR_PALETTE['bg_secondary']};
            }}
            QTabBar::tab {{
                background: {COLOR_PALETTE['bg_tertiary']};
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                padding: 10px 20px;
                margin-right: 4px;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QTabBar::tab:selected {{
                background: {COLOR_PALETTE['accent_blue']};
                color: {COLOR_PALETTE['bg_primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background: rgba(0, 212, 255, 0.3);
            }}
            
            /* Barre de progression */
            QProgressBar {{
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 6px;
                text-align: center;
                background: {COLOR_PALETTE['bg_tertiary']};
                color: {COLOR_PALETTE['text_primary']};
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_PALETTE['accent_blue']}, 
                    stop:1 {COLOR_PALETTE['accent_green']});
                border-radius: 4px;
            }}
            
            /* Scrollbars */
            QScrollBar:vertical {{
                background: {COLOR_PALETTE['bg_tertiary']};
                width: 16px;
                border-radius: 8px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {COLOR_PALETTE['accent_blue']};
                border-radius: 8px;
                min-height: 20px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {COLOR_PALETTE['accent_green']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            
            /* Labels */
            QLabel {{
                color: {COLOR_PALETTE['text_primary']};
                font-size: 10pt;
            }}
            
            /* Checkbox */
            QCheckBox {{
                color: {COLOR_PALETTE['text_primary']};
                font-size: 10pt;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 4px;
                background: {COLOR_PALETTE['bg_tertiary']};
            }}
            QCheckBox::indicator:checked {{
                background: {COLOR_PALETTE['accent_blue']};
                image: none;
            }}
            
            /* Menu */
            QMenuBar {{
                background: {COLOR_PALETTE['bg_tertiary']};
                color: {COLOR_PALETTE['text_primary']};
                border-bottom: 2px solid {COLOR_PALETTE['accent_blue']};
            }}
            QMenuBar::item {{
                background: transparent;
                padding: 8px 12px;
            }}
            QMenuBar::item:selected {{
                background: {COLOR_PALETTE['accent_blue']};
                color: {COLOR_PALETTE['bg_primary']};
            }}
            QMenu {{
                background: {COLOR_PALETTE['bg_tertiary']};
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                color: {COLOR_PALETTE['text_primary']};
            }}
            QMenu::item {{
                padding: 8px 24px;
            }}
            QMenu::item:selected {{
                background: {COLOR_PALETTE['accent_blue']};
                color: {COLOR_PALETTE['bg_primary']};
            }}
            
            /* Barre de statut */
            QStatusBar {{
                background: {COLOR_PALETTE['bg_tertiary']};
                color: {COLOR_PALETTE['text_primary']};
                border-top: 2px solid {COLOR_PALETTE['accent_blue']};
            }}
        """)

class StatsCard(QFrame):
    """Carte de statistiques avec thème moderne"""
    
    def __init__(self, title: str, icon: str, value: str = "0"):
        super().__init__()
        self.setFixedHeight(100)
        self.setFrameStyle(QFrame.Box)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Header avec icône et titre
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 24px; color: {COLOR_PALETTE['accent_blue']};")
        icon_label.setFixedWidth(32)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLOR_PALETTE['text_secondary']}; font-size: 11px; font-weight: 600;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valeur
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-size: 18px; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
        # Style de la carte
        self.setStyleSheet(f"""
            StatsCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_tertiary']}, 
                    stop:1 {COLOR_PALETTE['bg_secondary']});
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 12px;
            }}
        """)
        
    def setValue(self, value: str):
        self.value_label.setText(value)

class EnhancedLogTable(QTableWidget):
    """Table de logs améliorée avec couleurs par niveau"""
    
    def __init__(self):
        super().__init__()
        self.setup_table()
        
    def setup_table(self):
        """Configure la table"""
        headers = ["⏰ Timestamp", "📊 Level", "🏷️ Logger", "💬 Message", "📁 Module", "🔧 Function"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSortingEnabled(True)
        self.setShowGrid(True)
        
        # Redimensionnement des colonnes
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
    def add_log_entry(self, entry: LogEntry, auto_scroll: bool = True):
        """Ajoute une entrée de log avec couleurs"""
        row = self.rowCount()
        self.insertRow(row)
        
        # Couleurs par niveau
        level_colors = {
            'DEBUG': COLOR_PALETTE['neutral'],
            'INFO': COLOR_PALETTE['accent_blue'],
            'WARNING': COLOR_PALETTE['warning'], 
            'ERROR': COLOR_PALETTE['error'],
            'CRITICAL': COLOR_PALETTE['accent_purple']
        }
        
        level_color = level_colors.get(entry.level.value[0], COLOR_PALETTE['text_primary'])
        
        # Timestamp
        timestamp_item = QTableWidgetItem(entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        timestamp_item.setForeground(QColor(COLOR_PALETTE['text_secondary']))
        self.setItem(row, 0, timestamp_item)
        
        # Level avec couleur et icône
        level_icons = {
            'DEBUG': '🐛',
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌', 
            'CRITICAL': '💥'
        }
        level_icon = level_icons.get(entry.level.value[0], '📝')
        level_item = QTableWidgetItem(f"{level_icon} {entry.level.value[0]}")
        level_item.setForeground(QColor(level_color))
        level_item.setData(Qt.UserRole, entry.level.value[0])
        self.setItem(row, 1, level_item)
        
        # Logger
        logger_item = QTableWidgetItem(entry.logger_name)
        logger_item.setForeground(QColor(COLOR_PALETTE['accent_green']))
        self.setItem(row, 2, logger_item)
        
        # Message
        message_item = QTableWidgetItem(entry.message)
        message_item.setToolTip(entry.message)
        message_item.setForeground(QColor(COLOR_PALETTE['text_primary']))
        self.setItem(row, 3, message_item)
        
        # Module
        module_item = QTableWidgetItem(entry.module)
        module_item.setForeground(QColor(COLOR_PALETTE['text_secondary']))
        self.setItem(row, 4, module_item)
        
        # Function
        function_item = QTableWidgetItem(entry.function)
        function_item.setForeground(QColor(COLOR_PALETTE['text_secondary']))
        self.setItem(row, 5, function_item)
        
        # Scroll automatique seulement si demandé
        if auto_scroll:
            self.scrollToBottom()
    
    def update_logs(self, logs: List[LogEntry]):
        """Met à jour la table avec une liste de logs (optimisé)"""
        self.setRowCount(0)
        
        # Désactive temporairement le tri pour améliorer les performances
        self.setSortingEnabled(False)
        
        # Ajoute les logs sans auto-scroll
        for log in reversed(logs):
            self.add_log_entry(log, auto_scroll=False)
        
        # Réactive le tri
        self.setSortingEnabled(True)
        
        # Un seul scroll à la fin
        self.scrollToBottom()

class FilterPanel(QWidget):
    """Panel de filtrage moderne"""
    
    filter_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Groupe de filtres
        filter_group = QGroupBox("🔍 Filtres Avancés")
        filter_layout = QGridLayout(filter_group)
        
        # Niveau
        filter_layout.addWidget(QLabel("Niveau:"), 0, 0)
        self.level_combo = QComboBox()
        self.level_combo.addItems(["🌟 Tous", "🐛 DEBUG", "ℹ️ INFO", "⚠️ WARNING", "❌ ERROR", "💥 CRITICAL"])
        self.level_combo.currentTextChanged.connect(self.filter_changed)
        filter_layout.addWidget(self.level_combo, 0, 1)
        
        # Logger
        filter_layout.addWidget(QLabel("Logger:"), 1, 0)
        self.logger_combo = QComboBox()
        self.logger_combo.setEditable(True)
        self.logger_combo.addItem("📋 Tous")
        self.logger_combo.currentTextChanged.connect(self.filter_changed)
        filter_layout.addWidget(self.logger_combo, 1, 1)
        
        # Recherche
        filter_layout.addWidget(QLabel("Recherche:"), 2, 0)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔎 Rechercher dans les messages...")
        self.search_edit.textChanged.connect(self.filter_changed)
        filter_layout.addWidget(self.search_edit, 2, 1)
        
        # Dates
        filter_layout.addWidget(QLabel("Date début:"), 3, 0)
        self.start_date = QDateTimeEdit()
        self.start_date.setDateTime(QDateTime.currentDateTime().addDays(-7))
        self.start_date.setCalendarPopup(True)
        self.start_date.dateTimeChanged.connect(self.filter_changed)
        filter_layout.addWidget(self.start_date, 3, 1)
        
        filter_layout.addWidget(QLabel("Date fin:"), 4, 0)
        self.end_date = QDateTimeEdit()
        self.end_date.setDateTime(QDateTime.currentDateTime())
        self.end_date.setCalendarPopup(True)
        self.end_date.dateTimeChanged.connect(self.filter_changed)
        filter_layout.addWidget(self.end_date, 4, 1)
        
        # Limite
        filter_layout.addWidget(QLabel("Limite:"), 5, 0)
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(10, 10000)
        self.limit_spin.setValue(500)  # Valeur par défaut réduite pour de meilleures performances
        self.limit_spin.valueChanged.connect(self.filter_changed)
        filter_layout.addWidget(self.limit_spin, 5, 1)
        
        layout.addWidget(filter_group)
        
        # Boutons d'action
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Actualiser")
        self.refresh_btn.clicked.connect(self.filter_changed)
        button_layout.addWidget(self.refresh_btn)
        
        self.clear_btn = QPushButton("🗑️ Effacer")
        button_layout.addWidget(self.clear_btn)
        
        self.export_btn = QPushButton("💾 Exporter")
        button_layout.addWidget(self.export_btn)
        
        layout.addLayout(button_layout)
        
        # Auto-scroll
        self.auto_scroll_cb = QCheckBox("📜 Auto-scroll")
        self.auto_scroll_cb.setChecked(True)
        layout.addWidget(self.auto_scroll_cb)
        
        layout.addStretch()
        
    def get_filter_params(self):
        """Retourne les paramètres de filtrage"""
        level_text = self.level_combo.currentText()
        level_filter = None if "Tous" in level_text else [level_text.split(" ", 1)[1]]
        
        logger_text = self.logger_combo.currentText()
        logger_filter = None if "Tous" in logger_text else logger_text.replace("📋 ", "")
        
        return {
            'limit': self.limit_spin.value(),
            'level_filter': level_filter,
            'search_term': self.search_edit.text() or None,
            'start_date': self.start_date.dateTime().toPython(),
            'end_date': self.end_date.dateTime().toPython(),
            'logger_filter': logger_filter
        }
    
    def update_loggers(self, loggers: List[str]):
        """Met à jour la liste des loggers"""
        current = self.logger_combo.currentText()
        self.logger_combo.clear()
        self.logger_combo.addItem("📋 Tous")
        for logger in sorted(loggers):
            self.logger_combo.addItem(f"🏷️ {logger}")
        
        # Restore selection
        index = self.logger_combo.findText(current)
        if index >= 0:
            self.logger_combo.setCurrentIndex(index)

class StatsPanel(QWidget):
    """Panel de statistiques moderne"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("📊 Statistiques des Logs")
        title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLOR_PALETTE['accent_blue']}; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Cartes de stats
        self.total_card = StatsCard("Total Logs", "📊", "0")
        layout.addWidget(self.total_card)
        
        self.error_card = StatsCard("Erreurs", "❌", "0") 
        layout.addWidget(self.error_card)
        
        self.warning_card = StatsCard("Warnings", "⚠️", "0")
        layout.addWidget(self.warning_card)
        
        self.info_card = StatsCard("Infos", "ℹ️", "0")
        layout.addWidget(self.info_card)
        
        layout.addStretch()
        
    def update_stats(self, stats: Dict):
        """Met à jour les statistiques"""
        level_stats = stats.get('level_stats', {})
        total = stats.get('total_logs', 0)
        
        self.total_card.setValue(f"{total:,}")
        self.error_card.setValue(str(level_stats.get('ERROR', 0)))
        self.warning_card.setValue(str(level_stats.get('WARNING', 0)))
        self.info_card.setValue(str(level_stats.get('INFO', 0)))

class EnhancedLogViewer(QMainWindow):
    """Visionneur de logs avancé avec thème moderne"""
    
    def __init__(self):
        super().__init__()
        
        # Initialisation du gestionnaire de logs
        self.log_manager = get_log_manager()
        if not self.log_manager:
            # Déterminer les chemins appropriés
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(project_root, "data", "logs.db")
            config_path = os.path.join(project_root, "JSON", "log_config.json")
            
            try:
                self.log_manager = LogManager(db_path, config_path)
            except Exception as e:
                print(f"Erreur initialisation LogManager: {e}")
                # Gestionnaire par défaut si échec
                self.log_manager = LogManager(db_path)
        
        self.setup_ui()
        self.setup_connections()
        self.setup_timers()
        
        # Chargement initial avec limite réduite
        self.refresh_logs()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setWindowTitle("🤖 Kira-Bot - Visionneur de Logs Avancé")
        self.setGeometry(100, 100, 1600, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Panel gauche
        left_panel = QWidget()
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        
        # Filtres
        self.filter_panel = FilterPanel()
        left_layout.addWidget(self.filter_panel)
        
        # Statistiques
        self.stats_panel = StatsPanel()
        left_layout.addWidget(self.stats_panel)
        
        main_splitter.addWidget(left_panel)
        
        # Panel principal
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Onglets
        self.tab_widget = QTabWidget()
        
        # Onglet Table
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        
        self.log_table = EnhancedLogTable()
        table_layout.addWidget(self.log_table)
        
        self.tab_widget.addTab(table_widget, "📋 Table des Logs")
        
        # Onglet Texte
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        text_layout.addWidget(self.log_text)
        
        self.tab_widget.addTab(text_widget, "📄 Vue Texte")
        
        right_layout.addWidget(self.tab_widget)
        main_splitter.addWidget(right_panel)
        
        # Proportions
        main_splitter.setSizes([400, 1200])
        
        # Barre de statut
        self.statusBar().showMessage("✨ Prêt - Kira-Bot Log Viewer")
        
        # Menu
        self.create_menu()
        
    def create_menu(self):
        """Crée le menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("📁 Fichier")
        
        export_action = QAction("💾 Exporter les logs", self)
        export_action.triggered.connect(self.export_logs)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("❌ Quitter", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Outils
        tools_menu = menubar.addMenu("🔧 Outils")
        
        refresh_action = QAction("🔄 Actualiser", self)
        refresh_action.triggered.connect(self.refresh_logs)
        tools_menu.addAction(refresh_action)
        
        cleanup_action = QAction("🧹 Nettoyer anciens logs", self)
        cleanup_action.triggered.connect(self.cleanup_logs)
        tools_menu.addAction(cleanup_action)
        
    def setup_connections(self):
        """Configure les connexions"""
        self.filter_panel.filter_changed.connect(self.refresh_logs)
        self.filter_panel.clear_btn.clicked.connect(self.clear_display)
        self.filter_panel.export_btn.clicked.connect(self.export_logs)
        
    def setup_timers(self):
        """Configure les timers"""
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(5000)
        
    def refresh_logs(self):
        """Actualise les logs"""
        try:
            filter_params = self.filter_panel.get_filter_params()
            logs = self.log_manager.log_db.get_logs(**filter_params)
            
            # Met à jour la table
            self.log_table.update_logs(logs)
            
            # Met à jour le texte
            self.update_text_view(logs)
            
            # Met à jour les loggers
            loggers = list(set(log.logger_name for log in logs))
            self.filter_panel.update_loggers(loggers)
            
            self.statusBar().showMessage(f"✨ {len(logs)} logs chargés")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement: {e}")
            
    def update_text_view(self, logs: List[LogEntry]):
        """Met à jour la vue texte"""
        self.log_text.clear()
        
        for log in reversed(logs):
            timestamp = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            # Couleurs par niveau
            level_colors = {
                'DEBUG': COLOR_PALETTE['neutral'],
                'INFO': COLOR_PALETTE['accent_blue'], 
                'WARNING': COLOR_PALETTE['warning'],
                'ERROR': COLOR_PALETTE['error'],
                'CRITICAL': COLOR_PALETTE['accent_purple']
            }
            
            level_color = level_colors.get(log.level.value[0], COLOR_PALETTE['text_primary'])
            
            # Icônes
            level_icons = {
                'DEBUG': '🐛',
                'INFO': 'ℹ️',
                'WARNING': '⚠️', 
                'ERROR': '❌',
                'CRITICAL': '💥'
            }
            icon = level_icons.get(log.level.value[0], '📝')
            
            html_line = (
                f"<span style='color: {COLOR_PALETTE['text_secondary']}'>[{timestamp}]</span> "
                f"<span style='color: {level_color}; font-weight: bold'>{icon} {log.level.value[0]}</span> "
                f"<span style='color: {COLOR_PALETTE['accent_green']}'>{log.logger_name}</span> - "
                f"<span style='color: {COLOR_PALETTE['text_primary']}'>{log.message}</span>"
            )
            
            self.log_text.append(html_line)
            
    def update_stats(self):
        """Met à jour les statistiques"""
        try:
            stats = self.log_manager.log_db.get_log_stats(7)
            self.stats_panel.update_stats(stats)
        except Exception as e:
            print(f"Erreur stats: {e}")
            
    def clear_display(self):
        """Efface l'affichage"""
        self.log_table.setRowCount(0)
        self.log_text.clear()
        self.statusBar().showMessage("🗑️ Affichage effacé")
        
    def export_logs(self):
        """Exporte les logs"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les logs",
            f"kira_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON (*.json);;CSV (*.csv);;Texte (*.txt)"
        )
        
        if file_path:
            try:
                filter_params = self.filter_panel.get_filter_params()
                logs = self.log_manager.log_db.get_logs(**filter_params)
                
                # Export simple en JSON
                import json
                data = []
                for log in logs:
                    data.append({
                        'timestamp': log.timestamp.isoformat(),
                        'level': log.level.value[0],
                        'logger': log.logger_name,
                        'message': log.message,
                        'module': log.module,
                        'function': log.function
                    })
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                QMessageBox.information(self, "Succès", f"✅ Logs exportés vers:\n{file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"❌ Erreur export: {e}")
                
    def cleanup_logs(self):
        """Nettoie les anciens logs"""
        days, ok = QInputDialog.getInt(
            self,
            "Nettoyage des logs",
            "Conserver les logs des N derniers jours:",
            30, 1, 365, 1
        )
        
        if ok:
            try:
                deleted = self.log_manager.log_db.cleanup_old_logs(days)
                QMessageBox.information(
                    self, 
                    "Nettoyage terminé", 
                    f"🧹 {deleted} entrées supprimées"
                )
                self.refresh_logs()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"❌ Erreur nettoyage: {e}")

def main():
    """Point d'entrée principal"""
    # Vérifier si une application Qt existe déjà
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        need_exec = True
    else:
        need_exec = False
    
    # Applique le thème
    KiraTheme.apply(app)
    
    # Crée et affiche la fenêtre
    viewer = EnhancedLogViewer()
    viewer.show()
    
    # Seule l'application principale doit contrôler la boucle d'événements
    if need_exec:
        sys.exit(app.exec())
    
    # Retourner la fenêtre pour que l'app principale puisse la gérer
    return viewer

if __name__ == "__main__":
    main()