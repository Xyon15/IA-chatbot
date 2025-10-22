# 🔄 Migration de Kira-Bot vers Desktop-Mate

Ce guide vous aide à **migrer** de **Kira-Bot** vers **Desktop-Mate**.

---

## 📋 Vue d'Ensemble

**Kira-Bot** (archivé) → **Desktop-Mate** (actif)

### Qu'est-ce qui change ?

| Aspect | Kira-Bot | Desktop-Mate |
|--------|----------|--------------|
| **Type** | Bot Discord pur | Bot Discord + Avatar VRM 3D |
| **Interface** | GUI Python simple | Unity + Python hybride |
| **IA** | LLM conversationnel | LLM + Expressions émotionnelles |
| **Architecture** | Monolithique | Modulaire (sessions 0-10) |
| **Mémoire** | SQLite basique | SQLite optimisé + indexes |

---

## 🚀 Installation Desktop-Mate

### 1. Prérequis

**Python** :
- Python 3.10+ (même que Kira-Bot)

**Nouveau** :
- **Unity 2022.3 LTS** pour l'avatar 3D
- **UniVRM** (installation automatique)

### 2. Cloner Desktop-Mate

```bash
git clone https://github.com/Xyon15/desktop-mate.git
cd desktop-mate
```

### 3. Environnement Python

```powershell
# Créer le venv
python -m venv venv

# Activer
.\venv\Scripts\Activate.ps1

# Installer dépendances
pip install -r requirements.txt
```

### 4. Configuration

```powershell
# Copier .env.example
copy .env.example .env

# Éditer .env avec vos tokens
notepad .env
```

**.env Desktop-Mate** :
```
DISCORD_TOKEN=votre_token_discord
TOTP_SECRET=votre_secret_2fa
```

### 5. Modèle LLM

**Réutiliser votre modèle Kira-Bot** :

```powershell
# Copier depuis Kira-Bot
copy C:\Dev\IA-chatbot\models\zephyr-7b-beta.Q5_K_M.gguf C:\Dev\desktop-mate\models\
```

