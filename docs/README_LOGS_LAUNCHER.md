# 🚀 Lanceurs du Système de Logs Kira-Bot

## 📋 Fichiers disponibles

### 🔥 **`launch_logs_viewer.bat`** (Recommandé)
- **Type** : Fichier batch Windows classique
- **Usage** : Double-clic ou exécution en ligne de commande
- **Avantages** : Simple, rapide, compatible avec tous les Windows
- **Interface** : Console colorée avec vérifications

### ⚡ **`launch_logs_viewer.ps1`** (Avancé)  
- **Type** : Script PowerShell moderne
- **Usage** : Clic-droit → "Exécuter avec PowerShell"
- **Avantages** : Interface plus riche, gestion d'erreurs avancée
- **Prérequis** : PowerShell activé (généralement par défaut)

## 🎯 Utilisation rapide

### Option 1 : Fichier Batch (Le plus simple)
```cmd
# Double-cliquez sur le fichier
launch_logs_viewer.bat

# Ou en ligne de commande
cd c:\Dev\IA-chatbot
.\launch_logs_viewer.bat
```

### Option 2 : PowerShell (Plus de fonctionnalités)
```powershell
# Clic-droit → "Exécuter avec PowerShell"
# Ou en PowerShell :
cd c:\Dev\IA-chatbot
.\launch_logs_viewer.ps1
```

## ✅ Vérifications automatiques

Les deux lanceurs vérifient automatiquement :

- 🔍 **Environnement virtuel** : `llama-venv\Scripts\python.exe`
- 🔍 **Log viewer unifié** : `gui\tools\log_viewer_gui.py` 
- 🔍 **Répertoire de travail** : Positionnement automatique
- 🔍 **Dépendances Python** : Gestion des erreurs d'import

## 🎨 Fonctionnalités

### Interface Console
- ✅ **Couleurs modernes** : Vert/Cyan pour Kira-Bot
- ✅ **Messages clairs** : Emojis et statuts explicites
- ✅ **Gestion d'erreurs** : Messages d'aide en cas de problème
- ✅ **Pause intelligente** : Attend une action utilisateur en cas d'erreur

### Lancement Optimisé
- 🚀 **Démarrage rapide** : Environnement virtuel automatique
- 🚀 **Processus indépendant** : Le log viewer s'ouvre dans sa propre fenêtre
- 🚀 **Fermeture propre** : Gestion des codes de retour
- 🚀 **Multi-instances** : Possibilité d'ouvrir plusieurs viewers

## 🛠️ Dépannage

### Erreur "Environnement virtuel non trouvé"
```cmd
# Vérifiez que le dossier llama-venv existe
dir llama-venv\Scripts\python.exe

# Si manquant, recréez l'environnement :
python -m venv llama-venv
llama-venv\Scripts\activate
pip install -r requirements.txt
```

### Erreur "Log viewer non trouvé"
```cmd
# Vérifiez la présence du fichier unifié
dir gui\tools\log_viewer_gui.py

# Le fichier devrait être la version fusionnée moderne
```

### Erreur PowerShell "Execution Policy"
```powershell
# Autorisez l'exécution (une seule fois) :
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📊 Comparaison des lanceurs

| Caractéristique | Batch (.bat) | PowerShell (.ps1) |
|-----------------|--------------|-------------------|
| **Simplicité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Compatibilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Interface** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Gestion erreurs** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Vitesse** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🎯 Recommandation

**Utilisez `launch_logs_viewer.bat`** pour un usage quotidien simple et rapide.

**Utilisez `launch_logs_viewer.ps1`** si vous préférez une interface plus moderne avec plus d'informations.

---

*🤖 Créé pour Kira-Bot - Système de logs unifié*