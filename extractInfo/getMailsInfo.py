#entry result: partie du resultat que contient que les infos de mail de la personne
#return infoMail: dictionary avec les informations de mail
def getMailsInfo(result):
    infoMail = dict()

    for email in result:
        type = email["type"]
        address = email["address"]

        infoMail[type] = address
    
    return infoMail