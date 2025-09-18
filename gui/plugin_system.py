#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de plugins pour KiraBot GUI
Permet d'ajouter facilement des fonctionnalités personnalisées
"""

import os
import sys
import importlib
import importlib.util
import inspect
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import QObject, Signal

class PluginBase(ABC):
    """Classe de base pour tous les plugins"""
    
    def __init__(self):
        self.name = "Plugin de base"
        self.version = "1.0.0"
        self.description = "Plugin de base"
        self.author = "KiraBot"
        self.enabled = True
        
    @abstractmethod
    def initialize(self) -> bool:
        """Initialise le plugin. Retourne True si succès."""
        pass
        
    @abstractmethod
    def get_widget(self) -> Optional[QWidget]:
        """Retourne le widget principal du plugin, ou None."""
        pass
        
    @abstractmethod
    def cleanup(self):
        """Nettoie les ressources du plugin."""
        pass
        
    def get_info(self) -> Dict[str, str]:
        """Retourne les informations du plugin"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author,
            'enabled': str(self.enabled)
        }

class SystemInfoPlugin(PluginBase):
    """Plugin d'exemple - Informations système avancées"""
    
    def __init__(self):
        super().__init__()
        self.name = "Infos Système"
        self.version = "1.0.0"
        self.description = "Affiche des informations détaillées sur le système"
        self.author = "KiraBot Team"
        self.widget = None
        
    def initialize(self) -> bool:
        try:
            import platform
            import socket
            import uuid
            return True
        except ImportError:
            return False
            
    def get_widget(self) -> Optional[QWidget]:
        if self.widget is None:
            self.widget = self.create_system_info_widget()
        return self.widget
        
    def create_system_info_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("💻 INFORMATIONS SYSTÈME DÉTAILLÉES")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #034C36; margin: 10px 0;")
        layout.addWidget(title)
        
        try:
            import platform
            import socket
            import uuid
            
            info_items = [
                ("🖥️ Système:", f"{platform.system()} {platform.release()}"),
                ("🏗️ Architecture:", platform.architecture()[0]),
                ("🔧 Processeur:", platform.processor()),
                ("🖧 Machine:", platform.machine()),
                ("🌐 Nom réseau:", socket.gethostname()),
                ("🆔 UUID Machine:", str(uuid.getnode())),
                ("🐍 Python:", platform.python_version()),
                ("📦 Platform:", platform.platform())
            ]
            
            for label_text, value in info_items:
                item_layout = QHBoxLayout()
                
                label = QLabel(label_text)
                label.setStyleSheet("font-weight: bold; min-width: 150px;")
                label.setMinimumWidth(150)
                item_layout.addWidget(label)
                
                value_label = QLabel(str(value))
                value_label.setStyleSheet("color: #666;")
                item_layout.addWidget(value_label)
                
                item_layout.addStretch()
                layout.addLayout(item_layout)
                
        except Exception as e:
            error_label = QLabel(f"❌ Erreur: {e}")
            layout.addWidget(error_label)
            
        layout.addStretch()
        return widget
        
    def cleanup(self):
        self.widget = None

class NetworkMonitorPlugin(PluginBase):
    """Plugin de monitoring réseau"""
    
    def __init__(self):
        super().__init__()
        self.name = "Monitor Réseau"
        self.version = "1.0.0"
        self.description = "Surveillance du trafic réseau en temps réel"
        self.author = "KiraBot Team"
        self.widget = None
        
    def initialize(self) -> bool:
        try:
            import psutil
            return True
        except ImportError:
            return False
            
    def get_widget(self) -> Optional[QWidget]:
        if self.widget is None:
            self.widget = self.create_network_widget()
        return self.widget
        
    def create_network_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("🌐 MONITORING RÉSEAU")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #034C36; margin: 10px 0;")
        layout.addWidget(title)
        
        try:
            import psutil
            
            # Interfaces réseau
            interfaces = psutil.net_if_addrs()
            
            for interface_name, addresses in interfaces.items():
                if interface_name.startswith('lo'):  # Skip loopback
                    continue
                    
                interface_label = QLabel(f"📡 {interface_name}")
                interface_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
                layout.addWidget(interface_label)
                
                for addr in addresses:
                    addr_layout = QHBoxLayout()
                    
                    family_name = {
                        2: "IPv4",
                        10: "IPv6", 
                        17: "MAC"
                    }.get(addr.family, f"Family {addr.family}")
                    
                    type_label = QLabel(f"  {family_name}:")
                    type_label.setMinimumWidth(80)
                    addr_layout.addWidget(type_label)
                    
                    addr_label = QLabel(addr.address)
                    addr_label.setStyleSheet("font-family: monospace; color: #666;")
                    addr_layout.addWidget(addr_label)
                    
                    addr_layout.addStretch()
                    layout.addLayout(addr_layout)
                    
        except Exception as e:
            error_label = QLabel(f"❌ Erreur: {e}")
            layout.addWidget(error_label)
            
        layout.addStretch()
        return widget
        
    def cleanup(self):
        self.widget = None

