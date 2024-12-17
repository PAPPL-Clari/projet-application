#txt: entree du type json pour extraire les infos de adresse de la personne
#return: dictionary avec les infos d'adresse, ville, code postal, pays 
#et NPAI (n'habite pas à l'adresse indiqué)

def getAdressesInfo(result):
    infoAddresse = dict()
    coordonnees = dict()

    for address in result:

        if "address" in address:
            adresse1 = address['address']
        else:
            adresse1 = ""
    
        if "address_2" in address:
            adresse2 = address["address_2"]
        else:
            adresse2 = ""
        
        if "address_3" in address:
            adresse3 = address["address_3"]
        else:
            adresse3 = ""
        
        if "address_4" in address:
            adresse4 = address["address_4"]
        else:
            adresse4 = ""

        if "city" in address:
            ville = address["city"]
        else:
            ville = ""

        if "country_name" in address:
            nomPays = address["country_name"]
        else:
            nomPays = ""
        
        if "zip" in address:
            codePostal = address["zip"]
        else:
            codePostal=""
        
        type_adresse = address["type"]
        npai = address["npai"]

        coordonnees = { "adresse_1": adresse1,
                       "adresse_2":adresse2,
                       "adresse_3":adresse3,
                       "adresse_4":adresse4,
                       "ville": ville,
                       "code_postal": codePostal,
                       "nomPays": nomPays,
                       "npai": npai}
        
        infoAddresse.update({type_adresse: coordonnees})

    return infoAddresse