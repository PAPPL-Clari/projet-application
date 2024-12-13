#txt: entree du type json pour extraire les infos de contact de la personne
#return: string avec le type d'utilisateur
def getUtilisateurInfo(result):
    type = result["_embedded"]["type"]["name"]

    return type