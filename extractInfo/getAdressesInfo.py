def getAdressesInfo(result):
    infoAddresse = dict()
    coordonnees = dict()

    #print(result)

    for address in result:
        #print(address)

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