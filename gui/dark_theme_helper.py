#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper pour appliquer le thème sombre moderne
"""

def get_dark_palette():
    """Retourne la palette de couleurs sombre moderne"""
    return {
        'primary_dark': '#1a1a1a',      # Noir profond pour le fond
        'secondary_dark': '#2d2d2d',    # Gris très foncé pour cartes
        'neutral_light': '#3a3a3a',     # Gris moyen pour éléments
        'accent_light': '#4a4a4a',      # Gris clair pour bordures
        'accent_warm': '#555555',       # Gris plus clair pour hover
        'accent_orange': '#4a9eff',     # Bleu accent principal
        'text_dark': '#ffffff',         # Texte blanc principal
        'text_light': '#d1d5db',        # Texte gris clair secondaire
        'success': '#4ade80',           # Vert moderne succès
        'warning': '#fbbf24',           # Jaune moderne warning
        'error': '#ef4444',             # Rouge moderne erreur
        'purple': '#a855f7',            # Violet accent
        'cyan': '#06b6d4',              # Cyan accent
        'indigo': '#6366f1'             # Indigo accent
    }

def generate_dark_stylesheet():
    """Génère un stylesheet complet pour le thème sombre"""
    colors = get_dark_palette()
    
    return f"""
    /* Style principal pour toute l'application */
    QApplication {{
        background-color: {colors['primary_dark']};
        color: {colors['text_dark']};
        font-family: "Segoe UI", "Arial", sans-serif;
    }}
    
    /* Fenêtre principale */
    QMainWindow {{
        background-color: {colors['primary_dark']};
        color: {colors['text_light']};
    }}
    
    /* Widgets de base */
    QWidget {{
        background-color: transparent;
        color: {colors['text_light']};
    }}
    
    /* Labels */
    QLabel {{
        color: {colors['text_light']};
        background-color: transparent;
    }}
    
    /* Boutons */
    QPushButton {{
        background-color: {colors['secondary_dark']};
        border: 1px solid {colors['accent_light']};
        border-radius: 8px;
        padding: 8px 16px;
        color: {colors['text_dark']};
        font-weight: 500;
        min-height: 30px;
    }}
    
    QPushButton:hover {{
        background-color: {colors['accent_orange']};
        border-color: {colors['accent_orange']};
    }}
    
    QPushButton:pressed {{
        background-color: {colors['neutral_light']};
    }}
    
    QPushButton:disabled {{
        background-color: {colors['neutral_light']};
        color: {colors['text_light']};
        opacity: 0.5;
    }}
    
    /* Champs de texte */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {colors['secondary_dark']};
        border: 1px solid {colors['accent_light']};
        border-radius: 6px;
        padding: 8px;
        color: {colors['text_dark']};
        selection-background-color: {colors['accent_orange']};
        selection-color: {colors['text_dark']};
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {colors['accent_orange']};
        border-width: 2px;
    }}
    
    /* Barres de progression */
    QProgressBar {{
        background-color: {colors['neutral_light']};
        border: 1px solid {colors['accent_light']};
        border-radius: 8px;
        text-align: center;
        color: {colors['text_dark']};
        font-weight: bold;
    }}
    
    QProgressBar::chunk {{
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                          stop:0 {colors['accent_orange']}, 
                          stop:1 {colors['success']});
        border-radius: 6px;
        margin: 1px;
    }}
    
    /* Slider */
    QSlider::groove:horizontal {{
        background-color: {colors['neutral_light']};
        height: 6px;
        border-radius: 3px;
    }}
    
    QSlider::handle:horizontal {{
        background-color: {colors['accent_orange']};
        border: 2px solid {colors['text_dark']};
        width: 18px;
        height: 18px;
        border-radius: 9px;
        margin: -6px 0;
    }}
    
    QSlider::handle:horizontal:hover {{
        background-color: {colors['success']};
    }}
    
    /* Spin Box */
    QSpinBox, QDoubleSpinBox {{
        background-color: {colors['secondary_dark']};
        border: 1px solid {colors['accent_light']};
        border-radius: 6px;
        padding: 6px;
        color: {colors['text_dark']};
    }}
    
    /* Combo Box */
    QComboBox {{
        background-color: {colors['secondary_dark']};
        border: 1px solid {colors['accent_light']};
        border-radius: 6px;
        padding: 6px 12px;
        color: {colors['text_dark']};
        min-width: 100px;
    }}
    
    QComboBox::drop-down {{
        border: none;
        background-color: {colors['accent_orange']};
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 6px solid {colors['text_dark']};
        margin: 0 6px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {colors['secondary_dark']};
        border: 1px solid {colors['accent_light']};
        selection-background-color: {colors['accent_orange']};
        selection-color: {colors['text_dark']};
    }}
    
    /* Check Box */
    QCheckBox {{
        color: {colors['text_light']};
        spacing: 8px;
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
    }}
    
    QCheckBox::indicator:unchecked {{
        background-color: {colors['secondary_dark']};
        border: 2px solid {colors['accent_light']};
        border-radius: 4px;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {colors['accent_orange']};
        border: 2px solid {colors['accent_orange']};
        border-radius: 4px;
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iMTAiIHZpZXdCb3g9IjAgMCAxMCAxMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEuNSA1TDMuNSA3TDguNSAyIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
    }}
    
    /* Group Box */
    QGroupBox {{
        color: {colors['text_light']};
        border: 2px solid {colors['accent_light']};
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 8px;
        font-weight: bold;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: {colors['accent_orange']};
        background-color: {colors['primary_dark']};
    }}
    
    /* Tabs */
    QTabWidget::pane {{
        border: 1px solid {colors['accent_light']};
        border-radius: 8px;
        background-color: {colors['secondary_dark']};
        margin-top: -1px;
    }}
    
    QTabBar::tab {{
        background-color: {colors['neutral_light']};
        color: {colors['text_light']};
        padding: 12px 24px;
        margin-right: 2px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border: 1px solid {colors['accent_light']};
        min-width: 100px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {colors['accent_orange']};
        color: {colors['text_dark']};
        border-bottom: none;
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: {colors['accent_light']};
    }}
    
    /* Scroll Bar */
    QScrollBar:vertical {{
        background-color: {colors['secondary_dark']};
        width: 14px;
        border-radius: 7px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {colors['accent_light']};
        border-radius: 7px;
        min-height: 30px;
        margin: 2px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {colors['accent_orange']};
    }}
    
    /* Menu */
    QMenu {{
        background-color: {colors['secondary_dark']};
        color: {colors['text_light']};
        border: 1px solid {colors['accent_light']};
        border-radius: 6px;
        padding: 4px;
    }}
    
    QMenu::item {{
        padding: 8px 16px;
        border-radius: 4px;
    }}
    
    QMenu::item:selected {{
        background-color: {colors['accent_orange']};
        color: {colors['text_dark']};
    }}
    
    /* Tooltips */
    QToolTip {{
        background-color: {colors['secondary_dark']};
        color: {colors['text_light']};
        border: 1px solid {colors['accent_orange']};
        border-radius: 6px;
        padding: 6px;
    }}
    
    /* Splitter */
    QSplitter::handle {{
        background-color: {colors['accent_light']};
    }}
    
    QSplitter::handle:hover {{
        background-color: {colors['accent_orange']};
    }}
    """

if __name__ == "__main__":
    # Test du thème
    print("🎨 Palette de couleurs sombre moderne :")
    colors = get_dark_palette()
    for name, color in colors.items():
        print(f"  {name}: {color}")
    
    print("\n✨ Stylesheet généré avec succès !")
    print("📋 Pour utiliser ce thème, appelez generate_dark_stylesheet()")