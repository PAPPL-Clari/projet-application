import config
import json
import asyncio
import aiohttp
import asyncio
import json

# Imprimir dans le terminal
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

import asyncio

async def fetch_page(session, url, semaphore, retries=3, backoff_factor=1):
    async with semaphore:
        for attempt in range(retries):
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Essai {attempt + 1}: URL: {url}, Status Code: {response.status}, Response: {await response.text()}")
            except Exception as e:
                print(f"Erreur dans l'essai {attempt + 1} pour l'URL {url}: {e}")
            
            # Attendre pour essayer à nouveau (exponential backoff)
            await asyncio.sleep(backoff_factor * (2 ** attempt))
        print(f"Échec après {retries} essais: {url}")
        return None

async def fetchData_async(type): 
    # Base URL de la plataforme CNA
    base_url = "https://centraliens-nantes.org"

    if type == "diploma":
        query = "/api/v2/customer/academic/member/"
    elif type == "profile":
        query = "/api/v2/customer/profile/people"
    else:
        raise ValueError("Tipo inválido")

    urls = [
        f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}&page={pag}&limit=100"
        for pag in range(1, 248) # 248 pages de 100 utilisateurs
    ]

    result = []
    semaphore = asyncio.Semaphore(50)  # Limitation de 20 connexions simultanées

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url, semaphore) for url in urls]
        responses = await asyncio.gather(*tasks)

    for response in responses:
        if response and "_embedded" in response and "items" in response["_embedded"]:
            result.extend(response["_embedded"]["items"])

    return result