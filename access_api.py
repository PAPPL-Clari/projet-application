from urllib.request import HTTPBasicAuthHandler
import requests
import config
import json

# Imprimir dans le terminal
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
       
# Base URL de la plataforme CNA
base_url = f"https://centraliens-nantes.org"

# ID de Guillaume GAUTIER
id = f"000078K"

#Query
#query = f"/api/v2/customer/profile/people/{id}"

query = "/api/v2/customer/profile/people"

# url complète avec l'autentication (2460 pags)

for pag in range (1, 246):
    url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}&page={pag}&limit=100"

    response = requests.get(url)
    if response.status_code == 200:
        resultat = response.json() 
        # jprint(result)
        print("Ok")
        '''
        # ID de l'utilisateur (ID school, ID étudiant...)	
        for i in range (len(resultat["_embedded"]["items"])):
            result = resultat["_embedded"]["items"][i]
            id_util = result["id"]
            schoool_ref = result["school_ref"]

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

            # Lieu de naissance	-- pas trouvé

            # addresse email personnelle	et étudiant
            mails = result["_embedded"]["emails"]
            for email in mails:
                if email["type"] == "primary":
                    mail_personnel = email        
                elif email["type"] == "secondary":
                    mail_etudiant = email

            # Type d'utilisateur	
            type = result["_embedded"]["type"]["name"]

            # addresse - Ligne 1	
            # addresse - Ligne 	
            # addresse - Ligne 	
            addresses = []
            for item in result["_embedded"]["address"]:
                if len(item["address"]) > 0:
                    addresses.append(item)

            # Code postal	
            # Ville	
            # État	
            # Pays
            # N'habite pas à l'addresse indiquée (NPAI)	
            zips = []	
            villes = []
            etats = []
            pays = []
            for address in addresses:
                if len(address["zip"]) != 0 and address["zip"] not in zips:
                    zips.append(address["zip"])
                if len(address["city"]) != 0 and address["city"] not in villes:
                    villes.append(address["city"])
                if len(address["region"]) != 0 and address["region"] not in etats:
                    etats.append(address["region"])
                if len(address["country_name"]) != 0 and address["country_name"] not in pays:
                    pays.append(address["country_name"])
                
            # Genre   
            gender = result["_embedded"]["civil"]["gender"]
            if ( gender == "0"):
                gender = "masculin"
            else: 
                gender = "feminin" 
                '''
    else:
        print(f"Erro: {response.status_code}")



'''
# DIPLOME

#typeDiplome = 
#refDiplome = 
#estDiplome = 
#dateIntegration = 
#dateDiplomation = 
#ecole = 
#paysEcole = 

#listeaddresses = result["_embedded"]["address"]
#for addresse in listeaddresses:
#    print(addresse)


#Recuperer les infos du diplome
query = f"/api/v2/customer/academic/member/{id}"
url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}"

response = requests.get(url)
if response.status_code == 200:
    result = response.json() 
    #jprint(result)
    print("Ok")
    # Type diplôme	
    # Diplôme CNA	
    # Programme AURION	
    # Diplôme obtenu	
    # Date intégration	
    # Date probable obtention diplôme	
    # Accord diffusion	
    # Ecole
else:
    print(f"Erro: {response.status_code}")'''