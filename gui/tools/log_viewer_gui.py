#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visionneur de Logs Unifié pour Kira-Bot
Fusion optimisée : fonctionnalités complètes + thème moderne
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

# Configuration des couleurs - thème moderne Kira-Bot
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
    """Thème moderne unifié pour Kira-Bot"""
    
    @staticmethod
    def apply(app: QApplication):
        """Applique le thème Kira-Bot"""
        app.setStyle('Fusion')
        
        # Palette de couleurs
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(COLOR_PALETTE['bg_primary']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(COLOR_PALETTE['text_primary']))
        palette.setColor(QPalette.ColorRole.Base, QColor(COLOR_PALETTE['bg_secondary']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLOR_PALETTE['bg_tertiary']))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(COLOR_PALETTE['bg_secondary']))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(COLOR_PALETTE['text_primary']))
        palette.setColor(QPalette.ColorRole.Text, QColor(COLOR_PALETTE['text_primary']))
        palette.setColor(QPalette.ColorRole.Button, QColor(COLOR_PALETTE['bg_tertiary']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLOR_PALETTE['text_primary']))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(COLOR_PALETTE['error']))
        palette.setColor(QPalette.ColorRole.Link, QColor(COLOR_PALETTE['accent_blue']))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(COLOR_PALETTE['accent_blue']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLOR_PALETTE['bg_primary']))
        
        app.setPalette(palette)
        
        # Style CSS moderne et complet
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
            
            /* Table améliorée */
            QTableWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PALETTE['bg_secondary']}, 
                    stop:1 {COLOR_PALETTE['bg_primary']});
                alternate-background-color: {COLOR_PALETTE['bg_tertiary']};
                border: 2px solid {COLOR_PALETTE['accent_blue']};
                border-radius: 8px;
                gridline-color: {COLOR_PALETTE['neutral']};
                selection-background-color: {COLOR_PALETTE['accent_blue']};
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10pt;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {COLOR_PALETTE['neutral']};
            }}
            QTableWidget::item:selected {{
                background: {COLOR_PALETTE['accent_blue']};
                color: {COLOR_PALETTE['bg_primary']};
            }}
            QHeaderView::section {{
                background: {COLOR_PALETTE['bg_tertiary']};
                color: {COLOR_PALETTE['text_primary']};
                padding: 10px;
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
            
            /* GroupBox moderne */
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
            
            /* Scrollbars modernes */
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
            
            /* Labels et Checkbox */
            QLabel {{
                color: {COLOR_PALETTE['text_primary']};
                font-size: 10pt;
            }}
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
        """)

class StatsCard(QFrame):
    """Carte de statistiques moderne"""
    
    def __init__(self, title: str, icon: str, value: str = "0"):
        super().__init__()
        self.setFixedHeight(75)  # Plus compact
        self.setFrameStyle(QFrame.Shape.Box)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(2)
        
        # Header avec icône et titre
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 18px; color: {COLOR_PALETTE['accent_blue']};")
        icon_label.setFixedWidth(24)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLOR_PALETTE['text_secondary']}; font-size: 10px; font-weight: 600;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valeur
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-size: 14px; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

class LogTableWidget(QTableWidget):
    """Widget de table personnalisé pour afficher les logs avec thème moderne"""
    
    def __init__(self):
        super().__init__()
        self.setup_table()
        
    def setup_table(self):
        """Configure la table"""
        # Colonnes
        headers = ["⏰ Timestamp", "🎯 Level", "📋 Logger", "💬 Message", "📁 Module", "⚙️ Function"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Configuration
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSortingEnabled(True)
        
        # Redimensionnement des colonnes
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Timestamp
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Level
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Logger
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)           # Message
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Module
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Function
        
    def add_log_entry(self, entry: LogEntry):
        """Ajoute une entrée de log à la table"""
        row = self.rowCount()
        self.insertRow(row)
        
        # Timestamp
        timestamp_item = QTableWidgetItem(entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        timestamp_item.setData(Qt.ItemDataRole.UserRole, entry.timestamp)
        self.setItem(row, 0, timestamp_item)
        
        # Level avec couleur
        level_item = QTableWidgetItem(entry.level.value[0])
        level_color = QColor(entry.level.value[1])
        level_item.setForeground(level_color)
        level_item.setData(Qt.ItemDataRole.UserRole, entry.level.value[0])
        self.setItem(row, 1, level_item)
        
        # Logger
        logger_item = QTableWidgetItem(entry.logger_name)
        self.setItem(row, 2, logger_item)
        
        # Message
        message_item = QTableWidgetItem(entry.message)
        message_item.setToolTip(entry.message)  # Tooltip pour les longs messages
        self.setItem(row, 3, message_item)
        
        # Module
        module_item = QTableWidgetItem(entry.module)
        self.setItem(row, 4, module_item)
        
        # Function
        function_item = QTableWidgetItem(entry.function)
        self.setItem(row, 5, function_item)
        
        # Scroll vers le bas si auto-scroll activé
        if hasattr(self.parent(), 'auto_scroll_enabled') and self.parent().auto_scroll_enabled:
            self.scrollToBottom()
    
    def clear_logs(self):
        """Efface tous les logs de la table"""
        self.setRowCount(0)
    
    def update_logs(self, logs: List[LogEntry]):
        """Met à jour la table avec une liste de logs"""
        self.clear_logs()
        for log in reversed(logs):  # Plus récents en haut
            self.add_log_entry(log)

class LogStatsWidget(QWidget):
    """Widget pour afficher les statistiques des logs avec cartes modernes"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)
        
        # Titre plus compact
        title = QLabel("📊 Statistiques")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {COLOR_PALETTE['accent_blue']}; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Conteneur pour les cartes de statistiques
        cards_layout = QGridLayout()
        cards_layout.setSpacing(6)  # Espacement réduit
        
        # Cartes de statistiques modernes
        self.total_card = StatsCard("Total", "📊", "0")
        self.error_card = StatsCard("Erreurs", "❌", "0")
        self.warning_card = StatsCard("Warnings", "⚠️", "0")
        self.info_card = StatsCard("Info", "ℹ️", "0")
        
        cards_layout.addWidget(self.total_card, 0, 0)
        cards_layout.addWidget(self.error_card, 0, 1)
        cards_layout.addWidget(self.warning_card, 1, 0)
        cards_layout.addWidget(self.info_card, 1, 1)
        
        layout.addLayout(cards_layout)
        
        # Spacer pour pousser le contenu vers le haut
        layout.addStretch()
        
    def update_stats(self, stats: Dict):
        """Met à jour les statistiques"""
        level_stats = stats.get('level_stats', {})
        total = stats.get('total_logs', 0)
        
        self.total_card.setValue(f"{total:,}")
        self.error_card.setValue(f"{level_stats.get('ERROR', 0):,}")
        self.warning_card.setValue(f"{level_stats.get('WARNING', 0):,}")
        self.info_card.setValue(f"{level_stats.get('INFO', 0):,}")

class LogFilterWidget(QWidget):
    """Widget pour filtrer les logs avec interface moderne"""
    
    filter_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface de filtrage"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)
        
        # Groupe de filtres principal
        filter_group = QGroupBox("🔍 Filtres Avancés")
        filter_layout = QGridLayout(filter_group)
        filter_layout.setContentsMargins(12, 20, 12, 12)
        filter_layout.setHorizontalSpacing(8)
        filter_layout.setVerticalSpacing(10)
        filter_layout.setColumnStretch(1, 1)  # La colonne des widgets s'étire
        
        # Filtre par niveau
        level_label = QLabel("🎯 Niveau:")
        level_label.setFixedWidth(80)
        filter_layout.addWidget(level_label, 0, 0)
        self.level_combo = QComboBox()
        self.level_combo.setFixedHeight(30)
        self.level_combo.addItems(["Tous", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.level_combo.currentTextChanged.connect(lambda: self.filter_changed.emit())
        filter_layout.addWidget(self.level_combo, 0, 1)
        
        # Filtre par logger
        logger_label = QLabel("📋 Logger:")
        logger_label.setFixedWidth(80)
        filter_layout.addWidget(logger_label, 1, 0)
        self.logger_combo = QComboBox()
        self.logger_combo.setFixedHeight(30)
        self.logger_combo.setEditable(True)
        self.logger_combo.addItem("Tous")
        self.logger_combo.currentTextChanged.connect(lambda: self.filter_changed.emit())
        filter_layout.addWidget(self.logger_combo, 1, 1)
        
        # Recherche dans le message
        search_label = QLabel("🔍 Recherche:")
        search_label.setFixedWidth(80)
        filter_layout.addWidget(search_label, 2, 0)
        self.search_edit = QLineEdit()
        self.search_edit.setFixedHeight(30)
        self.search_edit.setPlaceholderText("Rechercher...")
        self.search_edit.textChanged.connect(lambda: self.filter_changed.emit())
        filter_layout.addWidget(self.search_edit, 2, 1)
        
        # Filtre par date
        start_label = QLabel("📅 Début:")
        start_label.setFixedWidth(80)
        filter_layout.addWidget(start_label, 3, 0)
        self.start_date = QDateTimeEdit()
        self.start_date.setFixedHeight(30)
        self.start_date.setDateTime(QDateTime.currentDateTime().addDays(-7))
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("dd/MM/yyyy hh:mm")
        self.start_date.dateTimeChanged.connect(lambda: self.filter_changed.emit())
        filter_layout.addWidget(self.start_date, 3, 1)
        
        end_label = QLabel("📅 Fin:")
        end_label.setFixedWidth(80)
        filter_layout.addWidget(end_label, 4, 0)
        self.end_date = QDateTimeEdit()
        self.end_date.setFixedHeight(30)
        self.end_date.setDateTime(QDateTime.currentDateTime())
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("dd/MM/yyyy hh:mm")
        self.end_date.dateTimeChanged.connect(lambda: self.filter_changed.emit())
        filter_layout.addWidget(self.end_date, 4, 1)
        
        # Limite d'entrées
        limit_label = QLabel("📊 Limite:")
        limit_label.setFixedWidth(80)
        filter_layout.addWidget(limit_label, 5, 0)
        self.limit_spin = QSpinBox()
        self.limit_spin.setFixedHeight(30)
        self.limit_spin.setRange(10, 10000)
        self.limit_spin.setValue(1000)
        self.limit_spin.setSuffix(" logs")
        self.limit_spin.valueChanged.connect(lambda: self.filter_changed.emit())
        filter_layout.addWidget(self.limit_spin, 5, 1)
        
        # Sélecteur de jours de conservation pour le nettoyage
        cleanup_label = QLabel("🗑️ Garder:")
        cleanup_label.setFixedWidth(80)
        filter_layout.addWidget(cleanup_label, 6, 0)
        self.cleanup_days_spin = QSpinBox()
        self.cleanup_days_spin.setFixedHeight(30)
        self.cleanup_days_spin.setRange(1, 3650)
        self.cleanup_days_spin.setValue(30)
        self.cleanup_days_spin.setSuffix(" jours")
        filter_layout.addWidget(self.cleanup_days_spin, 6, 1)
        
        layout.addWidget(filter_group)
        
        # Groupe de boutons d'action
        action_group = QGroupBox("⚙️ Actions")
        buttons_layout = QGridLayout(action_group)
        buttons_layout.setContentsMargins(10, 15, 10, 10)
        buttons_layout.setHorizontalSpacing(8)
        buttons_layout.setVerticalSpacing(8)
        buttons_layout.setColumnStretch(0, 1)
        buttons_layout.setColumnStretch(1, 1)
        
        self.refresh_btn = QPushButton("🔄 Actualiser")
        self.refresh_btn.setFixedHeight(32)
        self.refresh_btn.clicked.connect(self.filter_changed.emit)
        buttons_layout.addWidget(self.refresh_btn, 0, 0)
        
        self.clear_btn = QPushButton("🗑️ Effacer")
        self.clear_btn.setFixedHeight(32)
        buttons_layout.addWidget(self.clear_btn, 0, 1)
        
        self.export_btn = QPushButton("💾 Exporter")
        self.export_btn.setFixedHeight(32)
        buttons_layout.addWidget(self.export_btn, 1, 0)
        
        self.purge_btn = QPushButton("🧹 Purger")
        self.purge_btn.setFixedHeight(32)
        buttons_layout.addWidget(self.purge_btn, 1, 1)
        
        layout.addWidget(action_group)
        
        # Options
        options_group = QGroupBox("⚙️ Options")
        options_layout = QVBoxLayout(options_group)
        options_layout.setContentsMargins(10, 15, 10, 10)
        options_layout.setSpacing(8)
        
        self.auto_scroll_cb = QCheckBox("🔄 Auto-scroll activé")
        self.auto_scroll_cb.setChecked(True)
        self.auto_scroll_cb.setFixedHeight(25)
        options_layout.addWidget(self.auto_scroll_cb)
        
        layout.addWidget(options_group)
        
        # Spacer pour pousser le contenu vers le haut
        layout.addStretch(1)
        
    def get_filter_params(self) -> Dict:
        """Récupère les paramètres de filtrage"""
        params = {
            'limit': self.limit_spin.value(),
            'start_date': self.start_date.dateTime().toPython(),
            'end_date': self.end_date.dateTime().toPython()
        }
        
        # Filtre par niveau
        if self.level_combo.currentText() != "Tous":
            params['level'] = self.level_combo.currentText()
            
        # Filtre par logger
        if self.logger_combo.currentText() != "Tous":
            params['logger_name'] = self.logger_combo.currentText()
            
        # Recherche dans le message
        search_text = self.search_edit.text().strip()
        if search_text:
            params['message_contains'] = search_text
            
        return params

class LogViewerMainWindow(QMainWindow):
    """Fenêtre principale unifiée du visualiseur de logs"""
    
    def __init__(self):
        super().__init__()
        self.log_manager = get_log_manager()
        self.auto_scroll_enabled = True
        
        if not self.log_manager:
            # Initialiser le LogManager si nécessaire
            try:
                from tools.advanced_logging import LogManager
                
                # Déterminer les chemins appropriés
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                db_path = os.path.join(project_root, "data", "logs.db")
                config_path = os.path.join(project_root, "JSON", "log_config.json")
                
                self.log_manager = LogManager(db_path, config_path)
                print(f"✅ LogManager initialisé: {db_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'initialiser le gestionnaire de logs:\n{e}")
                sys.exit(1)
        
        self.setup_ui()
        self.setup_connections()
        self.setup_timers()
        self.setup_system_tray()
        self.setup_shortcuts()
        
        # Charge les logs initiaux
        self.refresh_logs()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setWindowTitle("🤖 Kira-Bot - Visionneur de Logs Unifié")
        self.setGeometry(100, 100, 1200, 700)
        
        # Lancement automatique en plein écran
        self.showMaximized()
        print("🖥️ Log Viewer lancé en plein écran")
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Panel gauche - Filtres et statistiques
        left_panel = QWidget()
        left_panel.setMinimumWidth(280)
        left_panel.setMaximumWidth(380)  # Plus compact
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(8)
        
        # Widget de filtrage
        self.filter_widget = LogFilterWidget()
        left_layout.addWidget(self.filter_widget)
        
        # Widget de statistiques
        self.stats_widget = LogStatsWidget()
        left_layout.addWidget(self.stats_widget)
        
        main_splitter.addWidget(left_panel)
        
        # Panel central - Table des logs
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(8, 8, 8, 8)
        
        # En-tête
        header_layout = QHBoxLayout()
        title_label = QLabel("📋 Logs en Temps Réel")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {COLOR_PALETTE['accent_blue']};")
        header_layout.addWidget(title_label)
        
        # Indicateur de statut
        self.status_label = QLabel("🟢 Connecté")
        self.status_label.setStyleSheet(f"color: {COLOR_PALETTE['success']}; font-weight: bold;")
        header_layout.addWidget(self.status_label)
        header_layout.addStretch()
        
        center_layout.addLayout(header_layout)
        
        # Table des logs
        self.log_table = LogTableWidget()
        center_layout.addWidget(self.log_table)
        
        main_splitter.addWidget(center_widget)
        
        # Répartition des tailles (plus flexible)
        main_splitter.setSizes([350, 850])
        main_splitter.setStretchFactor(0, 0)  # Panel gauche ne s'étire pas trop
        main_splitter.setStretchFactor(1, 1)  # Panel central prend l'espace restant
        
        # Barre d'état
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background: {COLOR_PALETTE['bg_tertiary']};
                color: {COLOR_PALETTE['text_primary']};
                border-top: 2px solid {COLOR_PALETTE['accent_blue']};
                font-weight: bold;
            }}
        """)
        self.statusBar().showMessage("🚀 Visualiseur de logs unifié initialisé")
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        # Filtres
        self.filter_widget.filter_changed.connect(self.refresh_logs)
        
        # Boutons
        self.filter_widget.clear_btn.clicked.connect(self.clear_display)
        self.filter_widget.export_btn.clicked.connect(self.export_logs)
        self.filter_widget.purge_btn.clicked.connect(self.cleanup_logs)
        
        # Auto-scroll
        self.filter_widget.auto_scroll_cb.toggled.connect(self.set_auto_scroll)
        
    def setup_timers(self):
        """Configure les timers"""
        # Timer pour rafraîchir les logs automatiquement
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_logs)
        self.refresh_timer.start(5000)  # Rafraîchir toutes les 5 secondes
        
        # Timer pour mettre à jour les statistiques
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(10000)  # Mettre à jour toutes les 10 secondes
        
    def setup_system_tray(self):
        """Configure l'icône de la barre système"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            # Menu contextuel
            tray_menu = QMenu()
            
            show_action = QAction("Afficher", self)
            show_action.triggered.connect(self.show)
            tray_menu.addAction(show_action)
            
            hide_action = QAction("Masquer", self)
            hide_action.triggered.connect(self.hide)
            tray_menu.addAction(hide_action)
            
            tray_menu.addSeparator()
            
            quit_action = QAction("Quitter", self)
            quit_action.triggered.connect(self.close)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
    
    def setup_shortcuts(self):
        """Configure les raccourcis clavier"""
        from PySide6.QtGui import QShortcut, QKeySequence
        
        # F11: Basculer plein écran/fenêtré
        self.fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
        self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)
        
        # F5: Actualiser les logs
        self.refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        self.refresh_shortcut.activated.connect(self.refresh_logs)
    
    def toggle_fullscreen(self):
        """Basculer entre plein écran et mode fenêtré"""
        if self.isFullScreen():
            self.showMaximized()
            self.statusBar().showMessage("🖥️ Mode fenêtré maximisé activé", 2000)
        else:
            self.showFullScreen()
            self.statusBar().showMessage("🖥️ Mode plein écran activé", 2000)
        
    def refresh_logs(self):
        """Rafraîchit l'affichage des logs"""
        if not self.log_manager:
            return
        
        try:
            # Récupère les paramètres de filtrage
            filter_params = self.filter_widget.get_filter_params()
            
            # Récupère les logs
            logs = self.log_manager.get_logs(**filter_params)
            
            # Met à jour la table
            self.log_table.update_logs(logs)
            
            # Met à jour le statut
            self.status_label.setText(f"🟢 {len(logs)} logs affichés")
            self.statusBar().showMessage(f"Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')} - {len(logs)} entrées")
            
        except Exception as e:
            self.status_label.setText("🔴 Erreur")
            self.statusBar().showMessage(f"Erreur lors du rafraîchissement: {e}")
            
    def update_stats(self):
        """Met à jour les statistiques"""
        if not self.log_manager:
            return
        
        try:
            stats = self.log_manager.get_stats()
            self.stats_widget.update_stats(stats)
        except Exception as e:
            print(f"Erreur lors de la mise à jour des stats: {e}")
    
    def set_auto_scroll(self, enabled: bool):
        """Active/désactive l'auto-scroll"""
        self.auto_scroll_enabled = enabled
        self.log_table.auto_scroll_enabled = enabled
        
    def clear_display(self):
        """Efface l'affichage"""
        self.log_table.clear_logs()
        self.statusBar().showMessage("Affichage effacé")
    
    def export_logs(self):
        """Exporte les logs vers un fichier"""
        if not self.log_manager:
            return
        
        # Dialogue de sauvegarde
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exporter les logs",
            f"kira_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "JSON (*.json);;CSV (*.csv);;Texte (*.txt)"
        )
        
        if not file_path:
            return
        
        try:
            # Détermine le format
            if selected_filter.startswith("JSON"):
                format_type = "json"
            elif selected_filter.startswith("CSV"):
                format_type = "csv"
            else:
                format_type = "txt"
            
            # Récupère les paramètres de filtrage
            filter_params = self.filter_widget.get_filter_params()
            
            # Exporte
            success = self.log_manager.export_logs(file_path, format_type, **filter_params)
            
            if success:
                QMessageBox.information(self, "Succès", f"✅ Logs exportés vers:\n{file_path}")
            else:
                QMessageBox.warning(self, "Erreur", "❌ Erreur lors de l'export des logs")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"❌ Erreur lors de l'export:\n{e}")
    
    def cleanup_logs(self):
        """Nettoie les anciens logs selon le sélecteur de jours"""
        if not self.log_manager:
            return
        
        # Demande confirmation
        days = self.filter_widget.cleanup_days_spin.value()
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous vraiment supprimer tous les logs de plus de {days} jours?\n"
            f"Cette action est irréversible.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                deleted_count = self.log_manager.cleanup_old_logs(days)
                QMessageBox.information(
                    self,
                    "Purge terminée",
                    f"✅ {deleted_count} entrées supprimées"
                )
                self.clear_display()
                self.refresh_logs()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"❌ Erreur lors de la purge:\n{e}")
    
    def closeEvent(self, event):
        """Gère la fermeture de la fenêtre"""
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()

def main():
    """Fonction principale"""
    # Vérifier si une application Qt existe déjà
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        need_exec = True
    else:
        need_exec = False
    
    # Applique le thème Kira-Bot unifié
    KiraTheme.apply(app)
    
    # Crée la fenêtre principale
    window = LogViewerMainWindow()
    window.show()
    
    # Seule l'application principale doit contrôler la boucle d'événements
    if need_exec:
        sys.exit(app.exec())
    
    # Retourner la fenêtre pour que l'app principale puisse la gérer
    return window

if __name__ == "__main__":
    main()