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
query = f"/api/v2/customer/social/group/"
#query = f"/api/v2/customer/academic/member/{id}"

# url complète avec l'autentication
url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}"

response = requests.get(url)
if response.status_code == 200:
    result = response.json() 
    jprint(result)
    print("Ok")
else:
    print(f"Erro: {response.status_code}")

'''
#print(response.json()["display_name"])

addresse = result["_embedded"]["address"]
#schoolRef = 
civil = result["_embedded"]["civil"]["_embedded"]["civility"]["name"]
prenom = result["_embedded"]["civil"]["firstname"]
nom = result["_embedded"]["civil"]["lastname"]
nomNaissance = result["_embedded"]["civil"]["birthname"]
dateNaissance = result["_embedded"]["civil"]["birthdate"]
nationalite = result["_embedded"]["civil"]["_embedded"]["nationality"]["name"]

gender = result["_embedded"]["civil"]["gender"]
if ( gender == "0"):
    gender = "masculin"
else: 
    gender = "feminin" 

nomUsage = result["_embedded"]["civil"]["name_used"]
if ( nomUsage == "lastname"):
    nomUsage = nom

#lieuNaissance = 
emailPerso = result["_embedded"]["emails"][0]
adresses = dict()
adressePerso = {"AdresseLigne1" : "",
                  "AddresseLigne2" : "",
                 "AddresseLigne3" : "",
                 "CodePostal" : 0,
                 "Ville" : "",
                 "Etat" : "",
                 "Pays" : "",
                 "NPAI" : 0} 
#emailEtudiant = 

#typeDiplome = 
#refDiplome = 
#estDiplome = 
#dateIntegration = 
#dateDiplomation = 
#ecole = 
#paysEcole = 

#listeAdresses = result["_embedded"]["address"]
#for adresse in listeAdresses:
#    print(adresse)

print(civil, prenom, nom, nomNaissance, dateNaissance, nationalite, gender, nomUsage, emailPerso, adressePerso)

#Recuperer les infos du diplome
query = f"/api/v2/customer/academic/member/{id}"
url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}"

response = requests.get(url)
if response.status_code == 200:
    result = response.json() 
    jprint(result)
    print("Ok")
else:
    print(f"Erro: {response.status_code}")'''