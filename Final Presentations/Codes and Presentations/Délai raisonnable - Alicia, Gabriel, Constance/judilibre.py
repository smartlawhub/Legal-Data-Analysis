from env import KeyId
import requests
import re
import asyncio
import aiohttp
from num2words import num2words

API_URL = "https://sandbox-api.piste.gouv.fr/cassation/judilibre/v1.0"

HEADERS = {
    "KeyId": KeyId,
    "accept": "application/json"
}


def get(url:str, params:dict) -> dict:
    res = requests.get(API_URL + url, params=params, headers=HEADERS)
    data = res.json()
    return data


def get_locations() -> list:
    data = get("/taxonomy", {"id": "location", "context_value": "ca"})
    return data["result"]


def get_decision_text(id:str) -> str:
    data = get("/decision", {"id": id})
    return data["text"]

async def get_async_text(session, id):
    async with session.get(API_URL + "/decision", params={"id": id}, headers=HEADERS) as response:
        # Si too many requests, attend et réessaye
        if response.status == 429:
            print("Waiting...")
            await asyncio.sleep(2)
            return await get_async_text(session, id)
        
        elif response.status == 200:
            return await response.json()
    
        else:
            print(response.status)


async def get_texts_async(ids):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        tasks = [get_async_text(session, id) for id in ids]
        return await asyncio.gather(*tasks)
    
def get_decisions_ids(query:str, jurisdiction:str="cc", location:str=None, sort:str="score", page_size:int=10, page:int=0, stop_at:int=99999) -> list[dict]:       
    params = {
        "query": query,
        "jurisdiction": jurisdiction,
        "sort": sort,
        "page_size": page_size,
        "page": page
    }
    
    if (jurisdiction != "cc" and location != None):
        params["location"] = location

    data = get("/search", params)

    ids = []
    for decision in data["results"]:
        ids.append(decision["id"])

    print(f'{location} : {(page+1)*page_size}/{data["total"]}')
    
    # Si dernière page sort de la récursion
    if (data["next_page"] == None) or ((page+1)*page_size >= stop_at):
        return ids
    else:
        return ids + get_decisions_ids(query, jurisdiction, location, sort, page_size, page+1, stop_at)


def delai_raisonnable(text:str) -> int:
    # délai (raisonnable) de X jours/mois/années/ans
    pattern = r'délai(?:\s+raisonnable)?\s+de\s+(?:\d+\s+(?:jours?|semaines?|mois?|années?|ans?)|\b(?:{})\s+(?:jours?|semaines?|mois?|années?|ans?))'.format("|".join(num2words(i, lang='fr') for i in range(1, 101)))
    matches = re.findall(pattern, text, re.IGNORECASE)

    print(matches)

    # Récupère la valeur numérique
    for i in range(len(matches)):
        try:
            words = matches[i].split(" ")
            
            if words[1].lower() == "raisonnable":
                num = words[3].lower()
                echelle = words[4].lower()
            else:
                num = words[2].lower()
                echelle = words[3].lower()

            if echelle in ["jour", "jours"] :
                matches[i] = num
            elif echelle in ["semaine", "semaines"]:
                matches[i] = num * 7
            elif echelle == "mois":
                matches[i] = num * 30
            elif echelle in ["an", "ans", "année", "années"]:
                matches[i] = num * 365
        except:
            continue

    # Retourne la moyenne des délais du texte ou -1
    try:
        return sum(matches)//len(matches) if len(matches) > 0 else -1
    except:
        return -1
