"""
Module core GUI - Imports et composants centralisés
Facilite l'importation des composants GUI essentiels avec support complet PySide6
"""

# Imports centralisés Qt
from .qt_imports import *

# Widgets communs
from .widgets import *

# Imports PySide6 spécifiques souvent utilisés  
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QTextEdit, QLineEdit,
    QScrollArea, QSplitter, QTabWidget, QGroupBox, QFrame,
    QProgressBar, QSlider, QSpinBox, QCheckBox, QRadioButton,
    QComboBox, QListWidget, QTreeWidget, QTableWidget,
    QFileDialog, QMessageBox, QDialog, QSizePolicy,
    QGraphicsOpacityEffect, QMenu, QMenuBar, QToolBar,
    QStatusBar, QDockWidget
)

from PySide6.QtCore import (
    Qt, Signal, QTimer, QThread, QObject, QPropertyAnimation,
    QEasingCurve, QRect, QSize, QPoint
)

from PySide6.QtGui import (
    QFont, QColor, QPainter, QPen, QBrush, QPixmap, QIcon,
    QPolygon, QPalette, QAction, QKeySequence
)

# Version du module
__version__ = "2.0.0"

# Export complet pour faciliter les développements
__all__ = [
    # De qt_imports - Styles et thèmes
    'COLOR_PALETTE', 'THEME_VARIANTS', 'UNIFIED_STYLE', 'FONTS', 'SIZES', 'ANIMATIONS',
    'apply_theme', 'create_gradient',
    
    # De widgets - Composants personnalisés
    'ModernButton', 'CircularIndicator', 'StatusCard',
    'TemperatureIndicator', 'SystemStatusCard', 
    'ModernLineEdit', 'SystemMonitorPanel',
    
    # PySide6 Widgets couramment utilisés
    'QApplication', 'QMainWindow', 'QWidget', 'QVBoxLayout', 'QHBoxLayout',
    'QGridLayout', 'QLabel', 'QPushButton', 'QTextEdit', 'QLineEdit',
    'QScrollArea', 'QSplitter', 'QTabWidget', 'QGroupBox', 'QFrame',
    'QProgressBar', 'QSlider', 'QSpinBox', 'QCheckBox', 'QRadioButton',
    'QComboBox', 'QListWidget', 'QTreeWidget', 'QTableWidget',
    'QFileDialog', 'QMessageBox', 'QDialog', 'QSizePolicy',
    'QGraphicsOpacityEffect', 'QMenu', 'QMenuBar', 'QToolBar',
    'QStatusBar', 'QDockWidget',
    
    # Qt Core
    'Qt', 'Signal', 'QTimer', 'QThread', 'QObject', 'QPropertyAnimation',
    'QEasingCurve', 'QRect', 'QSize', 'QPoint',
    
    # Qt Gui
    'QFont', 'QColor', 'QPainter', 'QPen', 'QBrush', 'QPixmap', 'QIcon',
    'QPolygon', 'QPalette', 'QAction', 'QKeySequence',
    
    # Utilitaires
    'apply_theme', 'setup_window_properties',
]