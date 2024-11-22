#Ajoute les donnees de resultat dans la database
def addDatabase(resultat):
    
    getDiplomaInfo(resultat)
    infosPersonnelles = getPersonneInfo(resultat)
    databasePush(infosCarriere, infosPersonnelles)