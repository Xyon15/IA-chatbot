"""
Interface graphique avancée pour visualiser les logs de Neuro-Bot
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
    QInputDialog
)
from PySide6.QtCore import (
    QTimer, Qt, QThread, Signal, QDateTime, QSize, QPropertyAnimation,
    QEasingCurve, QRect
)
from PySide6.QtGui import (
    QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush,
    QTextCharFormat, QTextCursor, QAction
)
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QLineSeries, QDateTimeAxis, QValueAxis

# Ajout du répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.advanced_logging import LogManager, LogEntry, LogLevel, get_log_manager

class DarkTheme:
    """Thème sombre pour l'interface"""
    
    @staticmethod
    def apply(app: QApplication):
        """Applique le thème sombre"""
        dark_palette = QPalette()
        
        # Couleurs principales
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        app.setPalette(dark_palette)
        
        # Style CSS pour les widgets spéciaux
        app.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QTableWidget {
                background-color: #1e1e1e;
                alternate-background-color: #2a2a2a;
                border: 1px solid #555;
                border-radius: 5px;
                gridline-color: #555;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #444;
            }
            QTableWidget::item:selected {
                background-color: #2a82da;
            }
            QPushButton {
                background-color: #0d7377;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5d61;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
            QComboBox, QLineEdit, QSpinBox, QDateTimeEdit {
                background-color: #2a2a2a;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #0d7377;
                border-radius: 3px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QTabWidget::pane {
                border: 1px solid #555;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                border: 1px solid #555;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0d7377;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #0d7377;
                border-radius: 5px;
            }
            QScrollBar:vertical {
                background-color: #2a2a2a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #777;
            }
        """)

class LogTableWidget(QTableWidget):
    """Widget de table personnalisé pour afficher les logs"""
    
    def __init__(self):
        super().__init__()
        self.setup_table()
        
    def setup_table(self):
        """Configure la table"""
        # Colonnes
        headers = ["Timestamp", "Level", "Logger", "Message", "Module", "Function"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Configuration
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSortingEnabled(True)
        
        # Redimensionnement des colonnes
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Timestamp
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Level
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Logger
        header.setSectionResizeMode(3, QHeaderView.Stretch)           # Message
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Module
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Function
        
    def add_log_entry(self, entry: LogEntry):
        """Ajoute une entrée de log à la table"""
        row = self.rowCount()
        self.insertRow(row)
        
        # Timestamp
        timestamp_item = QTableWidgetItem(entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        timestamp_item.setData(Qt.UserRole, entry.timestamp)
        self.setItem(row, 0, timestamp_item)
        
        # Level avec couleur
        level_item = QTableWidgetItem(entry.level.value[0])
        level_color = QColor(entry.level.value[1])
        level_item.setForeground(level_color)
        level_item.setData(Qt.UserRole, entry.level.value[0])
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
    """Widget pour afficher les statistiques des logs"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("📊 Statistiques des Logs")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Conteneur pour les stats
        stats_container = QScrollArea()
        stats_widget = QWidget()
        self.stats_layout = QGridLayout(stats_widget)
        stats_container.setWidget(stats_widget)
        stats_container.setWidgetResizable(True)
        layout.addWidget(stats_container)
        
        # Labels pour les statistiques
        self.total_logs_label = QLabel("Total: 0")
        self.error_count_label = QLabel("Erreurs: 0")
        self.warning_count_label = QLabel("Warnings: 0")
        self.info_count_label = QLabel("Info: 0")
        
        # Style des labels
        for label in [self.total_logs_label, self.error_count_label, 
                     self.warning_count_label, self.info_count_label]:
            label.setFont(QFont("Arial", 12))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    background-color: #2a2a2a;
                    border: 1px solid #555;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
        
        # Disposition des labels
        self.stats_layout.addWidget(self.total_logs_label, 0, 0)
        self.stats_layout.addWidget(self.error_count_label, 0, 1)
        self.stats_layout.addWidget(self.warning_count_label, 1, 0)
        self.stats_layout.addWidget(self.info_count_label, 1, 1)
        
    def update_stats(self, stats: Dict):
        """Met à jour les statistiques"""
        level_stats = stats.get('level_stats', {})
        total = stats.get('total_logs', 0)
        
        self.total_logs_label.setText(f"📊 Total: {total}")
        self.error_count_label.setText(f"❌ Erreurs: {level_stats.get('ERROR', 0)}")
        self.warning_count_label.setText(f"⚠️ Warnings: {level_stats.get('WARNING', 0)}")
        self.info_count_label.setText(f"ℹ️ Info: {level_stats.get('INFO', 0)}")

class LogFilterWidget(QWidget):
    """Widget pour filtrer les logs"""
    
    filter_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface de filtrage"""
        layout = QVBoxLayout(self)
        
        # Groupe de filtres
        filter_group = QGroupBox("🔍 Filtres")
        filter_layout = QGridLayout(filter_group)
        
        # Filtre par niveau
        filter_layout.addWidget(QLabel("Niveau:"), 0, 0)
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Tous", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.level_combo.currentTextChanged.connect(self.filter_changed.emit)
        filter_layout.addWidget(self.level_combo, 0, 1)
        
        # Filtre par logger
        filter_layout.addWidget(QLabel("Logger:"), 1, 0)
        self.logger_combo = QComboBox()
        self.logger_combo.setEditable(True)
        self.logger_combo.addItem("Tous")
        self.logger_combo.currentTextChanged.connect(self.filter_changed.emit)
        filter_layout.addWidget(self.logger_combo, 1, 1)
        
        # Recherche dans le message
        filter_layout.addWidget(QLabel("Recherche:"), 2, 0)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Rechercher dans les messages...")
        self.search_edit.textChanged.connect(self.filter_changed.emit)
        filter_layout.addWidget(self.search_edit, 2, 1)
        
        # Filtre par date
        filter_layout.addWidget(QLabel("Date début:"), 3, 0)
        self.start_date = QDateTimeEdit()
        self.start_date.setDateTime(QDateTime.currentDateTime().addDays(-7))
        self.start_date.setCalendarPopup(True)
        self.start_date.dateTimeChanged.connect(self.filter_changed.emit)
        filter_layout.addWidget(self.start_date, 3, 1)
        
        filter_layout.addWidget(QLabel("Date fin:"), 4, 0)
        self.end_date = QDateTimeEdit()
        self.end_date.setDateTime(QDateTime.currentDateTime())
        self.end_date.setCalendarPopup(True)
        self.end_date.dateTimeChanged.connect(self.filter_changed.emit)
        filter_layout.addWidget(self.end_date, 4, 1)
        
        # Limite d'entrées
        filter_layout.addWidget(QLabel("Limite:"), 5, 0)
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(10, 10000)
        self.limit_spin.setValue(1000)
        self.limit_spin.setSuffix(" entrées")
        self.limit_spin.valueChanged.connect(self.filter_changed.emit)
        filter_layout.addWidget(self.limit_spin, 5, 1)
        
        # Sélecteur de jours de conservation pour le nettoyage
        filter_layout.addWidget(QLabel("Garder (jours):"), 6, 0)
        self.cleanup_days_spin = QSpinBox()
        self.cleanup_days_spin.setRange(1, 3650)
        self.cleanup_days_spin.setValue(30)
        self.cleanup_days_spin.setSuffix(" jours")
        filter_layout.addWidget(self.cleanup_days_spin, 6, 1)
        
        layout.addWidget(filter_group)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Actualiser")
        self.refresh_btn.clicked.connect(self.filter_changed.emit)
        buttons_layout.addWidget(self.refresh_btn)
        
        self.clear_btn = QPushButton("🗑️ Effacer")
        buttons_layout.addWidget(self.clear_btn)
        
        self.export_btn = QPushButton("💾 Exporter")
        buttons_layout.addWidget(self.export_btn)
        
        layout.addLayout(buttons_layout)
        
        # Auto-scroll
        self.auto_scroll_cb = QCheckBox("Auto-scroll")
        self.auto_scroll_cb.setChecked(True)
        layout.addWidget(self.auto_scroll_cb)
        
    def get_filter_params(self) -> Dict:
        """Récupère les paramètres de filtrage"""
        params = {
            'limit': self.limit_spin.value(),
            'start_date': self.start_date.dateTime().toPython(),
            'end_date': self.end_date.dateTime().toPython()
        }
        
        # Niveau
        level = self.level_combo.currentText()
        if level != "Tous":
            params['level_filter'] = [level]
        
        # Logger
        logger = self.logger_combo.currentText()
        if logger and logger != "Tous":
            params['logger_filter'] = logger
        
        # Recherche
        search = self.search_edit.text().strip()
        if search:
            params['search_term'] = search
        
        return params
    
    def update_loggers(self, loggers: List[str]):
        """Met à jour la liste des loggers"""
        current = self.logger_combo.currentText()
        self.logger_combo.clear()
        self.logger_combo.addItem("Tous")
        self.logger_combo.addItems(loggers)
        
        # Restaure la sélection si possible
        index = self.logger_combo.findText(current)
        if index >= 0:
            self.logger_combo.setCurrentIndex(index)

class NotificationWidget(QWidget):
    """Widget pour afficher les notifications"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.notifications = []
        
    def setup_ui(self):
        """Configure l'interface des notifications"""
        self.setFixedHeight(100)
        self.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border: 1px solid #555;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("🔔 Notifications")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(title)
        
        # Zone de notifications
        self.notification_text = QTextEdit()
        self.notification_text.setMaximumHeight(60)
        self.notification_text.setReadOnly(True)
        layout.addWidget(self.notification_text)
        
    def add_notification(self, entry: LogEntry):
        """Ajoute une notification"""
        timestamp = entry.timestamp.strftime("%H:%M:%S")
        level_color = entry.level.value[1]
        
        message = f"<span style='color: {level_color}'>[{timestamp}] {entry.level.value[0]}</span>: {entry.message}"
        
        self.notification_text.append(message)
        
        # Limite le nombre de notifications affichées
        self.notifications.append(entry)
        if len(self.notifications) > 50:
            self.notifications = self.notifications[-50:]
            # Recharge le texte
            self.notification_text.clear()
            for notif in self.notifications[-10:]:  # Affiche les 10 dernières
                ts = notif.timestamp.strftime("%H:%M:%S")
                color = notif.level.value[1]
                msg = f"<span style='color: {color}'>[{ts}] {notif.level.value[0]}</span>: {notif.message}"
                self.notification_text.append(msg)

class LogViewerMainWindow(QMainWindow):
    """Fenêtre principale du visualiseur de logs"""
    
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
        
        # Charge les logs initiaux
        self.refresh_logs()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setWindowTitle("Neuro-Bot - Visualiseur de Logs Avancé")
        self.setGeometry(100, 100, 1400, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Panel de gauche (filtres et stats)
        left_panel = QWidget()
        left_panel.setMaximumWidth(350)
        left_layout = QVBoxLayout(left_panel)
        
        # Filtres (si UI sans panneau filtres, commentez ces deux lignes)
        self.filter_widget = LogFilterWidget()
        left_layout.addWidget(self.filter_widget)
        
        # Statistiques
        self.stats_widget = LogStatsWidget()
        left_layout.addWidget(self.stats_widget)
        
        main_splitter.addWidget(left_panel)
        
        # Panel de droite (logs et notifications)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Onglets
        self.tab_widget = QTabWidget()
        
        # Onglet Table
        table_tab = QWidget()
        table_layout = QVBoxLayout(table_tab)
        
        self.log_table = LogTableWidget()
        table_layout.addWidget(self.log_table)
        
        self.tab_widget.addTab(table_tab, "📋 Table")
        
        # Onglet Texte
        text_tab = QWidget()
        text_layout = QVBoxLayout(text_tab)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        text_layout.addWidget(self.log_text)
        
        self.tab_widget.addTab(text_tab, "📄 Texte")
        
        right_layout.addWidget(self.tab_widget)
        
        # Notifications
        self.notification_widget = NotificationWidget()
        right_layout.addWidget(self.notification_widget)
        
        main_splitter.addWidget(right_panel)
        
        # Proportions du splitter
        main_splitter.setSizes([350, 1050])
        
        # Barre de statut
        self.statusBar().showMessage("Prêt")
        
        # Barre de menu
        self.create_menu_bar()
        
    def create_menu_bar(self):
        """Crée la barre de menu"""
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
        
        # Menu Affichage
        view_menu = menubar.addMenu("👁️ Affichage")
        
        refresh_action = QAction("🔄 Actualiser", self)
        refresh_action.triggered.connect(self.refresh_logs)
        view_menu.addAction(refresh_action)
        
        clear_action = QAction("🗑️ Effacer l'affichage", self)
        clear_action.triggered.connect(self.clear_display)
        view_menu.addAction(clear_action)
        
        # Menu Outils
        tools_menu = menubar.addMenu("🔧 Outils")
        
        cleanup_action = QAction("🧹 Nettoyer les anciens logs", self)
        cleanup_action.triggered.connect(self.cleanup_logs)
        tools_menu.addAction(cleanup_action)
        
        purge_action = QAction("🗑️ Vider tous les logs", self)
        purge_action.triggered.connect(self.purge_all_logs)
        tools_menu.addAction(purge_action)
        
        config_action = QAction("⚙️ Configuration", self)
        config_action.triggered.connect(self.show_config)
        tools_menu.addAction(config_action)
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        # Filtres
        self.filter_widget.filter_changed.connect(self.refresh_logs)
        self.filter_widget.clear_btn.clicked.connect(self.clear_display)
        self.filter_widget.export_btn.clicked.connect(self.export_logs)
        self.filter_widget.auto_scroll_cb.toggled.connect(self.toggle_auto_scroll)
        
        # Gestionnaire de logs
        if self.log_manager:
            self.log_manager.add_gui_callback(self.on_new_log_entry)
    
    def setup_timers(self):
        """Configure les timers"""
        # Timer pour actualiser les stats
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(5000)  # Toutes les 5 secondes
        
        # Timer pour vérifier les notifications
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(1000)  # Toutes les secondes
    
    def setup_system_tray(self):
        """Configure l'icône de la barre système"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            # Icône (créer une icône simple)
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(13, 115, 119))
            self.tray_icon.setIcon(QIcon(pixmap))
            
            # Menu contextuel
            tray_menu = QMenu()
            
            show_action = tray_menu.addAction("Afficher")
            show_action.triggered.connect(self.show)
            
            hide_action = tray_menu.addAction("Masquer")
            hide_action.triggered.connect(self.hide)
            
            tray_menu.addSeparator()
            
            quit_action = tray_menu.addAction("Quitter")
            quit_action.triggered.connect(self.close)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
    
    def on_new_log_entry(self, entry: LogEntry):
        """Traite une nouvelle entrée de log"""
        # Ajoute à la table
        self.log_table.add_log_entry(entry)
        
        # Ajoute au texte
        timestamp = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        level_color = entry.level.value[1]
        
        # Format HTML pour le texte coloré
        html_line = (f"<span style='color: #888'>[{timestamp}]</span> "
                    f"<span style='color: {level_color}; font-weight: bold'>{entry.level.value[0]}</span> "
                    f"<span style='color: #aaa'>{entry.logger_name}</span> - "
                    f"<span style='color: white'>{entry.message}</span>")
        
        self.log_text.append(html_line)
        
        # Notification si nécessaire
        if (entry.level.value[0] in self.log_manager.config.get("notification_levels", ["ERROR", "CRITICAL"]) and
            self.log_manager.config.get("notifications_enabled", True)):
            self.notification_widget.add_notification(entry)
            
            # Notification système
            if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
                self.tray_icon.showMessage(
                    f"Neuro-Bot - {entry.level.value[0]}",
                    entry.message[:100] + ("..." if len(entry.message) > 100 else ""),
                    QSystemTrayIcon.Warning if entry.level.value[0] == "WARNING" else QSystemTrayIcon.Critical,
                    3000
                )
    
    def refresh_logs(self):
        """Actualise l'affichage des logs"""
        if not self.log_manager:
            return
        
        try:
            # Récupère les paramètres de filtrage
            filter_params = self.filter_widget.get_filter_params()
            
            # Charge les logs
            logs = self.log_manager.get_logs(**filter_params)
            
            # Met à jour la table
            self.log_table.update_logs(logs)
            
            # Met à jour le texte
            self.log_text.clear()
            for log in reversed(logs):
                timestamp = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                level_color = log.level.value[1]
                
                html_line = (f"<span style='color: #888'>[{timestamp}]</span> "
                           f"<span style='color: {level_color}; font-weight: bold'>{log.level.value[0]}</span> "
                           f"<span style='color: #aaa'>{log.logger_name}</span> - "
                           f"<span style='color: white'>{log.message}</span>")
                
                self.log_text.append(html_line)
            
            # Met à jour la liste des loggers
            loggers = list(set(log.logger_name for log in logs))
            loggers.sort()
            self.filter_widget.update_loggers(loggers)
            
            self.statusBar().showMessage(f"Logs chargés: {len(logs)}")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement des logs: {e}")
    
    def update_stats(self):
        """Met à jour les statistiques"""
        if not self.log_manager:
            return
        
        try:
            stats = self.log_manager.get_stats(7)  # 7 derniers jours
            self.stats_widget.update_stats(stats)
        except Exception as e:
            print(f"Erreur mise à jour stats: {e}")
    
    def check_notifications(self):
        """Vérifie les nouvelles notifications"""
        if not self.log_manager:
            return
        
        try:
            while True:
                try:
                    entry = self.log_manager.notification_queue.get_nowait()
                    # La notification est déjà traitée dans on_new_log_entry
                except Empty:
                    break
        except Exception as e:
            print(f"Erreur vérification notifications: {e}")
    
    def toggle_auto_scroll(self, enabled: bool):
        """Active/désactive l'auto-scroll"""
        self.auto_scroll_enabled = enabled
        self.log_table.auto_scroll_enabled = enabled
    
    def clear_display(self):
        """Efface l'affichage"""
        self.log_table.clear_logs()
        self.log_text.clear()
        self.statusBar().showMessage("Affichage effacé")
    
    def export_logs(self):
        """Exporte les logs vers un fichier"""
        if not self.log_manager:
            return
        
        # Dialogue de sauvegarde
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exporter les logs",
            f"neuro_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
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
                QMessageBox.information(self, "Succès", f"Logs exportés vers: {file_path}")
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de l'export des logs")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export: {e}")
    
    def cleanup_logs(self):
        """Nettoie les anciens logs selon le sélecteur de jours"""
        if not self.log_manager:
            return
        
        # Demande toujours le nombre de jours à conserver via une boîte de dialogue
        default_days = int(self.log_manager.config.get('cleanup_days', 30))
        days, ok = QInputDialog.getInt(
            self,
            "Nettoyage des anciens logs",
            "Garder (jours):",
            default_days,
            1, 3650, 1
        )
        if not ok:
            return
        # Calcul du cutoff à 00:00 locale (nettoyage par jour)
        now_local = datetime.now().astimezone()
        cutoff_dt = (now_local - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
        # Format selon locale système
        cutoff_str = cutoff_dt.strftime("%c")
        # Compte les entrées impactées
        try:
            to_delete = self.log_manager.count_logs_older_than(cutoff_dt)
        except Exception:
            to_delete = None
        info_count = f"\nEntrées concernées: {to_delete}" if to_delete is not None else ""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Supprimer les logs plus vieux que {days} jour(s) (avant le {cutoff_str}) ?{info_count}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                deleted_count = self.log_manager.cleanup_logs(cutoff_iso=cutoff_dt.isoformat())
                QMessageBox.information(
                    self,
                    "Nettoyage terminé",
                    f"{deleted_count} entrées de log supprimées"
                )
                self.refresh_logs()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors du nettoyage: {e}")

    def purge_all_logs(self):
        """Vider complètement la table des logs (avec confirmation)"""
        if not self.log_manager:
            return
        
        reply = QMessageBox.warning(
            self,
            "Vider tous les logs",
            "Cette opération supprimera TOUTES les entrées de logs de manière irréversible.\n\nConfirmer ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                deleted_count = self.log_manager.delete_all_logs()
                QMessageBox.information(
                    self,
                    "Purge terminée",
                    f"{deleted_count} entrées supprimées"
                )
                self.clear_display()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la purge: {e}")
    
    def show_config(self):
        """Affiche la configuration"""
        QMessageBox.information(
            self,
            "Configuration",
            "Interface de configuration à implémenter"
        )
    
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
    
    # Applique le thème sombre
    DarkTheme.apply(app)
    
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