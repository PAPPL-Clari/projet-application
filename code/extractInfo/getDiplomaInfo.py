def getDiplomaInfo(result):
    """
    Faire l'extraction des informations de diplôme de la personne.

    :param result: Une chaîne au format JSON avec tous les informations de diplome.
    :return infosDiplomation: Dictionnaire python avec les infos de la reference diplôme, le nom du diplôme, le parcours,
    le nom de la specialisation, le nom de l'école, l'acronyme de pays de l'école, la date d'intégration,
    la date de diplomation et la donnée si l'étudiant est diplômé ou pas.
    """
    infosDiplomation = []

    listeDiplomes = result["_embedded"]["diplomas"]

    for i in range(len(listeDiplomes)):
        #infos diplome
        id_diplome = listeDiplomes[i]["id"]
        ref_diplome = listeDiplomes[i]["diploma_ref"]
        nom_diplome = listeDiplomes[i]["full_name"]
        parcours = listeDiplomes[i]["concentration"]

        nom_specialisation = listeDiplomes[i]["specialization"]

        nom_ecole = listeDiplomes[i]["school"]
        
        if "study_year" in  listeDiplomes[i]:
            acronyme_pays_ecole = listeDiplomes[i]["study_year"]
        else:
            acronyme_pays_ecole = ''
                    
        if "integration" in  listeDiplomes[i]:
            dateIntegration = listeDiplomes[i]["integration"]
        else:
            dateIntegration = ''
            
        if "graduation" in  listeDiplomes[i]:
            dateDiplomation = listeDiplomes[i]["graduation"]
        else:
            dateDiplomation = ''
        estDiplome = listeDiplomes[i]["is_graduated"]

        diploma = dict(id_diplome = id_diplome, ref_diplome = ref_diplome, nom_diplome = nom_diplome,
                       parcours = parcours, nom_specialisation = nom_specialisation, nom_ecole = nom_ecole,
                       acronyme_pays_ecole = acronyme_pays_ecole, dateIntegration = dateIntegration,
                       dateDiplomation = dateDiplomation, estDiplome = estDiplome)
        
        infosDiplomation.append(diploma)

    return infosDiplomation