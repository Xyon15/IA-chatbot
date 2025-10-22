# Documentation Architecture GUI Modulaire - Kira-Bot

## Vue d'Ensemble

L'architecture GUI de Kira-Bot suit un design modulaire qui sépare les préoccupations et facilite la maintenance. Cette nouvelle architecture remplace l'ancienne approche monolithique par un système organisé en couches.

## Structure de l'Architecture

```
gui/
├── core/                          # Couche de base partagée
│   ├── __init__.py               # Exports principaux
│   ├── qt_imports.py             # Imports PySide6 centralisés
│   └── widgets.py                # Widgets de base communs
├── modules/                       # Modules spécialisés
│   ├── __init__.py               # Exports de modules
│   ├── notifications.py          # Système de notifications toast
│   ├── monitoring.py             # Widgets de monitoring système
│   └── chat.py                   # Interface de chat IA
├── launch_gui.py                 # Lanceur unifié principal
├── kira_gui.py                   # Interface legacy simple
├── enhanced_main_gui.py          # Interface principale améliorée
├── advanced_controls.py          # Contrôles avancés (en migration)
└── notification_system.py        # Système legacy (redirige vers modules)
```

## Couche Core (`gui/core/`)

### `qt_imports.py` - Hub Central
**Rôle** : Centralise tous les imports PySide6 et les configurations partagées

**Contenu** :
- ✅ **Imports PySide6** : Tous les widgets, layouts, core, gui
- ✅ **COLOR_PALETTE** : 23 couleurs standardisées (bg_primary, accent_blue, etc.)
- ✅ **FONTS** : 5 polices prédéfinies (main, bold, mono, etc.)
- ✅ **ANIMATIONS** : 4 configurations d'animation (fade, slide, bounce, etc.)
- ✅ **UNIFIED_STYLE** : CSS/QSS unifié pour toute l'application

**Usage** :
```python
from gui.core.qt_imports import QApplication, QWidget, COLOR_PALETTE, FONTS
```

### `widgets.py` - Composants de Base
**Rôle** : Widgets réutilisables et classes de base

**Composants** :
- ✅ **BaseWidget** : Classe de base avec styles appliqués
- ✅ **StyledButton** : Boutons avec thème uniforme
- ✅ **InfoCard** : Cartes d'information standardisées

## Couche Modules (`gui/modules/`)

### `notifications.py` - Système de Notifications
**Fonctionnalités** :
- ✅ **NotificationWidget** : Toast moderne avec animations
- ✅ **NotificationManager** : Gestionnaire global de notifications
- ✅ **Types** : INFO, SUCCESS, WARNING, ERROR
- ✅ **Animations** : Slide-in/out avec courbes d'accélération
- ✅ **Auto-dismiss** : Fermeture automatique configurable

**Usage** :
```python
from gui.modules.notifications import show_success, show_error
show_success("Opération réussie", "Le fichier a été sauvegardé")
```

### `monitoring.py` - Monitoring Système
**Composants** :
- ✅ **CircularProgressIndicator** : Indicateurs circulaires animés
- ✅ **SystemMetricCard** : Cartes métriques (CPU, RAM, GPU)
- ✅ **MiniChart** : Graphiques temps réel compacts
- ✅ **SystemMonitorPanel** : Panel complet de monitoring
- ✅ **CompactSystemMonitor** : Version compacte pour barres d'état

**Usage** :
```python
from gui.modules.monitoring import SystemMonitorPanel
monitor = SystemMonitorPanel()
monitor.start_monitoring()  # Lance le monitoring temps réel
```

### `chat.py` - Interface de Chat
**Composants** :
- ✅ **MessageBubble** : Bulles de messages stylées
- ✅ **ChatInput** : Zone de saisie avec suggestions
- ✅ **ChatHistory** : Historique scrollable avec recherche
- ✅ **ChatInterface** : Interface complète de chat IA

**Usage** :
```python
from gui.modules.chat import ChatInterface
chat = ChatInterface()
chat.add_message("user", "Bonjour Kira")
chat.add_message("bot", "Salut ! Comment puis-je t'aider ?")
```

## Lanceurs et Interfaces

### `launch_gui.py` - Lanceur Unifié
**Rôle** : Point d'entrée principal avec sélection d'interface

**Modes disponibles** :
- `--modern` : Interface enhanced_main_gui (par défaut)
- `--legacy` : Interface kira_gui simple
- `--select` : Sélection interactive