Ou télécharger un nouveau modèle (voir [models/README.md](https://github.com/Xyon15/desktop-mate/blob/main/models/README.md)).

### 6. Unity (Nouveau)

1. **Installer Unity Hub** : [unity.com/download](https://unity.com/download)
2. **Installer Unity 2022.3 LTS**
3. **Ouvrir le projet** : `unity/DesktopMateUnity/`
4. **Cliquer Play ▶️**

---

## 🔄 Migration des Données

### Mémoire Conversationnelle

**Kira-Bot** : `data/kira.db`  
**Desktop-Mate** : `data/chat_history.db`

#### Option 1 : Nouveau Départ (Recommandé)

Commencer avec une **base de données vide** dans Desktop-Mate.

#### Option 2 : Migrer les Données (Avancé)

**Script de migration** (à créer) :

```python
# migrate_memory.py
import sqlite3

# Connexion Kira-Bot
kira_db = sqlite3.connect('C:/Dev/IA-chatbot/data/kira.db')
kira_cursor = kira_db.cursor()

# Connexion Desktop-Mate
desktop_db = sqlite3.connect('C:/Dev/desktop-mate/data/chat_history.db')
desktop_cursor = desktop_db.cursor()

# Migrer conversations (adapter selon votre schéma)
kira_cursor.execute("SELECT user_id, message, response FROM conversations")
for row in kira_cursor.fetchall():
    user_id, user_input, bot_response = row
    desktop_cursor.execute(
        "INSERT INTO chat_history (user_id, source, user_input, bot_response) VALUES (?, ?, ?, ?)",
        (user_id, "discord", user_input, bot_response)
    )

desktop_db.commit()
print("✅ Migration terminée !")
```

### Configuration

**Kira-Bot** : `JSON/*.json`  
**Desktop-Mate** : `data/config.json` (centralisé)

**Migration manuelle** : Copier vos paramètres dans `data/config.json`.

---

## 🎮 Utilisation Desktop-Mate

### Démarrage Rapide

```powershell
# 1. Démarrer Unity (dans l'éditeur Unity)
# Ouvrir unity/DesktopMateUnity/, cliquer Play ▶️

# 2. Démarrer l'interface Python
python main.py

# 3. Dans l'interface
# - Cliquer "Connect to Unity"
# - Cliquer "Load VRM Model"
# - Sélectionner votre avatar VRM
```

### Bot Discord (Session 10)

**Phase 3-5 en cours** :
```powershell
# Sera disponible après Session 10 Phase 7
python start_kira.py  # (similaire à Kira-Bot)
```

---

## 📊 Comparaison des Fonctionnalités

### ✅ Fonctionnalités Migrées

| Fonctionnalité | Kira-Bot | Desktop-Mate | Status |
|----------------|----------|--------------|--------|
| **LLM Local** | ✅ | ✅ | Migré (Phase 4) |
| **Mémoire SQLite** | ✅ | ✅ | Amélioré (Phase 2) |
| **Bot Discord** | ✅ | ⏳ | Phase 7 (à venir) |
| **2FA TOTP** | ✅ | ⏳ | Phase 10 (à venir) |
| **Recherche Web** | ✅ | ⏳ | Phase future |
| **GPU Optimisation** | ✅ | ✅ | Migré (Phase 3) |

### ✨ Nouvelles Fonctionnalités

| Fonctionnalité | Status | Session |
|----------------|--------|---------|
| **Avatar VRM 3D** | ✅ | Session 5 |
| **Expressions Faciales** | ✅ | Session 6 |
| **Transitions Fluides** | ✅ | Session 7 |
| **Clignement Auto** | ✅ | Session 8 |
| **Mouvements Tête** | ✅ | Session 9 |
| **IA Conversationnelle** | 🔄 | Session 10 (14%) |
| **GUI Chat** | ⏳ | Session 10 Phase 8 |
| **Lip-Sync Audio** | ⏳ | Session 11 |

---

## 🔧 Commandes Discord

### Kira-Bot → Desktop-Mate

**Commandes identiques** (Phase 7 à venir) :

| Commande | Kira-Bot | Desktop-Mate (Phase 7) |
|----------|----------|------------------------|
| `!helpme` | ✅ | ⏳ |
| `!stats` | ✅ | ⏳ |
| `!context` | ✅ | ⏳ |
| `!remember` | ✅ | ⏳ |
| `!facts` | ✅ | ⏳ |
| `!forget` | ✅ (2FA) | ⏳ (2FA Phase 10) |
| `!reset` | ✅ (2FA) | ⏳ (2FA Phase 10) |

**Nouvelles commandes Desktop-Mate** :

| Commande | Description | Phase |
|----------|-------------|-------|
| `!expression <nom>` | Change expression avatar | Phase 11 |
| `!emotion auto on/off` | Émotions automatiques | Phase 11 |

---

## 📚 Documentation

### Kira-Bot (Archivé)
- [README.md](README.md)
- [ARCHIVED.md](ARCHIVED.md)

### Desktop-Mate (Actif)
- **Point d'entrée** : [docs/START_HERE.md](https://github.com/Xyon15/desktop-mate/blob/main/docs/START_HERE.md)
- **Index complet** : [docs/INDEX.md](https://github.com/Xyon15/desktop-mate/blob/main/docs/INDEX.md)
- **Session 10 (IA)** : [docs/sessions/session_10_ai_chat/](https://github.com/Xyon15/desktop-mate/tree/main/docs/sessions/session_10_ai_chat)

---

## ❓ FAQ Migration

### Dois-je désinstaller Kira-Bot ?

**Non**, les deux projets peuvent coexister sur votre machine.

Kira-Bot : `C:\Dev\IA-chatbot\`  
Desktop-Mate : `C:\Dev\desktop-mate\`

### Puis-je réutiliser mon token Discord ?

**Oui** ! Copiez simplement `DISCORD_TOKEN` de `.env` Kira-Bot vers `.env` Desktop-Mate.

### Mes conversations seront-elles perdues ?

**Non** si vous migrez la base de données (voir section ci-dessus).  
**Oui** si vous commencez avec une base vierge (recommandé).

### Unity est-il obligatoire ?

**Oui** pour l'avatar 3D.  
**Non** si vous utilisez uniquement le bot Discord (Phase 7+).

### Où signaler des bugs ?

**Desktop-Mate Issues** : [github.com/Xyon15/desktop-mate/issues](https://github.com/Xyon15/desktop-mate/issues)

---

## 🆘 Support

### Problèmes de Migration

1. **Ouvrir une issue** : [Desktop-Mate Issues](https://github.com/Xyon15/desktop-mate/issues)
2. **Consulter la doc** : [docs/START_HERE.md](https://github.com/Xyon15/desktop-mate/blob/main/docs/START_HERE.md)
3. **Lire les sessions** : [docs/sessions/](https://github.com/Xyon15/desktop-mate/tree/main/docs/sessions)

### Aide Unity

- **Installation Unity** : [docs/sessions/session_2_unity_installation/](https://github.com/Xyon15/desktop-mate/tree/main/docs/sessions/session_2_unity_installation)
- **Connexion Python↔Unity** : [docs/sessions/session_4_python_unity_connection/](https://github.com/Xyon15/desktop-mate/tree/main/docs/sessions/session_4_python_unity_connection)

---

## 🎉 Bienvenue sur Desktop-Mate !

Merci d'avoir utilisé **Kira-Bot** ! 🤖

Le projet continue avec encore plus d'ambition dans **Desktop-Mate** ! 🎭✨

**Prochaines étapes** :
1. ✅ Cloner Desktop-Mate
2. ✅ Installer dépendances
3. ✅ Configurer Unity
4. ✅ Lancer l'avatar VRM
5. ⏳ Attendre Session 10 Phase 7 pour Discord Bot

---

**Développé par** : Xyon  
**Migration vers** : [Desktop-Mate](https://github.com/Xyon15/desktop-mate) 🎭
