#txt: entree du type json pour extraire les infos pertinentes de la personne
#return: liste composé des dictionnaires qui contient les informations de chaque diplome 
#de l'individu: id, ref, nom du diplome, parcours, specialisation, nom ecole, pays ecole
def getDiplomaInfo(result):
    infosDiplomation = []

    listeDiplomes = result["_embedded"]["diplomas"]

    for i in range(len(listeDiplomes)):
        #infos diplome
        id_diplome = listeDiplomes[i]["id"]
        ref_diplome = listeDiplomes[i]["diploma_ref"]
        nom_diplome = listeDiplomes[i]["full_name"]
        parcours = listeDiplomes[i]["concentration"]

        #infos specialisation
        #id_specialisation =
        nom_specialisation = listeDiplomes[i]["specialization"]

        #Infos de l'ecole
        #id_ecole
        nom_ecole = listeDiplomes[i]["school"]
        acronyme_pays_ecole = listeDiplomes[i]["study_year"]

        dateIntegration = listeDiplomes[i]["integration"]
        dateDiplomation = listeDiplomes[i]["graduation"]
        estDiplome = listeDiplomes[i]["is_graduated"]

        diploma = dict(id_diplome = id_diplome, ref_diplome = ref_diplome, nom_diplome = nom_diplome,
                       parcours = parcours, nom_specialisation = nom_specialisation, nom_ecole = nom_ecole,
                       acronyme_pays_ecole = acronyme_pays_ecole, dateIntegration = dateIntegration,
                       dateDiplomation = dateDiplomation, estDiplome = estDiplome)
        
        infosDiplomation.append(diploma)

    return infosDiplomation