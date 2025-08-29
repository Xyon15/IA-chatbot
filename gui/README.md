# Interface Graphique NeuroBot

Ce dossier contient tous les composants de l'interface graphique de NeuroBot.

## Organisation des fichiers

### Lanceurs principaux
- `launch_gui.py` - **Lanceur unifié principal** avec sélection d'interface
- `launch_neuro_gui_legacy.py` - Ancien lanceur conservé pour référence

### Interfaces disponibles
- `neuro_gui.py` - Interface moderne avec dashboard et monitoring
- `enhanced_main_gui.py` - Interface améliorée avec fonctionnalités avancées
- `bot_gui.py` - Interface de base (legacy)

### Composants spécialisés
- `advanced_controls.py` - Contrôles avancés pour l'interface
- `chart_widgets.py` - Widgets graphiques et diagrammes
- `notification_system.py` - Système de notifications
- `theme_manager.py` - Gestionnaire de thèmes
- `dark_theme_helper.py` - Assistant pour le thème sombre
- `plugin_system.py` - Système de plugins

### Utilitaires
- `icons_generator.py` - Générateur d'icônes SVG
- `tools/log_viewer_gui.py` - Visualiseur de logs

### Ressources
- `assets/icons/` - Icônes SVG générées automatiquement

## Utilisation

### Lancement depuis la racine du projet
```bash
# Interface moderne (défaut)
python launch_gui.py

# Interface améliorée
python launch_gui.py --enhanced

# Sélection interactive
python launch_gui.py --select
```

### Lancement direct depuis le dossier gui
```bash
# Lanceur unifié avec options
python gui/launch_gui.py --enhanced

# Ou directement une interface spécifique
python gui/neuro_gui.py
python gui/enhanced_main_gui.py
```

## Interfaces disponibles

### 1. Interface Moderne (neuro_gui.py)
- Dashboard complet avec monitoring temps réel
- Graphiques animés pour CPU, RAM, GPU, VRAM
- Contrôle du bot Discord intégré
- Gestionnaire de mémoire conversationnelle
- Système de notifications
- Palette de couleurs moderne (vert émeraude, orange accent, rose pâle)

### 2. Interface Améliorée (enhanced_main_gui.py)
- Interface enrichie avec fonctionnalités avancées
- Contrôles détaillés du bot
- Monitoring système approfondi
- Outils de diagnostic

## Dépendances

Les interfaces requièrent :
- `PySide6` - Framework Qt pour l'interface graphique
- `psutil` - Monitoring système
- `pynvml` - Monitoring GPU NVIDIA

Installation :
```bash
pip install PySide6 psutil pynvml
```

## Configuration

Les interfaces utilisent les fichiers de configuration dans `../JSON/` :
- `config.json` - Configuration générale
- `context.json` - Paramètres de contexte
- `autoreply.json` - Configuration des réponses automatiques

## Documentation supplémentaire

- `GUI_USAGE.md` - Guide d'utilisation détaillé
- `THEME_GUIDE.md` - Guide de personnalisation des thèmes

## Migration depuis les anciens lanceurs

Les anciens fichiers `launch_gui.py` et `launch_enhanced_gui.py` de la racine ont été remplacés par le nouveau système unifié. L'ancien `launch_neuro_gui.py` a été conservé sous le nom `launch_neuro_gui_legacy.py` pour référence.