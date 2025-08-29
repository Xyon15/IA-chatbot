# 🚀 Interface Principale Améliorée - Neuro-Bot

## Vue d'ensemble

L'interface principale améliorée de Neuro-Bot offre une expérience moderne et intuitive pour contrôler et surveiller votre bot Discord. Conçue pour être à la fois belle et fonctionnelle, elle remplace l'interface basique par une solution professionnelle.

## ✨ Caractéristiques Principales

### 📊 Monitoring Temps Réel
- **Indicateurs circulaires** pour CPU, RAM, GPU et VRAM
- **Animation fluide** des valeurs en temps réel
- **Couleurs distinctives** pour chaque métrique
- **Affichage optimisé** avec température GPU

### 🎮 Contrôle du Bot
- **Démarrage/arrêt** en un clic
- **Redémarrage automatisé** avec temporisation
- **Statut visuel** en temps réel
- **Gestion propre** des threads Discord

### 📝 Système de Logs
- **Zone dédiée** avec horodatage automatique
- **Limitation intelligente** (100 lignes max)
- **Scroll automatique** vers les nouveaux messages
- **Effacement rapide** via raccourci

### ⌨️ Raccourcis Clavier
- **F5** - Démarrer/Arrêter le bot
- **Ctrl+R** - Redémarrer le bot  
- **Ctrl+L** - Effacer les logs
- **F1** - Afficher l'aide

## 🎨 Design Moderne

### Palette de Couleurs
```css
Fond principal:    #0f0f0f (Noir très profond)
Fond secondaire:   #1a1a1a (Noir profond)  
Fond tertiaire:    #2a2a2a (Gris très sombre)
Accent bleu:       #00d4ff (Néon)
Accent vert:       #00ff88 (Néon)
Accent orange:     #ff6b35 (Vif)
Accent violet:     #8b5cf6 (Moderne)
```

### Effets Visuels
- **Gradients** pour les panneaux principaux
- **Bordures arrondies** pour les cartes
- **Animations** pour les indicateurs
- **Hover effects** sur les boutons

## 🚀 Lancement Rapide

### Méthode 1: Script Python
```bash
python launch_enhanced_gui.py
```

### Méthode 2: Fichier Batch
```bash
start_enhanced_gui.bat
```

### Méthode 3: Import Direct
```python
from gui.enhanced_main_gui import main
main()
```

## 📋 Prérequis

### Dépendances Python
```bash
pip install PySide6 psutil pynvml
```

### Modules Neuro-Bot
- `bot.py` (pour le contrôle Discord)
- `config.py` (pour la configuration)
- `memory.py` (pour la base de données)

### Système
- Windows 11 (recommandé)
- GPU NVIDIA avec pynvml support
- Python 3.10+

## 🔧 Configuration

### Structure des Fichiers
```
C:/Dev/IA-chatbot/
├── gui/
│   ├── enhanced_main_gui.py    # Interface principale
│   ├── bot_gui.py             # Interface simple
│   └── neuro_gui.py          # Interface complète
├── launch_enhanced_gui.py     # Lanceur principal
├── start_enhanced_gui.bat     # Lanceur Windows
└── JSON/
    └── web.json              # Config recherche web
```

### Personnalisation
Vous pouvez modifier la palette de couleurs dans `COLOR_PALETTE` :
```python
COLOR_PALETTE = {
    'bg_primary': '#votre_couleur',    # Fond principal
    'accent_blue': '#votre_couleur',   # Couleur indicateur CPU
    # ... autres couleurs
}
```

## 📊 Fonctionnalités Détaillées

### Indicateurs Circulaires

