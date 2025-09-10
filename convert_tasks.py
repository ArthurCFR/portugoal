"""Script pour convertir rapidement toutes les tâches à la nouvelle structure"""

def convert_old_to_new_format():
    old_tasks = {
        # Salon
        "Passer l'aspirateur salon": {"points": 2, "lieu": "Salon"},
        "Épousseter les meubles salon": {"points": 1, "lieu": "Salon"},
        "Nettoyer la table basse": {"points": 1, "lieu": "Salon"},
        "Ranger le salon": {"points": 1, "lieu": "Salon"},
        "Nettoyer les vitres salon": {"points": 2, "lieu": "Salon"},
        
        # Salle de bain 1er étage
        "Nettoyer les toilettes 1er": {"points": 2, "lieu": "SDB 1er"},
        "Nettoyer la douche 1er": {"points": 3, "lieu": "SDB 1er"},
        "Nettoyer le lavabo 1er": {"points": 1, "lieu": "SDB 1er"},
        "Nettoyer le miroir 1er": {"points": 1, "lieu": "SDB 1er"},
        "Passer la serpillière SDB 1er": {"points": 2, "lieu": "SDB 1er"},
        
        # Salle de bain 2ème étage
        "Nettoyer les toilettes 2ème": {"points": 2, "lieu": "SDB 2ème"},
        "Nettoyer la douche 2ème": {"points": 3, "lieu": "SDB 2ème"},
        "Nettoyer le lavabo 2ème": {"points": 1, "lieu": "SDB 2ème"},
        "Nettoyer le miroir 2ème": {"points": 1, "lieu": "SDB 2ème"},
        "Passer la serpillière SDB 2ème": {"points": 2, "lieu": "SDB 2ème"},
        
        # Rez-de-chaussée
        "Passer l'aspirateur escaliers": {"points": 2, "lieu": "RDC"},
        "Épousseter hall d'entrée": {"points": 1, "lieu": "RDC"},
        "Nettoyer les vitres RDC": {"points": 2, "lieu": "RDC"},
        "Passer la serpillière RDC": {"points": 2, "lieu": "RDC"},
        
        # Garage
        "Ranger le garage": {"points": 2, "lieu": "Garage"},
        "Balayer le garage": {"points": 1, "lieu": "Garage"},
        "Sortir les vélos": {"points": 1, "lieu": "Garage"},
        "Organiser les outils": {"points": 1, "lieu": "Garage"},
        
        # Jardin
        "Tondre la pelouse": {"points": 3, "lieu": "Jardin"},
        "Arroser les plantes": {"points": 1, "lieu": "Jardin"},
        "Désherber": {"points": 2, "lieu": "Jardin"},
        "Tailler les haies": {"points": 3, "lieu": "Jardin"},
        "Ramasser les feuilles": {"points": 2, "lieu": "Jardin"},
        "Nettoyer la terrasse": {"points": 2, "lieu": "Jardin"},
        
        # Cour d'entrée
        "Balayer la cour": {"points": 1, "lieu": "Cour"},
        "Nettoyer les marches": {"points": 1, "lieu": "Cour"},
        "Arroser les plantes cour": {"points": 1, "lieu": "Cour"},
        
        # Tâches générales
        "Changer les draps communs": {"points": 2, "lieu": "Général"},
        "Faire une lessive commune": {"points": 2, "lieu": "Général"},
        "Repasser le linge commun": {"points": 2, "lieu": "Général"},
        "Acheter produits ménagers": {"points": 1, "lieu": "Général"},
        "Remplacer ampoules grillées": {"points": 1, "lieu": "Général"},
        "Nettoyer radiateurs": {"points": 2, "lieu": "Général"},
        "Dépoussiérer plinthes": {"points": 1, "lieu": "Général"},
        "Nettoyer interrupteurs": {"points": 1, "lieu": "Général"}
    }
    
    converted_tasks = {}
    for name, info in old_tasks.items():
        converted_tasks[name] = {
            "points_base": info["points"],
            "lieu": info["lieu"],
            "derniere_realisation": None,
            "points_actuels": info["points"]
        }
    
    # Imprimer le résultat formaté
    for name, info in converted_tasks.items():
        print(f'            "{name}": {info},')

if __name__ == "__main__":
    convert_old_to_new_format()