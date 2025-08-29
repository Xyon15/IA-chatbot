# Interface Graphique Principale Améliorée - Neuro-Bot

## 🚀 Nouvelle Interface Moderne

L'interface principale améliorée offre une expérience utilisateur moderne et intuitive pour contrôler et surveiller Neuro-Bot.

## ✨ Fonctionnalités Principales

### 📊 Indicateurs Circulaires de Performance
- **CPU**: Utilisation en temps réel avec pourcentage
- **RAM**: Utilisation mémoire en GB
- **GPU**: Utilisation et température
- **VRAM**: Mémoire vidéo utilisée en MB

### 🎮 Contrôle du Bot
- Démarrage/arrêt en un clic
- Redémarrage automatique
- Statut en temps réel
- Gestion propre des threads

### 📝 Logs en Temps Réel
- Zone dédiée aux logs (limité à 100 lignes)
- Horodatage automatique
- Messages colorés selon le type
- Scroll automatique

### 🔧 Fonctionnalités Utiles
- **Configuration**: Accès rapide aux fichiers JSON
- **Logs Avancés**: Ouverture du visualiseur détaillé
- **Informations Système**: GPU, modèle, base de données
- **Cartes de Statut**: Uptime, messages, utilisateurs

## 🎨 Design Moderne
- Palette de couleurs sombre élégante
- Gradients et effets visuels
- Interface responsive
- Animation fluide des indicateurs

## 🚀 Lancement

### Option 1: Script Python
```bash
python launch_enhanced_gui.py
```

### Option 2: Fichier Batch (Windows)
```bash
start_enhanced_gui.bat
```

### Option 3: Depuis le module GUI
```python
from gui.enhanced_main_gui import main
main()
```

## 📋 Configuration Requise
- PySide6 (interface graphique)
- psutil (statistiques système)
- pynvml (monitoring GPU NVIDIA)
- Modules du bot Neuro

## 🛠️ Structure des Fichiers
```
gui/
├── enhanced_main_gui.py      # Interface principale
├── bot_gui.py               # Interface simple (existante)
└── neuro_gui.py            # Interface complète (existante)

launch_enhanced_gui.py       # Lanceur principal
start_enhanced_gui.bat      # Lanceur Windows
```

## 🔍 Avantages vs Ancienne Interface

| Fonctionnalité | Ancienne | Nouvelle |
|---|---|---|
| Indicateurs | Texte brut | Cercles animés |
| Design | Basique | Moderne/sombre |
| Logs | Zone large | Zone optimisée |
| Contrôles | Bouton simple | Panel complet |
| Informations | Limitées | Complètes |
| Performance | Statique | Temps réel |

## 📈 Avantages Performance
- Mise à jour optimisée (2s pour stats, 1s pour statut)
- Gestion mémoire des logs (limite 100 lignes)
- Thread séparé pour le bot Discord
- Arrêt propre des processus

## 🎯 Utilisation Recommandée
Cette interface est idéale pour :
- Surveillance continue du bot
- Debug et développement  
- Présentation/démonstration
- Administration quotidienne

Pour une utilisation plus avancée (mémoire, configuration), utilisez `neuro_gui.py`.