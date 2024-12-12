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

async def fetch_page(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"URL: {url}, Status Code: {response.status}, Response: {await response.text()}")
                    return None
        except Exception as e:
            print(f"Erro ao buscar URL {url}: {e}")
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
    semaphore = asyncio.Semaphore(60)  # Limitation de 60 connexions simultanées

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url, semaphore) for url in urls]
        responses = await asyncio.gather(*tasks)

    for response in responses:
        if response and "_embedded" in response and "items" in response["_embedded"]:
            result.extend(response["_embedded"]["items"])

    return result