from urllib.request import HTTPBasicAuthHandler
import requests
import config
import json

# Imprimir dans le terminal
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def fetchData(type):

    # Base URL de la plataforme CNA
    base_url = f"https://centraliens-nantes.org"

    if(type == "diploma"):
        query = "/api/v2/customer/academic/member/"
    elif(type == "profile"):
        query = f"/api/v2/customer/profile/people" 

    result = []
    
    for pag in range (1, 246):
        
        url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}&page={pag}&limit=100"

        response = requests.get(url)
        if response.status_code == 200:
            resultat = response.json() 
            result = result + resultat["_embedded"]["items"]
            #jprint(result)
        
        else:
            print(f"Erro: {response.status_code}")
            return 0
        
    return result

