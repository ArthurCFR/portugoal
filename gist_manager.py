import requests
import json
import streamlit as st
from datetime import datetime

class GistManager:
    """Gestionnaire pour sauvegarder/charger les données via GitHub Gist"""
    
    def __init__(self):
        # Configuration via les secrets Streamlit Cloud
        self.github_token = st.secrets.get("GITHUB_TOKEN", None)
        self.gist_id = st.secrets.get("GIST_ID", None)
        self.headers = {
            'Authorization': f'token {self.github_token}' if self.github_token else None,
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def is_configured(self):
        """Vérifie si la configuration GitHub est disponible"""
        return self.github_token is not None and self.gist_id is not None
    
    def load_data_from_gist(self):
        """Charge les données depuis le Gist GitHub"""
        if not self.is_configured():
            return None
        
        try:
            url = f"https://api.github.com/gists/{self.gist_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                gist_data = response.json()
                # Le fichier principal est "colocation_data.json"
                if "colocation_data.json" in gist_data["files"]:
                    content = gist_data["files"]["colocation_data.json"]["content"]
                    return json.loads(content)
            else:
                st.error(f"Erreur lors du chargement du Gist: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Erreur lors du chargement depuis GitHub: {str(e)}")
            return None
    
    def save_data_to_gist(self, data):
        """Sauvegarde les données sur le Gist GitHub"""
        if not self.is_configured():
            return False
        
        try:
            url = f"https://api.github.com/gists/{self.gist_id}"
            
            # Ajouter un timestamp de dernière mise à jour
            data["last_updated"] = datetime.now().isoformat()
            
            payload = {
                "files": {
                    "colocation_data.json": {
                        "content": json.dumps(data, indent=2, ensure_ascii=False)
                    }
                },
                "description": "Données TaskGame Colocation - Mise à jour automatique"
            }
            
            response = requests.patch(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return True
            else:
                st.error(f"Erreur lors de la sauvegarde: {response.status_code}")
                return False
                
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde sur GitHub: {str(e)}")
            return False
    
    def create_initial_gist(self, data):
        """Crée le Gist initial (à utiliser une seule fois)"""
        if not self.github_token:
            return None
        
        try:
            url = "https://api.github.com/gists"
            
            data["last_updated"] = datetime.now().isoformat()
            data["created_at"] = datetime.now().isoformat()
            
            payload = {
                "description": "TaskGame Colocation - Données persistantes",
                "public": False,
                "files": {
                    "colocation_data.json": {
                        "content": json.dumps(data, indent=2, ensure_ascii=False)
                    },
                    "README.md": {
                        "content": "# TaskGame Colocation\n\nDonnées persistantes pour l'application de gamification des tâches ménagères.\n\n**Ne pas modifier ce fichier manuellement !**"
                    }
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 201:
                gist_data = response.json()
                return gist_data["id"]
            else:
                st.error(f"Erreur lors de la création du Gist: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Erreur lors de la création du Gist: {str(e)}")
            return None