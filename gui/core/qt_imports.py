"""
Module central pour les imports et configurations GUI communes
Centralise tous les imports PySide6 et configurations partagées
"""

# =============================================================================
# IMPORTS PYSIDE6 CENTRALISÉS
# =============================================================================

# Core Qt
from PySide6.QtCore import (
    QTimer, QThread, Signal, Qt, QPropertyAnimation, QEasingCurve,
    QRect, QSize, QPoint, QDateTime, QObject
)

# Widgets principaux
from PySide6.QtWidgets import (
    # Base
    QApplication, QMainWindow, QWidget, QDialog,
    
    # Layouts
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    
    # Containers
    QGroupBox, QFrame, QSplitter, QTabWidget, QScrollArea,
    QStackedWidget,
    
    # Controls
    QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QSlider, QProgressBar,
    QCheckBox, QRadioButton, QDateTimeEdit,
    
    # Displays
    QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem,
    QTreeWidget, QTreeWidgetItem,
    
    # Advanced
    QHeaderView, QSystemTrayIcon, QMenu, QMenuBar, QToolBar,
    QStatusBar, QMessageBox, QFileDialog, QInputDialog,
    QSpacerItem, QSizePolicy, QLCDNumber, QDial
)

# Graphics et Styling
from PySide6.QtGui import (
    QFont, QPixmap, QPainter, QColor, QBrush, QPen, QLinearGradient,
    QRadialGradient, QGradient, QPalette, QIcon, QAction,
    QTextCharFormat, QTextCursor
)

# Charts (import conditionnel)
try:
    from PySide6.QtCharts import (
        QChart, QChartView, QPieSeries, QLineSeries, QDateTimeAxis, 
        QValueAxis, QBarSeries, QBarSet, QBarCategoryAxis
    )
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False

# =============================================================================
# PALETTE DE COULEURS UNIFIÉE
# =============================================================================

# Palette principale unifiée pour tout le projet
COLOR_PALETTE = {
    # Arrière-plans
    'bg_primary': '#0f0f0f',       # Noir très profond
    'bg_secondary': '#1a1a1a',     # Noir profond  
    'bg_tertiary': '#2a2a2a',      # Gris très sombre
    'bg_card': '#1e1e1e',          # Cartes/panels
    'bg_input': '#2d2d2d',         # Champs de saisie
    
    # Accents et couleurs vives
    'accent_blue': '#00d4ff',      # Bleu néon principal
    'accent_green': '#00ff88',     # Vert succès
    'accent_orange': '#ff8128',    # Orange action
    'accent_purple': '#8b5cf6',    # Violet
    'accent_pink': '#ff0080',      # Rose
    
    # Textes
    'text_primary': '#ffffff',     # Blanc pur
    'text_secondary': '#b0b0b0',   # Gris clair
    'text_disabled': '#666666',    # Gris neutre
    'text_accent': '#00d4ff',      # Texte accentué
    
    # États
    'success': '#00ff88',          # Succès
    'warning': '#ffaa00',          # Avertissement
    'error': '#ff4444',            # Erreur
    'info': '#00d4ff',            # Information
    
    # Bordures et séparateurs
    'border_primary': '#3a3a3a',   # Bordures principales
    'border_accent': '#00d4ff',    # Bordures accentuées
    'separator': '#2a2a2a',        # Lignes de séparation
    
    # Transparences
    'overlay_dark': '#000000aa',   # Overlay sombre
    'overlay_light': '#ffffff22',  # Overlay clair
}

# Variantes pour différents thèmes
THEME_VARIANTS = {
    'dark': COLOR_PALETTE,  # Thème principal (sombre)
    
    'high_contrast': {
        **COLOR_PALETTE,
        'bg_primary': '#000000',
        'text_primary': '#ffffff',
        'accent_blue': '#00ffff',
    },
    
    'blue_accent': {
        **COLOR_PALETTE,
        'accent_blue': '#0099ff',
        'accent_green': '#00cc66',
    }
}

# =============================================================================
# STYLES CSS CENTRALISÉS
# =============================================================================

# Style de base pour l'application
BASE_STYLE = f"""
QApplication {{
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11px;
}}

QMainWindow {{
    background-color: {COLOR_PALETTE['bg_primary']};
    color: {COLOR_PALETTE['text_primary']};
}}

QWidget {{
    background-color: {COLOR_PALETTE['bg_primary']};
    color: {COLOR_PALETTE['text_primary']};
    border: none;
}}
"""

# Styles pour les boutons
BUTTON_STYLES = f"""
QPushButton {{
    background-color: {COLOR_PALETTE['bg_tertiary']};
    color: {COLOR_PALETTE['text_primary']};
    border: 1px solid {COLOR_PALETTE['border_primary']};
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {COLOR_PALETTE['accent_blue']};
    border-color: {COLOR_PALETTE['accent_blue']};
    color: {COLOR_PALETTE['bg_primary']};
}}

QPushButton:pressed {{
    background-color: {COLOR_PALETTE['bg_secondary']};
}}

QPushButton:disabled {{
    background-color: {COLOR_PALETTE['bg_secondary']};
    color: {COLOR_PALETTE['text_disabled']};
    border-color: {COLOR_PALETTE['text_disabled']};
}}
"""

