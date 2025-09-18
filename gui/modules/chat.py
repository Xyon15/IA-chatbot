"""
Interface de chat optimisée avec bulles de messages modernes
Utilise les modules core pour un style unifié
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

# Ajouter le répertoire parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from gui.core.qt_imports import *
from gui.core.widgets import ModernButton
from PySide6.QtWidgets import (
    QScrollArea, QGraphicsOpacityEffect, QMessageBox, QFileDialog
)
from PySide6.QtCore import QPropertyAnimation

class MessageBubble(QWidget):
    """Bulle de message moderne avec support markdown"""
    
    def __init__(self, message: str, is_user: bool = True, timestamp: Optional[datetime] = None):
        super().__init__()
        self.message = message
        self.is_user = is_user
        self.timestamp = timestamp or datetime.now()
        
        self._setupUI()
        self._setupStyle()
        
    def _setupUI(self):
        """Configure l'interface de la bulle"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Container principal pour l'alignement
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Avatar (pour les messages du bot)
        if not self.is_user:
            avatar = QLabel("🤖")
            avatar.setFixedSize(32, 32)
            avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            avatar.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLOR_PALETTE['primary']};
                    border-radius: 16px;
                    font-size: 16px;
                }}
            """)
            container_layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignTop)
            container_layout.addSpacing(8)
        
        # Contenu du message
        self.message_content = QWidget()
        message_layout = QVBoxLayout(self.message_content)
        message_layout.setContentsMargins(12, 8, 12, 8)
        message_layout.setSpacing(4)
        
        # Texte du message
        self.message_label = QLabel(self.message)
        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.message_label.setFont(FONTS['body'])
        message_layout.addWidget(self.message_label)
        
        # Timestamp
        time_str = self.timestamp.strftime("%H:%M")
        self.time_label = QLabel(time_str)
        self.time_label.setFont(FONTS['caption'])
        self.time_label.setStyleSheet(f"color: {COLOR_PALETTE['text_tertiary']};")
        
        if self.is_user:
            self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        message_layout.addWidget(self.time_label)
        
        # Alignement selon l'expéditeur
        if self.is_user:
            container_layout.addStretch()
            container_layout.addWidget(self.message_content)
        else:
            container_layout.addWidget(self.message_content)
            container_layout.addStretch()
        
        layout.addWidget(container)
        
    def _setupStyle(self):
        """Configure le style de la bulle"""
        if self.is_user:
            # Style utilisateur (droite, bleu)
            bg_color = COLOR_PALETTE['primary']
            text_color = "#FFFFFF"
            border_radius = "18px 18px 4px 18px"
        else:
            # Style bot (gauche, gris)
            bg_color = COLOR_PALETTE['bg_card']
            text_color = COLOR_PALETTE['text_primary']
            border_radius = "18px 18px 18px 4px"
        
        # Appliquer le style au widget message_content
        self.message_content.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: {border_radius};
                border: 1px solid {COLOR_PALETTE['border_primary']};
            }}
        """)
        
        self.message_label.setStyleSheet(f"color: {text_color};")

