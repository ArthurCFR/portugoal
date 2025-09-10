# Changelog - TaskGame Colocation

## Version 2.0.0 - Nouvelles fonctionnalités

### ✨ Nouveautés

#### 🎯 **Système d'attribution des tâches**
- Chaque tâche peut maintenant être attribuée à des colocataires spécifiques
- Les tâches non attribuées à un utilisateur apparaissent grisées avec un 🔒
- Attribution flexible : une tâche peut être assignée à 1 ou plusieurs colocataires
- Exemples d'attributions pré-configurées :
  - Tâches de garage/jardin : Antoine, Arthur, Raphael, Martin (pas Perrinne)
  - Tâches d'intérieur : Tous les colocataires
  - Réparations : Antoine, Arthur, Raphael, Martin

#### 🎨 **Couleurs par lieu**
- Chaque zone de la maison a maintenant une couleur distinctive :
  - 🟡 Cuisine
  - 🟢 Salon & Jardin
  - 🔵 SDB 1er étage
  - 🟣 SDB 2ème étage
  - 🟤 Rez-de-chaussée
  - ⚫ Garage
  - 🟠 Cour
  - ⚪ Tâches générales

#### 👤 **Historique détaillé**
- Affichage de qui a réalisé chaque tâche en dernier
- Date de réalisation avec format intelligent :
  - "Aujourd'hui" pour les tâches du jour
  - "Hier" pour les tâches d'hier
  - "Il y a X jours" pour les tâches plus anciennes
- Format : 👤 Nom - Date

#### ✏️ **Modification des tâches**
- Interface complète de modification en mode inline
- Modification des points, lieu, et attribution
- Boutons ✏️ (modifier) et 🗑️ (supprimer) pour chaque tâche
- Sauvegarde/Annulation des modifications
- Recalcul automatique des points après modification

### 📊 **Données complètes**

#### 🏠 **Structure JSON enrichie**
Nouveau format des tâches :
```json
{
  "nom_tache": {
    "points_base": 2,
    "lieu": "Cuisine",
    "derniere_realisation": "2025-01-10T15:30:00",
    "points_actuels": 3,
    "attribuee_a": ["Antoine", "Arthur", "Martin"],
    "derniere_realisation_par": "Antoine"
  }
}
```

#### 📋 **50+ tâches pré-configurées**
- **11 tâches** Cuisine
- **5 tâches** Salon  
- **10 tâches** Salles de bain (2 étages)
- **4 tâches** Rez-de-chaussée
- **4 tâches** Garage
- **6 tâches** Jardin
- **3 tâches** Cour d'entrée
- **8 tâches** Générales

### 🔧 **Améliorations techniques**

#### 🎮 **Interface utilisateur**
- Tâches grisées pour les utilisateurs non autorisés
- Affichage 🚫 au lieu du bouton ✓ pour les tâches non disponibles
- Meilleure lisibilité avec émojis et couleurs
- Interface de modification intuitive

#### 💾 **Stockage**
- Structure de données compatible avec l'ancien format
- Migration automatique des anciennes données
- Sauvegarde complète sur GitHub Gist

### 📁 **Fichiers fournis**

1. **`gist_data_complete.json`** : Fichier JSON complet à coller dans votre Gist GitHub
2. **`app.py`** : Application mise à jour avec toutes les nouvelles fonctionnalités
3. **`configGist.md`** : Guide de configuration GitHub Gist
4. **`CHANGELOG.md`** : Ce fichier de nouveautés

### 🚀 **Migration**

Pour mettre à jour votre installation :

1. **Remplacer le contenu de votre Gist** avec `gist_data_complete.json`
2. **Déployer** la nouvelle version sur Streamlit Cloud
3. **Tester** les nouvelles fonctionnalités

L'application détecte automatiquement l'ancienne structure et fonctionne en mode de compatibilité.

---

*Toutes ces améliorations ont été développées pour rendre TaskGame encore plus flexible et adapté aux besoins de votre colocation ! 🎯*