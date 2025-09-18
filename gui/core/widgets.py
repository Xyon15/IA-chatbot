"""
Composants GUI communs et réutilisables
Widgets personnalisés standardisés pour l'interface Kira-Bot
"""

import math
from typing import Optional, Dict, Any, List
from .qt_imports import *
from gpu_utils import get_gpu_info, get_vram_info, get_gpu_temperature
import psutil

# =============================================================================
# INDICATEURS CIRCULAIRES
# =============================================================================

class CircularIndicator(QWidget):
    """Widget indicateur circulaire personnalisé réutilisable"""
    
    def __init__(self, title: str = "", unit: str = "%", max_value: int = 100):
        super().__init__()
        self.title = title
        self.unit = unit
        self.max_value = max_value
        self.current_value = 0
        self.secondary_text = ""
        self.setMinimumSize(120, 120)
        
    def setValue(self, value: float, secondary_text: str = ""):
        """Met à jour la valeur affichée"""
        self.current_value = max(0, min(value, self.max_value))
        self.secondary_text = secondary_text
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 10
        
        # Cercle de fond
        painter.setPen(QPen(QColor(COLOR_PALETTE['bg_tertiary']), 8))
        painter.drawEllipse(center, radius, radius)
        
        # Arc de progression
        progress = (self.current_value / self.max_value) * 360
        color = self._getProgressColor()
        painter.setPen(QPen(QColor(color), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawArc(center.x() - radius, center.y() - radius, 
                       radius * 2, radius * 2, 90 * 16, -int(progress * 16))
        
        # Texte central
        painter.setPen(QPen(QColor(COLOR_PALETTE['text_primary'])))
        painter.setFont(FONTS['title'])
        
        # Valeur principale
        value_text = f"{self.current_value:.0f}{self.unit}"
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, value_text)
        
        # Titre
        if self.title:
            painter.setFont(FONTS['small'])
            painter.setPen(QPen(QColor(COLOR_PALETTE['text_secondary'])))
            title_rect = QRect(rect.x(), rect.y() + radius + 15, rect.width(), 20)
            painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, self.title)
            
        # Texte secondaire
        if self.secondary_text:
            painter.setFont(FONTS['small'])
            secondary_rect = QRect(rect.x(), rect.y() - radius - 5, rect.width(), 20)
            painter.drawText(secondary_rect, Qt.AlignmentFlag.AlignCenter, self.secondary_text)
    
    def _getProgressColor(self) -> str:
        """Retourne la couleur selon le niveau de progression"""
        percentage = self.current_value / self.max_value
        if percentage < 0.5:
            return COLOR_PALETTE['success']
        elif percentage < 0.8:
            return COLOR_PALETTE['warning']
        else:
            return COLOR_PALETTE['error']

class TemperatureIndicator(CircularIndicator):
    """Indicateur circulaire spécialisé pour la température"""
    
    def __init__(self):
        super().__init__("Température", "°C", 100)
        
    def _getProgressColor(self) -> str:
        """Couleur spécifique à la température"""
        if self.current_value < 60:
            return COLOR_PALETTE['success']
        elif self.current_value < 80:
            return COLOR_PALETTE['warning']
        else:
            return COLOR_PALETTE['error']

# =============================================================================
# CARTES DE STATUT
# =============================================================================