#### CPU
- **Couleur**: Bleu néon (#00d4ff)
- **Valeur**: Pourcentage d'utilisation
- **Mise à jour**: Toutes les 2 secondes

#### RAM
- **Couleur**: Vert néon (#00ff88)  
- **Valeur**: GB utilisés (ex: "8.2G")
- **Affichage**: Usage/Total en pourcentage

#### GPU
- **Couleur**: Orange vif (#ff6b35)
- **Valeur**: Température en °C
- **Info**: Pourcentage d'utilisation GPU

#### VRAM
- **Couleur**: Violet moderne (#8b5cf6)
- **Valeur**: MB utilisés (ex: "2048M")
- **Calcul**: Mémoire vidéo utilisée/totale

### Cartes de Statut

#### Bot Status
- **🤖** Icône du bot
- **États**: "En ligne" / "Arrêté"
- **Couleur**: Vert (en ligne) / Rouge (arrêté)

#### Uptime
- **⏱️** Icône temps  
- **Format**: "Xj Xh Xm"
- **Calcul**: Depuis le démarrage du bot

#### Messages
- **💬** Icône message
- **Source**: Compteur base SQLite
- **Table**: `memory`

#### Utilisateurs
- **👥** Icône groupe
- **Source**: Compteur unique SQLite
- **Calcul**: `DISTINCT user_id`

### Zone de Logs
- **Hauteur**: Limitée à 250px
- **Font**: Consolas/Monaco (monospace)
- **Couleur**: Gris clair sur fond sombre
- **Horodatage**: Format [HH:MM:SS]
- **Rotation**: 100 lignes maximum

### Boutons Utilitaires

#### Configuration
- **⚙️** Ouvre le dossier JSON/
- **Accès**: Fichiers de config du bot
- **Utilité**: Modification rapide des paramètres

#### Logs Avancés  
- **📋** Lance log_viewer_gui.py
- **Fonctionnalité**: Visualiseur de logs complet
- **Emplacement**: gui/tools/

#### Redémarrage
- **🔄** Arrêt + délai + redémarrage
- **Délai**: 2 secondes entre arrêt et redémarrage
- **Sécurité**: Vérification de l'état avant redémarrage

## 🛠️ Développement

### Structure du Code
```python
class CircularIndicator(QWidget):      # Indicateur circulaire
class StatusCard(QFrame):              # Carte de statut  
class DiscordBotThread(QThread):       # Thread bot Discord
class MainInterface(QMainWindow):      # Interface principale
```

### Points d'Extension
1. **Nouveaux indicateurs**: Héritez de `CircularIndicator`
2. **Nouvelles cartes**: Héritez de `StatusCard`  
3. **Nouvelles métriques**: Ajoutez dans `update_stats()`
4. **Nouveaux raccourcis**: Ajoutez dans `initShortcuts()`

### Tests
```bash
python "zen tests/test_enhanced_gui.py"
```

## 🔍 Dépannage

### Problème: Interface ne se lance pas
```bash
# Vérifiez PySide6
python -c "import PySide6; print('OK')"

# Vérifiez les modules bot
python -c "import bot; print('OK')"
```

### Problème: GPU non détecté
```bash
# Vérifiez pynvml
python -c "import pynvml; pynvml.nvmlInit(); print('GPU OK')"
```

### Problème: Base de données
- Vérifiez que `D:/neuro_memory/neuro.db` existe
- Vérifiez les permissions en écriture
- Utilisez un autre chemin si nécessaire

## 📈 Performance

### Optimisations Intégrées
- **Timers séparés** pour stats (2s) et statut (1s)
- **Limitation logs** pour éviter la surcharge mémoire  
- **Thread séparé** pour le bot Discord
- **Mise à jour conditionnelle** des indicateurs

### Utilisation Ressources
- **CPU**: ~1-2% en idle  
- **RAM**: ~50-80 MB
- **GPU**: Monitoring seulement (pas de rendu 3D)

## 🎯 Cas d'Usage

### Développement
- **Debug** en temps réel
- **Monitoring** des ressources
- **Tests** de performance
- **Logs** détaillés

### Production  
- **Surveillance** continue
- **Contrôle** à distance
- **Diagnostics** rapides
- **Interface** professionnelle

### Démonstration
- **Présentation** visuelle
- **Interface** moderne
- **Métriques** en temps réel
- **Contrôle** simple

---

## 📞 Support

Pour toute question ou problème :
1. Vérifiez cette documentation
2. Lancez les tests automatiques
3. Consultez les logs de l'application
4. Vérifiez la configuration système

**Bonne utilisation de votre interface Neuro-Bot améliorée ! 🎉**