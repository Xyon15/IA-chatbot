# 🔧 Résolution des Problèmes - Neuro-Bot

## 📋 Problèmes Identifiés et Solutions

### ❌ Problème 1: "Improper token has been passed"

**Cause**: Le token Discord dans le fichier `.env` est invalide ou expiré.

**Solution**:
```bash
python fix_discord_token.py
```

**Étapes manuelles**:
1. Allez sur https://discord.com/developers/applications
2. Créez une nouvelle application
3. Dans "Bot", copiez le token
4. Remplacez `DISCORD_TOKEN=...` dans `.env`

---

### ❌ Problème 2: Modèle se lance sur CPU au lieu de GPU

**Cause**: llama-cpp-python n'a pas été compilé avec le support CUDA.

**Solution immédiate**: ✅ **CORRIGÉ** - Configuration CPU activée
```
N_GPU_LAYERS=0  # CPU uniquement
```

**Pour activer GPU plus tard**:
```bash
python install_cuda_support.py
```

---

## ✅ État Actuel

### 🟢 Fonctionnel
- ✅ Modèle LLM chargé correctement (CPU)
- ✅ Base de données initialisée
- ✅ Configuration validée
- ✅ Fichiers requis présents

### 🟡 À Corriger
- ⚠️ Token Discord invalide

---

## 🚀 Étapes de Résolution

### 1. Corriger le Token Discord (OBLIGATOIRE)
```bash
python fix_discord_token.py
```

### 2. Tester le Bot
```bash
python start_bot.py
```

### 3. Activer GPU (OPTIONNEL)
```bash
# Installer CUDA Toolkit d'abord
python install_cuda_support.py
```

---

## 📊 Performance

### Configuration Actuelle (CPU)
- ⏱️ **Vitesse**: ~1-5 tokens/seconde
- 💾 **Mémoire**: ~5GB RAM utilisés
- 🔥 **Température**: CPU normal

### Configuration GPU (après installation CUDA)
- ⏱️ **Vitesse**: ~20-50 tokens/seconde
- 💾 **Mémoire**: ~2GB VRAM utilisés
- 🔥 **Température**: GPU RTX 4050

---

## 🛠️ Outils de Diagnostic

| Script | Description |
|--------|-------------|
| `diagnose_issues.py` | Diagnostic complet des problèmes |
| `test_gpu_config.py` | Test de configuration GPU/CPU |
| `fix_discord_token.py` | Guide pour corriger le token |
| `install_cuda_support.py` | Installation support CUDA |

---

## 🔍 Vérifications Finales

### Avant de lancer le bot:
- [ ] Token Discord valide dans `.env`
- [ ] Modèle GGUF présent dans `models/`
- [ ] Rôle "NeuroMaster" créé sur Discord
- [ ] Bot invité sur votre serveur

### Test de fonctionnement:
```bash
# Test complet
python start_bot.py

# Commandes Discord à tester:
!helpme
!stats
@Neuro-Bot Bonjour!
```

---

## 📞 Support

### Erreurs communes:
- **"Token invalide"** → `python fix_discord_token.py`
- **"Modèle lent"** → Configuration CPU normale
- **"Commandes refusées"** → Vérifiez le rôle "NeuroMaster"

### Logs utiles:
- `logs/neuro_bot.log` - Logs détaillés du bot
- Console - Erreurs en temps réel

---

## 🎯 Prochaines Étapes

1. **Immédiat**: Corriger le token Discord
2. **Test**: Lancer le bot et tester les fonctionnalités
3. **Optimisation**: Installer CUDA si performances insuffisantes
4. **Configuration**: Personnaliser les paramètres selon vos besoins

---

