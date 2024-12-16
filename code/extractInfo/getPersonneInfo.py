#txt: entree du type json pour extraire les infos pertinentes de la personne
#return: dictionary avec les infos de prenom, nom, id, school_ref, dateNaissance, nationalite (acronyme)
def getPersonneInfo(result):
    infosPersonnelles = dict()
    
    #Personne_id, school_ref
    id_util = result["id"]

    school_ref = ""
    if "school_ref" in result:
        school_ref = result["school_ref"]

    # Civilité	
    civil = result["_embedded"]["civil"]["_embedded"]["civility"]["name"]

    # Prénom	
    prenom = result["_embedded"]["civil"]["firstname"]

    # Nom d'usage ou marital
    nom = result["_embedded"]["civil"]["lastname"]
    nomUsage = result["_embedded"]["civil"]["name_used"]
    if ( nomUsage == "lastname"):
        nomUsage = nom
        
    # Date de naissance (aaaa-mm-dd)	
    dateNaissance = ""
    if "birthdate" in result["_embedded"]["civil"]:
        dateNaissance = result["_embedded"]["civil"]["birthdate"]

    # Nationalité (nom du pays)
    nationalite = ""
    if "nationality" in result["_embedded"]["civil"]:
        nationalite = result["_embedded"]["civil"]["_embedded"]["nationality"]["name"] # Country name, not acronym

    # Genre 
    genre = result["_embedded"]["civil"]["gender"]
    if ( genre == "0"):
        genre = "masculin"
    else: 
        genre = "feminin" 

    # Ville 
    ville = result["_embedded"]["address"][0]["city"]   
    
    # Type d'utilisateur
    nom_type_utilisateur = result["_embedded"]["type"]["name"]

    # Email -- not everyone has one, fix this
    if "username" in result:
        mail = result["username"]
    else:
        mail = result["_embedded"]["emails"][0]["address"]

    infosPersonnelles.update( id_personne = id_util, school_ref = school_ref, civilite = civil, prenom = prenom,
                             nom = nom, nomUsage = nomUsage, dateNaissance = dateNaissance,
                             nationalite = nationalite, genre = genre, ville = ville, nom_type_utilisateur = nom_type_utilisateur, mail = mail
                            )
    
    return infosPersonnelles