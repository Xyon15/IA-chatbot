# 🎨 Guide du Thème Sombre NeuroBot

## 🌙 Nouveau thème sombre moderne

Votre interface NeuroBot a maintenant un **thème sombre élégant** avec une palette de couleurs soigneusement choisie pour une utilisation confortable, même la nuit !

## 🎯 Palette de couleurs

### Couleurs principales
- **`#1a1a1a`** - Noir profond (fond principal)
- **`#2d2d2d`** - Gris très foncé (cartes et panneaux)
- **`#3a3a3a`** - Gris moyen (éléments interactifs)
- **`#4a4a4a`** - Gris clair (bordures et séparateurs)

### Couleurs d'accent
- **`#4a9eff`** - **Bleu moderne** (boutons et highlights)
- **`#4ade80`** - **Vert success** (statuts positifs)
- **`#fbbf24`** - **Jaune warning** (avertissements)
- **`#ef4444`** - **Rouge erreur** (erreurs et alertes)

### Couleurs de texte
- **`#ffffff`** - Blanc pur (texte principal)
- **`#d1d5db`** - Gris clair (texte secondaire)

## ✨ Avantages du thème sombre

### 🌙 **Confort visuel**
- Réduit la fatigue oculaire lors d'utilisation prolongée
- Parfait pour les sessions de monitoring nocturnes
- Contraste optimal pour la lisibilité

### ⚡ **Performance**
- Consommation énergétique réduite sur écrans OLED
- Interface moderne et professionnelle
- Couleurs cohérentes dans toute l'application

### 🎮 **Gaming/Streaming friendly**
- S'intègre parfaitement avec les setups gaming
- Idéal pour le streaming (moins de luminosité)
- Look professionnel pour les démonstrations

## 🎨 Éléments stylisés

### Boutons
- **État normal** : Fond gris foncé avec bordure
- **Hover** : Surbrillance bleue moderne (`#4a9eff`)
- **Actif** : État pressé avec feedback visuel

### Graphiques temps réel
- **Lignes** : Bleu accent avec dégradé
- **Fond** : Gris très foncé pour contraste optimal
- **Grilles** : Lignes subtiles grises

### Notifications
- **Info** : Fond gris-bleu avec accent bleu
- **Success** : Fond vert sombre avec accent vert clair
- **Warning** : Fond jaune sombre avec accent jaune
- **Error** : Fond rouge sombre avec accent rouge

## 🔧 Personnalisation

Si vous voulez ajuster les couleurs, modifiez la palette dans :
```python
# Dans neuro_gui.py
COLOR_PALETTE = {
    'primary_dark': '#1a1a1a',    # Votre couleur de fond
    'accent_orange': '#4a9eff',   # Votre couleur d'accent
    # ... autres couleurs
}
```

## 🚀 Comment lancer

```bash
# Activer l'environnement
llama-venv\Scripts\activate

# Lancer avec le nouveau thème sombre
python gui/launch_neuro_gui.py
```

## 📷 Capture d'écran

Votre interface affiche maintenant :
- 🖥️ **Fond noir profond** pour le confort
- 📊 **Graphiques bleus modernes** pour les métriques
- 🔔 **Notifications sombres** avec accents colorés
- 🎮 **Boutons stylisés** avec effets hover

---

🌟 **Profitez de votre nouvelle interface sombre moderne !** 

Cette palette a été choisie pour offrir un excellent contraste tout en restant agréable à l'œil, même lors de longues sessions de monitoring de votre bot NeuroBot.