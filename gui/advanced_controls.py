#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôles avancés pour NeuroBot GUI
Interface de configuration et contrôle approfondi
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QPushButton, QSlider, QSpinBox, QComboBox, QCheckBox,
    QProgressBar, QTextEdit, QTabWidget, QFrame, QSplitter,
    QScrollArea, QDial, QLCDNumber
)
from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QFont, QPixmap, QColor
import psutil
import json
import os
from typing import Dict, Any

class PerformanceWidget(QWidget):
    """Widget de monitoring de performance avancé"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_monitoring()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Titre avec icône
        title = QLabel("⚡ PERFORMANCE AVANCÉE")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #034C36; margin: 10px 0;")
        layout.addWidget(title)
        
        # Grille de métriques
        grid = QGridLayout()
        
        # CPU fréquence
        self.cpu_freq_group = self.create_metric_group("🔥 CPU Fréquence", "GHz")
        grid.addWidget(self.cpu_freq_group, 0, 0)
        
        # CPU température (si disponible)
        self.cpu_temp_group = self.create_metric_group("🌡️ Température", "°C")
        grid.addWidget(self.cpu_temp_group, 0, 1)
        
        # Réseau
        self.network_group = self.create_metric_group("🌐 Réseau", "MB/s")
        grid.addWidget(self.network_group, 1, 0)
        
        # Disque I/O
        self.disk_group = self.create_metric_group("💾 Disque I/O", "MB/s")
        grid.addWidget(self.disk_group, 1, 1)
        
        layout.addLayout(grid)
        
        # Graphique de charge système
        load_frame = QFrame()
        load_frame.setObjectName("card")
        load_layout = QVBoxLayout(load_frame)
        
        load_title = QLabel("📊 Charge Système (15 min)")
        load_title.setStyleSheet("font-weight: bold; margin: 5px 0;")
        load_layout.addWidget(load_title)
        
        # Barres de charge par CPU core
        self.cpu_bars = []
        cpu_count = psutil.cpu_count()
        for i in range(min(cpu_count, 8)):  # Maximum 8 barres pour l'affichage
            bar_layout = QHBoxLayout()
            
            core_label = QLabel(f"Core {i+1}")
            core_label.setFixedWidth(60)
            bar_layout.addWidget(core_label)
            
            progress_bar = QProgressBar()
            progress_bar.setMaximum(100)
            progress_bar.setTextVisible(True)
            bar_layout.addWidget(progress_bar)
            
            self.cpu_bars.append(progress_bar)
            load_layout.addLayout(bar_layout)
            
        layout.addWidget(load_frame)
        
    def create_metric_group(self, title: str, unit: str) -> QGroupBox:
        """Crée un groupe de métriques avec affichage LCD"""
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        
        # Afficheur LCD
        lcd = QLCDNumber()
        lcd.setDigitCount(6)
        lcd.display(0.0)
        lcd.setStyleSheet("""
            QLCDNumber {
                background: #034C36;
                color: #FF8128;
                border: 2px solid #BDCDCF;
                border-radius: 8px;
            }
        """)
        layout.addWidget(lcd)
        
        # Unité
        unit_label = QLabel(unit)
        unit_label.setAlignment(Qt.AlignCenter)
        unit_label.setStyleSheet("color: #666; font-size: 12px; font-weight: bold;")
        layout.addWidget(unit_label)
        
        # Stocke la référence LCD
        group.lcd = lcd
        return group
        
    def setup_monitoring(self):
        """Configure le monitoring en temps réel"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_performance)
        self.monitor_timer.start(1000)  # 1 seconde
        
        # Statistiques réseau initiales
        self.last_network_io = psutil.net_io_counters()
        self.last_disk_io = psutil.disk_io_counters()
        
    def update_performance(self):
        """Met à jour toutes les métriques de performance"""
        try:
            # CPU fréquence
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                self.cpu_freq_group.lcd.display(round(cpu_freq.current / 1000, 2))
            
            # CPU par core
            cpu_percents = psutil.cpu_percent(percpu=True)
            for i, (bar, percent) in enumerate(zip(self.cpu_bars, cpu_percents)):
                bar.setValue(int(percent))
                
            # Température CPU (si disponible)
            try:
                temps = psutil.sensors_temperatures()
                if 'coretemp' in temps and temps['coretemp']:
                    cpu_temp = temps['coretemp'][0].current
                    self.cpu_temp_group.lcd.display(round(cpu_temp, 1))
                else:
                    self.cpu_temp_group.lcd.display(0)
            except:
                self.cpu_temp_group.lcd.display(0)
            
            # Réseau
            current_network = psutil.net_io_counters()
            if hasattr(self, 'last_network_io'):
                net_speed = (current_network.bytes_recv - self.last_network_io.bytes_recv) / (1024 * 1024)
                self.network_group.lcd.display(round(net_speed, 2))
            self.last_network_io = current_network
            
            # Disque I/O
            current_disk = psutil.disk_io_counters()
            if current_disk and hasattr(self, 'last_disk_io'):
                disk_speed = (current_disk.read_bytes - self.last_disk_io.read_bytes) / (1024 * 1024)
                self.disk_group.lcd.display(round(disk_speed, 2))
            if current_disk:
                self.last_disk_io = current_disk
                
        except Exception as e:
            print(f"Erreur update performance: {e}")

