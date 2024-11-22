from urllib.request import HTTPBasicAuthHandler
import requests
import config
import json

# Imprimir dans le terminal
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def getDiplomaInfo(id):
    # Base URL de la plataforme CNA
    base_url = f"https://centraliens-nantes.org"

    # ID 
    #21 correspond pour Guillaume GAUTIER 

    #Query
    query = f"/api/v2/customer/academic/member/{id}"

    # url complète avec l'autentication
    url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}"


    response = requests.get(url)
    if response.status_code == 200:
        result = response.json() 
        jprint(result)
        print("Ok")
    else:
        print(f"Erro: {response.status_code}")


    #Infos des diplomes, specialisation et ecole
    listeDiplomes = result["_embedded"]["diplomas"]


    for i in range(len(listeDiplomes)):
        #infos diplome
        id_diplome = listeDiplomes[i]["id"]
        ref_diplome = listeDiplomes[i]["diploma_ref"]
        nom_diplome = listeDiplomes[i]["full_name"]
        parcours = listeDiplomes[i]["concentration"]

        #infos specialisation
        #id_specialisation =
        nom_specialisation = listeDiplomes[i]["specialization"]

        #Infos de l'ecole
        #id_ecole
        nom_ecole = listeDiplomes[i]["school"]
        acronyme_pays_ecole = listeDiplomes[i]["study_year"]
    
    return id_diplome, ref_diplome, nom_diplome, parcours, nom_specialisation, nom_ecole, acronyme_pays_ecole