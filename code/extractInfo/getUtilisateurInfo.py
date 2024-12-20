def getUtilisateurInfo(result):
    """
    Faire l'extraction des informations d'adresse postal de la personne.

    :param result: Une chaîne au format JSON avec tous les informations personnelles.
    :return type: String avec le type d'utilisateur: Staff, Diplomé, Membre externe, Enseignant ou Personnel, Étudiant ou Membre associé. 
    """
    type = result["_embedded"]["type"]["name"]

    return type