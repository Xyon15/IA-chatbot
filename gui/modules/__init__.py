"""
Module d'initialisation des composants GUI spécialisés
Exporte tous les modules de gui/modules pour faciliter les imports
"""

import sys
import os

# Ajouter le répertoire parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Import des modules de composants
from .notifications import (
    NotificationType, NotificationWidget, NotificationManager,
    notification_manager, show_info, show_success, show_warning, show_error
)

from .monitoring import (
    CircularProgressIndicator, SystemMetricCard, MiniChart,
    SystemMonitorPanel, CompactSystemMonitor
)

from .chat import (
    MessageBubble, ChatInput, ChatHistory, ChatInterface
)

# Exports consolidés
__all__ = [
    # Notifications
    'NotificationType', 'NotificationWidget', 'NotificationManager',
    'notification_manager', 'show_info', 'show_success', 'show_warning', 'show_error',
    
    # Monitoring
    'CircularProgressIndicator', 'SystemMetricCard', 'MiniChart',
    'SystemMonitorPanel', 'CompactSystemMonitor',
    
    # Chat
    'MessageBubble', 'ChatInput', 'ChatHistory', 'ChatInterface',
]

# Fonctions utilitaires pour l'initialisation
def init_notification_system():
    """Initialise le système de notifications"""
    return notification_manager

def create_system_monitor(compact: bool = False):
    """Crée un widget de monitoring système"""
    if compact:
        return CompactSystemMonitor()
    else:
        return SystemMonitorPanel()

def create_chat_interface():
    """Crée une interface de chat complète"""
    return ChatInterface()