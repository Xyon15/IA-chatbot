"""
Widgets de monitoring système optimisés
Utilise gpu_utils et core modules pour un monitoring unifié
"""

import sys
import os
import time
import psutil
from typing import Dict, List, Optional

# Ajouter le répertoire parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from gui.core.qt_imports import *
from gui.core.widgets import ModernButton
from gpu_utils import gpu_manager
from PySide6.QtGui import QPolygon, QColor
from PySide6.QtCore import QPoint

class CircularProgressIndicator(QWidget):
    """Indicateur de progression circulaire moderne"""
    
    def __init__(self, size: int = 100, line_width: int = 8):
        super().__init__()
        self.widget_size = size
        self.line_width = line_width
        self.value = 0
        self.max_value = 100
        self.text = ""
        self.color = COLOR_PALETTE['primary']
        
        self.setFixedSize(size, size)
        
    def setValue(self, value: float, text: str = ""):
        """Met à jour la valeur et le texte"""
        self.value = max(0, min(value, self.max_value))
        self.text = text
        self.update()
        
    def setColor(self, color: str):
        """Change la couleur de l'indicateur"""
        self.color = color
        self.update()
        
    def paintEvent(self, event):
        """Dessine l'indicateur circulaire"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Centre et rayon
        center = QPoint(self.widget_size // 2, self.widget_size // 2)
        radius = (self.widget_size - self.line_width) // 2
        
        # Rectangle pour l'arc
        rect = QRect(
            center.x() - radius, center.y() - radius,
            radius * 2, radius * 2
        )
        
        # Background circle
        pen = QPen(QColor(COLOR_PALETTE['border_secondary']), self.line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawEllipse(rect)
        
        # Progress arc
        if self.value > 0:
            pen.setColor(QColor(self.color))
            painter.setPen(pen)
            
            # Angle de départ (top = -90°)
            start_angle = -90 * 16  # QPainter utilise 1/16 de degré
            span_angle = int((self.value / self.max_value) * 360 * 16)
            
            painter.drawArc(rect, start_angle, span_angle)
        
        # Texte central
        if self.text:
            painter.setPen(COLOR_PALETTE['text_primary'])
            painter.setFont(FONTS['subtitle'])
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text)

class SystemMetricCard(QWidget):
    """Carte d'affichage d'une métrique système"""
    
    def __init__(self, title: str, icon: str = "", unit: str = "%"):
        super().__init__()
        self.title = title
        self.icon = icon
        self.unit = unit
        self.current_value = 0
        self.history: List[float] = []
        self.max_history = 60  # 60 points d'historique
        
        self._setupUI()
        
    def _setupUI(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # Header avec titre et icône
        header_layout = QHBoxLayout()
        
        if self.icon:
            icon_label = QLabel(self.icon)
            icon_label.setFont(QFont('Segoe UI', 14))
            header_layout.addWidget(icon_label)
            
        title_label = QLabel(self.title)
        title_label.setFont(FONTS['subtitle'])
        title_label.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']};")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Indicateur circulaire
        self.progress_indicator = CircularProgressIndicator(80, 6)
        layout.addWidget(self.progress_indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Mini graphique d'historique
        self.history_chart = MiniChart()
        self.history_chart.setFixedHeight(40)
        layout.addWidget(self.history_chart)
        
        # Style de la carte
        self.setStyleSheet(f"""
            SystemMetricCard {{
                background-color: {COLOR_PALETTE['bg_card']};
                border: 1px solid {COLOR_PALETTE['border_primary']};
                border-radius: 12px;
            }}
        """)
        
    def updateValue(self, value: float):
        """Met à jour la valeur de la métrique"""
        self.current_value = value
        
        # Mettre à jour l'indicateur
        display_text = f"{value:.1f}{self.unit}"
        self.progress_indicator.setValue(value, display_text)
        
        # Changer la couleur selon la valeur
        if value < 50:
            self.progress_indicator.setColor(COLOR_PALETTE['success'])
        elif value < 80:
            self.progress_indicator.setColor(COLOR_PALETTE['warning'])
        else:
            self.progress_indicator.setColor(COLOR_PALETTE['error'])
            
        # Ajouter à l'historique
        self.history.append(value)
        if len(self.history) > self.max_history:
            self.history.pop(0)
            
        # Mettre à jour le graphique
        self.history_chart.updateData(self.history)

class MiniChart(QWidget):
    """Mini graphique pour afficher l'historique"""
    
    def __init__(self):
        super().__init__()
        self.data: List[float] = []
        self.max_value = 100
        
    def updateData(self, data: List[float]):
        """Met à jour les données du graphique"""
        self.data = data.copy()
        if self.data:
            self.max_value = max(100, max(self.data))
        self.update()
        
    def paintEvent(self, event):
        """Dessine le mini graphique"""
        if not self.data or len(self.data) < 2:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dimensions
        width = self.width()
        height = self.height()
        
        # Calculer les points
        points = []
        for i, value in enumerate(self.data):
            x = int(i * width / (len(self.data) - 1))
            y = int(height - (value / self.max_value) * height)
            points.append(QPoint(x, y))
            
        # Dessiner la ligne
        pen = QPen(QColor(COLOR_PALETTE['primary']), 2)
        painter.setPen(pen)
        
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])
            
        # Zone sous la courbe
        if len(points) > 2:
            brush = QBrush(QColor(COLOR_PALETTE['primary'] + "20"))  # Transparence
            painter.setBrush(brush)
            painter.setPen(Qt.PenStyle.NoPen)
            
            polygon = QPolygon()
            polygon.append(QPoint(0, height))
            for point in points:
                polygon.append(point)
            polygon.append(QPoint(width, height))
            
            painter.drawPolygon(polygon)

