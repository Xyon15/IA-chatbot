# 🚀 Visionneur de Logs Avancé Neuro-Bot

## 📋 Vue d'ensemble

Le **Visionneur de Logs Avancé** est une interface moderne et intuitive pour analyser les logs de Neuro-Bot. Il reprend le thème visuel du GUI principal avec des couleurs néon et une interface sombre futuriste.

## ✨ Fonctionnalités

### 🎨 Interface Moderne
- **Thème sombre cohérent** avec le GUI principal
- **Couleurs néon** (bleu, vert, orange) pour une meilleure lisibilité
- **Icônes** pour chaque niveau de log et section
- **Animation fluide** et effets visuels

### 🔍 Filtrage Avancé
- **Par niveau** : DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Par logger** : Filtrage par source des logs
- **Par date** : Plage de dates personnalisable
- **Recherche textuelle** : Recherche dans le contenu des messages
- **Limite d'affichage** : Contrôle du nombre d'entrées

### 📊 Statistiques en Temps Réel
- **Cartes de stats** avec design moderne
- **Compteurs** par niveau de log (Total, Erreurs, Warnings, Infos)
- **Mise à jour automatique** toutes les 5 secondes

### 📋 Vues Multiples
- **Vue Table** : Affichage structuré avec colonnes
- **Vue Texte** : Format console avec couleurs
- **Tri et sélection** : Interaction avancée avec les données

### 💾 Export et Gestion
- **Export** en JSON, CSV, ou TXT
- **Nettoyage automatique** des anciens logs
- **Purge complète** avec confirmation
- **Auto-scroll** configurable

## 🚀 Utilisation

### Lancement Direct
```bash
# Depuis la racine du projet
python gui/tools/enhanced_log_viewer.py

# Ou via le script de lancement
python launch_log_viewer.py
```

### Depuis le GUI Principal
1. Ouvrir l'interface principale : `python gui/enhanced_main_gui.py`
2. Cliquer sur le bouton **"📋 Logs Avancés"**
3. Le visionneur s'ouvre dans une nouvelle fenêtre

## 🎯 Interface Utilisateur

### Panel de Filtres (Gauche)
- **🔍 Filtres Avancés** : Tous les contrôles de filtrage
- **📊 Statistiques** : Cartes visuelles des métriques

### Panel Principal (Droite)
- **📋 Table des Logs** : Vue tabulaire avec tri
- **📄 Vue Texte** : Format console coloré

### Barre de Menu
- **📁 Fichier** : Export et options de sauvegarde
- **🔧 Outils** : Actualisation, nettoyage, configuration

## 🎨 Niveaux de Logs et Couleurs

| Niveau | Icône | Couleur | Description |
|--------|--------|---------|-------------|
| `DEBUG` | 🐛 | Gris | Informations de débogage |
| `INFO` | ℹ️ | Bleu néon | Informations générales |
| `WARNING` | ⚠️ | Orange | Avertissements |
| `ERROR` | ❌ | Rouge | Erreurs |
| `CRITICAL` | 💥 | Violet | Erreurs critiques |

## ⚙️ Configuration

### Base de Données
- **Emplacement** : `c:/Dev/IA-chatbot/data/logs.db`
- **Format** : SQLite avec index optimisés
- **Capacité** : Plusieurs milliers d'entrées

### Paramètres par Défaut
- **Limite d'affichage** : 1000 logs
- **Période par défaut** : 7 derniers jours
- **Auto-scroll** : Activé
- **Mise à jour stats** : 5 secondes

## 🛠️ Maintenance

### Nettoyage Automatique
Le système propose plusieurs options de nettoyage :

1. **Nettoyage par âge** : Supprime les logs plus vieux que N jours
2. **Purge complète** : Vide toute la table (avec confirmation)
3. **Export avant nettoyage** : Sauvegarde recommandée

### Performance
- **Index optimisés** sur timestamp, level, logger_name, user_id
- **Pagination** pour les grandes quantités de données
- **Mise à jour incrémentale** des vues

## 🔗 Intégration

### Avec le Système de Logs
Le visionneur s'interface directement avec :
- `tools/advanced_logging.py` : Gestionnaire de logs principal
- `data/logs.db` : Base de données SQLite
- Configuration JSON pour les paramètres

### Avec le GUI Principal
- **Bouton intégré** dans l'interface principale
- **Thème cohérent** avec les couleurs système
- **Lancement automatique** en tant que processus séparé

## 📈 Statistiques Disponibles

### Métriques Principales
- **Total des logs** sur la période sélectionnée
- **Répartition par niveau** (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Top des loggers** les plus actifs
- **Évolution temporelle** par jour

### Cartes Visuelles
Chaque métrique est présentée dans une carte moderne avec :
- **Icône** distinctive
- **Valeur** mise en évidence
- **Couleur** thématique
- **Mise à jour** en temps réel

## 🐛 Dépannage

### Problèmes Courants

**Le visionneur ne s'ouvre pas :**
- Vérifier que la base `logs.db` existe
- S'assurer que les dépendances PySide6 sont installées
- Consulter les logs d'erreur dans le GUI principal

**Données manquantes :**
- Vérifier les filtres de date
- Réinitialiser les filtres avec le bouton "🔄 Actualiser"
- Vérifier que le système de logs advanced est actif

**Performance lente :**
- Réduire la limite d'affichage
- Nettoyer les anciens logs
- Utiliser des filtres plus restrictifs

### Logs de Débogage
Le visionneur log ses propres actions dans le système. En cas de problème, consulter les logs avec le niveau DEBUG activé.

## 🚀 Fonctionnalités Futures

### Améliorations Prévues
- **Graphiques temporels** : Visualisation des tendances
- **Alertes configurables** : Notifications par email/Discord
- **Recherche regex** : Expressions régulières avancées
- **Thèmes personnalisables** : Choix de couleurs
- **Export automatique** : Sauvegarde périodique

### Intégrations Possibles
- **Monitoring système** : Corrélation avec les métriques système
- **Dashboard web** : Interface web complémentaire
- **API REST** : Accès programmatique aux logs
- **Plugins** : Extensions personnalisées

---

**Développé pour Neuro-Bot** 🤖 | **Thème moderne** avec couleurs néon | **Interface intuitive** et performante