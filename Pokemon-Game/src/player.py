import os
import random
from src.enemy import type_calculator
from src.utils_pokemon_info import pokemon_attacks_actual_lv


def continue_or_exit(text_to_show):
    while True:
        try:
            player_wants = input(text_to_show)
            if player_wants.upper() not in ["S", "N"]:
                raise ValueError
            elif player_wants.upper() == "S":
                return True
            else:
                return False
        except ValueError:
            print("Opción inválida, responda con Ss o Nn.")

def set_or_get_player_name():
    # Utiliza os.path.expanduser para conseguir la ruta del usuario por defecto
    main_user_route = os.path.expanduser("~")

    # Utiliza os.makedirs con exist_ok=True para crear la carpeta si no existe
    os.makedirs(main_user_route + "/Pokemon-Game", exist_ok=True)
    game_user_route = main_user_route + "/Pokemon-Game"

    try:
        with open(f"{game_user_route}/username.txt", "r") as name_in_game:
            user_name = name_in_game.read().split("\n")[0]
            print(f"\nBienvenido/a a mi juego, {user_name}")
    except FileNotFoundError:
        with open(f"{game_user_route}/username.txt", "w") as name_in_game:
            user_name = input("¿Cuál es tu nombre?: ")
            name_in_game.write(user_name + "\n")

    return user_name


def create_player_profile(pokemon_list):
    # Selecciona Pokémon únicos aleatoriamente para el inventario
    pokemon_inventory = []
    while len(pokemon_inventory) < 3:
        random_pokemon = random.choice(pokemon_list)
        if random_pokemon not in pokemon_inventory:
            pokemon_inventory.append(random_pokemon)

    user_name = set_or_get_player_name()
    for pokemon in pokemon_inventory:
        if "attacks" not in pokemon:
            print(f"Error: {pokemon['name']} no tiene ataques definidos.")

    return {
        "player_name": user_name,
        "pokemon_inventory": pokemon_inventory,
        "combats": 0,
        "pokeballs": 0,
		"ultraballs":0,
        "health_potion": 0
    }


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def get_inventory_info(player):
    return f"Pokeballs: {player['pokeballs']} | Ultraballs: {player['ultraballs']} | Pociones: {player['health_potion']}"


def player_attack(player_pokemon, enemy_pokemon):
    """Solo son visibles los ataques de su nivel o inferior"""
    player_attacks = pokemon_attacks_actual_lv(player_pokemon["attacks"], player_pokemon["level"])

    while True:
        print(f"\nAtaques de {player_pokemon['name']}")
        for index in range(len(player_attacks)):
            print(f"{index} - {player_attacks[index]['name']}")
        try:
            user_attack = player_attacks[int(input("Elige un ataque: "))]
            break
        except (ValueError, IndexError):
            print("Opción no valida")

    user_damage_with_type_percentage_applied = int(str(user_attack['damage']).replace("--", "0")) * \
                                               type_calculator(player_pokemon, enemy_pokemon)

    enemy_pokemon["current_health"] -= user_damage_with_type_percentage_applied


def item_lottery(player_profile):
    lottery = random.random()

    if lottery <= 0.4:  # 40% de probabilidad para Pokéballs
        player_profile["pokeballs"] += 1
        print("Has conseguido una Pokéball!")
    elif lottery <= 0.5:  # 10% de probabilidad para Ultraballs
        player_profile["ultraballs"] += 1
        print("Has conseguido una Ultraball!")
    elif lottery <= 0.9:  # 40% de probabilidad para Pociones
        player_profile["health_potion"] += 1
        print("Has conseguido una Poción!")
    else:  # 10% de probabilidad para no obtener nada
        print("No has conseguido ningun objeto en este combate.")



def add_actual_combat(player_profile):
    player_profile["combats"] += 1
