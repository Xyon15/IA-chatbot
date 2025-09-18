# 🚀 Dossier Launchers

Ce dossier contient tous les fichiers de lancement et scripts d'exécution du projet IA-chatbot.

## 📁 Organisation

### Scripts Python (.py)
- `launch_gui.py` - Lanceur GUI principal unifié avec sélection automatique (recommandé)
- `launch_kira_fullscreen.py` - Interface Kira en plein écran
- `launch_neuro_fullscreen.py` - Interface Neuro en plein écran
- `launch_logs_fullscreen.py` - Visualiseur de logs en plein écran
- `launch_log_viewer.py` - Visualiseur de logs standard
- `start_kira.py` - Script de démarrage principal Kira
- `start_neuro.py` - Script de démarrage Neuro

### Scripts Batch (.bat)
- `start_kira_gui.bat` - Lancement GUI Kira via batch
- `START_KIRA_FULLSCREEN.bat` - Kira plein écran via batch
- `START_LOGS_FULLSCREEN.bat` - Logs plein écran via batch
- `launch_logs_viewer.bat` - Visualiseur logs via batch

## 🎯 Utilisation

### Lancement recommandé
```bash
python launchers/launch_gui.py
```

### Lancement via batch (Windows)
```cmd
launchers\start_kira_gui.bat
```

## 📋 Notes
- Tous les lanceurs doivent être exécutés depuis la racine du projet
- Les chemins relatifs sont configurés en conséquence
- Les dépendances Python doivent être installées via `requirements.txt`