#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widgets de graphiques pour le monitoring temps réel NeuroBot GUI
Graphiques avec animation et couleurs de la palette
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QLinearGradient, QFont, QPolygonF
from typing import List, Tuple
import time
from collections import deque

COLOR_PALETTE = {
    'primary_dark': '#1a1a1a',
    'secondary_dark': '#2d2d2d',
    'neutral_light': '#3a3a3a',
    'accent_light': '#4a4a4a',
    'accent_warm': '#555555',
    'accent_orange': '#4a9eff',
    'text_dark': '#ffffff',
    'text_light': '#d1d5db',
    'success': '#4ade80',
    'warning': '#fbbf24',
    'error': '#ef4444'
}

class RealtimeChart(QWidget):
    """Widget de graphique temps réel avec animation fluide"""
    
    def __init__(self, title: str, max_points: int = 60, max_value: float = 100.0):
        super().__init__()
        self.title = title
        self.max_points = max_points
        self.max_value = max_value
        self.data_points = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)
        
        # Couleurs du graphique pour thème sombre
        self.line_color = QColor(COLOR_PALETTE['accent_orange'])
        self.fill_color = QColor(COLOR_PALETTE['accent_orange'])
        self.fill_color.setAlpha(80)
        self.grid_color = QColor(COLOR_PALETTE['accent_light'])
        self.text_color = QColor(COLOR_PALETTE['text_light'])
        self.bg_color = QColor(COLOR_PALETTE['secondary_dark'])
        
        self.setMinimumSize(300, 200)
        
        # Timer pour redessiner le graphique
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(100)  # Redessine toutes les 100ms
        
    def add_data_point(self, value: float):
        """Ajoute un nouveau point de données"""
        current_time = time.time()
        self.data_points.append(max(0, min(value, self.max_value)))
        self.timestamps.append(current_time)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        margin = 20
        chart_rect = rect.adjusted(margin, margin + 20, -margin, -margin - 20)
        
        # Fond sombre
        painter.fillRect(rect, QBrush(self.bg_color))
        
        # Titre
        painter.setPen(QPen(self.text_color))
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect.adjusted(0, 5, 0, 0), Qt.AlignTop | Qt.AlignHCenter, self.title)
        
        if len(self.data_points) < 2:
            return
            
        # Grille
        self.draw_grid(painter, chart_rect)
        
        # Graphique
        self.draw_chart(painter, chart_rect)
        
        # Valeur actuelle
        if self.data_points:
            current_value = self.data_points[-1]
            value_text = f"{current_value:.1f}%"
            
            font = QFont("Arial", 14, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QPen(self.line_color))
            painter.drawText(chart_rect, Qt.AlignTop | Qt.AlignRight, value_text)
    
    def draw_grid(self, painter: QPainter, rect):
        """Dessine la grille du graphique"""
        painter.setPen(QPen(self.grid_color, 1, Qt.DashLine))
        
        # Lignes horizontales (valeurs)
        for i in range(0, int(self.max_value) + 1, int(self.max_value / 4)):
            y = rect.bottom() - (i / self.max_value) * rect.height()
            painter.drawLine(rect.left(), y, rect.right(), y)
            
            # Labels des valeurs
            painter.setPen(QPen(self.text_color))
            font = QFont("Arial", 8)
            painter.setFont(font)
            painter.drawText(rect.left() - 15, y + 3, f"{i}")
            painter.setPen(QPen(self.grid_color, 1, Qt.DashLine))
        
        # Lignes verticales (temps)
        time_intervals = 5
        for i in range(time_intervals + 1):
            x = rect.left() + (i / time_intervals) * rect.width()
            painter.drawLine(x, rect.top(), x, rect.bottom())
    
    def draw_chart(self, painter: QPainter, rect):
        """Dessine la courbe du graphique"""
        if len(self.data_points) < 2:
            return
            
        # Points de la courbe
        points = []
        width = rect.width()
        height = rect.height()
        
        for i, value in enumerate(self.data_points):
            x = rect.left() + (i / max(1, len(self.data_points) - 1)) * width
            y = rect.bottom() - (value / self.max_value) * height
            points.append(QPointF(x, y))
        
        if len(points) < 2:
            return
            
        # Zone remplie sous la courbe
        fill_points = [QPointF(rect.left(), rect.bottom())]
        fill_points.extend(points)
        fill_points.append(QPointF(rect.right(), rect.bottom()))
        
        polygon = QPolygonF(fill_points)
        painter.setBrush(QBrush(self.fill_color))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(polygon)
        
        # Ligne principale
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(self.line_color, 3))
        
        line_polygon = QPolygonF(points)
        painter.drawPolyline(line_polygon)
        
        # Points sur la courbe
        painter.setBrush(QBrush(self.line_color))
        painter.setPen(QPen(QColor("white"), 2))
        
        for point in points[-5:]:  # Seulement les 5 derniers points
            painter.drawEllipse(point, 4, 4)

