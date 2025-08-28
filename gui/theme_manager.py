#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de thèmes pour NeuroBot GUI
Permet de basculer entre différents thèmes de couleurs
"""

from typing import Dict, Optional
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget
import json
import os

class ThemeManager(QObject):
    theme_changed = Signal(str)  # Émis quand le thème change
    
    def __init__(self):
        super().__init__()
        self.current_theme = "emerald"
        self.themes = self.load_themes()
        
    def load_themes(self) -> Dict[str, Dict[str, str]]:
        """Charge les thèmes disponibles"""
        return {
            "emerald": {
                'primary_dark': '#034C36',
                'secondary_dark': '#003332', 
                'accent_orange': '#FF8128',
                'accent_light': '#F2E0DF',
                'neutral_light': '#BDCDCF',
                'success': '#00C851',
                'warning': '#FFA726',
                'error': '#FF5252',
                'text_dark': '#003332',
                'text_light': '#F2E0DF'
            },
            "ocean": {
                'primary_dark': '#1A365D',
                'secondary_dark': '#0A1928',
                'accent_orange': '#3182CE',
                'accent_light': '#EDF2F7',
                'neutral_light': '#A0AEC0',
                'success': '#38A169',
                'warning': '#D69E2E',
                'error': '#E53E3E',
                'text_dark': '#0A1928',
                'text_light': '#EDF2F7'
            },
            "sunset": {
                'primary_dark': '#7C2D12',
                'secondary_dark': '#431407',
                'accent_orange': '#EA580C',
                'accent_light': '#FED7AA',
                'neutral_light': '#FDBA74',
                'success': '#16A34A',
                'warning': '#CA8A04',
                'error': '#DC2626',
                'text_dark': '#431407',
                'text_light': '#FED7AA'
            },
            "midnight": {
                'primary_dark': '#1E1E2E',
                'secondary_dark': '#11111B',
                'accent_orange': '#CBA6F7',
                'accent_light': '#F2F4F8',
                'neutral_light': '#6C7086',
                'success': '#A6E3A1',
                'warning': '#F9E2AF',
                'error': '#F38BA8',
                'text_dark': '#11111B',
                'text_light': '#F2F4F8'
            }
        }
    
    def get_current_palette(self) -> Dict[str, str]:
        """Retourne la palette de couleurs actuelle"""
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_name: str):
        """Change le thème actuel"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.theme_changed.emit(theme_name)
            return True
        return False
    
    def get_available_themes(self) -> list:
        """Retourne la liste des thèmes disponibles"""
        return list(self.themes.keys())
    
    def generate_stylesheet(self) -> str:
        """Génère le CSS complet pour le thème actuel"""
        colors = self.get_current_palette()
        
        return f"""
        QMainWindow {{
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 {colors['neutral_light']}, 
                        stop:1 {colors['accent_light']});
        }}

        QWidget#sidebar {{
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['primary_dark']}, 
                        stop:1 {colors['secondary_dark']});
            border-radius: 15px;
        }}

        QPushButton#nav_button {{
            background: transparent;
            color: {colors['text_light']};
            border: none;
            padding: 18px;
            text-align: left;
            font-size: 14px;
            font-weight: bold;
            border-radius: 10px;
            margin: 3px;
        }}

        QPushButton#nav_button:hover {{
            background: {colors['accent_orange']};
            color: white;
            transform: translateX(5px);
        }}

        QPushButton#nav_button:checked {{
            background: {colors['accent_orange']};
            color: white;
        }}

        QPushButton#action_button {{
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['primary_dark']}, 
                        stop:1 {colors['secondary_dark']});
            color: {colors['text_light']};
            border: none;
            padding: 15px 30px;
            font-size: 13px;
            font-weight: bold;
            border-radius: 8px;
        }}

        QPushButton#action_button:hover {{
            background: {colors['accent_orange']};
            transform: scale(1.05);
        }}

        QPushButton#action_button:pressed {{
            background: {colors['secondary_dark']};
            transform: scale(0.95);
        }}

        QFrame#card {{
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid {colors['neutral_light']};
            border-radius: 15px;
            padding: 20px;
        }}

        QFrame#glass_card {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}

        QProgressBar {{
            border: 2px solid {colors['neutral_light']};
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.3);
            height: 28px;
        }}

        QProgressBar::chunk {{
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['primary_dark']}, 
                        stop:1 {colors['accent_orange']});
            border-radius: 8px;
            margin: 2px;
        }}

        QTextEdit {{
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid {colors['neutral_light']};
            border-radius: 10px;
            padding: 15px;
            font-family: 'Cascadia Code', 'Consolas', 'Monaco', monospace;
            font-size: 11px;
            color: {colors['text_dark']};
        }}

        QTabWidget::pane {{
            border: 2px solid {colors['neutral_light']};
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
        }}

        QTabBar::tab {{
            background: {colors['neutral_light']};
            color: {colors['text_dark']};
            padding: 15px 25px;
            margin-right: 3px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            font-weight: bold;
        }}

        QTabBar::tab:selected {{
            background: {colors['primary_dark']};
            color: {colors['text_light']};
        }}

        QTabBar::tab:hover {{
            background: {colors['accent_orange']};
            color: white;
        }}
        """

# Instance globale du gestionnaire de thèmes
theme_manager = ThemeManager()

def apply_theme_to_app(app, theme_name: str):
    """Applique un thème à toute l'application"""
    if theme_manager.set_theme(theme_name):
        stylesheet = theme_manager.generate_stylesheet()
        app.setStyleSheet(stylesheet)
        return True
    return False