**Fonctionnalités** :
- ✅ Vérification automatique des dépendances
- ✅ Fallback intelligent en cas d'erreur
- ✅ Génération d'icônes automatique
- ✅ Messages d'erreur détaillés

### `kira_gui.py` - Interface Legacy
**Rôle** : Interface simple pour compatibilité et tests

**Caractéristiques** :
- ✅ Interface à onglets (Information, Configuration, Logs)
- ✅ Compatible avec l'architecture modulaire
- ✅ Fallback gracieux si modules indisponibles
- ✅ Boutons de navigation vers interface moderne

## Guide de Migration

### Depuis l'Ancienne Architecture

**Étape 1 : Remplacer les imports**
```python
# ❌ Ancien
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

# ✅ Nouveau
from gui.core.qt_imports import QApplication, QWidget, Qt, QColor, COLOR_PALETTE
```

**Étape 2 : Utiliser la palette centralisée**
```python
# ❌ Ancien
bg_color = "#1a1a1a"
text_color = "#ffffff"

# ✅ Nouveau
bg_color = COLOR_PALETTE['bg_secondary']
text_color = COLOR_PALETTE['text_primary']
```

**Étape 3 : Intégrer les modules spécialisés**
```python
# ❌ Ancien - Code de notification custom
def show_message():
    # Code custom complexe...

# ✅ Nouveau
from gui.modules.notifications import show_success
show_success("Titre", "Message")
```

### Création de Nouveaux Modules

**Structure recommandée** :
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nouveau Module GUI - Description
"""

from gui.core.qt_imports import *

class MonNouveauWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(UNIFIED_STYLE)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Configuration UI...

# Export dans gui/modules/__init__.py
def setup_exports():
    return ['MonNouveauWidget']
```

## Tests et Validation

### Test d'Intégration
**Fichier** : `launchers/test_integration.py`

**Tests disponibles** :
- ✅ **test_core_imports** : Vérification imports centralisés
- ✅ **test_modules_imports** : Validation modules spécialisés
- ✅ **test_gpu_utils** : Test fonctionnalités GPU
- ✅ **test_widgets_creation** : Création de widgets
- ✅ **test_notifications** : Système de notifications

**Commande** :
```bash
# Activer venv OBLIGATOIRE
llama-venv\Scripts\activate
python launchers/test_integration.py
```

**Résultat attendu** : `6/6 tests passés`

### Validation Continue
Le launcher optimisé inclut un mode test :
```bash
python launchers/launch_optimized.py --mode test
```

## Bonnes Pratiques

### 1. Imports Centralisés
- ✅ Toujours importer depuis `gui.core.qt_imports`
- ✅ Utiliser `COLOR_PALETTE` au lieu de couleurs hardcodées
- ✅ Préférer `FONTS` pour la cohérence typographique

### 2. Modularité
- ✅ Un module = une responsabilité claire
- ✅ Exports explicites dans `__init__.py`
- ✅ Documentation des interfaces publiques

### 3. Compatibility
- ✅ Toujours prévoir des fallbacks
- ✅ Gérer les imports optionnels gracieusement
- ✅ Maintenir la compatibilité ascendante

### 4. Tests
- ✅ Ajouter des tests pour nouveaux modules
- ✅ Valider avec l'environnement virtuel
- ✅ Tester les fallbacks et cas d'erreur

## Dépannage

### Erreurs Communes

**1. Import errors**
```
❌ ModuleNotFoundError: No module named 'gui.core'
✅ Solution: Vérifier l'activation du venv et sys.path
```

**2. Styles non appliqués**
```
❌ Interface sans styles
✅ Solution: Importer et appliquer UNIFIED_STYLE
```

**3. Notifications non visibles**
```
❌ show_success ne fonctionne pas
✅ Solution: Vérifier que QApplication est créé
```

### Debug Mode
Activer le mode debug dans le launcher :
```bash
python launchers/launch_optimized.py --debug
```

## Feuille de Route

### ✅ Complété
- Structure modulaire de base
- Modules notifications, monitoring, chat
- Tests d'intégration
- Documentation

### 🔄 En Cours
- Migration complète des anciens fichiers
- Optimisation des performances
- Tests unitaires étendus

### 📋 Prévu
- Module d'authentification GUI
- Système de plugins visuels
- Interface de configuration avancée
- Documentation interactive

---

Cette architecture modulaire garantit une maintenance facilitée, une réutilisabilité maximale et une évolutivité pérenne pour l'interface graphique de Kira-Bot.