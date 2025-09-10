# Configuration GitHub Gist pour TaskGame

Ce guide vous explique comment configurer GitHub Gist pour sauvegarder les données de votre application TaskGame de manière persistante.

## Étape 1 : Créer un Personal Access Token GitHub

### 1.1 Accéder aux paramètres GitHub
1. Connectez-vous sur GitHub
2. Cliquez sur votre avatar en haut à droite
3. Allez dans **Settings** (Paramètres)
4. Dans le menu de gauche, cliquez sur **Developer settings**
5. Cliquez sur **Personal access tokens** → **Tokens (classic)**

### 1.2 Générer un nouveau token
1. Cliquez sur **Generate new token** → **Generate new token (classic)**
2. Remplissez les informations :
   - **Note** : `TaskGame Colocation - Gist Access`
   - **Expiration** : `No expiration` (ou selon votre préférence)
3. **Permissions requises** : Cochez uniquement `gist`
   ```
   ✅ gist (Create gists)
   ```
4. Cliquez sur **Generate token**
5. **IMPORTANT** : Copiez immédiatement le token et sauvegardez-le (il ne sera plus visible après)
   ```
   Format : ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

## Étape 2 : Créer un Gist pour les données

### 2.1 Créer le Gist
1. Allez sur https://gist.github.com/
2. Créez un nouveau Gist avec :
   - **Nom du fichier** : `colocation_data.json`
   - **Contenu** : (copiez le JSON ci-dessous)
   - **Type** : Sélectionnez **Secret gist** (privé)

### 2.2 Contenu initial du Gist
```json
{
  "colocataires": {
    "Antoine": {"points": 0},
    "Arthur": {"points": 0},
    "Raphael": {"points": 0},
    "Martin": {"points": 0},
    "Perrinne": {"points": 0}
  },
  "taches": {
    "Faire la vaisselle": {
      "points_base": 2, 
      "lieu": "Cuisine",
      "derniere_realisation": null,
      "points_actuels": 2
    },
    "Nettoyer le plan de travail": {
      "points_base": 1, 
      "lieu": "Cuisine",
      "derniere_realisation": null,
      "points_actuels": 1
    }
  },
  "created_at": "2025-01-10T12:00:00",
  "last_updated": "2025-01-10T12:00:00"
}
```

### 2.3 Récupérer l'ID du Gist
1. Après création, regardez l'URL de votre Gist
2. L'ID est la partie après votre nom d'utilisateur :
   ```
   https://gist.github.com/ArthurCFR/a1b2c3d4e5f6g7h8i9j0
                                    ^^^^^^^^^^^^^^^^^^^^
                                    Votre GIST_ID
   ```
3. Copiez cet ID (exemple : `a1b2c3d4e5f6g7h8i9j0`)

## Étape 3 : Configuration pour développement local

### 3.1 Créer le fichier de secrets
1. Dans votre projet, créez le fichier `.streamlit/secrets.toml` :
   ```bash
   mkdir -p .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Éditez `.streamlit/secrets.toml` avec vos vraies valeurs :
   ```toml
   # Votre token GitHub (étape 1)
   GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   
   # ID de votre Gist (étape 2)
   GIST_ID = "a1b2c3d4e5f6g7h8i9j0"
   ```

### 3.2 Ajouter au .gitignore
Créez ou modifiez `.gitignore` pour ne pas commit vos secrets :
```gitignore
.streamlit/secrets.toml
*.pyc
__pycache__/
.env
```

## Étape 4 : Configuration pour Streamlit Cloud

### 4.1 Déployer sur Streamlit Cloud
1. Allez sur https://share.streamlit.io
2. Connectez-vous avec GitHub
3. Cliquez sur **New app**
4. Sélectionnez votre repository : `ArthurCFR/portugoal`
5. Fichier principal : `app.py`
6. Branche : `main`

### 4.2 Configurer les secrets sur Streamlit Cloud
1. Dans la page de déploiement, cliquez sur **Advanced settings**
2. Dans la section **Secrets**, collez :
   ```toml
   GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   GIST_ID = "a1b2c3d4e5f6g7h8i9j0"
   ```
3. Cliquez sur **Deploy**

## Étape 5 : Vérification du fonctionnement

### 5.1 Test local
```bash
# Lancer l'app localement
streamlit run app.py
```
- Vous devriez voir : "✅ Données sauvegardées sur GitHub!" après chaque action
- Si erreur, vérifiez vos secrets dans `.streamlit/secrets.toml`

### 5.2 Test sur Streamlit Cloud
1. Attendez que le déploiement soit terminé
2. Ouvrez votre app déployée
3. Effectuez une action (compléter une tâche)
4. Vérifiez votre Gist sur GitHub - il devrait être mis à jour automatiquement

## Étape 6 : Maintenance et monitoring

### 6.1 Surveillance des données
- Votre Gist sera mis à jour à chaque modification dans l'app
- Vous pouvez consulter l'historique des modifications sur GitHub
- Les données sont automatiquement horodatées

### 6.2 Backup de sécurité
L'application sauvegarde aussi localement dans `colocation_data.json` en cas de problème avec GitHub.

### 6.3 Régénérer le token si nécessaire
Si votre token expire ou est compromis :
1. Générez un nouveau token (Étape 1)
2. Mettez à jour vos secrets localement et sur Streamlit Cloud
3. Redéployez si nécessaire

## Sécurité

⚠️ **Important** :
- Ne jamais commiter vos tokens dans le code
- Utilisez des Gists privés (secrets)
- Régénérez vos tokens régulièrement
- Limitez les permissions au strict nécessaire (`gist` uniquement)

## Dépannage

### Problème : "Impossible de charger depuis GitHub Gist"
- Vérifiez votre token GitHub
- Vérifiez l'ID du Gist
- Assurez-vous que le Gist contient bien `colocation_data.json`

### Problème : "Erreur lors de la sauvegarde sur GitHub"
- Vérifiez les permissions de votre token
- Le Gist existe-t-il toujours ?
- Y a-t-il des problèmes de réseau ?

### Problème : Secrets non reconnus sur Streamlit Cloud
- Vérifiez le format dans la section Advanced settings
- Redéployez l'application après modification des secrets
- Les secrets doivent être au format TOML exact

---

Avec cette configuration, vos données seront automatiquement sauvegardées et synchronisées entre tous les utilisateurs de votre application ! 🎮