class SystemMonitorPanel(QWidget):
    """Panel principal de monitoring système"""
    
    def __init__(self):
        super().__init__()
        self.gpu_available = gpu_manager.is_available()
        self._setupUI()
        self._setupTimer()
        
    def _setupUI(self):
        """Configure l'interface du panel"""
        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Titre du panel
        title = QLabel("Monitoring Système")
        title.setFont(FONTS['title'])
        title.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']};")
        layout.addWidget(title, 0, 0, 1, 4)
        
        # Métriques CPU
        self.cpu_card = SystemMetricCard("CPU", "🔧", "%")
        layout.addWidget(self.cpu_card, 1, 0)
        
        # Métriques RAM
        self.ram_card = SystemMetricCard("RAM", "💾", "%")
        layout.addWidget(self.ram_card, 1, 1)
        
        # Métriques GPU (si disponible)
        if self.gpu_available:
            self.gpu_card = SystemMetricCard("GPU", "🎮", "%")
            layout.addWidget(self.gpu_card, 1, 2)
            
            self.vram_card = SystemMetricCard("VRAM", "📊", "%")
            layout.addWidget(self.vram_card, 1, 3)
        
        # Métriques réseau
        self.network_card = SystemMetricCard("Réseau", "🌐", "MB/s")
        layout.addWidget(self.network_card, 2, 0)
        
        # Métriques disque
        self.disk_card = SystemMetricCard("Disque", "💿", "%")
        layout.addWidget(self.disk_card, 2, 1)
        
        # Températures
        if self.gpu_available:
            self.temp_card = SystemMetricCard("Temp GPU", "🌡️", "°C")
            self.temp_card.progress_indicator.max_value = 100  # Températures jusqu'à 100°C
            layout.addWidget(self.temp_card, 2, 2)
        
    def _setupTimer(self):
        """Configure le timer de mise à jour"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._updateMetrics)
        self.update_timer.start(1000)  # Mise à jour chaque seconde
        
        # Variables pour calculs réseau
        self.last_network_time = time.time()
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0
        
    def _updateMetrics(self):
        """Met à jour toutes les métriques"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=None)
            self.cpu_card.updateValue(cpu_percent)
            
            # RAM
            memory = psutil.virtual_memory()
            self.ram_card.updateValue(memory.percent)
            
            # GPU (si disponible)
            if self.gpu_available:
                gpu_info = gpu_manager.get_gpu_info()
                if gpu_info:
                    self.gpu_card.updateValue(gpu_info.utilization_gpu)
                    self.vram_card.updateValue(gpu_info.vram_usage_percent)
                    
                    if hasattr(gpu_info, 'temperature_c') and gpu_info.temperature_c is not None:
                        self.temp_card.updateValue(gpu_info.temperature_c)
            
            # Réseau
            network_stats = psutil.net_io_counters()
            current_time = time.time()
            
            if hasattr(self, 'last_network_time'):
                time_diff = current_time - self.last_network_time
                bytes_sent_diff = network_stats.bytes_sent - self.last_bytes_sent
                bytes_recv_diff = network_stats.bytes_recv - self.last_bytes_recv
                
                if time_diff > 0:
                    # Calcul en MB/s
                    network_speed = (bytes_sent_diff + bytes_recv_diff) / time_diff / 1024 / 1024
                    self.network_card.updateValue(network_speed)
                    self.network_card.unit = "MB/s"
                    self.network_card.progress_indicator.max_value = 100  # Max 100 MB/s pour l'affichage
            
            self.last_network_time = current_time
            self.last_bytes_sent = network_stats.bytes_sent
            self.last_bytes_recv = network_stats.bytes_recv
            
            # Disque
            disk_usage = psutil.disk_usage('/')
            self.disk_card.updateValue(disk_usage.percent)
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour des métriques: {e}")

