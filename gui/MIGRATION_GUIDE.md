# Guide de Migration GUI - Kira-Bot

## Introduction

Ce guide vous accompagne dans la migration de l'ancienne architecture GUI vers le nouveau système modulaire de Kira-Bot.

## Migration Rapide - Checklist

### ✅ Étapes Essentielles

1. **Vérification de l'environnement**
   ```bash
   # OBLIGATOIRE : Activer le venv
   llama-venv\Scripts\activate
   
   # Tester l'architecture
   python launchers/test_integration.py
   ```

2. **Mise à jour des imports**
   ```python
   # ❌ Ancien style
   from PySide6.QtWidgets import QApplication, QWidget, QLabel
   from PySide6.QtCore import Qt
   from PySide6.QtGui import QColor, QFont
   
   # ✅ Nouveau style
   from gui.core.qt_imports import QApplication, QWidget, QLabel, Qt, QColor, QFont
   from gui.core.qt_imports import COLOR_PALETTE, FONTS
   ```

3. **Utilisation de la palette centralisée**
   ```python
   # ❌ Couleurs hardcodées
   widget.setStyleSheet("background-color: #1a1a1a; color: #ffffff;")
   
   # ✅ Palette centralisée
   widget.setStyleSheet(f"""
       background-color: {COLOR_PALETTE['bg_secondary']};
       color: {COLOR_PALETTE['text_primary']};
   """)
   ```

4. **Intégration des modules spécialisés**
   ```python
   # ❌ Code de notification custom
   def show_message(text):
       msg = QMessageBox()
       msg.setText(text)
       msg.exec()
   
   # ✅ Module de notifications
   from gui.modules.notifications import show_success
   show_success("Succès", "Opération terminée")
   ```

## Migration par Composant

### 1. Notifications

**Ancien système** → **Nouveau système**

```python
# ❌ Ancien
class CustomNotification(QWidget):
    def __init__(self, message):
        super().__init__()
        # 50+ lignes de code...

# ✅ Nouveau
from gui.modules.notifications import show_info, show_success, show_warning, show_error

# Usage simple
show_success("Titre", "Message de succès")
show_error("Erreur", "Quelque chose s'est mal passé")
```

### 2. Monitoring Système

**Ancien système** → **Nouveau système**

```python
# ❌ Ancien
class CPUMonitor(QWidget):
    def __init__(self):
        super().__init__()
        # Code custom pour CPU monitoring...

# ✅ Nouveau
from gui.modules.monitoring import SystemMonitorPanel, CircularProgressIndicator

# Panel complet
monitor_panel = SystemMonitorPanel()
self.layout().addWidget(monitor_panel)

# Ou indicateur simple
cpu_indicator = CircularProgressIndicator("CPU", 0.0)
cpu_indicator.setValue(75.5, "75.5%")
```

### 3. Interface de Chat

**Ancien système** → **Nouveau système**

```python
# ❌ Ancien
class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Implémentation custom complexe...

# ✅ Nouveau
from gui.modules.chat import ChatInterface

chat = ChatInterface()
chat.add_message("user", "Bonjour Kira")
chat.add_message("bot", "Salut ! Comment ça va ?")
```

## Patterns de Migration

### Pattern 1 : Import Progressif

**Stratégie** : Migrer les imports d'abord, puis les fonctionnalités

```python
# Étape 1 : Ajouter les nouveaux imports
try:
    from gui.core.qt_imports import *
    from gui.modules import show_success
    MODULAR_GUI = True
except ImportError:
    from PySide6.QtWidgets import *
    MODULAR_GUI = False

# Étape 2 : Utilisation conditionnelle
def notify_success(title, message):
    if MODULAR_GUI:
        show_success(title, message)
    else:
        # Fallback ancien système
        print(f"{title}: {message}")
```

### Pattern 2 : Wrapper de Compatibilité

**Stratégie** : Créer des wrappers pour transition graduelle

```python
# compatibility_layer.py
def create_notification(msg_type, title, message):
    try:
        from gui.modules.notifications import show_info, show_success, show_warning, show_error
        
        if msg_type == "info":
            return show_info(title, message)
        elif msg_type == "success":
            return show_success(title, message)
        elif msg_type == "warning":
            return show_warning(title, message)
        elif msg_type == "error":
            return show_error(title, message)
    except ImportError:
        # Fallback ancien système
        return legacy_notification(msg_type, title, message)
```

### Pattern 3 : Migration Complète

