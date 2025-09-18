# 🤖 IA-ChatBot (Kira-Bot)

Développé par Xyon

Idée principale de vedal (https://vedal.ai).

**Kira-Bot** est un chatbot Discord intelligent alimenté par des modèles de langage locaux (LLM). Il offre des capacités de conversation avancées avec mémoire persistante, recherche web, optimisation GPU automatique, et une interface graphique moderne avec système de plugins extensible.

## ✨ Fonctionnalités

### 🧠 Intelligence Artificielle
- **Modèles LLM locaux** : Utilise des modèles quantifiés GGUF pour des performances optimales
- **Accélération GPU** : Support NVIDIA CUDA avec optimisation automatique RTX 4050
- **Profils adaptatifs** : 6+ profils d'optimisation GPU (Performance, Balanced, Emergency, etc.)
- **Monitoring temps réel** : Surveillance VRAM, température GPU et performances système
- **Mémoire conversationnelle** : Se souvient des échanges précédents avec chaque utilisateur (SQLite optimisé)
- **Mémoire à long terme** : Stockage persistant de faits importants avec indexation avancée

### 🌐 Capacités Web
- **Recherche DuckDuckGo** : Accès aux informations en temps réel
- **Recherche intelligente** : Intégration automatique des résultats dans les réponses

### 🎮 Interface Discord
- **Réponses automatiques** : Peut répondre automatiquement dans certains canaux
- **Commandes avancées** : 15+ commandes avec sécurité 2FA (TOTP)
- **Système d'autorisation** : Contrôle d'accès basé sur les rôles Discord avec authentification renforcée
- **Optimisation GPU** : Commandes `!optimize` avec profils adaptatifs en temps réel

### 🖥️ Interface Graphique
- **GUI PySide6** : Interface de bureau moderne avec lanceur unifié intelligent
- **Sélection automatique** : Détection automatique de l'interface optimale (Enhanced/Unified)
- **Monitoring avancé** : Graphiques temps réel GPU/CPU, métriques de performance
- **Architecture modulaire** : Tous les composants GUI organisés dans le dossier `gui/` avec système de plugins
- **Interface moderne** : Design sombre avec notifications toast, graphiques animés et générateur d'icônes SVG
- **Interface enhanced** : Interface améliorée avec contrôles avancés
- **Visualiseur de logs** : GUI intégré pour la supervision des logs système
- **Fallback intelligent** : Mécanisme de basculement automatique en cas d'échec

## 🏗️ Architecture

```
c:\Dev\IA-chatbot\
├── 📝 README.md           # Documentation du projet
├── 🚀 start_kira.py      # Script de démarrage principal
├── 🖥️ launch_gui.py       # Lanceur GUI principal unifié avec sélection automatique (recommandé)
├── 🖥️ select_gui.py       # Sélecteur d'interface GUI
├── 🤖 bot.py              # Bot Discord principal 
├── 🧠 model.py            # Gestion des modèles LLM avec optimisation GPU
├── 💾 memory.py           # Système de mémoire SQLite avec indexation avancée
├── 🌐 web.py              # Fonctionnalités de recherche web 
├── ⚙️ config.py           # Configuration centralisée 
├── 🗄️ database.py         # Gestionnaire de base de données thread-safe
├── 🔒 auth_decorators.py  # Authentification 2FA TOTP sécurisée
├── 🛠️ utils.py            # Utilitaires divers 
├── 📦 requirements.txt    # Dépendances du projet
├── 📁 scripts/            # Scripts de lancement et utilitaires
├── 📁 zen tests/          # Tests unitaires et d'intégration
├── 📁 zen rapports/       # Rapports techniques et documentation avancée
├── 📁 gui/                # Interface graphique modulaire
│   ├── 🎯 launch_gui.py   # Lanceur GUI unifié (PRINCIPAL)
│   ├── 🎨 kira_gui.py    # Interface GUI moderne
│   ├── 🔧 enhanced_main_gui.py # Interface GUI enhanced avec contrôles avancés
│   ├── 📊 chart_widgets.py # Widgets de graphiques temps réel
│   ├── 🎨 theme_manager.py # Gestionnaire de thèmes dynamiques
│   ├── 🔔 notification_system.py # Notifications toast modernes
│   ├── ⚙️ advanced_controls.py # Contrôles avancés et monitoring
│   ├── 🔌 plugin_system.py # Système de plugins extensible
│   ├── 🎨 icons_generator.py # Générateur d'icônes SVG
│   ├── 🌙 dark_theme_helper.py # Helper thème sombre
│   ├── 📁 assets/         # Ressources (icônes SVG)
│   ├── 📁 tools/          # Outils GUI
│   │   └── 📄 log_viewer_gui.py # Visualiseur de logs GUI
│   ├── 📖 THEME_GUIDE.md  # Guide des thèmes GUI
│   ├── 📖 GUI_USAGE.md    # Guide d'utilisation des interfaces
│   └── 📖 REORGANISATION_GUI.md # Documentation réorganisation
├── 📁 commands/           # Commandes Discord avec sécurité par rôles + 2FA sélectif
│   ├── ⚙️ auto.py         # Gestion réponses automatiques (rôle seul)
│   ├── ⚙️ bye.py          # Arrêt du bot (rôle seul)
│   ├── ⚙️ context.py      # Configuration contexte + logging avancé
│   ├── ❓ help.py         # Aide et documentation + sécurité renforcée
│   ├── 📏 limits.py       # Limites de caractères + validation
│   ├── 🧠 memory.py       # Commandes mémoire + 2FA + indexation
│   ├── 🚀 optimize.py     # Optimisation GPU avancée et profils adaptatifs (rôle seul)
│   ├── 📊 stats.py        # Statistiques système + monitoring GPU temps réel
│   └── 🌐 web_cmd.py      # Commandes web + gestion d'erreurs robuste
├── 📁 events/             # Gestionnaires d'événements
│   └── 💬 on_message.py   # Traitement des messages avec recherche intelligente
├── 📁 tools/              # Utilitaires et outils avancés
│   ├── 🚀 gpu_optimizer.py # Optimiseur GPU RTX 4050 avec monitoring temps réel
│   ├── 📊 advanced_logging.py # Système de logs avancé avec rotation
│   └── 🎮 demo_logs.py    # Démonstration système de logs
├── 📁 JSON/               # Fichiers de configuration
│   ├── 🔄 autoreply.json  # Config réponses auto
│   ├── 📏 character_limits.json # Limites caractères
│   ├── ⚙️ config.json     # Configuration générale (OBSOLÈTE - supprimé)
│   ├── 💬 context.json    # Paramètres contexte conversationnel
│   ├── 📊 log_config.json # Configuration système de logs avancé (NOUVEAU)
│   └── 🌐 web.json        # État recherche web
├── 📁 models/             # Modèles LLM quantifiés
│   ├── zephyr-7b-beta.Q5_K_M.gguf
│   ├── mistral-7b-instruct-v0.2.Q5_K_M.gguf
│   └── phi-2.Q5_K_M.gguf
├── 📁 data/               # Base de données et logs
│   ├── 🗄️ kira.db        # SQLite avec index optimisés et pool de connexions
│   ├── 📊 logs.db         # Base de données des logs avancés (NOUVEAU)
│   └── 📄 kira_bot_advanced.log # Logs avancés avec rotation (NOUVEAU)
├── 📁 logs/               # Logs système legacy
│   └── 📄 kira_bot.log   # Logging standard (legacy)
├── 📁 llama-venv/         # Environnement virtuel Python optimisé
├── 🔧 start_kira_gui.bat # Script de lancement GUI rapide (NOUVEAU)
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

## 🚀 Lanceur GUI Unifié - Nouveau *(FUSION RÉALISÉE)*

Le nouveau `launch_gui.py` combine intelligemment toutes les fonctionnalités des anciens lanceurs :

### ✨ Fonctionnalités du Lanceur Unifié
- **🔧 Sélection automatique** : Détecte automatiquement la meilleure interface disponible
- **🎯 Modes multiples** : Auto, Enhanced, Unified, Select avec arguments de ligne de commande
- **🛡️ Fallback intelligent** : Enhanced → Unified en cas d'échec
- **🚀 Optimisation** : Lancement via subprocess ou import selon l'interface
- **📋 Aide intégrée** : Documentation complète avec `--help`
- **✅ Validation** : Vérification automatique des dépendances

### 🎮 Modes de Lancement Disponibles
```bash
python launch_gui.py           # Mode AUTO - Sélection intelligente (recommandé)
python launch_gui.py --enhanced    # Mode ENHANCED - Interface avancée directe
python launch_gui.py --unified     # Mode UNIFIED - Lanceur avec sélection
python launch_gui.py --select      # Mode SELECT - Sélection interactive
python launch_gui.py --help        # AIDE - Documentation complète
```

## 🚀 Démarrage Rapide - Méthodes Recommandées

### Option 1: Interface Graphique Unifiée (RECOMMANDÉE)
```bash
# Lanceur GUI principal unifié avec sélection automatique
python launch_gui.py

# Ou lancement rapide via script batch
start_kira_gui.bat

# Options de lancement spécifiques
python launch_gui.py --enhanced         # Force interface Enhanced
python launch_gui.py --unified          # Force interface Unified  
python launch_gui.py --select           # Sélection interactive

# Sélecteur d'interface manuel (legacy)
python select_gui.py
```

### Option 2: Bot Discord Direct
```bash
# Démarrage du bot Discord avec optimisation automatique
python start_kira.py

# Démarrage avec interface graphique intégrée
python start_kira.py --gui
```

### Option 3: Interfaces Spécialisées
```bash
# Interface GUI moderne principale
python gui/kira_gui.py

# Interface GUI enhanced avec monitoring avancé
python gui/enhanced_main_gui.py

# Visualiseur de logs intégré
python gui/tools/log_viewer_gui.py
```

## 📋 Méthodes de Lancement Alternatives

### Démarrage du bot Discord (Python direct)
```bash
python start_kira.py
```

### Démarrage avec interface graphique (Python direct)
```bash
# Méthode 1 : Lanceur principal unifié (recommandé)
python launch_gui.py

# Options avancées du lanceur unifié
python launch_gui.py --enhanced         # Interface Enhanced directe
python launch_gui.py --unified          # Interface Unified avec sélection
python launch_gui.py --select           # Sélection interactive
python launch_gui.py --help             # Aide complète

# Méthode 2 : Avec start_kira.py
python start_kira.py --gui

# Méthode 3 : Lancement direct des interfaces spécialisées
python gui/kira_gui.py
python gui/enhanced_main_gui.py
```

### Tests et Validation
```bash
# Tests unitaires et d'intégration
python "zen tests/test_start_kira.py"
python "zen tests/integration_test.py"

# Tests avec pytest (recommandé)
pytest "zen tests/"

# Démonstration du système de logs avancé
python tools/demo_logs.py

# Visualiseur de logs avec interface GUI
python gui/tools/log_viewer_gui.py
```

### Commandes Discord

#### 💬 Conversation
- Mentionnez simplement `@Kira-Bot` ou envoyez un message sans préfixe `!`
- Le bot répondra en utilisant son IA et sa mémoire

#### 🔧 Commandes administratives
*(Nécessite le rôle "KiraMaster" - Authentification 2FA uniquement pour commandes critiques)*

| Commande | Description | Sécurité |
|----------|-------------|----------|
| | | *✅ = Rôle "KiraMaster" requis* |
| | | *🔒 2FA = Rôle + Code 2FA* |
| `!helpme` | Affiche l'aide complète | ✅ |
| `!stats` | Statistiques système et GPU temps réel | ✅ |
| **🚀 OPTIMISATION GPU (NOUVEAU)** |
| `!optimize` | Menu d'optimisation GPU avec profils adaptatifs | ✅ |
| `!optimize analyze` | Analyse VRAM et recommandations | ✅ |
| `!optimize apply` | Applique l'optimisation recommandée | ✅ |
| `!optimize profiles` | Liste tous les profils disponibles | ✅ |
| `!optimize current` | Affiche le profil actuellement actif | ✅ |
| `!optimize set <profil>` | Change le profil d'optimisation | ✅ |
| `!optimize report` | Rapport d'optimisation détaillé | ✅ |
| `!optimize metrics` | Métriques de performance temps réel | ✅ |
| `!optimize auto on/off` | Optimisation automatique adaptative | ✅ |
| `!optimize task <type>` | Optimise pour un type de tâche spécifique | ✅ |
| **💬 CONVERSATION & MÉMOIRE** |
| `!auto on/off` | Active/désactive les réponses automatiques | ✅ |
| `!context <1-50>` | Définit le nombre d'échanges mémorisés | ✅ |
| `!remember [texte]` | Ajoute un fait à la mémoire long terme | ✅ |
| `!facts [@user]` | Affiche les faits connus avec indexation | ✅ |
| `!forget me/@user/all` | Efface les faits mémorisés | 🔒 2FA |
| `!reset` | Réinitialise la mémoire conversationnelle | 🔒 2FA |
| **🌐 RECHERCHE WEB** |
| `!web on/off` | Active/désactive la recherche web | ✅ |
| `!web test <texte>` | Test de recherche web avec diagnostics | ✅ |
| **⚙️ CONFIGURATION** |
| `!limits [valeur]` | Définit la longueur max des réponses | ✅ |
| `!resetlimits` | Restaure la limite par défaut (1900 caractères) | ✅ |
| `!bye` | Arrêt propre du bot avec sauvegarde | ✅ |

## 🚀 Optimisation GPU Avancée *(NOUVEAU)*

### Profils Adaptatifs Intelligents
- **🚀 Turbo Max** : Performance maximale (RTX 4050 optimisé)
- **⚡ Performance Optimized** : Équilibre performance/stabilité 
- **⚖️ Balanced Adaptive** : Adaptatif selon l'usage VRAM
- **💾 Conservative Stable** : Utilisation conservatrice stable
- **🆘 Emergency Safe** : Mode secours pour VRAM limitée
- **🖥️ CPU Fallback** : Fallback CPU si GPU indisponible

### Monitoring Temps Réel
- **VRAM Usage** : Surveillance continue de l'utilisation mémoire GPU
- **Température GPU** : Monitoring thermique avec alertes
- **Performance Metrics** : FPS, latence, efficacité contexte
- **Auto-optimisation** : Changement automatique de profil selon les conditions

### Commandes d'Optimisation
```bash
!optimize analyze     # Analyse VRAM et recommandations
!optimize apply       # Application automatique du profil optimal
!optimize set turbo   # Change vers profil Turbo Max
!optimize auto on     # Active l'optimisation automatique
!optimize metrics     # Métriques temps réel détaillées
```

## 🧠 Système de Mémoire Avancé

### Mémoire Conversationnelle
- **Base de données optimisée** : SQLite avec index pour de meilleures performances
- **Pool de connexions** : Gestion thread-safe des connexions multi-utilisateurs
- **Contexte configurable** : 1-50 échanges par utilisateur avec validation
- **Logging détaillé** : Traçabilité complète de toutes les opérations

### Mémoire Long Terme
- **Stockage persistant** : Faits importants sur les utilisateurs avec indexation avancée
- **Gestion sécurisée** : Commandes `!remember` et `!facts` avec validation
- **Effacement protégé** : Authentification 2FA obligatoire pour `!forget` et `!reset`
- **Performance optimisée** : Index automatiques sur les requêtes fréquentes + mise en cache

## 🔒 Sécurité et Authentification 2FA *(NOUVEAU)*

### Authentification TOTP (Time-based One-Time Password)
- **Sécurité renforcée** : Protection des commandes critiques par 2FA obligatoire
- **Compatible Google Authenticator** : Support des apps d'authentification standard
- **Secret personnalisable** : Variable d'environnement `AUTH_SECRET`
- **Timeout sécurisé** : Codes TOTP avec expiration automatique

### Commandes Protégées par 2FA
- `!forget` - Effacement mémoire
- `!reset` - Réinitialisation système

### Configuration 2FA
```bash
# Dans votre fichier .env
AUTH_SECRET=votre_secret_totp_personnalise
```

## 🌐 Recherche Web Intelligente

- **Moteur** : DuckDuckGo avec fallback HTML robuste et récupération gracieuse
- **Activation** : Commande `!web on/off` avec persistance
- **Test** : `!web test <requête>` avec diagnostics détaillés
- **Détection intelligente** : Reconnaissance automatique des besoins de recherche contextuelle
- **Mots-clés configurables** : Patterns regex avancés pour déclencher la recherche
- **Gestion d'erreurs** : Messages informatifs et récupération automatique
- **Logging détaillé** : Traçabilité complète de toutes les recherches avec métriques

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

#### `JSON/log_config.json` *(NOUVEAU)*
```json
{
  "version": 1,
  "formatters": {
    "detailed": {
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
  },
  "handlers": {
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "filename": "data/kira_bot_advanced.log",
      "maxBytes": 10485760,
      "backupCount": 5,
      "formatter": "detailed"
    }
  }
}
```

### Variables d'environnement
- `DISCORD_TOKEN` : Token du bot Discord (obligatoire)
- `AUTH_SECRET` : Secret pour l'authentification 2FA TOTP (obligatoire)
- `DB_PATH` : Chemin vers la base de données SQLite (optionnel, défaut: data/kira.db)
- `LOG_LEVEL` : Niveau de logging (optionnel, défaut: INFO)

## 🖥️ Interfaces Graphiques Modernes

### 🎯 Lanceur GUI Unifié (PRINCIPAL)
**Commande** : `python launch_gui.py`
- **Menu de sélection** d'interface avec prévisualisation
- **Détection automatique** des dépendances et compatibilité
- **Messages d'erreur** explicites avec solutions
- **Lancement sécurisé** avec gestion d'exceptions

### 🎨 Interface GUI Moderne 
**Commande** : `python gui/kira_gui.py`
- **Design moderne** avec thème sombre adaptatif
- **Notifications toast** animées et non-intrusives
- **Graphiques temps réel** GPU/CPU/Mémoire
- **Générateur d'icônes SVG** intégré

### 🔧 Interface GUI Enhanced
**Commande** : `python gui/enhanced_main_gui.py`
- **Contrôles avancés** pour utilisateurs experts  
- **Monitoring détaillé** VRAM, température, performances
- **Configuration en temps réel** des profils GPU
- **Debug et diagnostics** intégrés

### 🔌 Système de Plugins GUI
- **Architecture modulaire** extensible
- **Widgets personnalisés** réutilisables
- **Thèmes dynamiques** avec préférences utilisateur
- **API unifiée** pour le développement d'extensions

## 📊 Système de Logs Avancé *(NOUVEAU)*

### 🔍 Visualiseur de Logs GUI
**Commande** : `python gui/tools/log_viewer_gui.py`
- **Interface moderne** pour consultation des logs
- **Filtrage en temps réel** par niveau/module/date
- **Recherche textuelle** avec regex
- **Export** vers fichiers ou clipboard

### 🎮 Démonstration Interactive
**Commande** : `python tools/demo_logs.py`
- **Tests automatisés** de tous les niveaux de logging
- **Simulation d'erreurs** pour validation
- **Métriques de performance** système
- **Rotation automatique** des fichiers de logs

### 📈 Logging Multi-niveaux
```bash
# Configuration automatique avec rotation
data/kira_bot_advanced.log      # Log principal avec rotation 10MB
data/logs.db                     # Base de données logs structurés  
logs/kira_bot.log              # Legacy logging (compatibilité)
```

## 🚨 Résolution de Problèmes Modernes

### ❌ Erreurs de Dépendances
```bash
# Vérification et installation automatique
pip install -r requirements.txt

# Test des imports critiques
python -c "import discord, llama_cpp, PySide6; print('✅ Dépendances OK')"
```

### ⚡ Problèmes de Performance GPU
```bash
# Diagnostic GPU détaillé
python -c "from tools.gpu_optimizer import GPUOptimizer; GPUOptimizer().get_gpu_info()"

# Optimisation automatique
python start_kira.py --optimize-gpu
```

### 🔒 Erreurs d'Authentification
```bash
# Vérification du fichier .env
python -c "from config import DISCORD_TOKEN, AUTH_SECRET; print('✅ Tokens OK')"

# Test 2FA
python -c "import pyotp; print('✅ 2FA disponible')"
```

## 🔧 Développement Avancé

### 🏗️ Architecture Moderne
- **Modularité** : Séparation claire des responsabilités avec inversion de dépendances
- **Extensibilité** : Système de commandes, événements et GUI modulaires
- **Configuration centralisée** : Système unifié thread-safe avec `config.py`
- **Gestion d'erreurs robuste** : Logging structuré et récupération gracieuse
- **Sécurité intégrée** : Décorateurs 2FA TOTP et validation avancée des entrées

### 🔌 Ajout de Nouvelles Commandes
```python
# commands/ma_commande.py
from discord.ext.commands import has_role
from config import AUTHORIZED_ROLE, logger
from auth_decorators import require_2fa

def setup(bot):
    @bot.command()
    @has_role(AUTHORIZED_ROLE)
    @require_2fa  # Optionnel pour commandes critiques
    async def ma_commande(ctx, param: str = None):
        """Description de ma commande"""
        logger.info(f"Commande exécutée par {ctx.author}")
        # Votre logique ici
        await ctx.send("✅ Commande exécutée")
```

### 🎮 Extension du Système GUI
```python
# gui/plugins/mon_plugin.py
from PySide6.QtWidgets import QWidget
from gui.plugin_system import PluginBase

class MonPlugin(PluginBase):
    def __init__(self):
        super().__init__("Mon Plugin", "1.0.0")
    
    def create_widget(self) -> QWidget:
        # Retourner votre widget personnalisé
        pass
```

### 🧪 Tests et Validation
```bash
# Tests unitaires complets
pytest "zen tests/" -v --cov

# Tests d'intégration système
python "zen tests/test_start_kira.py"
python "zen tests/integration_test.py"

# Validation du code
python -m flake8 . --max-line-length=120
```

## 📊 Monitoring et Métriques

### 🖥️ Statistiques Système Temps Réel
- **GPU** : Utilisation VRAM, température, puissance, efficacité
- **CPU** : Utilisation, threads actifs, température 
- **Mémoire** : RAM système, swap, cache
- **Base de données** : Requêtes/sec, temps de réponse, index usage
- **Réseau** : Latence Discord, recherches web, débit

### 📈 Métriques de Performance
- **LLM** : Tokens/sec, temps de génération, efficacité contexte
- **Discord** : Messages traités/min, commandes exécutées, erreurs
- **Mémoire conversationnelle** : Rappels réussis, faits stockés/utilisateur
- **Interface GUI** : FPS, temps de réponse, utilisation CPU

## 📝 Notes de Version et Changements Récents

### 🔄 Version 1.0 - Fusion des Lanceurs GUI *(NOUVEAU - Décembre 2024)*

#### ✨ Changements Majeurs
- **🔧 Fusion réalisée** : `launch_enhanced_gui.py` fusionné dans `launch_gui.py`
- **🚀 Lanceur unifié** : Point d'entrée unique avec sélection automatique intelligente
- **🎯 Modes multiples** : Auto, Enhanced, Unified, Select avec arguments de ligne de commande
- **🛡️ Robustesse** : Fallback automatique Enhanced → Unified
- **📋 Documentation** : Aide intégrée complète avec `--help`

#### 🗂️ Fichiers Supprimés
- ❌ `launch_enhanced_gui.py` - Fonctionnalités intégrées dans `launch_gui.py`

#### 🎮 Nouveaux Arguments de Ligne de Commande
```bash
python launch_gui.py           # Mode AUTO - Sélection intelligente (défaut)
python launch_gui.py --enhanced    # Mode ENHANCED - Interface avancée directe
python launch_gui.py --unified     # Mode UNIFIED - Lanceur avec sélection
python launch_gui.py --select      # Mode SELECT - Sélection interactive
python launch_gui.py --help        # AIDE - Documentation complète
```

#### ✅ Tests et Validation
- **13 tests unitaires** créés et validés (100% réussite)
- **Couverture complète** des fonctionnalités fusionnées
- **Validation fonctionnelle** de tous les modes de lancement

#### 🎯 Avantages de la Fusion
- **Simplicité** : Un seul point d'entrée pour toutes les interfaces GUI
- **Intelligence** : Détection automatique de l'interface optimale disponible
- **Compatibilité** : Maintien de toutes les fonctionnalités précédentes
- **Robustesse** : Mécanismes de fallback intégrés
- **Maintenance** : Code unifié plus facile à maintenir

---

*Documentation mise à jour - Kira-Bot v1.0 (Fusion GUI)*

**Développé par** : Xyon | **Idée principale** : [vedal.ai](https://vedal.ai)
