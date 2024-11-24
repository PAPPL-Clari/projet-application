from urllib.request import HTTPBasicAuthHandler
import requests
import config
import json

# Imprimir dans le terminal
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def fetchData():

    # Base URL de la plataforme CNA
    base_url = f"https://centraliens-nantes.org"
    query = "/api/v2/customer/academic/member/" 

    result = []
    
    for pag in range (1, 2):
        
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