class ChatInput(QWidget):
    """Zone de saisie de messages avancée"""
    
    # Signaux
    message_sent = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._setupUI()
        self._setupConnections()
        
    def _setupUI(self):
        """Configure l'interface de saisie"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        
        # Zone de texte
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Tapez votre message... (Ctrl+Entrée pour envoyer)")
        self.text_input.setMaximumHeight(120)
        self.text_input.setFont(FONTS['body'])
        
        # Style de la zone de texte
        self.text_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLOR_PALETTE['bg_secondary']};
                border: 2px solid {COLOR_PALETTE['border_primary']};
                border-radius: 12px;
                padding: 8px;
                color: {COLOR_PALETTE['text_primary']};
            }}
            QTextEdit:focus {{
                border-color: {COLOR_PALETTE['primary']};
            }}
        """)
        
        layout.addWidget(self.text_input)
        
        # Boutons d'action
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(4)
        
        # Bouton envoyer
        self.send_button = ModernButton("Envoyer", style="primary")
        self.send_button.setFixedSize(80, 36)
        buttons_layout.addWidget(self.send_button)
        
        # Bouton clear
        self.clear_button = ModernButton("Effacer", style="secondary")
        self.clear_button.setFixedSize(80, 28)
        buttons_layout.addWidget(self.clear_button)
        
        layout.addLayout(buttons_layout)
        
        # Style du widget principal
        self.setStyleSheet(f"""
            ChatInput {{
                background-color: {COLOR_PALETTE['bg_card']};
                border-top: 1px solid {COLOR_PALETTE['border_primary']};
            }}
        """)
        
    def _setupConnections(self):
        """Configure les connexions des signaux"""
        self.send_button.clicked.connect(self._sendMessage)
        self.clear_button.clicked.connect(self._clearInput)
        
        # Raccourci clavier
        self.text_input.keyPressEvent = self._handleKeyPress
        
    def _handleKeyPress(self, event):
        """Gère les raccourcis clavier"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._sendMessage()
                return
        
        # Comportement par défaut
        QTextEdit.keyPressEvent(self.text_input, event)
        
    def _sendMessage(self):
        """Envoie le message"""
        text = self.text_input.toPlainText().strip()
        if text:
            self.message_sent.emit(text)
            self._clearInput()
            
    def _clearInput(self):
        """Efface le champ de saisie"""
        self.text_input.clear()
        self.text_input.setFocus()
        
    def setFocus(self):
        """Met le focus sur la zone de saisie"""
        self.text_input.setFocus()

class ChatHistory(QScrollArea):
    """Zone d'historique des messages avec scroll automatique"""
    
    def __init__(self):
        super().__init__()
        self.messages: List[MessageBubble] = []
        self._setupUI()
        
    def _setupUI(self):
        """Configure l'interface de l'historique"""
        # Widget conteneur pour les messages
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(12)
        self.content_layout.addStretch()  # Pour pousser les messages vers le bas
        
        # Configuration du scroll area
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Style
        self.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLOR_PALETTE['bg_primary']};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {COLOR_PALETTE['bg_secondary']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLOR_PALETTE['border_primary']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {COLOR_PALETTE['primary']};
            }}
        """)
        
    def addMessage(self, message: str, is_user: bool = True, timestamp: Optional[datetime] = None):
        """Ajoute un message à l'historique"""
        bubble = MessageBubble(message, is_user, timestamp)
        self.messages.append(bubble)
        
        # Insérer avant le stretch
        self.content_layout.insertWidget(self.content_layout.count() - 1, bubble)
        
        # Animation d'apparition
        effect = QGraphicsOpacityEffect()
        bubble.setGraphicsEffect(effect)
        
        self.fade_animation = QPropertyAnimation(effect, b"opacity")
        self.fade_animation.setDuration(ANIMATIONS['fast'])
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
        
        # Scroll automatique vers le bas
        QTimer.singleShot(50, self._scrollToBottom)
        
    def _scrollToBottom(self):
        """Scroll automatiquement vers le bas"""
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def clearHistory(self):
        """Efface tout l'historique"""
        for message in self.messages:
            message.deleteLater()
        self.messages.clear()
        
    def exportHistory(self) -> List[Dict]:
        """Exporte l'historique au format JSON"""
        history = []
        for bubble in self.messages:
            history.append({
                'message': bubble.message,
                'is_user': bubble.is_user,
                'timestamp': bubble.timestamp.isoformat()
            })
        return history
        
    def importHistory(self, history_data: List[Dict]):
        """Importe un historique depuis du JSON"""
        self.clearHistory()
        for msg_data in history_data:
            timestamp = datetime.fromisoformat(msg_data['timestamp'])
            self.addMessage(
                msg_data['message'],
                msg_data['is_user'],
                timestamp
            )

class ChatInterface(QWidget):
    """Interface de chat complète"""
    
    # Signaux
    message_sent = Signal(str)
    history_cleared = Signal()
    
    def __init__(self):
        super().__init__()
        self._setupUI()
        self._setupConnections()
        
    def _setupUI(self):
        """Configure l'interface principale"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header avec titre et actions
        header = self._createHeader()
        layout.addWidget(header)
        
        # Zone d'historique
        self.chat_history = ChatHistory()
        layout.addWidget(self.chat_history, stretch=1)
        
        # Zone de saisie
        self.chat_input = ChatInput()
        layout.addWidget(self.chat_input)
        
    def _createHeader(self) -> QWidget:
        """Crée le header de l'interface de chat"""
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_PALETTE['bg_card']};
                border-bottom: 1px solid {COLOR_PALETTE['border_primary']};
            }}
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 8, 16, 8)
        
        # Titre
        title = QLabel("💬 Chat IA")
        title.setFont(FONTS['title'])
        title.setStyleSheet(f"color: {COLOR_PALETTE['text_primary']};")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Boutons d'action
        self.clear_history_btn = ModernButton("Effacer historique", style="secondary")
        self.clear_history_btn.clicked.connect(self._clearHistory)
        layout.addWidget(self.clear_history_btn)
        
        self.export_btn = ModernButton("Exporter", style="secondary")
        self.export_btn.clicked.connect(self._exportHistory)
        layout.addWidget(self.export_btn)
        
        return header
        
    def _setupConnections(self):
        """Configure les connexions des signaux"""
        self.chat_input.message_sent.connect(self.message_sent)
        self.chat_input.message_sent.connect(self.addUserMessage)
        
    def addUserMessage(self, message: str):
        """Ajoute un message utilisateur"""
        self.chat_history.addMessage(message, is_user=True)
        
    def addBotMessage(self, message: str):
        """Ajoute un message du bot"""
        self.chat_history.addMessage(message, is_user=False)
        
    def _clearHistory(self):
        """Efface l'historique avec confirmation"""
        reply = QMessageBox.question(
            self, 
            "Confirmation",
            "Êtes-vous sûr de vouloir effacer tout l'historique ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_history.clearHistory()
            self.history_cleared.emit()
            
    def _exportHistory(self):
        """Exporte l'historique vers un fichier"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter l'historique",
            f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )
        
        if filename:
            try:
                history_data = self.chat_history.exportHistory()
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(history_data, f, indent=2, ensure_ascii=False)
                    
                QMessageBox.information(
                    self,
                    "Export réussi",
                    f"Historique exporté vers:\n{filename}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erreur d'export",
                    f"Impossible d'exporter l'historique:\n{str(e)}"
                )
                
    def setEnabled(self, enabled: bool):
        """Active/désactive l'interface"""
        self.chat_input.setEnabled(enabled)
        if enabled:
            self.chat_input.setFocus()

# Exports
__all__ = [
    'MessageBubble',
    'ChatInput', 
    'ChatHistory',
    'ChatInterface'
]