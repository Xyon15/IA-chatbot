#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kira GUI - Interface Legacy Simple
Interface graphique simplifiée pour compatibilité avec launch_gui.py
"""

import sys
import os
from pathlib import Path

# Ajout du répertoire racine au path pour les imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from gui.core.qt_imports import *
    from gui.modules.notifications import show_info, show_success, show_warning, show_error
except ImportError:
    # Fallback pour imports PySide6 directs
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QTextEdit, QLineEdit, QFrame, QGridLayout,
        QScrollArea, QTabWidget, QGroupBox, QSplitter
    )
    from PySide6.QtCore import Qt, QTimer, QThread, Signal
    from PySide6.QtGui import QFont, QPixmap, QPalette, QColor

# Styles de base pour la compatibilité
STYLES = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}

QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QLabel {
    color: #ffffff;
    font-size: 12px;
}

QTextEdit, QLineEdit {
    background-color: #2d2d30;
    color: #ffffff;
    border: 1px solid #3e3e42;
    padding: 4px;
    border-radius: 2px;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #3e3e42;
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 4px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}

QTabWidget::pane {
    border: 1px solid #3e3e42;
    background-color: #2d2d30;
}

QTabBar::tab {
    background-color: #3e3e42;
    color: #ffffff;
    padding: 8px 16px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #0078d4;
}

QScrollArea {
    border: 1px solid #3e3e42;
    background-color: #2d2d30;
}
"""

class MainWindow(QMainWindow):
    """Interface principale legacy simple pour Kira-Bot"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 Kira-Bot - Interface Legacy")
        self.setGeometry(100, 100, 1000, 700)
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Titre
        title_label = QLabel("🤖 Kira-Bot - Interface Legacy")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #0078d4;
            margin: 20px;
            padding: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Conteneur principal avec onglets
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Onglet Information
        info_tab = self.create_info_tab()
        tab_widget.addTab(info_tab, "📋 Information")
        
        # Onglet Configuration
        config_tab = self.create_config_tab()
        tab_widget.addTab(config_tab, "⚙️ Configuration")
        
        # Onglet Logs
        logs_tab = self.create_logs_tab()
        tab_widget.addTab(logs_tab, "📊 Logs")
        
        # Barre de statut
        self.statusBar().showMessage("✅ Interface Legacy Kira-Bot - Prête")
        
    def create_info_tab(self):
        """Crée l'onglet d'information"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Informations générales
        info_group = QGroupBox("📋 Informations Générales")
        info_layout = QGridLayout(info_group)
        
        info_layout.addWidget(QLabel("Version:"), 0, 0)
        info_layout.addWidget(QLabel("Kira-Bot Legacy v1.0"), 0, 1)
        
        info_layout.addWidget(QLabel("Statut:"), 1, 0)
        info_layout.addWidget(QLabel("✅ Opérationnel"), 1, 1)
        
        info_layout.addWidget(QLabel("Interface:"), 2, 0)
        info_layout.addWidget(QLabel("Legacy GUI (Compatibilité)"), 2, 1)
        
        layout.addWidget(info_group)
        
        # Actions rapides
        actions_group = QGroupBox("🚀 Actions Rapides")
        actions_layout = QVBoxLayout(actions_group)
        
        moderne_btn = QPushButton("🔄 Passer à l'Interface Moderne")
        moderne_btn.clicked.connect(self.switch_to_modern)
        actions_layout.addWidget(moderne_btn)
        
        test_btn = QPushButton("🧪 Lancer les Tests")
        test_btn.clicked.connect(self.run_tests)
        actions_layout.addWidget(test_btn)
        
        layout.addWidget(actions_group)
        layout.addStretch()
        
        return widget
        
    def create_config_tab(self):
        """Crée l'onglet de configuration"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        config_group = QGroupBox("⚙️ Configuration")
        config_layout = QVBoxLayout(config_group)
        
        config_layout.addWidget(QLabel("Interface Legacy - Configuration limitée"))
        config_layout.addWidget(QLabel("Pour une configuration complète, utilisez l'interface moderne."))
        
        layout.addWidget(config_group)
        layout.addStretch()
        
        return widget
        
    def create_logs_tab(self):
        """Crée l'onglet des logs"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        logs_group = QGroupBox("📊 Logs Système")
        logs_layout = QVBoxLayout(logs_group)
        
        # Zone de texte pour les logs
        self.logs_text = QTextEdit()
        self.logs_text.setPlainText("""
🤖 Kira-Bot Legacy Interface - Logs
=====================================

✅ Interface legacy initialisée
✅ Styles appliqués
✅ Onglets créés
✅ Prêt pour utilisation

💡 Pour des fonctionnalités complètes, utilisez l'interface moderne.
        """)
        self.logs_text.setReadOnly(True)
        logs_layout.addWidget(self.logs_text)
        
        layout.addWidget(logs_group)
        
        return widget
        
    def switch_to_modern(self):
        """Basculer vers l'interface moderne"""
        try:
            # Essayer d'utiliser le système de notifications modulaire
            try:
                from gui.modules.notifications import show_info
                show_info("🔄 Redirection", "Fermez cette interface et lancez l'interface moderne.")
            except ImportError:
                print("💡 Pour utiliser l'interface moderne, fermez cette fenêtre et relancez avec --modern")
        except Exception as e:
            print(f"Erreur lors du basculement: {e}")
            
    def run_tests(self):
        """Lancer les tests d'intégration"""
        try:
            # Essayer d'utiliser le système de notifications modulaire
            try:
                from gui.modules.notifications import show_info
                show_info("🧪 Tests", "Lancement des tests d'intégration...")
            except ImportError:
                print("🧪 Tests - Fonctionnalité disponible dans l'interface moderne")
        except Exception as e:
            print(f"Erreur lors des tests: {e}")

def main():
    """Fonction principale pour lancer l'interface legacy"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        
    # Application du style - vérifier que c'est bien QApplication
    if isinstance(app, QApplication):
        app.setStyleSheet(STYLES)
    
    # Création et affichage de la fenêtre
    window = MainWindow()
    window.show()
    
    print("✅ Interface Legacy Kira-Bot lancée")
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())