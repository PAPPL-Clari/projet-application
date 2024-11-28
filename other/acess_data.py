from urllib.request import HTTPBasicAuthHandler
import requests
import config as config
import json

# Imprimir dans le terminal
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
       
# Base URL de la plataforme CNA
base_url = f"https://centraliens-nantes.org"

# ID de Guillaume GAUTIER
for x in range(4174,100000):
    id = f"0000{x}K"
    query = f"/api/v2/customer/profile/people/{id}"

    # url complète avec l'autentication
    url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}"
    
    try:
        response = requests.get(url)
    except:
        (f"Non-success status code: {response.status_code}")

    if response.status_code==200:
        #jprint(response.json())
        name = response.json()["display_name"]
        print(f"{x}: {name}")

#20 resultats par page par default, mais on peut monter a 100