class PluginManager(QObject):
    """Gestionnaire de plugins"""
    
    plugin_loaded = Signal(str)
    plugin_unloaded = Signal(str)
    plugin_error = Signal(str, str)
    
    def __init__(self):
        super().__init__()
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_directory = "plugins"
        
        # Plugins intégrés
        self.builtin_plugins = {
            'system_info': SystemInfoPlugin,
            'network_monitor': NetworkMonitorPlugin
        }
        
    def initialize_builtin_plugins(self):
        """Initialise les plugins intégrés"""
        for plugin_id, plugin_class in self.builtin_plugins.items():
            try:
                plugin = plugin_class()
                if plugin.initialize():
                    self.plugins[plugin_id] = plugin
                    self.plugin_loaded.emit(plugin_id)
                else:
                    self.plugin_error.emit(plugin_id, "Échec de l'initialisation")
            except Exception as e:
                self.plugin_error.emit(plugin_id, str(e))
                
    def load_plugin_from_file(self, filepath: str) -> bool:
        """Charge un plugin depuis un fichier"""
        try:
            # Ajoute le répertoire des plugins au path Python
            plugin_dir = os.path.dirname(filepath)
            if plugin_dir not in sys.path:
                sys.path.insert(0, plugin_dir)
                
            # Import du module
            module_name = os.path.splitext(os.path.basename(filepath))[0]
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            
                # Recherche des classes de plugins dans le module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, PluginBase) and 
                        obj != PluginBase):
                        
                        plugin = obj()
                        if plugin.initialize():
                            plugin_id = f"file_{module_name}"
                            self.plugins[plugin_id] = plugin
                            self.plugin_loaded.emit(plugin_id)
                            return True
                        else:
                            self.plugin_error.emit(module_name, "Échec de l'initialisation")
                            return False
                        
        except Exception as e:
            self.plugin_error.emit(filepath, str(e))
            return False
            
        return False
        
    def unload_plugin(self, plugin_id: str) -> bool:
        """Décharge un plugin"""
        if plugin_id in self.plugins:
            try:
                self.plugins[plugin_id].cleanup()
                del self.plugins[plugin_id]
                self.plugin_unloaded.emit(plugin_id)
                return True
            except Exception as e:
                self.plugin_error.emit(plugin_id, f"Erreur déchargement: {e}")
                return False
        return False
        
    def get_plugin_widget(self, plugin_id: str) -> Optional[QWidget]:
        """Retourne le widget d'un plugin"""
        if plugin_id in self.plugins:
            return self.plugins[plugin_id].get_widget()
        return None
        
    def get_loaded_plugins(self) -> List[Dict[str, str]]:
        """Retourne la liste des plugins chargés avec leurs infos"""
        return [
            {**plugin.get_info(), 'id': plugin_id}
            for plugin_id, plugin in self.plugins.items()
        ]
        
    def enable_plugin(self, plugin_id: str):
        """Active un plugin"""
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = True
            
    def disable_plugin(self, plugin_id: str):
        """Désactive un plugin"""
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = False

class PluginManagerWidget(QWidget):
    """Widget de gestion des plugins"""
    
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager()
        self.initUI()
        self.setup_connections()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("🔌 GESTIONNAIRE DE PLUGINS")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #034C36; margin: 10px 0;")
        layout.addWidget(title)
        
        # Boutons d'actions
        buttons_layout = QHBoxLayout()
        
        load_builtin_btn = QPushButton("📦 Charger Plugins Intégrés")
        load_builtin_btn.setObjectName("action_button")
        load_builtin_btn.clicked.connect(self.load_builtin_plugins)
        buttons_layout.addWidget(load_builtin_btn)
        
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setObjectName("action_button")
        refresh_btn.clicked.connect(self.refresh_plugin_list)
        buttons_layout.addWidget(refresh_btn)
        
        layout.addLayout(buttons_layout)
        
        # Liste des plugins
        self.plugin_info_label = QLabel("Aucun plugin chargé")
        self.plugin_info_label.setStyleSheet("margin: 10px; padding: 10px; background: white; border-radius: 8px;")
        layout.addWidget(self.plugin_info_label)
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        self.plugin_manager.plugin_loaded.connect(self.on_plugin_loaded)
        self.plugin_manager.plugin_unloaded.connect(self.on_plugin_unloaded)
        self.plugin_manager.plugin_error.connect(self.on_plugin_error)
        
    def load_builtin_plugins(self):
        """Charge tous les plugins intégrés"""
        self.plugin_manager.initialize_builtin_plugins()
        self.refresh_plugin_list()
        
    def refresh_plugin_list(self):
        """Met à jour l'affichage de la liste des plugins"""
        plugins = self.plugin_manager.get_loaded_plugins()
        
        if not plugins:
            self.plugin_info_label.setText("Aucun plugin chargé")
            return
            
        info_text = f"📊 {len(plugins)} plugin(s) chargé(s):\n\n"
        
        for plugin in plugins:
            status = "🟢 Activé" if plugin['enabled'] == 'True' else "🔴 Désactivé"
            info_text += f"• {plugin['name']} v{plugin['version']} - {status}\n"
            info_text += f"  📝 {plugin['description']}\n"
            info_text += f"  👤 Par {plugin['author']}\n\n"
            
        self.plugin_info_label.setText(info_text)
        
    def on_plugin_loaded(self, plugin_id: str):
        print(f"✅ Plugin chargé: {plugin_id}")
        
    def on_plugin_unloaded(self, plugin_id: str):
        print(f"📤 Plugin déchargé: {plugin_id}")
        
    def on_plugin_error(self, plugin_id: str, error: str):
        print(f"❌ Erreur plugin {plugin_id}: {error}")

# Instance globale du gestionnaire de plugins
plugin_manager = PluginManager()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    widget = PluginManagerWidget()
    widget.show()
    
    sys.exit(app.exec())