import os
import random
from src.enemy import type_calculator
from src.utils_pokemon_info import pokemon_attacks_actual_lv


def continue_or_exit(text_to_show):
    while True:
        try:
            player_wants = input(text_to_show)
            if player_wants.upper() not in ["ENTER", "X"]:
                raise ValueError
            elif player_wants.upper() == "ENTER":
                return True
            else:
                return False
        except ValueError:
            print("Opción inválida, responda con [ENTER] o [X]")

def create_player_name():
    #os.path.expanduser sirve para conseguir la ruta del usuario por defecto
    main_user_route = os.path.expanduser("~")

    #os.makedirs con exist_ok=True para crear la carpeta si no existe
    os.makedirs(main_user_route + "/Pokemon-Game", exist_ok=True)
    game_user_route = main_user_route + "/Pokemon-Game"

    try:
        with open(f"{game_user_route}/username.txt", "r") as name_in_game:
            user_name = name_in_game.read().split("\n")[0]
            print(f"\n\n\nBienvenido/a a mi juego, {user_name}, preparate para derrotar a todos "
                "los pokemon salvajes que puedas. SUERTE ;)")
    except FileNotFoundError:
        with open(f"{game_user_route}/username.txt", "w") as name_in_game:
            user_name = input("\n\n\nComo te llamas? ")
            name_in_game.write(user_name + "\n")

    return user_name

def create_player_profile(pokemon_list):
    #Pokémon aleatorios para el equipo
    pokemon_team = []
    while len(pokemon_team) < 3:
        random_pokemon = random.choice(pokemon_list)
        if random_pokemon not in pokemon_team:
            pokemon_team.append(random_pokemon)

    user_name = create_player_name()
    for pokemon in pokemon_team:
        if "attacks" not in pokemon:
            print(f"Error: {pokemon['name']} no tiene ataques cargados.")

    return {
        "player_name": user_name,
        "pokemon_team": pokemon_team,
        "combats": 0,
        "pokeballs": 0,
		"ultraballs":0,
        "health_potion": 0
    }

def player_attack(player_pokemon, enemy_pokemon):
    """Solo son visibles los ataques de su nivel o inferior"""
    player_attacks = pokemon_attacks_actual_lv(player_pokemon["attacks"], player_pokemon["level"])

    while True:
        print(f"\nAtaques de {player_pokemon['name']}")
        for index in range(len(player_attacks)):
            print(f"{index + 1} - {player_attacks[index]['name']}")
        try:
            attack_choice = int(input("Elige un ataque: "))
            if 1 <= attack_choice <= len(player_attacks):  # ataques entre el 1 y el 4
                user_attack = player_attacks[attack_choice - 1]
                break
            else:
                 print("Selecciona un ataque valido.")
        except (ValueError, IndexError):
            print("Opción no valida")

    user_type_damage_applied = int(str(user_attack['damage']).replace("--", "0")) * \
                                               type_calculator(player_pokemon, enemy_pokemon)

    enemy_pokemon["current_health"] -= user_type_damage_applied

def item_lottery(player_profile):
    lottery = random.random()

    if lottery <= 0.4:  # 40% de probabilidad para Pokéballs
        player_profile["pokeballs"] += 1
        print("\nHas conseguido una Pokéball!")
    elif lottery <= 0.5:  # 10% de probabilidad para Ultraballs
        player_profile["ultraballs"] += 1
        print("\nHas conseguido una Ultraball!")
    elif lottery <= 0.9:  # 40% de probabilidad para Pociones
        player_profile["health_potion"] += 1
        print("\nHas conseguido una Poción!")
    else:  # 10% de probabilidad para no obtener nada
        print("\nNo has conseguido ningun objeto en este combate.")

def player_pokemon_hp(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_team"]]) > 0

def create_inventory(player):
    return f"Pokeballs: {player['pokeballs']} | Ultraballs: {player['ultraballs']} | Pociones: {player['health_potion']}"

def add_actual_combat(player_profile):
    player_profile["combats"] += 1
