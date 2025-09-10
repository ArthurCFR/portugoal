import streamlit as st
import json
import os
from datetime import datetime, timedelta
from gist_manager import GistManager

st.set_page_config(
    page_title="TaskGame - Colocation",
    page_icon="🏠",
    layout="wide"
)

DATA_FILE = "colocation_data.json"

def load_data():
    """Charge les données depuis GitHub Gist ou fichier local"""
    gist_manager = GistManager()
    
    # Essayer de charger depuis GitHub Gist d'abord
    if gist_manager.is_configured():
        data = gist_manager.load_data_from_gist()
        if data is not None:
            return data
        else:
            st.warning("⚠️ Impossible de charger depuis GitHub Gist, utilisation des données locales")
    
    # Fallback vers le fichier local
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return get_default_data()

def save_data(data):
    """Sauvegarde les données sur GitHub Gist et localement"""
    gist_manager = GistManager()
    
    # Sauvegarder sur GitHub Gist si configuré
    if gist_manager.is_configured():
        success = gist_manager.save_data_to_gist(data)
        if success:
            st.success("✅ Données sauvegardées sur GitHub!")
        else:
            st.error("❌ Erreur lors de la sauvegarde sur GitHub")
    
    # Sauvegarder localement aussi (backup)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def calculate_task_points(task_info):
    """Calcule les points actuels d'une tâche en fonction du temps écoulé"""
    points_base = task_info.get('points_base', task_info.get('points', 1))
    derniere_realisation = task_info.get('derniere_realisation')
    
    if derniere_realisation is None:
        # Tâche jamais réalisée, utiliser les points de base
        return points_base
    
    try:
        # Calculer les jours depuis la dernière réalisation
        derniere_date = datetime.fromisoformat(derniere_realisation)
        jours_ecoules = (datetime.now() - derniere_date).days
        
        # Incrémentation graduelle : +1 point tous les 7 jours, max 3 points bonus
        bonus = min(3, jours_ecoules // 7)
        return points_base + bonus
    
    except:
        # En cas d'erreur, utiliser les points de base
        return points_base

def update_task_points(data):
    """Met à jour les points actuels de toutes les tâches"""
    for tache_nom, tache_info in data['taches'].items():
        tache_info['points_actuels'] = calculate_task_points(tache_info)
    return data

def complete_task(data, user, task_name):
    """Marque une tâche comme terminée et attribue les points"""
    if task_name in data['taches']:
        points_gagnes = data['taches'][task_name]['points_actuels']
        data['colocataires'][user]['points'] += points_gagnes
        
        # Mettre à jour la date de dernière réalisation et qui l'a réalisée
        data['taches'][task_name]['derniere_realisation'] = datetime.now().isoformat()
        data['taches'][task_name]['derniere_realisation_par'] = user
        
        # Réinitialiser les points actuels aux points de base
        data['taches'][task_name]['points_actuels'] = data['taches'][task_name]['points_base']
        
        return points_gagnes
    return 0

def get_lieu_color(lieu):
    """Retourne la couleur associée à chaque lieu"""
    colors = {
        "Cuisine": "🟡",  # Jaune
        "Salon": "🟢",    # Vert
        "SDB 1er": "🔵",  # Bleu
        "SDB 2ème": "🟣", # Violet
        "RDC": "🟤",      # Marron
        "Garage": "⚫",   # Noir
        "Jardin": "🟢",   # Vert
        "Cour": "🟠",     # Orange
        "Général": "⚪"   # Blanc
    }
    return colors.get(lieu, "⚪")

def is_task_available_for_user(task_info, user):
    """Vérifie si une tâche est disponible pour un utilisateur"""
    return user in task_info.get('attribuee_a', [])

def get_default_data():
    """Retourne les données par défaut de l'application"""
    return {
        "colocataires": {
            "Antoine": {"points": 0},
            "Arthur": {"points": 0},
            "Raphael": {"points": 0},
            "Martin": {"points": 0},
            "Perrinne": {"points": 0}
        },
        "taches": {
            # Cuisine
            "Faire la vaisselle": {
                "points_base": 2, 
                "lieu": "Cuisine",
                "derniere_realisation": None,
                "points_actuels": 2,
                "attribuee_a": ["Antoine", "Arthur", "Raphael", "Martin", "Perrinne"],
                "derniere_realisation_par": None
            },
            "Nettoyer le plan de travail": {
                "points_base": 1, 
                "lieu": "Cuisine",
                "derniere_realisation": None,
                "points_actuels": 1,
                "attribuee_a": ["Antoine", "Arthur", "Raphael", "Martin", "Perrinne"],
                "derniere_realisation_par": None
            },
            "Nettoyer les plaques de cuisson": {"points_base": 2, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 2},
            "Nettoyer le four": {"points_base": 3, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 3},
            "Nettoyer le micro-ondes": {"points_base": 2, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 2},
            "Nettoyer le frigo (intérieur)": {"points_base": 3, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 3},
            "Nettoyer l'évier": {"points_base": 1, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 1},
            "Vider le lave-vaisselle": {"points_base": 1, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 1},
            "Sortir les poubelles": {"points_base": 1, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer la hotte": {"points_base": 2, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 2},
            "Ranger les courses": {"points_base": 1, "lieu": "Cuisine", "derniere_realisation": None, "points_actuels": 1},
            
            # Salon
            "Passer l'aspirateur salon": {"points_base": 2, "lieu": "Salon", "derniere_realisation": None, "points_actuels": 2},
            "Épousseter les meubles salon": {"points_base": 1, "lieu": "Salon", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer la table basse": {"points_base": 1, "lieu": "Salon", "derniere_realisation": None, "points_actuels": 1},
            "Ranger le salon": {"points_base": 1, "lieu": "Salon", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer les vitres salon": {"points_base": 2, "lieu": "Salon", "derniere_realisation": None, "points_actuels": 2},
            
            # Salle de bain 1er étage
            "Nettoyer les toilettes 1er": {"points_base": 2, "lieu": "SDB 1er", "derniere_realisation": None, "points_actuels": 2},
            "Nettoyer la douche 1er": {"points_base": 3, "lieu": "SDB 1er", "derniere_realisation": None, "points_actuels": 3},
            "Nettoyer le lavabo 1er": {"points_base": 1, "lieu": "SDB 1er", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer le miroir 1er": {"points_base": 1, "lieu": "SDB 1er", "derniere_realisation": None, "points_actuels": 1},
            "Passer la serpillière SDB 1er": {"points_base": 2, "lieu": "SDB 1er", "derniere_realisation": None, "points_actuels": 2},
            
            # Salle de bain 2ème étage
            "Nettoyer les toilettes 2ème": {"points_base": 2, "lieu": "SDB 2ème", "derniere_realisation": None, "points_actuels": 2},
            "Nettoyer la douche 2ème": {"points_base": 3, "lieu": "SDB 2ème", "derniere_realisation": None, "points_actuels": 3},
            "Nettoyer le lavabo 2ème": {"points_base": 1, "lieu": "SDB 2ème", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer le miroir 2ème": {"points_base": 1, "lieu": "SDB 2ème", "derniere_realisation": None, "points_actuels": 1},
            "Passer la serpillière SDB 2ème": {"points_base": 2, "lieu": "SDB 2ème", "derniere_realisation": None, "points_actuels": 2},
            
            # Rez-de-chaussée
            "Passer l'aspirateur escaliers": {"points_base": 2, "lieu": "RDC", "derniere_realisation": None, "points_actuels": 2},
            "Épousseter hall d'entrée": {"points_base": 1, "lieu": "RDC", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer les vitres RDC": {"points_base": 2, "lieu": "RDC", "derniere_realisation": None, "points_actuels": 2},
            "Passer la serpillière RDC": {"points_base": 2, "lieu": "RDC", "derniere_realisation": None, "points_actuels": 2},
            
            # Garage
            "Ranger le garage": {"points_base": 2, "lieu": "Garage", "derniere_realisation": None, "points_actuels": 2},
            "Balayer le garage": {"points_base": 1, "lieu": "Garage", "derniere_realisation": None, "points_actuels": 1},
            "Sortir les vélos": {"points_base": 1, "lieu": "Garage", "derniere_realisation": None, "points_actuels": 1},
            "Organiser les outils": {"points_base": 1, "lieu": "Garage", "derniere_realisation": None, "points_actuels": 1},
            
            # Jardin
            "Tondre la pelouse": {"points_base": 3, "lieu": "Jardin", "derniere_realisation": None, "points_actuels": 3},
            "Arroser les plantes": {"points_base": 1, "lieu": "Jardin", "derniere_realisation": None, "points_actuels": 1},
            "Désherber": {"points_base": 2, "lieu": "Jardin", "derniere_realisation": None, "points_actuels": 2},
            "Tailler les haies": {"points_base": 3, "lieu": "Jardin", "derniere_realisation": None, "points_actuels": 3},
            "Ramasser les feuilles": {"points_base": 2, "lieu": "Jardin", "derniere_realisation": None, "points_actuels": 2},
            "Nettoyer la terrasse": {"points_base": 2, "lieu": "Jardin", "derniere_realisation": None, "points_actuels": 2},
            
            # Cour d'entrée
            "Balayer la cour": {"points_base": 1, "lieu": "Cour", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer les marches": {"points_base": 1, "lieu": "Cour", "derniere_realisation": None, "points_actuels": 1},
            "Arroser les plantes cour": {"points_base": 1, "lieu": "Cour", "derniere_realisation": None, "points_actuels": 1},
            
            # Tâches générales
            "Changer les draps communs": {"points_base": 2, "lieu": "Général", "derniere_realisation": None, "points_actuels": 2},
            "Faire une lessive commune": {"points_base": 2, "lieu": "Général", "derniere_realisation": None, "points_actuels": 2},
            "Repasser le linge commun": {"points_base": 2, "lieu": "Général", "derniere_realisation": None, "points_actuels": 2},
            "Acheter produits ménagers": {"points_base": 1, "lieu": "Général", "derniere_realisation": None, "points_actuels": 1},
            "Remplacer ampoules grillées": {"points_base": 1, "lieu": "Général", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer radiateurs": {"points_base": 2, "lieu": "Général", "derniere_realisation": None, "points_actuels": 2},
            "Dépoussiérer plinthes": {"points_base": 1, "lieu": "Général", "derniere_realisation": None, "points_actuels": 1},
            "Nettoyer interrupteurs": {"points_base": 1, "lieu": "Général", "derniere_realisation": None, "points_actuels": 1}
        }
    }

def page_accueil():
    """Page d'accueil pour sélectionner le colocataire"""
    st.title("🏠 T'ES QUI ?")
    st.markdown("---")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    colocataires = ["Antoine", "Arthur", "Raphael", "Martin", "Perrinne"]
    
    for i, coloc in enumerate(colocataires):
        col = [col1, col2, col3, col4, col5][i]
        with col:
            if st.button(coloc, key=f"btn_{coloc}", use_container_width=True):
                st.session_state.current_user = coloc
                st.session_state.page = "dashboard"
                st.rerun()

def page_dashboard():
    """Dashboard principal avec les tâches ménagères"""
    data = load_data()
    
    # Mettre à jour les points des tâches au chargement
    data = update_task_points(data)
    
    user = st.session_state.current_user
    
    st.title(f"🎮 Dashboard - {user}")
    st.markdown(f"**Points actuels: {data['colocataires'][user]['points']}**")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🏆 Scores"):
            st.session_state.page = "scores"
            st.rerun()
        if st.button("⚙️ Paramètres"):
            st.session_state.page = "parametres"
            st.rerun()
    
    st.markdown("---")
    
    # Grouper les tâches par lieu
    taches_par_lieu = {}
    for tache, info in data['taches'].items():
        lieu = info['lieu']
        if lieu not in taches_par_lieu:
            taches_par_lieu[lieu] = []
        taches_par_lieu[lieu].append((tache, info))
    
    # Afficher les tâches par lieu avec couleurs
    for lieu, taches in taches_par_lieu.items():
        color_emoji = get_lieu_color(lieu)
        st.subheader(f"{color_emoji} {lieu}")
        cols = st.columns(2)
        
        for i, (tache, info) in enumerate(taches):
            col = cols[i % 2]
            with col:
                # Vérifier si la tâche est disponible pour l'utilisateur
                is_available = is_task_available_for_user(info, user)
                
                # Créer un container avec style conditionnel
                if is_available:
                    container = st.container()
                else:
                    # Tâche grisée pour utilisateur non autorisé
                    container = st.container()
                    with container:
                        st.markdown(f"<div style='opacity: 0.4; background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
                
                with container:
                    col_task, col_points, col_btn = st.columns([3, 1, 1])
                    
                    with col_task:
                        # Afficher le nom de la tâche
                        if is_available:
                            st.write(f"**{tache}**")
                        else:
                            st.write(f"~~{tache}~~ 🔒")
                        
                        # Afficher des informations sur la dernière réalisation
                        if info.get('derniere_realisation') and info.get('derniere_realisation_par'):
                            try:
                                derniere_date = datetime.fromisoformat(info['derniere_realisation'])
                                jours_ecoules = (datetime.now() - derniere_date).days
                                qui = info['derniere_realisation_par']
                                if jours_ecoules == 0:
                                    st.caption(f"👤 {qui} - Aujourd'hui")
                                elif jours_ecoules == 1:
                                    st.caption(f"👤 {qui} - Hier")
                                else:
                                    st.caption(f"👤 {qui} - Il y a {jours_ecoules} jours")
                            except:
                                pass
                        elif info.get('derniere_realisation'):
                            # Ancienne structure sans "qui"
                            try:
                                derniere_date = datetime.fromisoformat(info['derniere_realisation'])
                                jours_ecoules = (datetime.now() - derniere_date).days
                                if jours_ecoules > 0:
                                    st.caption(f"🕒 Il y a {jours_ecoules} jour(s)")
                            except:
                                pass
                    
                    with col_points:
                        points_actuels = info['points_actuels']
                        points_base = info.get('points_base', info.get('points', 1))
                        
                        if points_actuels > points_base:
                            # Tâche avec bonus
                            st.write(f"**{points_actuels} pts** ⚡")
                            st.caption(f"(base: {points_base})")
                        else:
                            st.write(f"**{points_actuels} pts**")
                    
                    with col_btn:
                        if is_available:
                            if st.button("✓", key=f"task_{tache}"):
                                if st.session_state.get(f"confirm_{tache}"):
                                    # Confirmer la tâche
                                    points_gagnes = complete_task(data, user, tache)
                                    save_data(data)
                                    st.success(f"+{points_gagnes} points!")
                                    del st.session_state[f"confirm_{tache}"]
                                    st.rerun()
                                else:
                                    st.session_state[f"confirm_{tache}"] = True
                                    st.rerun()
                        else:
                            st.write("🚫")
                    
                    # Afficher la confirmation si nécessaire
                    if is_available and st.session_state.get(f"confirm_{tache}"):
                        st.write("**C'est fait ?**")
                        col_oui, col_non = st.columns(2)
                        with col_oui:
                            if st.button("Oui", key=f"oui_{tache}"):
                                points_gagnes = complete_task(data, user, tache)
                                save_data(data)
                                st.success(f"+{points_gagnes} points!")
                                del st.session_state[f"confirm_{tache}"]
                                st.rerun()
                        with col_non:
                            if st.button("Non", key=f"non_{tache}"):
                                del st.session_state[f"confirm_{tache}"]
                                st.rerun()
                
                if not is_available:
                    st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")

def page_scores():
    """Page des scores/classement"""
    data = load_data()
    
    st.title("🏆 Tableau des Scores")
    
    if st.button("← Retour"):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.markdown("---")
    
    # Trier les colocataires par points
    scores = [(nom, info['points']) for nom, info in data['colocataires'].items()]
    scores.sort(key=lambda x: x[1], reverse=True)
    
    st.subheader("🥇 Classement")
    
    for i, (nom, points) in enumerate(scores, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
        st.write(f"{emoji} **{i}. {nom}**: {points} points")

def page_parametres():
    """Page de paramètres pour gérer tâches et colocataires"""
    data = load_data()
    
    st.title("⚙️ Paramètres")
    
    if st.button("← Retour"):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.markdown("---")
    
    # Onglets pour différentes sections
    tab1, tab2, tab3 = st.tabs(["Tâches", "Colocataires", "Reset"])
    
    with tab1:
        st.subheader("Gestion des Tâches")
        
        # Ajouter une tâche
        st.write("**Ajouter une nouvelle tâche:**")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            new_task = st.text_input("Nom de la tâche")
        with col2:
            new_points = st.number_input("Points", min_value=1, max_value=3, value=1)
        with col3:
            new_lieu = st.selectbox("Lieu", ["Cuisine", "Salon", "SDB 1er", "SDB 2ème", "RDC", "Garage", "Jardin", "Cour", "Général"])
        
        if st.button("Ajouter tâche") and new_task:
            data['taches'][new_task] = {
                "points_base": new_points,
                "lieu": new_lieu,
                "derniere_realisation": None,
                "points_actuels": new_points,
                "attribuee_a": ["Antoine", "Arthur", "Raphael", "Martin", "Perrinne"],
                "derniere_realisation_par": None
            }
            save_data(data)
            st.success("Tâche ajoutée!")
            st.rerun()
        
        st.markdown("---")
        
        # Modifier/supprimer tâches existantes
        st.write("**Modifier/Supprimer des tâches:**")
        
        # Interface de modification
        if 'editing_task' not in st.session_state:
            st.session_state.editing_task = None
        
        for tache, info in data['taches'].items():
            # Affichage normal ou mode édition
            if st.session_state.editing_task == tache:
                # Mode édition
                st.write(f"**Édition: {tache}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_points_base = st.number_input("Points de base", 
                                                     min_value=1, max_value=3, 
                                                     value=info.get('points_base', info.get('points', 1)),
                                                     key=f"edit_points_{tache}")
                with col2:
                    new_lieu = st.selectbox("Lieu", 
                                          ["Cuisine", "Salon", "SDB 1er", "SDB 2ème", "RDC", "Garage", "Jardin", "Cour", "Général"],
                                          index=["Cuisine", "Salon", "SDB 1er", "SDB 2ème", "RDC", "Garage", "Jardin", "Cour", "Général"].index(info['lieu']) if info['lieu'] in ["Cuisine", "Salon", "SDB 1er", "SDB 2ème", "RDC", "Garage", "Jardin", "Cour", "Général"] else 0,
                                          key=f"edit_lieu_{tache}")
                with col3:
                    st.write("**Attribuée à:**")
                    colocataires_actuels = info.get('attribuee_a', [])
                    new_attribution = {}
                    for coloc in ["Antoine", "Arthur", "Raphael", "Martin", "Perrinne"]:
                        new_attribution[coloc] = st.checkbox(coloc, 
                                                            value=coloc in colocataires_actuels,
                                                            key=f"edit_attr_{tache}_{coloc}")
                
                # Boutons d'action
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("💾 Sauvegarder", key=f"save_{tache}"):
                        # Mettre à jour la tâche
                        data['taches'][tache]['points_base'] = new_points_base
                        data['taches'][tache]['lieu'] = new_lieu
                        data['taches'][tache]['attribuee_a'] = [coloc for coloc, selected in new_attribution.items() if selected]
                        
                        # Recalculer les points actuels
                        data['taches'][tache]['points_actuels'] = calculate_task_points(data['taches'][tache])
                        
                        save_data(data)
                        st.session_state.editing_task = None
                        st.success("Tâche modifiée!")
                        st.rerun()
                
                with col_cancel:
                    if st.button("❌ Annuler", key=f"cancel_{tache}"):
                        st.session_state.editing_task = None
                        st.rerun()
                        
                st.markdown("---")
            
            else:
                # Affichage normal
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                with col1:
                    color_emoji = get_lieu_color(info['lieu'])
                    st.write(f"{color_emoji} **{tache}**")
                    
                    # Afficher qui peut faire cette tâche
                    attribuee_a = info.get('attribuee_a', [])
                    if len(attribuee_a) < 5:
                        st.caption(f"👥 {', '.join(attribuee_a)}")
                    
                    # Afficher la date de dernière réalisation si elle existe
                    if info.get('derniere_realisation') and info.get('derniere_realisation_par'):
                        try:
                            date = datetime.fromisoformat(info['derniere_realisation'])
                            qui = info['derniere_realisation_par']
                            st.caption(f"👤 {qui} - {date.strftime('%d/%m/%Y')}")
                        except:
                            pass
                    elif info.get('derniere_realisation'):
                        try:
                            date = datetime.fromisoformat(info['derniere_realisation'])
                            st.caption(f"Dernière: {date.strftime('%d/%m/%Y')}")
                        except:
                            pass
                
                with col2:
                    points_base = info.get('points_base', info.get('points', 1))
                    points_actuels = info.get('points_actuels', points_base)
                    
                    if points_actuels > points_base:
                        st.write(f"**{points_actuels} pts** ⚡")
                        st.caption(f"(base: {points_base})")
                    else:
                        st.write(f"**{points_base} pts**")
                
                with col3:
                    st.write(info['lieu'])
                
                with col4:
                    if st.button("✏️", key=f"edit_{tache}", help="Modifier"):
                        st.session_state.editing_task = tache
                        st.rerun()
                
                with col5:
                    if st.button("🗑️", key=f"del_{tache}", help="Supprimer"):
                        del data['taches'][tache]
                        save_data(data)
                        st.rerun()
    
    with tab2:
        st.subheader("Gestion des Colocataires")
        
        # Ajouter un colocataire
        st.write("**Ajouter un nouveau colocataire:**")
        new_coloc = st.text_input("Nom du colocataire")
        if st.button("Ajouter colocataire") and new_coloc:
            data['colocataires'][new_coloc] = {"points": 0}
            save_data(data)
            st.success("Colocataire ajouté!")
            st.rerun()
        
        st.markdown("---")
        
        # Liste des colocataires
        st.write("**Colocataires actuels:**")
        for nom, info in data['colocataires'].items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(nom)
            with col2:
                st.write(f"{info['points']} pts")
            with col3:
                if st.button("🗑️", key=f"del_coloc_{nom}"):
                    if len(data['colocataires']) > 1:
                        del data['colocataires'][nom]
                        save_data(data)
                        st.rerun()
                    else:
                        st.error("Impossible de supprimer le dernier colocataire!")
    
    with tab3:
        st.subheader("Remise à zéro")
        st.write("**Attention: Ces actions sont irréversibles!**")
        
        if st.button("🔄 Remettre tous les scores à zéro"):
            for nom in data['colocataires']:
                data['colocataires'][nom]['points'] = 0
            save_data(data)
            st.success("Scores remis à zéro!")
            st.rerun()
        
        if st.button("🔄 Réinitialiser toute l'application"):
            data = get_default_data()
            save_data(data)
            st.success("Application réinitialisée!")
            st.rerun()

def main():
    # Initialisation des variables de session
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'page' not in st.session_state:
        st.session_state.page = "accueil"
    
    # Navigation entre les pages
    if st.session_state.page == "accueil" or st.session_state.current_user is None:
        page_accueil()
    elif st.session_state.page == "dashboard":
        page_dashboard()
    elif st.session_state.page == "scores":
        page_scores()
    elif st.session_state.page == "parametres":
        page_parametres()

if __name__ == "__main__":
    main()