class CompactSystemMonitor(QWidget):
    """Version compacte du monitoring pour la barre de statut"""
    
    def __init__(self):
        super().__init__()
        self.gpu_available = gpu_manager.is_available()
        self._setupUI()
        self._setupTimer()
        
    def _setupUI(self):
        """Configure l'interface compacte"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(12)
        
        # CPU
        self.cpu_label = QLabel("CPU: --")
        self.cpu_label.setFont(FONTS['small'])
        layout.addWidget(self.cpu_label)
        
        # RAM
        self.ram_label = QLabel("RAM: --")
        self.ram_label.setFont(FONTS['small'])
        layout.addWidget(self.ram_label)
        
        # GPU (si disponible)
        if self.gpu_available:
            self.gpu_label = QLabel("GPU: --")
            self.gpu_label.setFont(FONTS['small'])
            layout.addWidget(self.gpu_label)
        
        # Style
        self.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_PALETTE['text_secondary']};
                padding: 2px 6px;
                border-radius: 4px;
                background-color: {COLOR_PALETTE['bg_secondary']};
            }}
        """)
        
    def _setupTimer(self):
        """Configure le timer de mise à jour"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._updateMetrics)
        self.update_timer.start(2000)  # Mise à jour toutes les 2 secondes
        
    def _updateMetrics(self):
        """Met à jour les métriques compactes"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=None)
            self.cpu_label.setText(f"CPU: {cpu_percent:.0f}%")
            self._updateLabelColor(self.cpu_label, cpu_percent)
            
            # RAM
            memory = psutil.virtual_memory()
            self.ram_label.setText(f"RAM: {memory.percent:.0f}%")
            self._updateLabelColor(self.ram_label, memory.percent)
            
            # GPU
            if self.gpu_available:
                gpu_info = gpu_manager.get_gpu_info()
                if gpu_info:
                    self.gpu_label.setText(f"GPU: {gpu_info.utilization_gpu:.0f}%")
                    self._updateLabelColor(self.gpu_label, gpu_info.utilization_gpu)
                else:
                    self.gpu_label.setText("GPU: N/A")
                    
        except Exception as e:
            print(f"Erreur monitoring compact: {e}")
            
    def _updateLabelColor(self, label: QLabel, value: float):
        """Met à jour la couleur selon la valeur"""
        if value < 50:
            color = COLOR_PALETTE['success']
        elif value < 80:
            color = COLOR_PALETTE['warning']
        else:
            color = COLOR_PALETTE['error']
            
        label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                padding: 2px 6px;
                border-radius: 4px;
                background-color: {COLOR_PALETTE['bg_secondary']};
                font-weight: bold;
            }}
        """)

# Exports
__all__ = [
    'CircularProgressIndicator',
    'SystemMetricCard', 
    'MiniChart',
    'SystemMonitorPanel',
    'CompactSystemMonitor'
]