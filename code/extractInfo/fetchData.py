import config
import json
import asyncio
import aiohttp

# Fonction pour afficher un objet JSON dans le terminal avec une indentation
def jprint(obj):
    """
    Affiche un objet JSON de manière lisible dans le terminal.

    :param obj: Objet JSON à afficher
    """
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Fonction asynchrone pour récupérer les données d'une page web
async def fetch_page(session, url, semaphore, retries=3, backoff_factor=1):
    """
    Récupère une page depuis une URL avec gestion des erreurs et des tentatives multiples.

    :param session: Session de connexion aiohttp
    :param url: URL de la page à récupérer
    :param semaphore: Sémaphore pour limiter le nombre de connexions simultanées
    :param retries: Nombre maximum de tentatives en cas d'échec
    :param backoff_factor: Facteur pour augmenter le délai entre chaque tentative (exponential backoff)
    :return: Données JSON si la requête réussit, None sinon
    """
    async with semaphore:  # Limite le nombre de connexions simultanées
        for attempt in range(retries):  # Répète la requête plusieurs fois en cas d'erreur
            try:
                async with session.get(url) as response:
                    if response.status == 200:  # Vérifie si la réponse est réussie
                        return await response.json()  # Retourne les données JSON
                    else:
                        print(f"Essai {attempt + 1}: URL: {url}, Code d'état: {response.status}, Réponse: {await response.text()}")
            except Exception as e:
                print(f"Erreur dans l'essai {attempt + 1} pour l'URL {url}: {e}")
            
            # Attend avant de réessayer (délai croissant)
            await asyncio.sleep(backoff_factor * (2 ** attempt))
        
        print(f"Échec après {retries} essais: {url}")
        return None  # Retourne None si toutes les tentatives échouent

# Fonction principale pour récupérer des données en fonction d'un type
async def fetchData_async(type): 
    """
    Récupère les données asynchrones depuis l'API CNA en fonction du type spécifié.

    :param type: Type de données à récupérer ("diploma" ou "profile")
    :return: Liste de résultats extraits de l'API
    """
    # URL de base de l'API
    base_url = "https://centraliens-nantes.org"

    # Détermine l'endpoint selon le type
    if type == "diploma":
        query = "/api/v2/customer/academic/member/"
    elif type == "profile":
        query = "/api/v2/customer/profile/people"
    else:
        raise ValueError("Type invalide")  # Erreur si le type est invalide

    # Génère une liste d'URL pour les pages à récupérer (248 pages, 100 utilisateurs par page)
    urls = [
        f"{base_url}{query}?access_id={config.key}&access_secret={config.secret}&page={pag}&limit=100"
        for pag in range(1, 248)
    ]

    result = []  # Liste pour stocker les résultats finaux
    semaphore = asyncio.Semaphore(50)  # Limite à 50 connexions simultanées

    # Utilisation d'une session asynchrone pour les requêtes HTTP
    async with aiohttp.ClientSession() as session:
        # Crée une tâche pour chaque URL
        tasks = [fetch_page(session, url, semaphore) for url in urls]
        
        # Exécute toutes les tâches de manière asynchrone
        responses = await asyncio.gather(*tasks)

    # Parcourt les réponses pour extraire les données utiles
    for response in responses:
        if response and "_embedded" in response and "items" in response["_embedded"]:
            result.extend(response["_embedded"]["items"])  # Ajoute les éléments extraits aux résultats

    return result  # Retourne la liste des données récupérées
