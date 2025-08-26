# Scripts de Test et Vérification - Neuro-Bot

Ce dossier contient tous les scripts de test et de vérification pour le système Neuro-Bot.

## 📋 Scripts Disponibles

### 🔍 Vérifications Complètes

#### `test_database_integrity_fixed.py`
**Vérification complète de la base de données**
- Existence et structure de la base
- Intégrité SQLite (PRAGMA integrity_check)
- Cohérence des données
- Tests d'opérations CRUD
- Statistiques détaillées

```bash
python "zen tests/test_database_integrity_fixed.py"
```

#### `test_model_integrity.py`
**Vérification complète du modèle LLM**
- Existence et intégrité du fichier modèle
- Initialisation et configuration
- Tests de génération de texte
- Vérification des performances
- Tests des fonctions utilitaires

```bash
python "zen tests/test_model_integrity.py"
```

#### `test_memory_functions.py`
**Tests des fonctions de mémoire**
- Auto-reply
- Mémoire conversationnelle
- Gestion des faits
- Fonctions de suppression

```bash
python "zen tests/test_memory_functions.py"
```

### ⚡ Vérification Rapide

#### `quick_health_check.py`
**Vérification rapide de l'état de santé**
- Test rapide de la base de données
- Test rapide du modèle LLM
- Idéal pour les vérifications de routine

```bash
python "zen tests/quick_health_check.py"
```

### 🔧 Outils de Maintenance

#### `auto_migrate_database.py`
**Migration automatique de la base de données**
- Corrige la structure de la table `facts`
- Sauvegarde automatique avant migration
- Vérification post-migration

```bash
python "zen tests/auto_migrate_database.py"
```

#### `debug_database.py`
**Debug détaillé de la base de données**
- Analyse approfondie de la structure
- Tests d'opérations spécifiques
- Utile pour le diagnostic

```bash
python "zen tests/debug_database.py"
```

## 📊 Rapports Générés

### `rapport_complet_neuro_bot.md`
**Rapport complet du système**
- État global du système
- Détails de tous les composants
- Métriques de performance
- Recommandations

### `rapport_verification_db.md`
**Rapport spécifique à la base de données**
- Détails de la structure
- Actions correctives effectuées
- Statistiques d'utilisation

## 🚀 Utilisation Recommandée

### Vérification Initiale
```bash
# Vérification complète du système
python "zen tests/test_database_integrity_fixed.py"
python "zen tests/test_model_integrity.py"
python "zen tests/test_memory_functions.py"
```

### Vérifications de Routine
```bash
# Vérification rapide quotidienne
python "zen tests/quick_health_check.py"
```

### En cas de Problème
```bash
# Debug approfondi
python "zen tests/debug_database.py"

# Migration si nécessaire
python "zen tests/auto_migrate_database.py"
```

## 📈 Résultats des Derniers Tests

**Date** : 26 août 2025 - 21:14:54

### Base de Données
- ✅ **5/5 vérifications passées**
- Structure corrigée et optimisée
- 34 entrées de mémoire, 0 faits

### Modèle LLM
- ✅ **8/8 vérifications passées**
- Zephyr-7B-Beta (4.78 GB)
- Performances : 3.4s par génération
- GPU CUDA entièrement utilisé

### Fonctions Mémoire
- ✅ **4/4 tests passés**
- Toutes les fonctionnalités opérationnelles

## 🔒 Sécurité

- **Sauvegardes automatiques** avant toute migration
- **Tests non-destructifs** par défaut
- **Validation des données** avant modifications
- **Logging détaillé** de toutes les opérations

## 📝 Notes

- Tous les scripts utilisent des chemins absolus
- Les tests nettoient automatiquement leurs données temporaires
- Les rapports sont générés automatiquement
- Compatible avec l'environnement virtuel `llama-venv`

---

**Dernière mise à jour** : 26 août 2025  
**Statut global** : ✅ SYSTÈME ENTIÈREMENT FONCTIONNEL