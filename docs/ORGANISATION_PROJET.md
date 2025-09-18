# 📁 Organisation du Projet IA-ChatBot

Ce document décrit la nouvelle organisation du projet après le nettoyage et l'optimisation.

## 🗂️ Structure des Dossiers

```
c:\Dev\IA-chatbot\
├── 📝 README.md                    # Documentation principale du projet
├── 🤖 bot.py                       # Bot Discord principal
├── 🧠 model.py                     # Gestion des modèles LLM
├── 💾 memory.py                    # Système de mémoire
├── 🌐 web.py                       # Fonctionnalités web
├── ⚙️ config.py                    # Configuration générale
├── 🗃️ database.py                  # Gestion base de données
├── 🔧 utils.py                     # Utilitaires généraux
├── 🔒 auth_decorators.py           # Décorateurs d'authentification
├── 📋 requirements.txt             # Dépendances Python
├── 🚫 .gitignore                   # Fichiers à ignorer par git
├── 📄 Xyon-chatbot.txt             # Fichier important (ne pas supprimer!)
│
├── 🚀 launchers/                   # Scripts de lancement
│   ├── 📖 README.md               # Guide d'utilisation des lanceurs
│   ├── 🖥️ launch_gui.py           # Lanceur GUI principal (recommandé)
│   ├── 🖥️ launch_*_fullscreen.py # Lanceurs plein écran
│   ├── 🐍 start_*.py              # Scripts de démarrage
│   └── 🔲 *.bat                   # Scripts batch Windows
│
├── 📚 docs/                       # Documentation
│   ├── 📖 GUI_USAGE.md            # Guide utilisation interface
│   ├── 📖 PLEIN_ECRAN_GUIDE.md    # Guide plein écran
│   ├── 📖 README_LOGS_LAUNCHER.md # Guide logs
│   ├── 📖 NOUVELLE_ORGANISATION.md # Organisation GUI
│   └── 📄 Context zencoder kira.txt # Contexte projet
│
├── 🧪 tests/                      # Tests et vérifications
│   ├── 🧪 test_*.py               # Scripts de test
│   └── 🔍 check_logs_db.py        # Vérification logs/DB
│
├── 📦 archives/                   # Archives et anciens fichiers
│   ├── 📂 rapports/               # Anciens rapports utiles
│   ├── 📂 zen rapports/           # Rapports zen
│   └── 📂 zen tests/              # Tests zen
│
├── 🎮 commands/                   # Commandes Discord
│   ├── 📝 __init__.py
│   ├── 🤖 auto.py
│   ├── 👋 bye.py
│   ├── 🧠 memory.py
│   └── ... (autres commandes)
│
├── 🎯 events/                     # Gestionnaires d'événements Discord
│   ├── 📝 __init__.py
│   └── 💬 on_message.py
│
├── 🖥️ gui/                        # Interface graphique
│   ├── 📝 __init__.py
│   ├── 🎛️ enhanced_main_gui.py
│   ├── 🔧 advanced_controls.py
│   ├── 🔔 notification_system.py
│   ├── 🧩 plugin_system.py
│   ├── 🎨 icons_generator.py
│   └── 🛠️ tools/
│
├── 🔧 tools/                      # Outils système
│   ├── 📝 __init__.py
│   ├── 📊 advanced_logging.py
│   ├── 🎮 gpu_optimizer.py
│   └── 🧪 demo_logs.py
│
├── 📊 data/                       # Données et bases de données
│   ├── 🗃️ kira.db
│   ├── 🗃️ neuro.db
│   ├── 🗃️ logs.db
│   ├── 📋 log_config.json
│   └── 📝 *.log
│
├── 📝 logs/                       # Fichiers de logs
│   └── 📄 *.log
│
├── 🧠 models/                     # Modèles LLM
│   └── 🤖 *.gguf
│
├── ⚙️ JSON/                       # Fichiers de configuration JSON
│   ├── 📋 autoreply.json
│   ├── 📋 character_limits.json
│   ├── 📋 context.json
│   ├── 📋 log_config.json
│   └── 📋 web.json
│
├── 🐍 llama-venv/                 # Environnement virtuel Python
│   └── ... (ignoré par git)
│
└── 📜 scripts/                    # Scripts utilitaires
    └── 🔍 validate_log_system.py
```

## ✨ Améliorations Apportées

### 🧹 Nettoyage
- ✅ Suppression de tous les dossiers `__pycache__` (régénérés automatiquement)
- ✅ Regroupement des scripts de lancement dans `launchers/`
- ✅ Organisation de la documentation dans `docs/`
- ✅ Archive des anciens rapports dans `archives/`
- ✅ Regroupement des tests dans `tests/`

### 📁 Organisation
- ✅ Structure claire et logique des dossiers
- ✅ Documentation README dans chaque dossier important
- ✅ Séparation des préoccupations (code, docs, tests, archives)
- ✅ .gitignore mis à jour pour la nouvelle structure

### 🎯 Avantages
- 🚀 **Navigation plus facile** : Structure claire et intuitive
- 🔍 **Maintenance simplifiée** : Fichiers organisés par fonction
- 📚 **Documentation centralisée** : Tout dans le dossier `docs/`
- 🧪 **Tests isolés** : Environnement de test dédié
- 📦 **Archives séparées** : Anciens fichiers conservés mais organisés
- 🚫 **Moins de pollution** : .gitignore optimisé

## 🚀 Utilisation

### Lancement rapide
```bash
# Interface GUI recommandée
python launchers/launch_gui.py

# Ou via batch (Windows)
launchers\start_kira_gui.bat
```

### Structure de développement
- **Code principal** : Racine du projet
- **Scripts de lancement** : `launchers/`
- **Tests** : `tests/`
- **Documentation** : `docs/`
- **Configuration** : `JSON/`

## 📋 Notes importantes

⚠️ **Fichier protégé** : `Xyon-chatbot.txt` est conservé à la racine comme demandé

🔄 **Migration** : Tous les scripts de lancement ont été mis à jour pour fonctionner depuis la nouvelle structure

📝 **Documentation** : Chaque dossier contient sa propre documentation README