# Styles pour les groupes et frames
FRAME_STYLES = f"""
QGroupBox {{
    background-color: {COLOR_PALETTE['bg_secondary']};
    border: 1px solid {COLOR_PALETTE['border_primary']};
    border-radius: 8px;
    margin: 5px 0px;
    padding-top: 20px;
    font-weight: bold;
    color: {COLOR_PALETTE['text_primary']};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {COLOR_PALETTE['accent_blue']};
}}

QFrame {{
    background-color: {COLOR_PALETTE['bg_secondary']};
    border: 1px solid {COLOR_PALETTE['border_primary']};
    border-radius: 6px;
}}
"""

# Styles pour les champs de saisie
INPUT_STYLES = f"""
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLOR_PALETTE['bg_input']};
    color: {COLOR_PALETTE['text_primary']};
    border: 1px solid {COLOR_PALETTE['border_primary']};
    border-radius: 4px;
    padding: 6px;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {COLOR_PALETTE['accent_blue']};
}}

QComboBox {{
    background-color: {COLOR_PALETTE['bg_input']};
    color: {COLOR_PALETTE['text_primary']};
    border: 1px solid {COLOR_PALETTE['border_primary']};
    border-radius: 4px;
    padding: 6px;
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {COLOR_PALETTE['text_secondary']};
}}
"""

# Style complet unifié
UNIFIED_STYLE = BASE_STYLE + BUTTON_STYLES + FRAME_STYLES + INPUT_STYLES

# =============================================================================
# CONFIGURATIONS COMMUNES
# =============================================================================

# Configuration des polices
FONTS = {
    'default': QFont('Segoe UI', 10),
    'title': QFont('Segoe UI', 14, QFont.Weight.Bold),
    'subtitle': QFont('Segoe UI', 12, QFont.Weight.Medium),
    'small': QFont('Segoe UI', 9),
    'mono': QFont('Consolas', 10),
}

# Tailles communes
SIZES = {
    'icon_small': QSize(16, 16),
    'icon_medium': QSize(24, 24),
    'icon_large': QSize(32, 32),
    'button_height': 32,
    'input_height': 28,
}

# Animations communes
ANIMATIONS = {
    'fast': 150,        # ms
    'normal': 250,      # ms  
    'slow': 500,        # ms
    'easing': QEasingCurve.Type.OutCubic,
}

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def apply_theme(widget: QWidget, theme_name: str = 'dark'):
    """Applique un thème à un widget"""
    theme = THEME_VARIANTS.get(theme_name, COLOR_PALETTE)
    widget.setStyleSheet(UNIFIED_STYLE)

def create_gradient(color1: str, color2: str, orientation='vertical') -> QLinearGradient:
    """Crée un gradient entre deux couleurs"""
    gradient = QLinearGradient()
    if orientation == 'vertical':
        gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setStart(0, 0)
        gradient.setFinalStop(0, 1)
    else:  # horizontal
        gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setStart(0, 0)
        gradient.setFinalStop(1, 0)
    
    gradient.setColorAt(0, QColor(color1))
    gradient.setColorAt(1, QColor(color2))
    return gradient

def get_status_color(status: str) -> str:
    """Retourne la couleur associée à un statut"""
    status_colors = {
        'success': COLOR_PALETTE['success'],
        'warning': COLOR_PALETTE['warning'],
        'error': COLOR_PALETTE['error'],
        'info': COLOR_PALETTE['info'],
        'default': COLOR_PALETTE['text_secondary'],
    }
    return status_colors.get(status.lower(), COLOR_PALETTE['text_secondary'])

def setup_window_properties(window: QMainWindow, title: str, size: tuple = (1200, 800)):
    """Configure les propriétés communes d'une fenêtre"""
    window.setWindowTitle(title)
    window.resize(size[0], size[1])
    window.setMinimumSize(800, 600)
    apply_theme(window)

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Qt Core
    'QTimer', 'QThread', 'Signal', 'Qt', 'QPropertyAnimation', 'QEasingCurve',
    'QRect', 'QSize', 'QPoint', 'QDateTime', 'QObject',
    
    # Qt Widgets (principaux)
    'QApplication', 'QMainWindow', 'QWidget', 'QDialog',
    'QVBoxLayout', 'QHBoxLayout', 'QGridLayout', 'QFormLayout',
    'QGroupBox', 'QFrame', 'QSplitter', 'QTabWidget',
    'QLabel', 'QPushButton', 'QLineEdit', 'QTextEdit', 'QComboBox',
    'QTableWidget', 'QProgressBar', 'QCheckBox',
    
    # Qt GUI
    'QFont', 'QPixmap', 'QPainter', 'QColor', 'QBrush', 'QPen',
    'QLinearGradient', 'QIcon', 'QAction',
    
    # Configurations
    'COLOR_PALETTE', 'THEME_VARIANTS', 'UNIFIED_STYLE', 'FONTS', 'SIZES', 'ANIMATIONS',
    
    # Utilitaires
    'apply_theme', 'create_gradient', 'get_status_color', 'setup_window_properties',
    
    # Constantes
    'CHARTS_AVAILABLE',
]