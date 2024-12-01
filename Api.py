import requests

def fetch_data(name:str):
    name.lower()
    url = 'https://pokeapi.co/api/v2/pokemon/{name}'
    
    res = requests.get(url.format(name=name))
    # Error Check
    if res.status_code != 200:
        return("Fehler beim Abrufen der Daten:", res.status_code)
        
    result = res.json()
    return result

result = fetch_data('ditto')
#print(result[0].keys())

def abilities(result):
    if "abilities" in result:
        return [ability['ability']['name'] for ability in result['abilities']]
    else:
        return []
        
        
def abilities_url(result):
    if result:
        abilities_dict = {ability['ability']['name']: ability['ability']['url'] for ability in result['abilities']}
        return abilities_dict
    else:
        return {}
        
def ability_description(ability_name, name):#
    result = fetch_data(name)
    abilities_dic = abilities_url(result)
    url = abilities_dic.get(ability_name, '')
    
    # Wenn URL nicht gefunden ist
    if not url:
        return f"URL für Ability {ability_name} hab nicht gefunden"
    
    
    res = requests.get(url)
    
    #Fehler prufen
    if res.status_code != 200:
        return f"Fehler beim Abrufen der Daten: {res.status_code}"
    
    result = res.json()
    
    # Извлечение описания способности (первый элемент из effect_entries)
    effect_entries = result.get("effect_entries", [])
    if effect_entries:
        return effect_entries[0].get("effect", "Описание отсутствует")
    
    return "Описание отсутствует"

print(ability_description("limber", 'ditto'))        
    
def pokemon_list()->list:
    url = "https://pokeapi.co/api/v2/pokemon?limit=100"
    res= requests.get(url)
    if res.status_code != 200:
        return("Fehler beim Abrufen der Daten:", response.status_code)
    response = res.json()
    return [pokemon["name"] for pokemon in response["results"]]    
#print(pokemon_list())  

def weight(name)->int:
    result = fetch_data(name)
    pokemon_weight = int(result["weight"])
    
    return pokemon_weight

def height(name)->int:   
    result = fetch_data(name)
    pokemon_height = int(result["height"])
    
    return pokemon_height

def id(name)->int:
       
    result = fetch_data(name)
    pokemon_id = int(result["id"])
    
    return pokemon_id

def image(name)->str:
       
    result = fetch_data(name)
    image_url = result["sprites"]["front_default"]
    return image_url
    
def get_pokemon_stats(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        stats = {}
        for stat in data['stats']:
            stats[stat['stat']['name']] = stat['base_stat']
        return stats
    else:
        return f"Error: {response.status_code}"
