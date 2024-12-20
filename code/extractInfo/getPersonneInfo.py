from extractInfo.format import format_str

def getPersonneInfo(result):
    """
    Faire l'extraction des informations de civilité de la personne.

    :param result: Une chaîne au format JSON
    :return infosPersonnelles: Dictionnaire python avec les infos de la personne: nom, prénom, nom d'usage, id,
    school_ref, date de Naissance, nationalité, ville, date de la dernière modification,
    type d'utilisateur et son adresse mail.
    """
    infosPersonnelles = dict()
    
    #Personne_id, school_ref
    id_util = result["id"]

    school_ref = "NULL"
    if "school_ref" in result:
        school_ref = result["school_ref"]
        school_ref = format_str(school_ref)

    # Civilité	
    civil = result["_embedded"]["civil"]["_embedded"]["civility"]["name"]
    civil = format_str(civil)

    # Prénom	
    prenom = result["_embedded"]["civil"]["firstname"]
    prenom = format_str(prenom)

    # Nom d'usage ou marital
    nom = result["_embedded"]["civil"]["lastname"]
    nom = format_str(nom)
    nomUsage = result["_embedded"]["civil"]["name_used"]
    if ( nomUsage == "lastname"):
        nomUsage = nom

    # Date de naissance (aaaa-mm-dd)	
    dateNaissance = "NULL"
    if "birthdate" in result["_embedded"]["civil"]:
        dateNaissance = result["_embedded"]["civil"]["birthdate"]
        dateNaissance = format_str(dateNaissance)

    # Nationalité (nom du pays)
    nationalite = "NULL"
    if "nationality" in result["_embedded"]["civil"]["_embedded"]:
        nationalite = result["_embedded"]["civil"]["_embedded"]["nationality"]["name"] # Country name, not acronym
        nationalite = format_str(nationalite)

    # Ville 
    ville = "NULL"
    if 'city' in result["_embedded"]["address"][0]:
        ville = result["_embedded"]["address"][0]["city"]   
        ville = format_str(ville)

    # Type d'utilisateur
    nom_type_utilisateur = result["_embedded"]["type"]["name"]
    nom_type_utilisateur = "'" + nom_type_utilisateur + "'"

    # Date de la dernière mise a jour
    mise_a_jour = "NULL"
    if "updated" in result:
        mise_a_jour = result["updated"]
        # Séparer date et timestamp
        mise_a_jour = mise_a_jour.split()
        # Prendre que la date
        mise_a_jour = mise_a_jour[0]
        mise_a_jour = format_str(mise_a_jour)

    # Email 
    mail = "NULL"
    if "emails" in result["_embedded"]:
        mail = result["_embedded"]["emails"][0]["address"]
        mail = format_str(mail)
        
    infosPersonnelles.update( id_personne = id_util, school_ref = school_ref, civilite = civil, prenom = prenom,
                             nom = nom, nomUsage = nomUsage, dateNaissance = dateNaissance,
                             nationalite = nationalite, ville = ville, nom_type_utilisateur = nom_type_utilisateur, 
                             mail = mail, miseAJour = mise_a_jour
                            )
    
    return infosPersonnelles