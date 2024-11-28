from urllib.request import HTTPBasicAuthHandler
import requests
import config as config
import json

# Imprimir dans le terminal
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def request (numId):
    # Base URL de la plataforme CNA
    base_url = f"https://centraliens-nantes.org"
    
    id = f"0000{numId}K"
    query = f"/api/v2/customer/profile/people/{id}"
    url = f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}"
    response = requests.get(url)

    return response



#Initialize counter
count = 0

#Initialize number id
numId = 1325

response = request(numId)
test = response.status_code

while test == 200:
    count += 1 
    numId += 1

    response = request(numId)
    #print(response.json()["display_name"])

    prox = response.status_code 

    if prox != 200:
        numId+=1
        response = request(numId)
        test = response.status_code
    else:
        test = prox

        

print("Counter: ", count, "\nFinal num id: ", numId)