class StatusCard(QFrame):
    """Carte de statut moderne avec icône et informations"""
    
    def __init__(self, title: str, icon: str = "", value: str = ""):
        super().__init__()
        self.title = title
        self.icon = icon
        self.value = value
        self._setupUI()
        self._applyStyle()
        
    def _setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header avec icône et titre
        header_layout = QHBoxLayout()
        
        if self.icon:
            icon_label = QLabel(self.icon)
            icon_label.setFont(QFont('Segoe UI', 16))
            header_layout.addWidget(icon_label)
            
        self.title_label = QLabel(self.title)
        self.title_label.setFont(FONTS['subtitle'])
        self.title_label.setStyleSheet(f"color: {COLOR_PALETTE['text_secondary']};")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valeur principale
        self.value_label = QLabel(self.value)
        self.value_label.setFont(FONTS['title'])
        self.value_label.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']};")
        layout.addWidget(self.value_label)
        
        layout.addStretch()
        
    def _applyStyle(self):
        self.setStyleSheet(f"""
            StatusCard {{
                background-color: {COLOR_PALETTE['bg_card']};
                border: 1px solid {COLOR_PALETTE['border_primary']};
                border-radius: 8px;
            }}
            StatusCard:hover {{
                border-color: {COLOR_PALETTE['accent_blue']};
                background-color: {COLOR_PALETTE['bg_secondary']};
            }}
        """)
        
    def updateValue(self, value: str):
        """Met à jour la valeur affichée"""
        self.value = value
        self.value_label.setText(value)

class SystemStatusCard(StatusCard):
    """Carte de statut système avec monitoring automatique"""
    
    def __init__(self, system_type: str):
        self.system_type = system_type
        super().__init__(self._getTitle(), self._getIcon())
        self.timer = QTimer()
        self.timer.timeout.connect(self._updateStatus)
        self.timer.start(2000)  # Mise à jour toutes les 2 secondes
        
    def _getTitle(self) -> str:
        titles = {
            'cpu': 'Processeur',
            'ram': 'Mémoire',
            'gpu': 'GPU',
            'vram': 'VRAM'
        }
        return titles.get(self.system_type, 'Système')
        
    def _getIcon(self) -> str:
        icons = {
            'cpu': '🔥',
            'ram': '💾', 
            'gpu': '🎮',
            'vram': '📊'
        }
        return icons.get(self.system_type, '📊')
        
    def _updateStatus(self):
        """Met à jour automatiquement le statut"""
        try:
            if self.system_type == 'cpu':
                value = psutil.cpu_percent(interval=0.1)
                self.updateValue(f"{value:.1f}%")
                
            elif self.system_type == 'ram':
                ram = psutil.virtual_memory()
                used_gb = ram.used / (1024**3)
                total_gb = ram.total / (1024**3)
                self.updateValue(f"{used_gb:.1f}G / {total_gb:.1f}G")
                
            elif self.system_type == 'gpu':
                gpu_info = get_gpu_info()
                if gpu_info:
                    self.updateValue(f"{gpu_info.utilization_gpu}% - {gpu_info.temperature_c}°C")
                else:
                    self.updateValue("Non disponible")
                    
            elif self.system_type == 'vram':
                vram_info = get_vram_info()
                if vram_info:
                    used_gb = vram_info['used_mb'] / 1024
                    total_gb = vram_info['total_mb'] / 1024
                    self.updateValue(f"{used_gb:.1f}G / {total_gb:.1f}G")
                else:
                    self.updateValue("Non disponible")
                    
        except Exception as e:
            self.updateValue("Erreur")

# =============================================================================
# WIDGETS D'ENTRÉE AMÉLIORÉS
# =============================================================================

