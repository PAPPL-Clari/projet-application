def getMailsInfo(result):
    """
    Faire l'extraction des informations d'adresse postal de la personne.

    :param result: Une chaîne au format JSON qui contient les informations de mail de la personne
    :return infoMail: Dictionnaire python avec les infos du type d'adresse mail et le l'adresse mail lui même
    """
    infoMail = dict()

    for mail in result:
        type = mail["type"]
        address = mail["address"]
        infoMail[type] = address
    
    return infoMail