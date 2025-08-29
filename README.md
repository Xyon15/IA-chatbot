# 🤖 IA-ChatBot

Développé par Xyon

Idée principale de vedal (https://vedal.ai).

**Neuro-Bot** est un chatbot Discord intelligent alimenté par des modèles de langage locaux (LLM). Il offre des capacités de conversation avancées avec mémoire persistante, recherche web, et une interface graphique intuitive.

## ✨ Fonctionnalités

### 🧠 Intelligence Artificielle
- **Modèles LLM locaux** : Utilise des modèles quantifiés GGUF pour des performances optimales
- **Accélération GPU** : Support NVIDIA CUDA pour des réponses rapides
- **Mémoire conversationnelle** : Se souvient des échanges précédents avec chaque utilisateur
- **Mémoire à long terme** : Stockage persistant de faits importants sur les utilisateurs

### 🌐 Capacités Web
- **Recherche DuckDuckGo** : Accès aux informations en temps réel
- **Recherche intelligente** : Intégration automatique des résultats dans les réponses

### 🎮 Interface Discord
- **Réponses automatiques** : Peut répondre automatiquement dans certains canaux
- **Commandes avancées** : Gestion complète via commandes slash
- **Système d'autorisation** : Contrôle d'accès basé sur les rôles Discord

### 🖥️ Interface Graphique
- **GUI PySide6** : Interface de bureau moderne pour la gestion du bot
- **Monitoring en temps réel** : Surveillance des performances GPU et système
- **Architecture modulaire** : Tous les composants GUI organisés dans le dossier `gui/`
- **Interface moderne** : Design sombre avec notifications toast et graphiques animés
- **Interface legacy** : Interface basique pour compatibilité

## 🏗️ Architecture

```
c:\Dev\IA-chatbot\
├── 📝 README.md           # Documentation du projet
├── 🚀 start_neuro.py      # Script de démarrage principal
├── 🖥️ launch_gui.py       # Lanceur GUI principal (recommandé)
├── 🤖 bot.py              # Bot Discord principal 
├── 🧠 model.py            # Gestion des modèles LLM 
├── 💾 memory.py           # Système de mémoire SQLite 
├── 🌐 web.py              # Fonctionnalités de recherche web 
├── ⚙️ config.py           # Configuration centralisée 
├── 🗄️ database.py         # Gestionnaire de base de données 
├── 🔒 auth_decorators.py  # Authentification 2FA 
├── 🛠️ utils.py            # Utilitaires divers 
├── 📦 requirements.txt    # Dépendances du projet
├── 📁 batch/              # Scripts de lancement batch
│   ├── launch_neuro.bat  # Menu principal (RECOMMANDÉ)
│   ├── start_bot.bat     # Lancement rapide bot Discord
│   ├── start_gui.bat     # Interface graphique PySide6
│   ├── dev_start.bat     # Mode développeur
│   ├── setup.bat         # Configuration initiale
│   ├── final_diagnostic.bat # Diagnostic système complet
│   ├── rebuild_env.bat   # Reconstruction environnement
│   ├── README.md         # Documentation scripts batch
│   ├── LANCEMENT.md      # Guide de lancement rapide
│   └── STATUS.md         # État des scripts
├── 📁 gui/                # Interface graphique modulaire
│   ├── neuro_gui.py      # Interface GUI moderne (principale)
│   ├── launch_neuro_gui.py # Lanceur GUI moderne
│   ├── bot_gui.py        # Interface GUI legacy
│   ├── chart_widgets.py  # Widgets de graphiques temps réel
│   ├── theme_manager.py  # Gestionnaire de thèmes
│   ├── notification_system.py # Notifications toast modernes
│   ├── advanced_controls.py # Contrôles avancés
│   ├── plugin_system.py  # Système de plugins extensible
│   ├── icons_generator.py # Générateur d'icônes SVG
│   ├── dark_theme_helper.py # Helper thème sombre
│   ├── THEME_GUIDE.md    # Guide des thèmes GUI
│   ├── assets/           # Ressources (icônes SVG)
│   └── tools/            # Outils GUI
│       └── log_viewer_gui.py # Visualiseur de logs GUI
├── 📁 commands/           # Commandes Discord 
│   ├── auto.py           # Gestion réponses automatiques + 2FA
│   ├── bye.py            # Arrêt du bot + 2FA
│   ├── context.py        # Configuration contexte + logging
│   ├── help.py           # Aide et documentation + sécurité
│   ├── limits.py         # Limites de caractères + validation
│   ├── memory.py         # Commandes mémoire + 2FA
│   ├── optimize.py       # Optimisation GPU et profils
│   ├── stats.py          # Statistiques système + monitoring
│   └── web_cmd.py        # Commandes web + gestion d'erreurs
├── 📁 events/             # Gestionnaires d'événements
│   └── on_message.py     # Traitement des messages (recherche intelligente)
├── 📁 tools/              # Utilitaires et outils
│   ├── gpu_optimizer.py  # Optimiseur GPU RTX 4050
│   └── advanced_logging.py # Système de logs avancé
├── 📁 JSON/               # Fichiers de configuration
│   ├── autoreply.json    # Config réponses auto
│   ├── character_limits.json # Limites caractères
│   ├── config.json       # Configuration générale
│   ├── context.json      # Paramètres contexte
│   ├── log_config.json   # Configuration système de logs
│   └── web.json          # État recherche web
├── 📁 models/             # Modèles LLM quantifiés
│   ├── zephyr-7b-beta.Q5_K_M.gguf
│   ├── mistral-7b-instruct-v0.2.Q5_K_M.gguf
│   └── phi-2.Q5_K_M.gguf
├── 📁 data/               # Base de données et logs
│   ├── neuro.db          # SQLite avec index optimisés
│   ├── logs.db           # Base de données des logs
│   └── neuro_bot_advanced.log # Logs avancés
├── 📁 logs/               # Logs système
│   └── neuro_bot.log     # Logging standard
├── 📁 llama-venv/         # Environnement virtuel Python
├── 🔧 launch.bat          # Raccourci vers batch/launch_neuro.bat
```

## 🚀 Installation

### Prérequis
- **Python 3.10+**
- **GPU NVIDIA** (recommandé pour de meilleures performances)
- **Token Discord Bot**
- **Windows 11** (testé sur cette plateforme)

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd IA-chatbot
```

### 2. Installation automatique (Windows) - RECOMMANDÉE
```bash
# Exécutez le script d'installation batch
batch\setup.bat
```

### 2bis. Diagnostic en cas de problème
```bash
# Diagnostic complet de l'environnement
batch\final_diagnostic.bat

# Réparation automatique si nécessaire
batch\rebuild_env.bat
```

### 3. Installation manuelle
```bash
# Créer l'environnement virtuel
python -m venv llama-venv
llama-venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Configuration
```bash
# Copiez le fichier d'exemple et éditez-le
copy .env.example .env
# Puis éditez .env avec vos tokens
```

### 5. Télécharger les modèles
Placez vos modèles GGUF dans le dossier `models/`. Les modèles supportés :
- `zephyr-7b-beta.Q5_K_M.gguf` (par défaut)
- `mistral-7b-instruct-v0.2.Q5_K_M.gguf`
- `phi-2.Q5_K_M.gguf`

## 🎯 Utilisation

## 🚀 Démarrage Rapide - Scripts Batch (RECOMMANDÉ)

### Option 1: Menu Principal (Simple & Efficace)
```bash
# Double-cliquez sur le fichier ou dans un terminal :
launch.bat

# Ou directement :
batch\launch_neuro.bat
```

### Option 2: Accès Direct aux Scripts
```bash
# Bot Discord uniquement (optimal)
batch\start_bot.bat

# Interface graphique
batch\start_gui.bat

# Mode développeur (avec création auto de l'environnement)
batch\dev_start.bat
```

## 📊 État des Scripts Batch

### ✅ Scripts Fonctionnels
- **`batch\final_diagnostic.bat`** - **PARFAIT** : Diagnostic complet de l'environnement
- **`batch\start_bot.bat`** - **PARFAIT** : Lance le bot Discord avec optimisation GPU
- **`batch\launch_neuro.bat`** - **FONCTIONNEL** : Menu interactif de lancement

### 🔧 Scripts de Maintenance
- **`batch\start_gui.bat`** - Interface graphique (nécessite PySide6)
- **`batch\rebuild_env.bat`** - Reconstruction complète de l'environnement
- **`batch\setup.bat`** - Configuration initiale du projet

### 🆘 En cas de Problème
1. **Diagnostic** : `batch\final_diagnostic.bat`
2. **Réparation automatique** : `batch\rebuild_env.bat`
3. **Documentation** : `batch\README.md`

## 📋 Méthodes de Lancement Alternatives

### Démarrage du bot Discord (Python direct)
```bash
python start_neuro.py
```

### Démarrage avec interface graphique (Python direct)
```bash
# Méthode 1 : Lanceur principal (recommandé)
python launch_gui.py

# Méthode 2 : Avec start_neuro.py
python start_neuro.py --gui

# Méthode 3 : Lancement direct
python gui/launch_neuro_gui.py
```

### Tests de validation
```bash
python "zen tests/test_start_neuro.py"
python "zen tests/integration_test.py"
```

### Commandes Discord

#### 💬 Conversation
- Mentionnez simplement `@Neuro-Bot` ou envoyez un message sans préfixe `!`
- Le bot répondra en utilisant son IA et sa mémoire

#### 🔧 Commandes administratives
*(Nécessite le rôle "NeuroMaster")*

| Commande | Description | Sécurité |
|----------|-------------|----------|
| `!helpme` | Affiche l'aide complète | ✅ |
| `!stats` | Statistiques système et GPU | ✅ |
| `!auto on/off` | Active/désactive les réponses automatiques | 🔒 2FA |
| `!context <1-50>` | Définit le nombre d'échanges mémorisés | ✅ |
| `!web on/off` | Active/désactive la recherche web | ✅ |
| `!web test <texte>` | Test de recherche web | ✅ |
| `!remember [texte]` | Ajoute un fait à la mémoire long terme | ✅ |
| `!facts [@user]` | Affiche les faits connus | ✅ |
| `!forget me/@user/all` | Efface les faits mémorisés | 🔒 2FA |
| `!limits [valeur]` | Définit la longueur max des réponses | ✅ |
| `!resetlimits` | Restaure la limite par défaut (1900 caractères) | ✅ |
| `!reset` | Réinitialise la mémoire | 🔒 2FA |
| `!bye` | Arrêt propre du bot | ✅ |

## 🧠 Système de Mémoire 

### Mémoire Conversationnelle
- **Base de données optimisée** : SQLite avec index pour de meilleures performances
- **Pool de connexions** : Gestion thread-safe des connexions
- **Contexte configurable** : 1-50 échanges par utilisateur
- **Logging détaillé** : Traçabilité de toutes les opérations

### Mémoire Long Terme
- **Stockage persistant** : Faits importants sur les utilisateurs
- **Gestion sécurisée** : Commandes `!remember` et `!facts`
- **Effacement protégé** : Authentification 2FA pour `!forget` et `!reset`
- **Performance optimisée** : Index automatiques sur les requêtes fréquentes

## 🌐 Recherche Web 

- **Moteur** : DuckDuckGo avec fallback HTML robuste
- **Activation** : Commande `!web on/off`
- **Test** : `!web test <requête>`
- **Détection intelligente** : Reconnaissance automatique des besoins de recherche
- **Mots-clés configurables** : Patterns regex pour déclencher la recherche
- **Gestion d'erreurs** : Messages informatifs et récupération gracieuse
- **Logging détaillé** : Traçabilité de toutes les recherches

## ⚙️ Configuration

### Fichiers de configuration JSON

#### `JSON/context.json`
```json
{
  "context_length": 10
}
```

#### `JSON/autoreply.json`
```json
{
  "enabled": true
}
```

#### `JSON/character_limits.json`
```json
{
  "max_length": 1900
}
```

#### `JSON/web.json`
```json
{
  "enabled": false
}
```

### Variables d'environnement
- `DISCORD_TOKEN` : Token du bot Discord
- `AUTH_SECRET` : Secret pour l'authentification 2FA

## 🚨 Scripts Batch - Documentation Détaillée

### 📋 Scripts Disponibles

#### 🎯 `launch_neuro.bat` - **RECOMMANDÉ**
- **Menu interactif** avec choix du mode de lancement
- Options : Bot automatique, Bot interactif, Interface graphique, Configuration
- Gestion d'erreur complète et messages explicites
- Parfait pour tous les utilisateurs

#### ⚡ `start_bot.bat` - Démarrage Rapide
- Lance directement le bot Discord
- Optimisation GPU automatique (`--auto`)
- Activation automatique de l'environnement virtuel `llama-venv`
- Messages d'erreur clairs avec codes de retour

#### 🎨 `start_gui.bat` - Interface Graphique
- Lance l'interface graphique PySide6
- Optimisation GPU automatique
- Vérification automatique des dépendances GUI
- Création d'environnement si absent

#### 🧪 `dev_start.bat` - Mode Développeur
- Création automatique de l'environnement virtuel si absent
- Installation automatique des dépendances manquantes
- Logs détaillés pour le développement
- Configuration optimisée pour le développement

#### 🔍 `final_diagnostic.bat` - Diagnostic Système
- Diagnostic complet de l'environnement Windows/Python
- Vérification de tous les modules installés
- Détection automatique des problèmes de configuration
- Recommandations de réparation précises
- Vérification de la base de données et des modèles LLM

#### 🛠️ `rebuild_env.bat` - Reconstruction Environnement
- Suppression et reconstruction complète de l'environnement virtuel
- Installation fraîche de toutes les dépendances
- Correction des références de chemins obsolètes
- Utile en cas de corruption d'environnement

#### ⚙️ Fonctionnalités Automatiques de tous les Scripts
- ✅ **Vérification de l'environnement virtuel** `llama-venv`
- ✅ **Activation automatique** de l'environnement Python
- ✅ **Optimisation GPU automatique** (avec paramètre `--auto`)
- ✅ **Gestion d'erreurs** avec messages explicites et codes de retour
- ✅ **Chemins relatifs corrigés** (`%~dp0..` pour compatibilité)

### 🚨 Résolution de Problèmes avec Scripts Batch

#### Erreur "No module named 'dotenv'" ou modules manquants
```bash
cd batch
final_diagnostic.bat    # Voir le problème exact
rebuild_env.bat         # Réparation automatique
```

#### Environnement virtuel corrompu ou chemins obsolètes
```bash
cd batch
rebuild_env.bat    # Reconstruction complète
```

#### Interface graphique "Aucune interface disponible"
```bash
cd batch
rebuild_env.bat    # Réinstalle PySide6 correctement
```

#### Bot Discord ne se connecte pas
```bash
cd batch
final_diagnostic.bat    # Vérifie DISCORD_TOKEN et configuration
```

### 🎮 Utilisation Recommandée des Scripts

#### Pour les Utilisateurs Finaux
1. **Démarrage quotidien** : Double-cliquez sur `launch.bat`
2. **Bot uniquement** : `batch\start_bot.bat`
3. **Interface graphique** : `batch\start_gui.bat`

#### En Cas de Problème
1. **Diagnostic d'abord** : `batch\final_diagnostic.bat`
2. **Réparation si nécessaire** : `batch\rebuild_env.bat`
3. **Documentation complète** : `batch\README.md`

#### Pour le Développement
1. **Première fois** : `batch\dev_start.bat`
2. **Tests réguliers** : `batch\final_diagnostic.bat`
3. **Problèmes persistants** : `batch\rebuild_env.bat`

### 🔍 Structure Attendue pour les Scripts
```
c:\Dev\IA-chatbot\
├── batch\               # 📁 Scripts batch de lancement
├── llama-venv\          # Environnement virtuel Python (auto-créé)
├── models\              # Modèles LLM .gguf (à télécharger)
├── .env                 # Variables d'environnement (DISCORD_TOKEN)
├── start_neuro.py       # Script principal de démarrage
└── requirements.txt     # Dépendances Python
```

## 🔧 Développement

### Structure du code
- **Modularité** : Séparation claire des responsabilités
- **Extensibilité** : Système de commandes et d'événements modulaire
- **Configuration centralisée** : Système unifié avec `config.py`
- **Gestion d'erreurs robuste** : Logging et récupération gracieuse
- **Sécurité intégrée** : Décorateurs 2FA et validation des entrées

### Ajout de nouvelles commandes
1. Créez un fichier dans `commands/`
2. Implémentez la fonction `setup(bot)`
3. Utilisez les décorateurs de sécurité (`@require_2fa`, `@require_authorized_role`)
4. Ajoutez le logging avec `from config import logger`
5. La commande sera automatiquement chargée

### Ajout de nouveaux événements
1. Créez un fichier dans `events/`
2. Implémentez la fonction `setup(bot)`
3. Ajoutez la gestion d'erreurs et le logging
4. L'événement sera automatiquement enregistré

### Tests et validation
- **Diagnostic automatique** : `batch\final_diagnostic.bat` (recommandé avant tests)
- Exécutez `python test_improvements.py` après chaque modification
- Tests d'intégration : `python "zen tests/test_start_neuro.py"`
- Tests avancés : `python "zen tests/integration_test.py"`
- Vérifiez les logs dans le dossier `logs/`
- Utilisez les scripts batch pour démarrage sécurisé : `batch\start_bot.bat`

## 📊 Monitoring

### Statistiques disponibles
- **GPU** : Utilisation, mémoire, température
- **Mémoire** : Nombre d'échanges stockés par utilisateur
- **Base de données** : Performances et statistiques des requêtes
- **Système** : Performances générales et utilisation des ressources

### Logging avancé
- **Logs rotatifs** : Conservation automatique de 7 jours
- **Niveaux configurables** : DEBUG, INFO, WARNING, ERROR
- **Formatage structuré** : Timestamps et contexte détaillé
- **Fichiers séparés** : Logs dans le dossier `logs/`

### Interface graphique
- **Interface moderne** (`neuro_gui.py`) : Design sombre avec animations
- **Monitoring temps réel** : CPU, RAM, GPU avec graphiques animés
- **Notifications toast** : Alertes visuelles modernes
- **Système de thèmes** : Couleurs personnalisables
- **Contrôles intuitifs** : Interface utilisateur simplifiée
- **Logs détaillés** : Visualiseur avancé avec filtrage (`log_viewer_gui.py`)
- **Système de plugins** : Architecture extensible

## 🖥️ Interface Graphique Complète

### 🎨 Interfaces disponibles

#### Interface Moderne (`neuro_gui.py`)
- **Design moderne** : Thème sombre avec palette de couleurs personnalisée
- **Monitoring temps réel** : CPU, RAM, GPU avec graphiques animés
- **Notifications toast** : Alertes visuelles avec animations fluides
- **Système de thèmes** : Gestionnaire de thèmes intégré
- **Plugins extensibles** : Architecture modulaire pour fonctionnalités custom

#### Interface Legacy (`bot_gui.py`)
- **Interface simple** : Contrôles basiques de démarrage/arrêt
- **Monitoring basique** : Informations système essentielles  
- **Compatibilité** : Maintenue pour rétrocompatibilité

### 🧩 Composants GUI

#### Widgets Spécialisés
- **`chart_widgets.py`** : Graphiques temps réel avec animations
- **`notification_system.py`** : Système de notifications toast
- **`advanced_controls.py`** : Contrôles de performance avancés
- **`plugin_system.py`** : Framework de plugins extensible

#### Personnalisation
- **`theme_manager.py`** : Gestion de thèmes dynamique
- **`icons_generator.py`** : Générateur d'icônes SVG
- **`dark_theme_helper.py`** : Helper pour thème sombre

#### Outils Avancés
- **`tools/log_viewer_gui.py`** : Visualiseur de logs avancé
- **`assets/`** : Bibliothèque d'icônes SVG

### 🚀 Lancement de l'interface

```bash
# Recommandé : Lanceur principal
python launch_gui.py

# Alternative : Lancement direct
python gui/launch_neuro_gui.py

# Via start_neuro.py
python start_neuro.py --gui
```

### 📁 Organisation modulaire

```
gui/
├── neuro_gui.py              # Interface principale moderne
├── launch_neuro_gui.py       # Lanceur GUI moderne
├── bot_gui.py                # Interface legacy
├── chart_widgets.py          # Widgets de graphiques
├── theme_manager.py          # Gestionnaire de thèmes
├── notification_system.py    # Notifications toast
├── advanced_controls.py      # Contrôles avancés
├── plugin_system.py          # Système de plugins
├── icons_generator.py        # Générateur d'icônes
├── dark_theme_helper.py      # Helper thème sombre
├── THEME_GUIDE.md           # Guide des thèmes
├── assets/                   # Ressources (icônes)
└── tools/
    └── log_viewer_gui.py     # Visualiseur de logs
```

## 🛡️ Sécurité 

### Authentification 2FA
- **TOTP (Time-based One-Time Password)** avec pyotp
- **Protection des commandes sensibles** : `!reset`, `!forget`, `!bye`, `!auto`
- **Codes temporaires** : Expiration automatique après 30 secondes
- **Logging de sécurité** : Traçabilité de toutes les tentatives d'authentification

### Contrôle d'accès
- **Système de rôles Discord** : Rôle "NeuroMaster" requis
- **Décorateurs de sécurité** : `@require_authorized_role` et `@require_2fa`
- **Validation des entrées** : Sanitisation et vérification des paramètres
- **Gestion des sessions** : Timeout automatique des sessions 2FA

### Sécurité des données
- **Base de données chiffrée** : Protection des données sensibles
- **Logs sécurisés** : Pas de stockage des tokens ou secrets
- **Isolation** : Environnement virtuel et permissions restreintes
- **Audit trail** : Traçabilité complète des actions administratives

## 🚀 Nouvelles Fonctionnalités (v2.0)

### ✨ Améliorations majeures
- 🔒 **Système d'authentification 2FA** complet
- 🗄️ **Base de données optimisée** avec index et pool de connexions
- 📊 **Logging avancé** avec rotation et niveaux configurables
- 🌐 **Recherche web intelligente** avec détection automatique
- ⚙️ **Configuration centralisée** pour une maintenance simplifiée
- 🧪 **Tests automatisés** pour valider les fonctionnalités
- 🚀 **Script de démarrage sécurisé** avec vérifications préalables
- 🖥️ **Interface GUI modulaire** : Architecture organisée dans le dossier `gui/`
- 🎨 **Design moderne** : Interface sombre avec notifications toast et graphiques animés

### 📈 Performances améliorées
- **+300% plus rapide** : Index automatiques sur les requêtes fréquentes
- **Thread-safe** : Pool de connexions pour la concurrence
- **Mémoire optimisée** : Gestion efficace des ressources
- **Récupération gracieuse** : Gestion robuste des erreurs

### 🔧 Maintenabilité
- **Code documenté** : Docstrings pour toutes les fonctions
- **Structure modulaire** : Séparation claire des responsabilités  
- **Tests intégrés** : Validation automatique des composants
- **Logging détaillé** : Débogage et monitoring facilités
- **Scripts batch automatisés** : Démarrage, diagnostic et maintenance simplifiés

---

## 📚 Documentation Supplémentaire

- **Scripts Batch** : `batch/README.md` - Documentation complète des scripts de lancement
- **Lancement Rapide** : `batch/LANCEMENT.md` - Guide de démarrage simplifié
- **État des Scripts** : `batch/STATUS.md` - État et diagnostic des scripts batch
- **Thèmes GUI** : `gui/THEME_GUIDE.md` - Guide des thèmes d'interface graphique

---

**Dernière mise à jour du README.md** : 29 août 2025 - 12:30  
**Version** : v2.0 avec scripts batch intégrés  
**Développé par** : Xyon | **Idée principale** : [vedal.ai](https://vedal.ai)