class ModernLineEdit(QLineEdit):
    """Champ de saisie avec design moderne"""
    
    def __init__(self, placeholder: str = ""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self._setupStyle()
        
    def _setupStyle(self):
        self.setStyleSheet(f"""
            ModernLineEdit {{
                background-color: {COLOR_PALETTE['bg_input']};
                color: {COLOR_PALETTE['text_primary']};
                border: 2px solid {COLOR_PALETTE['border_primary']};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11px;
            }}
            ModernLineEdit:focus {{
                border-color: {COLOR_PALETTE['accent_blue']};
                background-color: {COLOR_PALETTE['bg_secondary']};
            }}
            ModernLineEdit:hover {{
                border-color: {COLOR_PALETTE['text_secondary']};
            }}
        """)

class ModernButton(QPushButton):
    """Bouton avec design moderne et animations"""
    
    def __init__(self, text: str = "", icon: str = "", style: str = "primary"):
        super().__init__()
        self.setText(f"{icon} {text}".strip())
        self.button_style = style
        self._setupStyle()
        self._setupAnimation()
        
    def _setupStyle(self):
        if self.button_style == "primary":
            bg_color = COLOR_PALETTE['accent_blue']
            text_color = COLOR_PALETTE['bg_primary']
            hover_bg = COLOR_PALETTE['text_primary']
        elif self.button_style == "success":
            bg_color = COLOR_PALETTE['success']
            text_color = COLOR_PALETTE['bg_primary']
            hover_bg = COLOR_PALETTE['accent_green']
        elif self.button_style == "warning":
            bg_color = COLOR_PALETTE['warning']
            text_color = COLOR_PALETTE['bg_primary']
            hover_bg = COLOR_PALETTE['accent_orange']
        else:  # secondary
            bg_color = COLOR_PALETTE['bg_tertiary']
            text_color = COLOR_PALETTE['text_primary']
            hover_bg = COLOR_PALETTE['bg_secondary']
            
        self.setStyleSheet(f"""
            ModernButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 500;
                font-size: 11px;
            }}
            ModernButton:hover {{
                background-color: {hover_bg};
            }}
            ModernButton:pressed {{
                background-color: {COLOR_PALETTE['bg_secondary']};
            }}
        """)
        
    def _setupAnimation(self):
        """Configuration des animations de hover"""
        # Sera implémenté avec les propriétés d'animation Qt
        pass

# =============================================================================
# PANNEAUX DE MONITORING
# =============================================================================

class SystemMonitorPanel(QWidget):
    """Panneau de monitoring système complet"""
    
    def __init__(self):
        super().__init__()
        self._setupUI()
        
    def _setupUI(self):
        layout = QGridLayout(self)
        layout.setSpacing(12)
        
        # Titre
        title = QLabel("📊 Monitoring Système")
        title.setFont(FONTS['title'])
        title.setStyleSheet(f"color: {COLOR_PALETTE['accent_blue']};")
        layout.addWidget(title, 0, 0, 1, 4)
        
        # Indicateurs circulaires
        self.cpu_indicator = CircularIndicator("CPU", "%")
        self.ram_indicator = CircularIndicator("RAM", "%")
        self.gpu_indicator = CircularIndicator("GPU", "%")
        self.temp_indicator = TemperatureIndicator()
        
        layout.addWidget(self.cpu_indicator, 1, 0)
        layout.addWidget(self.ram_indicator, 1, 1)
        layout.addWidget(self.gpu_indicator, 1, 2)
        layout.addWidget(self.temp_indicator, 1, 3)
        
        # Cartes de statut
        self.cpu_card = SystemStatusCard('cpu')
        self.ram_card = SystemStatusCard('ram')
        self.gpu_card = SystemStatusCard('gpu')
        self.vram_card = SystemStatusCard('vram')
        
        layout.addWidget(self.cpu_card, 2, 0)
        layout.addWidget(self.ram_card, 2, 1)
        layout.addWidget(self.gpu_card, 2, 2)
        layout.addWidget(self.vram_card, 2, 3)
        
        # Timer pour les indicateurs circulaires
        self.timer = QTimer()
        self.timer.timeout.connect(self._updateIndicators)
        self.timer.start(1000)
        
    def _updateIndicators(self):
        """Met à jour les indicateurs circulaires"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_indicator.setValue(cpu_percent)
            
            # RAM
            ram = psutil.virtual_memory()
            self.ram_indicator.setValue(ram.percent)
            
            # GPU
            gpu_info = get_gpu_info()
            if gpu_info:
                self.gpu_indicator.setValue(gpu_info.utilization_gpu)
                self.temp_indicator.setValue(gpu_info.temperature_c)
            
        except Exception:
            pass  # Ignorer les erreurs de monitoring

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'CircularIndicator',
    'TemperatureIndicator', 
    'StatusCard',
    'SystemStatusCard',
    'ModernLineEdit',
    'ModernButton',
    'SystemMonitorPanel',
]