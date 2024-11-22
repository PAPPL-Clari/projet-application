#txt: entree du type json pour extraire les infos pertinentes de la personne
#return: dictionary avec les infos de prenom, nom, id, school_ref, dateNaissance, nationalite
def getPersonneInfo(result):
    infosPersonnelles = dict()
    
    #Personne_id, school_ref
    id_util = result["id"]
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
        
    # Nom d'état-civil	
    nomNaissance = result["_embedded"]["civil"]["birthname"]

    # Date de naissance (jj/mm/aaaa)	
    dateNaissance = result["_embedded"]["civil"]["birthdate"]

    # Nationalité	
    nationalite = result["_embedded"]["civil"]["_embedded"]["nationality"]["name"]

    # Genre  -- NAO TEM NA DATABASE!! TERIA QUE ADICIONAR 
    gender = result["_embedded"]["civil"]["gender"]
    if ( gender == "0"):
        gender = "masculin"
    else: 
        gender = "feminin" 
                

    infosPersonnelles.update( id_personne = id_util, school_ref = school_ref, civilite = civil, prenom = prenom,
                             nom = nom, nomUsage = nomUsage, nomNaissance = nomNaissance, dateNaissance = dateNaissance,
                             nationalite = nationalite, gender = gender
                            )
    
    return infosPersonnelles