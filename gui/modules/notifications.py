"""
Système de notifications optimisé
Version améliorée utilisant les modules core centralisés
"""

import sys
import os
from enum import Enum
from typing import Optional, List, Callable

# Ajouter le répertoire parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from gui.core.qt_imports import *
from gui.core.widgets import ModernButton

class NotificationType(Enum):
    """Types de notifications disponibles"""
    INFO = "info"
    SUCCESS = "success" 
    WARNING = "warning"
    ERROR = "error"

class NotificationWidget(QWidget):
    """Widget de notification toast moderne"""
    
    # Signaux
    closed = Signal()
    clicked = Signal()
    
    def __init__(self, title: str, message: str, 
                 notification_type: NotificationType = NotificationType.INFO,
                 duration: int = 5000, 
                 action_text: str = "",
                 action_callback: Optional[Callable] = None):
        super().__init__()
        
        self.title = title
        self.message = message
        self.type = notification_type
        self.duration = duration
        self.action_callback = action_callback
        
        # Configuration de base
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(350, 80)
        
        self._setupUI(action_text)
        self._setupStyle()
        self._setupAnimations()
        self._setupTimers()
        
    def _setupUI(self, action_text: str):
        """Configure l'interface utilisateur"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # Icône du type
        icon_label = QLabel(self._getIcon())
        icon_label.setFont(QFont('Segoe UI', 16))
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Contenu principal
        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)
        
        # Titre
        title_label = QLabel(self.title)
        title_label.setFont(FONTS['subtitle'])
        title_label.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']}; font-weight: bold;")
        content_layout.addWidget(title_label)
        
        # Message
        message_label = QLabel(self.message)
        message_label.setFont(FONTS['small'])
        message_label.setStyleSheet(f"color: {COLOR_PALETTE['text_secondary']};")
        message_label.setWordWrap(True)
        content_layout.addWidget(message_label)
        
        layout.addLayout(content_layout)
        
        # Bouton d'action (optionnel)
        if action_text and self.action_callback:
            action_btn = ModernButton(action_text, style="primary")
            action_btn.clicked.connect(self.action_callback)
            action_btn.clicked.connect(self.close)
            layout.addWidget(action_btn)
        
        # Bouton fermer
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLOR_PALETTE['text_secondary']};
                border: none;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {COLOR_PALETTE['text_primary']};
                background-color: {COLOR_PALETTE['error']};
                border-radius: 10px;
            }}
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
    def _setupStyle(self):
        """Configure le style selon le type de notification"""
        colors = {
            NotificationType.INFO: COLOR_PALETTE['info'],
            NotificationType.SUCCESS: COLOR_PALETTE['success'],
            NotificationType.WARNING: COLOR_PALETTE['warning'],
            NotificationType.ERROR: COLOR_PALETTE['error'],
        }
        
        accent_color = colors[self.type]
        
        self.setStyleSheet(f"""
            NotificationWidget {{
                background-color: {COLOR_PALETTE['bg_card']};
                border: 1px solid {COLOR_PALETTE['border_primary']};
                border-left: 4px solid {accent_color};
                border-radius: 8px;
            }}
        """)
        
    def _setupAnimations(self):
        """Configure les animations d'entrée et sortie"""
        # Animation d'entrée (slide in from right)
        self.slide_in_animation = QPropertyAnimation(self, b"pos")
        self.slide_in_animation.setDuration(ANIMATIONS['normal'])
        self.slide_in_animation.setEasingCurve(ANIMATIONS['easing'])
        
        # Animation de sortie (fade out)
        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(ANIMATIONS['fast'])
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.finished.connect(self._onFadeOutFinished)
        
    def _setupTimers(self):
        """Configure les timers de disparition automatique"""
        if self.duration > 0:
            self.auto_close_timer = QTimer()
            self.auto_close_timer.timeout.connect(self.close)
            self.auto_close_timer.setSingleShot(True)
            self.auto_close_timer.start(self.duration)
        
    def _getIcon(self) -> str:
        """Retourne l'icône appropriée selon le type"""
        icons = {
            NotificationType.INFO: "ℹ️",
            NotificationType.SUCCESS: "✅",
            NotificationType.WARNING: "⚠️",
            NotificationType.ERROR: "❌",
        }
        return icons[self.type]
        
    def show(self):
        """Affiche la notification avec animation"""
        super().show()
        self._animateIn()
        
    def _animateIn(self):
        """Animation d'entrée"""
        # Position de départ (hors écran à droite)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        start_pos = QPoint(screen_geometry.width(), self.y())
        end_pos = QPoint(screen_geometry.width() - self.width() - 20, self.y())
        
        self.move(start_pos)
        
        self.slide_in_animation.setStartValue(start_pos)
        self.slide_in_animation.setEndValue(end_pos)
        self.slide_in_animation.start()
        
    def close(self):
        """Ferme la notification avec animation"""
        if hasattr(self, 'auto_close_timer'):
            self.auto_close_timer.stop()
        self.fade_out_animation.start()
        
    def _onFadeOutFinished(self):
        """Callback appelé à la fin de l'animation de sortie"""
        self.closed.emit()
        super().close()

