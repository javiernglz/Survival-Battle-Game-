import random
from src.pokeload import pokemon_base

""" def get_pokemon_info(pokemon, enemy=False, *args):
    if not enemy:
        return f"{pokemon['name']} | lvl {pokemon['level']} | hp {pokemon['current_health']}/{pokemon['base_health']}"
    else:
        max_leveled_pokemon = max_level_for_enemy(args[0])
        return f"{pokemon['name']} | lvl {max_leveled_pokemon['level']} | hp {pokemon['current_health']}/" \
               f"{pokemon['base_health']}" """
def get_pokemon_info(pokemon, is_enemy=False, player_profile=None):

    hp_percentage = pokemon_base['current_health'] / pokemon_base['base_health']
    hp_bar = '█' * int(hp_percentage * 10)  # Barra de vida de 10 segmentos
    hp_empty = '─' * (10 - len(hp_bar))  # Espacios vacíos para la barra de vida

    if is_enemy:
        return f"{pokemon['name']} | {hp_bar}{hp_empty} | lvl {pokemon['level']} | hp {pokemon['current_health']}/{pokemon['base_health']}"
    else:
        return f"{pokemon['name']} | {hp_bar}{hp_empty} | lvl {pokemon['level']} | hp {pokemon['current_health']}/{pokemon['base_health']}"


def max_level_for_enemy(*args):
    max = args[0]["pokemon_inventory"][0].copy()

    for _ in range(len(args[0]["pokemon_inventory"]) - 1):
        if args[0]["pokemon_inventory"][_ + 1]["level"] > max["level"]:
            max = args[0]["pokemon_inventory"][_ + 1].copy()

    return max


def choose_pokemon(player_profile):
    while True:
        print("\nTu equipo Pokemon es: \n")
        for index in range(len(player_profile["pokemon_inventory"])):
            print(f"{index} - {get_pokemon_info(player_profile['pokemon_inventory'][index])}\n")
        try:
            pokemon_selected = player_profile["pokemon_inventory"][int(input("Con quien quieres empezar?\n"))]
            if pokemon_selected["current_health"] > 0:
                return pokemon_selected
            else:
                print("\nPor favor elige un pokémon con salud.")
        except (ValueError, IndexError):
            print("Opción inválida")


def pokemon_attacks_actual_lv(attacks, actual_level):
    posible_attacks_in_that_level = []

    for item in attacks:
        if int(item.get("main_level", "0") or "0") <= actual_level:
            posible_attacks_in_that_level.append(item)
        else:
            break

    while True:
        if len(posible_attacks_in_that_level) > 4:
            posible_attacks_in_that_level.pop(0)
        else:
            break

    return posible_attacks_in_that_level


def assign_experience(attack_history):
    for pokemon in attack_history:
        if pokemon["current_health"] > 0:
            points = random.randint(1, 5)
            pokemon["current_exp"] += points

            while pokemon["current_exp"] > 20:
                pokemon["current_exp"] -= 20
                pokemon["level"] += 1
                pokemon["current_health"] = pokemon["base_health"]
                print(f"Tu pokemon ha subido al nivel {get_pokemon_info(pokemon)}")


def pokemon_heal(player_profile, player_pokemon):
    if player_profile["health_potion"] > 0:
        player_pokemon["current_health"] += 50
        if player_pokemon["current_health"] > 100:
            player_pokemon["current_health"] = 100
        player_profile["health_potion"] -= 1
        print(f"Salud de {player_pokemon['name']} restaurada hasta {player_pokemon['current_health']}")
    else:
        print(f"¡No tienes pociones para curar a {player_pokemon['name']}!")
