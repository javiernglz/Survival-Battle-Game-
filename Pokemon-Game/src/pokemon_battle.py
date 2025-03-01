import random
from src.enemy import enemy_attack, capture_pokeball
from src.load_play import load_game, delete_play, save_game
from src.player import any_player_pokemon_lives, get_inventory_info, player_attack, \
    create_player_profile, item_lottery, add_actual_combat
from src.utils_pokemon_info import choose_pokemon, get_pokemon_info, pokemon_heal, \
    assign_experience
from src.pokeload import get_all_pokemons


def poke_info_battle(player_pokemon, enemy_pokemon, player_profile):
    print(f"\nRIVAL:" f" {enemy_pokemon['name']}")

    print(f"\n{get_pokemon_info(player_pokemon)}     VS     "
          f"{get_pokemon_info(enemy_pokemon, True, player_profile)}")

    print(f"\nInventario: {get_inventory_info(player_profile)}")


def user_turn(action, player_pokemon, enemy_pokemon, attack_history, player_profile):
    enemy_can_attack = True

    if action.upper() == "A":
        player_attack(player_pokemon, enemy_pokemon)
        attack_history.append(player_pokemon)
    elif action.upper() == "V":
        pokemon_heal(player_profile, player_pokemon)
    elif action.upper() == "P":
        its_captured = capture_pokeball(player_profile, enemy_pokemon)
        if its_captured:
            enemy_can_attack = False
    elif action.upper() == "C":
        player_pokemon = choose_pokemon(player_profile)

    return [enemy_can_attack, player_pokemon]


def player_pok_no_hp(player_profile, player_pokemon):
    for pokemon in player_profile["pokemon_inventory"]:
        if pokemon["current_health"] < 0:
            pokemon["current_health"] = 0  # No puede tener vida negativa

    print(f"\n¡Han derrotado a {player_pokemon['name']}!")


def fight(player_profile, enemy_pokemon):
    print(f"\n\n----------- COMBATE Nº {player_profile['combats'] + 1} -----------\n\n")
    attack_history = []
    print(f"Vas a combatir contra {enemy_pokemon['name']}")
    player_pokemon = choose_pokemon(player_profile)

    its_captured = False
    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0 and not its_captured:
        poke_info_battle(player_pokemon, enemy_pokemon, player_profile)

        action = ""  # Para poder empezar
        while action.upper() not in ["A", "P", "V", "C"]:
            action = input(f"Que deberia hacer {player_pokemon['name']}?: "
                           "[A]tacar, "
                           "[P]okeball, "
                           "Poción de [V]ida, "
                           "[C]ambiar: ")

        reaction_to_user_actions = user_turn(action, player_pokemon, enemy_pokemon, attack_history, player_profile)
        if reaction_to_user_actions[1] != player_pokemon:
            player_pokemon = reaction_to_user_actions[1]
        if reaction_to_user_actions[0]:
            enemy_attack(player_pokemon, enemy_pokemon)
        else:
            break  # Si el pokemon ha sido capturado

        if player_pokemon["current_health"] <= 0 and any_player_pokemon_lives(player_profile):
            player_pok_no_hp(player_profile, player_pokemon)
            player_pokemon = choose_pokemon(player_profile)

    if player_pokemon["current_health"] > 0:
        print("\n----- Has ganado! -----")
        assign_experience(attack_history)
    elif not any_player_pokemon_lives(player_profile):
        print("\nTus POKEMON han sido debilitados...\n")

    print("--- FIN DEL COMBATE ---")

def continue_or_exit(text_to_show):
    while True:
        try:
            player_wants = input(text_to_show).strip().upper()
            if player_wants == "":
                return True #Continuar combates
            elif player_wants == "X":
                return False #Salir de la partida
            else:
                print("Opción no valida, ENTER para continuar o X para salir.")
        except KeyboardInterrupt:
            return False  # Permitir salir con Ctrl+C

def game_loader(pokemon_list):
    if continue_or_exit("\n[ENTER] Cargar partida anterior | [X] Partida nueva: "):
        data = load_game()
        if data is not None:
            delete_play()
            return data

    return create_player_profile(pokemon_list)


def main():
    isGameEnded = False
    pokemon_list = get_all_pokemons()
    player_profile = game_loader(pokemon_list)

    while not isGameEnded:

        # Main game loop
        while any_player_pokemon_lives(player_profile) and not isGameEnded:
            enemy_pokemon = random.choice(pokemon_list)

            fight(player_profile, enemy_pokemon)
            if any_player_pokemon_lives(player_profile):
                item_lottery(player_profile)
            add_actual_combat(player_profile)

            if any_player_pokemon_lives(player_profile) and not continue_or_exit("\n[ENTER] Siguiente combate | [X] Salir"):
                isGameEnded = True
                save_game(player_profile)

        print(f"\nHas terminado en el combate nº{player_profile['combats']}")

        if not isGameEnded:
            if not continue_or_exit("\n[ENTER] Siguiente combate | [X] Salir"):
                break

if __name__ == "__main__":
    main()
