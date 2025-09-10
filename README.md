# TaskGame - Colocation 🏠

Application Streamlit de gamification des tâches ménagères pour votre colocation.

## Fonctionnalités

- **Page d'accueil** : Sélection des colocataires (Antoine, Arthur, Raphael, Martin, Perrinne)
- **Dashboard principal** : Liste de ~50 tâches ménagères organisées par lieu
- **Système de points** : Chaque tâche rapporte 1-3 points avec incrémentation automatique
- **Tableau des scores** : Classement dynamique des colocataires
- **Page paramètres** : Gestion des tâches et colocataires
- **Stockage persistent** : Données sauvegardées sur GitHub Gist
- **Incrémentation des points** : +1 point tous les 7 jours pour les tâches non réalisées (max +3)

## Structure des lieux

L'application couvre tous les espaces de votre maison :
- **Cuisine** : vaisselle, plans de travail, électroménager, etc.
- **Salon** : aspirateur, dépoussiérage, rangement
- **SDB 1er étage** : toilettes, douche, lavabo, miroir, sol
- **SDB 2ème étage** : toilettes, douche, lavabo, miroir, sol  
- **Rez-de-chaussée** : escaliers, hall d'entrée, vitres
- **Garage** : rangement, balayage, organisation
- **Jardin** : pelouse, arrosage, désherbage, haies
- **Cour d'entrée** : balayage, marches, plantes
- **Tâches générales** : lessive, produits ménagers, ampoules

## Installation locale

```bash
# Cloner le projet
git clone <votre-repo>
cd taskgame-colocation

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## Déploiement sur Streamlit Cloud

### 1. Préparation du repository

1. Créez un repository GitHub avec ces fichiers :
   - `app.py` (application principale)
   - `gist_manager.py` (gestionnaire GitHub Gist)
   - `requirements.txt` (dépendances)
   - `README.md` (cette documentation)

### 2. Configuration des secrets

Pour que l'application fonctionne sur Streamlit Cloud, vous devez configurer les secrets :

1. **Créer un GitHub Personal Access Token** :
   - Allez sur GitHub → Settings → Developer settings → Personal access tokens
   - Créez un token avec les permissions "gist"
   - Copiez le token

2. **Créer un Gist pour stocker les données** :
   - Allez sur https://gist.github.com/
   - Créez un nouveau Gist privé
   - Nommez le fichier `colocation_data.json`
   - Copiez l'ID du Gist depuis l'URL (ex: `https://gist.github.com/username/GIST_ID`)

3. **Configurer les secrets sur Streamlit Cloud** :
   ```toml
   # .streamlit/secrets.toml (pour le développement local)
   GITHUB_TOKEN = "ghp_votre_token_ici"
   GIST_ID = "votre_gist_id_ici"
   ```

   Sur Streamlit Cloud, ajoutez ces secrets dans l'interface de déploiement.

### 3. Déploiement

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez votre compte GitHub
3. Sélectionnez votre repository
4. Définissez `app.py` comme fichier principal
5. Ajoutez vos secrets dans la section "Advanced settings"
6. Déployez !

## Structure des données

### Format des tâches
```json
{
  "nom_tache": {
    "points_base": 2,
    "lieu": "Cuisine",
    "derniere_realisation": "2025-01-10T15:30:00",
    "points_actuels": 3
  }
}
```

### Calcul des points bonus
- Points de base : définis lors de la création (1-3 points)
- Bonus : +1 point tous les 7 jours sans réalisation
- Maximum : +3 points de bonus
- Reset : les points reviennent à la base après réalisation

## Utilisation

1. **Page d'accueil** : Cliquez sur votre prénom
2. **Dashboard** : 
   - Consultez les tâches par lieu
   - Voyez les points actuels (avec ⚡ pour les bonus)
   - Cliquez sur ✓ pour réaliser une tâche
   - Confirmez avec "Oui" pour gagner les points
3. **Scores** : Consultez le classement général
4. **Paramètres** : Ajoutez/supprimez des tâches et colocataires

## Support technique

En cas de problème :
- Vérifiez que vos secrets GitHub sont correctement configurés
- Consultez les logs de Streamlit Cloud
- Les données sont automatiquement sauvegardées sur GitHub Gist

## Développements futurs

L'application est préparée pour :
- Ajout de nouvelles fonctionnalités de gamification
- Système de récompenses
- Notifications personnalisées
- Statistiques avancées

---

*Application créée pour gamifier les tâches ménagères en colocation ! 🎮*