**Stratégie** : Réécriture complète avec nouvelle architecture

```python
# nouveau_module.py
from gui.core.qt_imports import *
from gui.modules.notifications import NotificationManager
from gui.modules.monitoring import SystemMonitorPanel

class ModernInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(UNIFIED_STYLE)
        self.setup_ui()
        
        # Manager de notifications
        self.notification_manager = NotificationManager()
        
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Panel de monitoring intégré
        self.monitor = SystemMonitorPanel()
        layout.addWidget(self.monitor)
```

## Cas d'Usage Spécifiques

### Cas 1 : Interface Principale

**Problème** : `enhanced_main_gui.py` trop complexe

**Solution** :
```python
# Décomposer en modules
from gui.modules.monitoring import SystemMonitorPanel
from gui.modules.notifications import NotificationManager
from gui.modules.chat import ChatInterface

class EnhancedMainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_modules()
        
    def setup_modules(self):
        # Monitoring
        self.monitor = SystemMonitorPanel()
        
        # Notifications
        self.notifications = NotificationManager()
        
        # Chat
        self.chat = ChatInterface()
```

### Cas 2 : Contrôles Avancés

**Problème** : `advanced_controls.py` avec imports directs

**Solution** :
```python
# Migration progressive
try:
    from gui.core.qt_imports import *
    from gui.modules.monitoring import CircularProgressIndicator
    NEW_ARCH = True
except ImportError:
    from PySide6.QtWidgets import *
    NEW_ARCH = False

class AdvancedControls(QWidget):
    def create_indicator(self, title, value):
        if NEW_ARCH:
            return CircularProgressIndicator(title, value)
        else:
            # Fallback implementation
            return self.legacy_indicator(title, value)
```

## Validation de Migration

### Test de Régression

```bash
# Test complet de l'architecture
python launchers/test_integration.py

# Test avec launcher optimisé
python launchers/launch_optimized.py --mode test

# Test de lancement
python gui/launch_gui.py --legacy
python gui/launch_gui.py --modern
```

### Checklist de Validation

- [ ] **Imports** : Tous les imports utilisent `gui.core.qt_imports`
- [ ] **Couleurs** : Utilisation de `COLOR_PALETTE` au lieu de hardcodés
- [ ] **Notifications** : Migration vers `gui.modules.notifications`
- [ ] **Monitoring** : Utilisation de `gui.modules.monitoring`
- [ ] **Tests** : 6/6 tests passent dans `test_integration.py`
- [ ] **Fallbacks** : Gestion gracieuse des imports échoués
- [ ] **Documentation** : Code documenté avec nouveaux patterns

### Métriques de Succès

**Performance** :
- Temps de lancement < 3 secondes
- Utilisation mémoire réduite de 20%
- Responsive à 60 FPS

**Maintenance** :
- Réduction de 50% des lignes de code dupliquées
- Imports centralisés à 100%
- Tests couvrant 80% des fonctionnalités

**Utilisabilité** :
- Interface cohérente sur tous les composants
- Notifications uniformes
- Pas de régression fonctionnelle

## Dépannage Migration

### Erreurs Fréquentes

**1. ModuleNotFoundError**
```
❌ Erreur: No module named 'gui.core'
🔧 Solution: 
   - Vérifier activation venv
   - Vérifier sys.path
   - Redémarrer l'IDE
```

**2. Attributs Qt manquants**
```
❌ Erreur: Cannot access attribute "AlignCenter"
🔧 Solution:
   - Vérifier import Qt depuis gui.core.qt_imports
   - Utiliser Qt.AlignmentFlag.AlignCenter pour PySide6
```

**3. Styles non appliqués**
```
❌ Problème: Interface sans styles
🔧 Solution:
   - Appliquer UNIFIED_STYLE
   - Vérifier COLOR_PALETTE importé
   - Redémarrer l'application
```

### Support et Resources

**Documentation** :
- `gui/GUI_ARCHITECTURE.md` - Architecture complète
- `gui/GUI_USAGE.md` - Guide d'utilisation
- `launchers/README.md` - Documentation launchers

**Tests** :
- `launchers/test_integration.py` - Tests complets
- `python gui/launch_gui.py --help` - Options disponibles

**Exemples** :
- `gui/kira_gui.py` - Interface simple fonctionnelle
- `gui/modules/` - Modules de référence

---

Cette migration vers l'architecture modulaire améliore significativement la maintenabilité et l'évolutivité de votre interface graphique ! 🚀