class ModelConfigWidget(QWidget):
    """Widget de configuration du modèle LLM"""
    
    config_changed = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_current_config()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("🧠 CONFIGURATION MODÈLE LLM")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #034C36; margin: 10px 0;")
        layout.addWidget(title)
        
        # Configuration principale
        main_group = QGroupBox("Paramètres Principaux")
        main_layout = QGridLayout(main_group)
        
        # Context length
        main_layout.addWidget(QLabel("Longueur contexte:"), 0, 0)
        self.context_spin = QSpinBox()
        self.context_spin.setRange(512, 32768)
        self.context_spin.setValue(8192)
        self.context_spin.setSuffix(" tokens")
        main_layout.addWidget(self.context_spin, 0, 1)
        
        # GPU layers
        main_layout.addWidget(QLabel("Couches GPU:"), 1, 0)
        self.gpu_layers_spin = QSpinBox()
        self.gpu_layers_spin.setRange(0, 50)
        self.gpu_layers_spin.setValue(25)
        main_layout.addWidget(self.gpu_layers_spin, 1, 1)
        
        # Threads
        main_layout.addWidget(QLabel("Threads CPU:"), 2, 0)
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, psutil.cpu_count())
        self.threads_spin.setValue(6)
        main_layout.addWidget(self.threads_spin, 2, 1)
        
        # Batch size
        main_layout.addWidget(QLabel("Taille batch:"), 3, 0)
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 1024)
        self.batch_spin.setValue(128)
        main_layout.addWidget(self.batch_spin, 3, 1)
        
        layout.addWidget(main_group)
        
        # Paramètres avancés
        advanced_group = QGroupBox("Paramètres Avancés")
        advanced_layout = QGridLayout(advanced_group)
        
        self.flash_attn_check = QCheckBox("Flash Attention")
        advanced_layout.addWidget(self.flash_attn_check, 0, 0)
        
        self.use_mmap_check = QCheckBox("Memory Mapping")
        self.use_mmap_check.setChecked(True)
        advanced_layout.addWidget(self.use_mmap_check, 0, 1)
        
        self.use_mlock_check = QCheckBox("Memory Lock")
        advanced_layout.addWidget(self.use_mlock_check, 1, 0)
        
        self.offload_kqv_check = QCheckBox("Offload KQV")
        self.offload_kqv_check.setChecked(True)
        advanced_layout.addWidget(self.offload_kqv_check, 1, 1)
        
        layout.addWidget(advanced_group)
        
        # Boutons d'actions
        buttons_layout = QHBoxLayout()
        
        apply_btn = QPushButton("✅ Appliquer Configuration")
        apply_btn.setObjectName("action_button")
        apply_btn.clicked.connect(self.apply_config)
        buttons_layout.addWidget(apply_btn)
        
        reset_btn = QPushButton("🔄 Réinitialiser")
        reset_btn.setObjectName("action_button")
        reset_btn.clicked.connect(self.reset_config)
        buttons_layout.addWidget(reset_btn)
        
        save_btn = QPushButton("💾 Sauvegarder")
        save_btn.setObjectName("action_button")
        save_btn.clicked.connect(self.save_config)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
    def load_current_config(self):
        """Charge la configuration actuelle depuis le fichier"""
        try:
            config_path = "JSON/model_config.json"
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # Applique les valeurs
                self.context_spin.setValue(config.get('n_ctx', 8192))
                self.gpu_layers_spin.setValue(config.get('n_gpu_layers', 25))
                self.threads_spin.setValue(config.get('n_threads', 6))
                self.batch_spin.setValue(config.get('n_batch', 128))
                self.flash_attn_check.setChecked(config.get('flash_attn', False))
                self.use_mmap_check.setChecked(config.get('use_mmap', True))
                self.use_mlock_check.setChecked(config.get('use_mlock', False))
                self.offload_kqv_check.setChecked(config.get('offload_kqv', True))
        except Exception as e:
            print(f"Erreur chargement config: {e}")
            
    def get_current_config(self) -> Dict[str, Any]:
        """Retourne la configuration actuelle"""
        return {
            'n_ctx': self.context_spin.value(),
            'n_gpu_layers': self.gpu_layers_spin.value(),
            'n_threads': self.threads_spin.value(),
            'n_batch': self.batch_spin.value(),
            'flash_attn': self.flash_attn_check.isChecked(),
            'use_mmap': self.use_mmap_check.isChecked(),
            'use_mlock': self.use_mlock_check.isChecked(),
            'offload_kqv': self.offload_kqv_check.isChecked(),
            'verbose': False
        }
        
    def apply_config(self):
        """Applique la configuration"""
        config = self.get_current_config()
        self.config_changed.emit(config)
        
    def reset_config(self):
        """Remet les valeurs par défaut"""
        self.context_spin.setValue(8192)
        self.gpu_layers_spin.setValue(25)
        self.threads_spin.setValue(6)
        self.batch_spin.setValue(128)
        self.flash_attn_check.setChecked(False)
        self.use_mmap_check.setChecked(True)
        self.use_mlock_check.setChecked(False)
        self.offload_kqv_check.setChecked(True)
        
    def save_config(self):
        """Sauvegarde la configuration dans un fichier"""
        try:
            config = self.get_current_config()
            
            os.makedirs("JSON", exist_ok=True)
            config_path = "JSON/model_config.json"
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
            print("✅ Configuration sauvegardée")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")

class AdvancedControlsWidget(QWidget):
    """Widget principal des contrôles avancés"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Titre principal
        title = QLabel("🔧 CONTRÔLES AVANCÉS")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #034C36; margin: 15px 0;")
        layout.addWidget(title)
        
        # Tabs pour organiser les contrôles
        tabs = QTabWidget()
        
        # Onglet Performance
        self.performance_widget = PerformanceWidget()
        tabs.addTab(self.performance_widget, "⚡ Performance")
        
        # Onglet Configuration Modèle
        self.model_config_widget = ModelConfigWidget()
        tabs.addTab(self.model_config_widget, "🧠 Modèle LLM")
        
        layout.addWidget(tabs)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    widget = AdvancedControlsWidget()
    widget.show()
    
    sys.exit(app.exec())