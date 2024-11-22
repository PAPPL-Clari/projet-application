import getMailsInfo
import getAdressesInfo

#txt: entree du type json pour extraire les infos de contact de la personne
#return: dictionary avec les infos de mail et addresse dans cet ordre
def getContactInfo(result):
    
    infoMail = getMailsInfo.getMailsInfo(result["_embedded"]["emails"])
    infoAddresse = getAdressesInfo.getAdressesInfo(result["_embedded"]["adress"])

    return infoMail, infoAddresse