# 🚀 Scripts de Lancement Neuro-Bot

Ce dossier `batch/` contient tous les scripts batch pour différents modes de lancement du bot.

## 📋 Scripts Disponibles

### 🎯 `launch_neuro.bat` - **RECOMMANDÉ**
- **Menu interactif** avec choix du mode
- Options : Bot automatique, Bot interactif, GUI, Configuration
- Gestion d'erreur complète
- Parfait pour les utilisateurs

### ⚡ `start_bot.bat` - Démarrage Rapide Bot
- Lance directement le bot Discord
- Optimisation GPU automatique (`--auto`)
- Messages d'erreur clairs

### 🎨 `start_gui.bat` - Interface Graphique
- Lance l'interface graphique PySide6
- Optimisation GPU automatique
- Vérification des dépendances GUI

### 🧪 `dev_start.bat` - Mode Développeur
- Création automatique de l'environnement virtuel si absent
- Installation automatique des dépendances
- Logs détaillés pour le développement

### 🔧 `setup.bat` - Configuration Initiale
- Installation des dépendances
- Vérification de la configuration
- Tests des imports

### 🔍 `diagnostic.bat` - **NOUVEAU**
- Diagnostic complet de l'environnement
- Vérification des modules installés
- Détection des problèmes

### 🛠️ `repair.bat` - **NOUVEAU**
- Réparation automatique de l'environnement
- Installation/réinstallation des dépendances
- Création de l'environnement virtuel

## 🚨 Résolution de Problèmes

### Erreur "No module named 'dotenv'"
```bash
cd batch
repair.bat    # Réparation automatique
```

### Environnement virtuel corrompu
```bash
cd batch
diagnostic.bat    # Voir l'état
repair.bat        # Réparer automatiquement
```

## 🎮 Utilisation

### Pour les Utilisateurs
```bash
# Double-cliquer sur le fichier ou dans un terminal :
cd batch
launch_neuro.bat
```

### En cas de problème
```bash
cd batch
diagnostic.bat    # Voir le problème
repair.bat        # Réparer automatiquement
```

### Pour un Lancement Rapide
```bash
cd batch
start_bot.bat    # Bot Discord
start_gui.bat    # Interface graphique
```

### Pour le Développement
```bash
cd batch
dev_start.bat    # Configuration automatique + lancement
```

## ⚙️ Fonctionnalités Automatiques

Tous les scripts incluent :
- ✅ **Vérification de l'environnement virtuel**
- ✅ **Activation automatique de `llama-venv`**
- ✅ **Optimisation GPU automatique** (avec `--auto`)
- ✅ **Gestion d'erreurs** avec messages explicites
- ✅ **Codes de retour** pour diagnostics

## 🔍 Diagnostics d'Erreur

Si un script échoue :

1. **Environnement virtuel manquant** → Lancez `batch\repair.bat`
2. **Token Discord invalide** → Vérifiez `.env`
3. **Modèle LLM absent** → Téléchargez un modèle `.gguf` dans `models/`
4. **Module manquant** → Lancez `batch\repair.bat`

## 🚦 Variables d'Environnement

Les scripts utilisent `start_neuro.py` qui lit :
- `DISCORD_TOKEN` : Token du bot Discord
- `AUTH_SECRET` : Secret TOTP pour 2FA (optionnel)
- `N_CTX`, `N_GPU_LAYERS`, `N_BATCH` : Configuration GPU (auto-générées)

## 🔧 Personnalisation

Pour modifier le comportement, éditez les paramètres dans `start_neuro.py` :
- `--auto` : Optimisation GPU automatique
- `--gui` : Mode interface graphique
- Sans paramètre : Mode interactif

## 📁 Structure Attendue

```
c:\Dev\IA-chatbot\
├── batch\               # 📁 Scripts batch de lancement
│   ├── launch_neuro.bat # Menu principal (RECOMMANDÉ)
│   ├── start_bot.bat    # Lancement rapide bot
│   ├── start_gui.bat    # Interface graphique
│   ├── dev_start.bat    # Mode développeur
│   ├── setup.bat        # Configuration initiale
│   ├── diagnostic.bat   # 🆕 Diagnostic système
│   ├── repair.bat       # 🆕 Réparation auto
│   └── README.md        # Cette documentation
├── llama-venv\          # Environnement virtuel Python
├── models\              # Modèles LLM .gguf
├── .env                 # Variables d'environnement
├── start_neuro.py       # Script principal de démarrage
└── requirements.txt     # Dépendances Python
```