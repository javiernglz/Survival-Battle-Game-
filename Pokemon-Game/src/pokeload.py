import os.path
import pickle
import sys
from time import sleep
from requests_html import HTMLSession


pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": None,
    "current_exp": 0
}

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="

def get_pokemon(index):
    url = "{}{}".format(URL_BASE, index)
    session = HTMLSession()

    new_pokemon =pokemon_base.copy()
    pokemon_page = session.get(url)

    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text.split('\n')[0]

    new_pokemon["type"]=[]

    for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        new_pokemon["type"].append(img.attrs["alt"])
    #la pagina cambio, los ataques no estan donde indica el video
    new_pokemon["attacks"] = []

    for attack_item in pokemon_page.html.find(".pkmain")[-1].find(".check3"):
        try:
            attack = {
                "name": attack_item.find("td", first=True).find("a", first=True).text,
                "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
                "main_level": attack_item.find("th", first=True).text,
                "damage": int(attack_item.find("td")[3].text.replace("--", "0")),
            }
            print(attack)
        except Exception as e:
            print(f"Error al procesar el ataque: {e}")

        new_pokemon["attacks"].append(attack)

    return new_pokemon

def upload_pokemons():
    game_user_route = os.path.expanduser("~/Pokemon-Game")

    # Creamos la carpeta si no existe
    os.makedirs(game_user_route, exist_ok=True)

    try:
        with open(f"{game_user_route}/pokefile.pkl", "rb") as pokefile:
            all_pokemons = pickle.load(pokefile)
    except FileNotFoundError:
        print("Archivo no encontrado (primera vez), cargando de internet...")
        all_pokemons = []

        for index in range(151): #cambiar a 151, esta en 21 para que tarde menos en las pruebas
            try:
                pokemon = get_pokemon(index + 1)
                if pokemon is not None:
                    all_pokemons.append(pokemon)
            except Exception as e:
                print(f"Error al cargar el Pokémon {index + 1}: {e}") #la pagina web tiene errores
            download_bar(index + 1, 150)

        with open(f"{game_user_route}/pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemons, pokefile)

        print("\n¡Todos los Pokémon han sido descargados!\n")

    return all_pokemons

def min_level_with_attack(attack_item):
    min_level = 1
	#esto hace que no haya errores si un pokemon no tiene ataques al nivel 1
    try:
        min_level = int(attack_item.find("th")[1].text.replace("--", "0"))
    except ValueError:
        min_level = int(attack_item.find("th", first=True).text.replace("--", "0"))
    finally:
        return min_level

def download_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    arrow = '=' * int(round(bar_length * progress))
    spaces = ' ' * (bar_length - len(arrow))
    percentage = round(progress * 100, 2)
    if percentage > 100:
        percentage = 100
    sys.stdout.write(f'\r[{arrow + spaces}] {percentage}%')
    sys.stdout.flush()