class NotificationManager(QObject):
    """Gestionnaire des notifications"""
    
    def __init__(self):
        super().__init__()
        self.notifications: List[NotificationWidget] = []
        self.max_notifications = 5
        self.notification_spacing = 90
        
    def show_notification(self, title: str, message: str, 
                         notification_type: NotificationType = NotificationType.INFO,
                         duration: int = 5000,
                         action_text: str = "",
                         action_callback: Optional[Callable] = None):
        """Affiche une nouvelle notification"""
        
        # Limiter le nombre de notifications affichées
        if len(self.notifications) >= self.max_notifications:
            self._removeOldestNotification()
            
        # Créer la nouvelle notification
        notification = NotificationWidget(
            title, message, notification_type, duration, 
            action_text, action_callback
        )
        
        # Positionner la notification
        self._positionNotification(notification)
        
        # Connecter les signaux
        notification.closed.connect(lambda: self._onNotificationClosed(notification))
        
        # Ajouter à la liste et afficher
        self.notifications.append(notification)
        notification.show()
        
        return notification
        
    def _positionNotification(self, notification: NotificationWidget):
        """Positionne une notification à l'écran"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        
        # Position Y basée sur le nombre de notifications existantes
        y_offset = 20 + (len(self.notifications) * self.notification_spacing)
        
        notification.move(
            screen_geometry.width() - notification.width() - 20,
            y_offset
        )
        
    def _onNotificationClosed(self, notification: NotificationWidget):
        """Callback appelé quand une notification se ferme"""
        if notification in self.notifications:
            self.notifications.remove(notification)
            self._repositionNotifications()
            
    def _removeOldestNotification(self):
        """Supprime la notification la plus ancienne"""
        if self.notifications:
            oldest = self.notifications[0]
            oldest.close()
            
    def _repositionNotifications(self):
        """Repositionne toutes les notifications après une fermeture"""
        for i, notification in enumerate(self.notifications):
            new_y = 20 + (i * self.notification_spacing)
            
            # Animation de repositionnement
            animation = QPropertyAnimation(notification, b"pos")
            animation.setDuration(ANIMATIONS['fast'])
            animation.setEasingCurve(ANIMATIONS['easing'])
            animation.setStartValue(notification.pos())
            animation.setEndValue(QPoint(notification.x(), new_y))
            animation.start()
            
    # Méthodes de convenance pour différents types
    def info(self, title: str, message: str, **kwargs):
        return self.show_notification(title, message, NotificationType.INFO, **kwargs)
        
    def success(self, title: str, message: str, **kwargs):
        return self.show_notification(title, message, NotificationType.SUCCESS, **kwargs)
        
    def warning(self, title: str, message: str, **kwargs):
        return self.show_notification(title, message, NotificationType.WARNING, **kwargs)
        
    def error(self, title: str, message: str, **kwargs):
        return self.show_notification(title, message, NotificationType.ERROR, **kwargs)

# Instance globale du gestionnaire
notification_manager = NotificationManager()

# Fonctions de convenance globales
def show_info(title: str, message: str, **kwargs):
    return notification_manager.info(title, message, **kwargs)

def show_success(title: str, message: str, **kwargs):
    return notification_manager.success(title, message, **kwargs)

def show_warning(title: str, message: str, **kwargs):
    return notification_manager.warning(title, message, **kwargs)

def show_error(title: str, message: str, **kwargs):
    return notification_manager.error(title, message, **kwargs)

# Exports
__all__ = [
    'NotificationType',
    'NotificationWidget', 
    'NotificationManager',
    'notification_manager',
    'show_info', 'show_success', 'show_warning', 'show_error'
]