class MultiChart(QWidget):
    """Widget contenant plusieurs graphiques côte à côte"""
    
    def __init__(self, charts_config: List[Tuple[str, float]]):
        super().__init__()
        self.charts = []
        
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        
        for title, max_value in charts_config:
            chart = RealtimeChart(title, max_points=60, max_value=max_value)
            self.charts.append(chart)
            layout.addWidget(chart)
    
    def update_data(self, values: List[float]):
        """Met à jour tous les graphiques avec de nouvelles valeurs"""
        for chart, value in zip(self.charts, values):
            chart.add_data_point(value)

class CircularProgressWidget(QWidget):
    """Widget de progression circulaire moderne"""
    
    def __init__(self, title: str, max_value: float = 100.0):
        super().__init__()
        self.title = title
        self.max_value = max_value
        self.current_value = 0.0
        self.target_value = 0.0
        
        # Animation fluide vers la valeur cible
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_value)
        self.animation_timer.start(16)  # ~60 FPS
        
        self.setFixedSize(120, 120)
        
    def set_value(self, value: float):
        """Définit la valeur cible (avec animation)"""
        self.target_value = max(0, min(value, self.max_value))
        
    def animate_value(self):
        """Animation fluide vers la valeur cible"""
        if abs(self.current_value - self.target_value) < 0.1:
            self.current_value = self.target_value
        else:
            # Interpolation fluide
            self.current_value += (self.target_value - self.current_value) * 0.1
            
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 10
        
        # Cercle de fond
        painter.setPen(QPen(QColor(COLOR_PALETTE['neutral_light']), 8))
        painter.drawEllipse(center, radius, radius)
        
        # Arc de progression
        progress_angle = int(360 * (self.current_value / self.max_value))
        
        # Couleur selon la valeur
        if self.current_value < self.max_value * 0.5:
            color = QColor(COLOR_PALETTE['success'])
        elif self.current_value < self.max_value * 0.8:
            color = QColor(COLOR_PALETTE['warning'])
        else:
            color = QColor(COLOR_PALETTE['error'])
            
        painter.setPen(QPen(color, 8, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(center.x() - radius, center.y() - radius, 
                       radius * 2, radius * 2, 90 * 16, -progress_angle * 16)
        
        # Texte central
        painter.setPen(QPen(QColor(COLOR_PALETTE['primary_dark'])))
        
        # Valeur
        font = QFont("Arial", 14, QFont.Bold)
        painter.setFont(font)
        value_text = f"{self.current_value:.1f}%"
        painter.drawText(rect, Qt.AlignCenter, value_text)
        
        # Titre
        font = QFont("Arial", 9)
        painter.setFont(font)
        title_rect = rect.adjusted(0, 40, 0, 0)
        painter.drawText(title_rect, Qt.AlignCenter, self.title)

class DashboardWidget(QWidget):
    """Widget tableau de bord avec graphiques et métriques"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_update_timer()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("📈 DASHBOARD TEMPS RÉEL")
        title.setStyleSheet(f"color: {COLOR_PALETTE['primary_dark']}; font-size: 20px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Métriques circulaires
        circles_layout = QHBoxLayout()
        
        self.cpu_circle = CircularProgressWidget("CPU", 100.0)
        self.ram_circle = CircularProgressWidget("RAM", 100.0)
        self.gpu_circle = CircularProgressWidget("GPU", 100.0)
        self.vram_circle = CircularProgressWidget("VRAM", 100.0)
        
        circles_layout.addWidget(self.cpu_circle)
        circles_layout.addWidget(self.ram_circle)
        circles_layout.addWidget(self.gpu_circle)
        circles_layout.addWidget(self.vram_circle)
        circles_layout.addStretch()
        
        layout.addLayout(circles_layout)
        
        # Graphiques temps réel
        self.charts = MultiChart([
            ("CPU Usage", 100.0),
            ("Memory Usage", 100.0),
            ("GPU Usage", 100.0)
        ])
        
        layout.addWidget(self.charts)
        
    def setup_update_timer(self):
        """Configure le timer de mise à jour des données"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_metrics)
        self.update_timer.start(2000)  # Mise à jour toutes les 2 secondes
        
    def update_metrics(self):
        """Met à jour toutes les métriques (sera connecté aux vraies données)"""
        import psutil
        import random
        
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_circle.set_value(cpu_percent)
            
            # RAM  
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            self.ram_circle.set_value(ram_percent)
            
            # GPU (simulation pour test)
            gpu_usage = random.uniform(10, 90)
            self.gpu_circle.set_value(gpu_usage)
            
            # VRAM (simulation pour test) 
            vram_usage = random.uniform(20, 80)
            self.vram_circle.set_value(vram_usage)
            
            # Met à jour les graphiques
            self.charts.update_data([cpu_percent, ram_percent, gpu_usage])
            
        except Exception as e:
            print(f"Erreur mise à jour métriques: {e}")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    dashboard = DashboardWidget()
    dashboard.show()
    
    sys.exit(app.exec())