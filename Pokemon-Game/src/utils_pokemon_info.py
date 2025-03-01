import random
from src.pokeload import pokemon_base


def get_pokemon_info(pokemon, is_enemy=False, player_profile=None):

    hp_percentage = pokemon['current_health'] / pokemon['base_health']
    hp_bar = '█' * int(hp_percentage * 20)  # Barra de vida de 20 segmentos
    hp_empty = '░' * (20 - len(hp_bar))

    if is_enemy:
        return f"{pokemon['name']} | {hp_bar}{hp_empty} {pokemon['current_health']}/{pokemon['base_health']} hp | lv {pokemon['level']}"
    else:
        return f"{pokemon['name']} | {hp_bar}{hp_empty} {pokemon['current_health']}/{pokemon['base_health']} hp | lv {pokemon['level']} "

def max_enemy_level(*args):
    max = args[0]["pokemon_team"][0].copy()

    for _ in range(len(args[0]["pokemon_team"]) - 1):
        if args[0]["pokemon_team"][_ + 1]["level"] > max["level"]:
            max = args[0]["pokemon_team"][_ + 1].copy()

    return max

def choose_pokemon(player_profile):
    while True:
        print("\nTu equipo Pokémon es: \n")
        for index, pokemon in enumerate(player_profile["pokemon_team"], start=1):  #start=1 para numerar pk del 1 al 6
            print(f"{index} - {get_pokemon_info(pokemon)}\n")
        try:
            choice = int(input("¿Con quién quieres empezar?\n"))
            pokemon_selected = player_profile["pokemon_team"][choice - 1]  # Ajustamos para que el índice sea correcto
            if pokemon_selected["current_health"] > 0:
                return pokemon_selected
            else:
                print("\nPor favor, elige un Pokémon con salud.")
        except (ValueError, IndexError):
            print("Opción inválida. Por favor, elige un número válido.")


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

def assign_experience(attack_history, team):
    for pokemon in attack_history:
        if pokemon["current_health"] > 0:
            points = random.randint(3, 6)
            pokemon["current_exp"] += points

            while pokemon["current_exp"] >= 10 + (pokemon["level"] * 2): #cuanto mas nivel mas cuesta de subir
                pokemon["current_exp"] -= (10 + (pokemon["level"] * 2))
                pokemon["level"] += 1
                pokemon["current_health"] = pokemon["base_health"]
                print(f"{pokemon['name']} ha subido al nivel {pokemon['level']}")
            distribute_experience(pokemon, team, points)

def distribute_experience(pokemon, team, points):
    #Todos los miembros del equipo ganan algo de xp tras un combate aunque no participen
    share_points = points // len(team)  # Se divide la experiencia entre el número total de Pokémon

    for member in team:
        if member != pokemon:  # No se distribuye a sí mismo
            member["current_exp"] += share_points
            # Subir de nivel si la experiencia acumulada supera el limite
            while member["current_exp"] >= 10 + (member["level"] * 2):
                member["current_exp"] -= (10 + (member["level"] * 2))
                member["level"] += 1
                member["current_health"] = member["base_health"]  # Recupera la salud completamente
                print(f"¡{member['name']} ha subido al nivel {member['level']}!")

def pokemon_heal(player_profile, player_pokemon):
    if player_profile["health_potion"] > 0:
        player_pokemon["current_health"] += 50
        if player_pokemon["current_health"] > 100:
            player_pokemon["current_health"] = 100
        player_profile["health_potion"] -= 1
        print(f"Salud de {player_pokemon['name']} restaurada hasta {player_pokemon['current_health']}")
    else:
        print(f"¡No tienes pociones para curar a {player_pokemon['name']}!")
