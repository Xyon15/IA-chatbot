# Guide d'utilisation GUI NeuroBot

## 🚀 Lancement rapide

### Méthode 1 : Lanceur principal (recommandé)
```bash
python launch_gui.py
```

### Méthode 2 : Lancement direct
```bash
python gui/launch_neuro_gui.py
```

## 📁 Structure GUI

Tous les fichiers GUI ont été déplacés dans le dossier `gui/` :

```
gui/
├── neuro_gui.py              # Interface principale moderne
├── launch_neuro_gui.py       # Lanceur GUI moderne
├── bot_gui.py                # Interface GUI basique (legacy)
├── chart_widgets.py          # Widgets de graphiques
├── theme_manager.py          # Gestionnaire de thèmes
├── notification_system.py    # Système de notifications
├── advanced_controls.py      # Contrôles avancés
├── plugin_system.py          # Système de plugins
├── icons_generator.py        # Générateur d'icônes
├── dark_theme_helper.py      # Helper thème sombre
├── assets/                   # Ressources (icônes, etc.)
├── tools/
│   └── log_viewer_gui.py     # Visualiseur de logs
└── THEME_GUIDE.md           # Guide des thèmes
```

## 🎨 Interfaces disponibles

### Interface moderne (neuro_gui.py)
- Design moderne avec thème sombre
- Monitoring temps réel (CPU, RAM, GPU)
- Notifications toast
- Système de plugins
- Graphiques animés

### Interface basique (bot_gui.py)  
- Interface simple pour démarrage/arrêt
- Monitoring basique
- Compatible legacy

## 🔧 Dépendances

```bash
pip install PySide6 psutil pynvml
```

## ⚡ Fonctionnalités

- **Monitoring** : CPU, RAM, GPU en temps réel
- **Contrôle** : Start/Stop du bot Discord
- **Logs** : Visualisation avancée des logs
- **Thèmes** : Plusieurs thèmes de couleurs
- **Plugins** : Système extensible
- **Notifications** : Alertes visuelles modernes