from urllib.request import HTTPBasicAuthHandler
import requests
import config
import json
import addDatabase
import getPersonneInfo
import getDiplomaInfo
#import getContactInfo

# Imprimir dans le terminal
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
       
# Base URL de la plataforme CNA
base_url = f"https://centraliens-nantes.org"

# ID de Guillaume GAUTIER
id = f"21"

#Query
#query = f"/api/v2/customer/profile/people/{id}"

query = "/api/v2/customer/profile/people" #query para pegar infos pessoais e gerais do individuo
#query = "/api/v2/customer/academic/member" #Usar essa query para adquirir infos do diploma do individuo

# url complète avec l'autentication (2460 pags)

pag = 12
url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}&page={pag}&limit=1"

response = requests.get(url)
if response.status_code == 200:
    resultat = response.json() 
    #jprint(resultat)
    #print("Ok")

    #jprint(resultat["_embedded"]["items"])
    
    result = resultat["_embedded"]["items"][0]

    
    #addDatabase(result)
    
    #jprint(result)
    #print(getPersonneInfo.getPersonneInfo(result))
    #print(getDiplomaInfo.getDiplomaInfo(result))
    #print(getContactInfo.getContactInfo(result))

    
else:
    print(f"Erro: {response.status_code}")

