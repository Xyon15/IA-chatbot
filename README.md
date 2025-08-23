# 🤖 Neuro-Bot

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
- **GUI PySide6** : Interface de bureau pour la gestion du bot
- **Monitoring en temps réel** : Surveillance des performances GPU et système

## 🏗️ Architecture

```
neuro-bot/
├── 🤖 bot.py              # Bot Discord principal
├── 🖥️ bot_gui.py          # Interface graphique
├── 🧠 model.py            # Gestion des modèles LLM
├── 💾 memory.py           # Système de mémoire SQLite
├── 🌐 web.py              # Fonctionnalités de recherche web
├── ⚙️ config.py           # Configuration globale
├── 🛠️ utils.py            # Utilitaires divers
├── 📁 commands/           # Commandes Discord
│   ├── auto.py           # Gestion réponses automatiques
│   ├── bye.py            # Arrêt du bot
│   ├── context.py        # Configuration contexte
│   ├── help.py           # Aide et documentation
│   ├── limits.py         # Limites de caractères
│   ├── memory.py         # Commandes mémoire
│   ├── stats.py          # Statistiques système
│   └── web_cmd.py        # Commandes web
├── 📁 events/             # Gestionnaires d'événements
│   └── on_message.py     # Traitement des messages
├── 📁 JSON/               # Fichiers de configuration
│   ├── autoreply.json    # Config réponses auto
│   ├── character_limits.json # Limites caractères
│   ├── config.json       # Configuration générale
│   ├── context.json      # Paramètres contexte
│   └── web.json          # État recherche web
├── 📁 models/             # Modèles LLM quantifiés
│   ├── zephyr-7b-beta.Q5_K_M.gguf
│   ├── mistral-7b-instruct-v0.2.Q5_K_M.gguf
│   └── phi-2.Q5_K_M.gguf
└── 📁 llama-cpp-python/   # Bindings Python pour llama.cpp
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
cd neuro-bot
```

### 2. Créer l'environnement virtuel
```bash
python -m venv llama-venv
llama-venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install discord.py llama-cpp-python python-dotenv pyside6 pynvml
```

### 4. Configuration
Créez un fichier `.env` à la racine du projet :
```env
DISCORD_TOKEN=votre_token_discord_ici
AUTH_SECRET=votre_secret_2fa_ici
```

### 5. Télécharger les modèles
Placez vos modèles GGUF dans le dossier `models/`. Les modèles supportés :
- `zephyr-7b-beta.Q5_K_M.gguf` (par défaut)
- `mistral-7b-instruct-v0.2.Q5_K_M.gguf`
- `phi-2.Q5_K_M.gguf`

## 🎯 Utilisation

### Démarrage du bot Discord
```bash
python bot.py
```

### Démarrage de l'interface graphique
```bash
python bot_gui.py
```

### Commandes Discord

#### 💬 Conversation
- Mentionnez simplement `@Neuro-Bot` ou envoyez un message sans préfixe `!`
- Le bot répondra en utilisant son IA et sa mémoire

#### 🔧 Commandes administratives
*(Nécessite le rôle "NeuroMaster")*

| Commande | Description |
|----------|-------------|
| `!helpme` | Affiche l'aide complète |
| `!stats` | Statistiques système et GPU |
| `!auto on/off` | Active/désactive les réponses automatiques |
| `!context <1-50>` | Définit le nombre d'échanges mémorisés |
| `!web on/off` | Active/désactive la recherche web |
| `!web test <texte>` | Test de recherche web |
| `!remember [texte]` | Ajoute un fait à la mémoire long terme |
| `!facts [@user]` | Affiche les faits connus |
| `!forget me/@user/all` | Efface les faits mémorisés |
| `!limits [valeur]` | Définit la longueur max des réponses |
| `!resetlimits` | Restaure la limite par défaut (1900 caractères) |
| `!reset` | Réinitialise la mémoire (avec 2FA) |
| `!bye` | Arrêt propre du bot |

## 🧠 Système de Mémoire

### Mémoire Conversationnelle
- Stockage SQLite des échanges récents
- Contexte configurable (1-50 échanges)
- Mémoire par utilisateur

### Mémoire Long Terme
- Stockage de faits persistants sur les utilisateurs
- Commandes `!remember` et `!facts` pour la gestion
- Base de données SQLite séparée

## 🌐 Recherche Web

- **Moteur** : DuckDuckGo
- **Activation** : Commande `!web on/off`
- **Test** : `!web test <requête>`
- **Intégration automatique** dans les réponses contextuelles

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

## 🔧 Développement

### Structure du code
- **Modularité** : Séparation claire des responsabilités
- **Extensibilité** : Système de commandes et d'événements modulaire
- **Configuration** : Paramètres centralisés et persistants

### Ajout de nouvelles commandes
1. Créez un fichier dans `commands/`
2. Implémentez la fonction `setup(bot)`
3. La commande sera automatiquement chargée

### Ajout de nouveaux événements
1. Créez un fichier dans `events/`
2. Implémentez la fonction `setup(bot)`
3. L'événement sera automatiquement enregistré

## 📊 Monitoring

### Statistiques disponibles
- **GPU** : Utilisation, mémoire, température
- **Mémoire** : Nombre d'échanges stockés
- **Système** : Performances générales

### Interface graphique
- Monitoring en temps réel
- Contrôles intuitifs
- Logs détaillés

## 🛡️ Sécurité

- **Authentification 2FA** pour les commandes critiques
- **Système de rôles** Discord pour l'autorisation
- **Validation** des entrées utilisateur
- **Isolation** de l'environnement virtuel


