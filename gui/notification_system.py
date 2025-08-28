#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de notifications pour NeuroBot GUI
Notifications toast modernes avec animation
"""

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import QTimer, QPropertyAnimation, QRect, QEasingCurve, Signal, Qt
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPixmap
from enum import Enum
from typing import Optional, List
import time

class NotificationType(Enum):
    INFO = "info"
    SUCCESS = "success" 
    WARNING = "warning"
    ERROR = "error"

class NotificationWidget(QWidget):
    closed = Signal()
    
    def __init__(self, title: str, message: str, notification_type: NotificationType = NotificationType.INFO, duration: int = 5000):
        super().__init__()
        self.title = title
        self.message = message
        self.type = notification_type
        self.duration = duration
        
        self.setupUI()
        self.setupAnimations()
        self.setupTimer()
        
    def setupUI(self):
        self.setFixedSize(350, 100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Couleurs selon le type (thème sombre)
        colors = {
            NotificationType.INFO: {'bg': '#2d3748', 'accent': '#4a9eff'},
            NotificationType.SUCCESS: {'bg': '#22543d', 'accent': '#4ade80'},
            NotificationType.WARNING: {'bg': '#744210', 'accent': '#fbbf24'},
            NotificationType.ERROR: {'bg': '#742a2a', 'accent': '#ef4444'}
        }
        
        self.colors = colors[self.type]
        
        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Icône
        icon_label = QLabel()
        icon_label.setFixedSize(30, 30)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Icônes selon le type
        icons = {
            NotificationType.INFO: "ℹ️",
            NotificationType.SUCCESS: "✅", 
            NotificationType.WARNING: "⚠️",
            NotificationType.ERROR: "❌"
        }
        
        icon_label.setText(icons[self.type])
        icon_label.setStyleSheet(f"font-size: 20px;")
        layout.addWidget(icon_label)
        
        # Texte
        text_layout = QVBoxLayout()
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"color: white; font-size: 14px; font-weight: bold;")
        text_layout.addWidget(title_label)
        
        message_label = QLabel(self.message)
        message_label.setStyleSheet(f"color: #F2E0DF; font-size: 12px;")
        message_label.setWordWrap(True)
        text_layout.addWidget(message_label)
        
        layout.addLayout(text_layout)
        
        # Bouton fermer
        close_btn = QPushButton("×")
        close_btn.setFixedSize(25, 25)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }
        """)
        close_btn.clicked.connect(self.close_notification)
        layout.addWidget(close_btn)
        
        # Ombre portée
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
    def setupAnimations(self):
        # Animation d'entrée (glissement depuis la droite)
        self.slide_in = QPropertyAnimation(self, b"geometry")
        self.slide_in.setDuration(300)
        self.slide_in.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animation de sortie
        self.slide_out = QPropertyAnimation(self, b"geometry") 
        self.slide_out.setDuration(200)
        self.slide_out.setEasingCurve(QEasingCurve.InCubic)
        self.slide_out.finished.connect(self.close)
        
    def setupTimer(self):
        if self.duration > 0:
            self.timer = QTimer()
            self.timer.timeout.connect(self.close_notification)
            self.timer.setSingleShot(True)
            self.timer.start(self.duration)
            
    def show_at_position(self, x: int, y: int):
        # Position finale
        final_rect = QRect(x, y, 350, 100)
        
        # Position initiale (hors écran à droite)
        start_rect = QRect(x + 350, y, 350, 100)
        
        self.setGeometry(start_rect)
        self.show()
        
        # Lance l'animation d'entrée
        self.slide_in.setStartValue(start_rect)
        self.slide_in.setEndValue(final_rect)
        self.slide_in.start()
        
    def close_notification(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
            
        # Animation de sortie
        current_rect = self.geometry()
        end_rect = QRect(current_rect.x() + 350, current_rect.y(), 350, 100)
        
        self.slide_out.setStartValue(current_rect)
        self.slide_out.setEndValue(end_rect)
        self.slide_out.start()
        
        self.closed.emit()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fond avec bordures arrondies
        rect = self.rect().adjusted(5, 5, -5, -5)  # Marge pour l'ombre
        
        # Gradient de fond
        bg_color = QColor(self.colors['bg'])
        accent_color = QColor(self.colors['accent'])
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(accent_color, 2))
        painter.drawRoundedRect(rect, 10, 10)
        
        # Barre de progression si durée limitée
        if self.duration > 0 and hasattr(self, 'timer'):
            remaining = self.timer.remainingTime()
            progress = 1 - (remaining / self.duration)
            
            progress_rect = QRect(rect.left(), rect.bottom() - 3, int(rect.width() * progress), 3)
            painter.setBrush(QBrush(accent_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(progress_rect)

class NotificationManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.notifications: List[NotificationWidget] = []
        self.max_notifications = 5
        self.spacing = 10
        
        # Timer pour mettre à jour les positions
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_positions)
        self.update_timer.start(100)  # 10 FPS
        
    def show_notification(self, title: str, message: str, 
                         notification_type: NotificationType = NotificationType.INFO,
                         duration: int = 5000):
        """Affiche une nouvelle notification"""
        
        # Supprime les anciennes notifications si on dépasse la limite
        while len(self.notifications) >= self.max_notifications:
            old_notification = self.notifications.pop(0)
            old_notification.close_notification()
            
        # Crée la nouvelle notification
        notification = NotificationWidget(title, message, notification_type, duration)
        notification.closed.connect(lambda: self.remove_notification(notification))
        
        self.notifications.append(notification)
        
        # Position initiale (coin supérieur droit de l'écran)
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        
        x = screen.width() - 370  # 350 + 20 de marge
        y = 20 + len(self.notifications) * (100 + self.spacing)
        
        notification.show_at_position(x, y)
        
    def remove_notification(self, notification: NotificationWidget):
        """Supprime une notification et réorganise les autres"""
        if notification in self.notifications:
            self.notifications.remove(notification)
            self.reorganize_notifications()
            
    def reorganize_notifications(self):
        """Réorganise les positions des notifications restantes"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        
        for i, notification in enumerate(self.notifications):
            x = screen.width() - 370
            y = 20 + i * (100 + self.spacing)
            
            # Animation vers la nouvelle position
            current_rect = notification.geometry()
            target_rect = QRect(x, y, 350, 100)
            
            if current_rect != target_rect:
                animation = QPropertyAnimation(notification, b"geometry")
                animation.setDuration(200)
                animation.setStartValue(current_rect)
                animation.setEndValue(target_rect)
                animation.setEasingCurve(QEasingCurve.OutCubic)
                animation.start()
                
    def update_positions(self):
        """Met à jour les positions si nécessaire"""
        # Vérifie si certaines notifications sont fermées
        active_notifications = [n for n in self.notifications if n.isVisible()]
        if len(active_notifications) != len(self.notifications):
            self.notifications = active_notifications
            self.reorganize_notifications()
            
    def clear_all(self):
        """Ferme toutes les notifications"""
        for notification in self.notifications:
            notification.close_notification()
        self.notifications.clear()

# Instance globale du gestionnaire de notifications
notification_manager = NotificationManager()

def show_info(title: str, message: str, duration: int = 5000):
    """Affiche une notification d'information"""
    notification_manager.show_notification(title, message, NotificationType.INFO, duration)
    
def show_success(title: str, message: str, duration: int = 5000):
    """Affiche une notification de succès"""
    notification_manager.show_notification(title, message, NotificationType.SUCCESS, duration)
    
def show_warning(title: str, message: str, duration: int = 5000):
    """Affiche une notification d'avertissement"""
    notification_manager.show_notification(title, message, NotificationType.WARNING, duration)
    
def show_error(title: str, message: str, duration: int = 5000):
    """Affiche une notification d'erreur"""
    notification_manager.show_notification(title, message, NotificationType.ERROR, duration)