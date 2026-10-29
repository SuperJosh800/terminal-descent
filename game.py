import random
from colorama import Fore, Style
from player import Player
from enemy import spawn_enemy, spawn_boss, is_boss_floor
from combat import combat, coop_combat
from loot import drop_loot, drop_consumable, get_equipped_set
from tavern import tavern, get_current_zone

ROOMS_PER_FLOOR = 5

RARITY_COLOURS = {
    "common":    Style.RESET_ALL,
    "uncommon":  Fore.GREEN,
    "rare":      Fore.BLUE,
    "legendary": Fore.YELLOW,
}

def rarity_colour(item):
    rarity = item.get("rarity", "common")
    return RARITY_COLOURS.get(rarity, Style.RESET_ALL)

COOP_ENEMY_HP_MULTIPLIER = 2

def show_title():
    print(f"\n  {Fore.YELLOW}=========================================={Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}       TERMINAL DESCENT{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}=========================================={Style.RESET_ALL}")
    print("\n  A dungeon of endless depth awaits.")
    print("  Few who enter return. None who descend far enough do.")
    print(f"\n  {Fore.YELLOW}=========================================={Style.RESET_ALL}")

def choose_mode():
    print("\n  Choose a mode:")
    print("  1. Solo")
    print("  2. Co-op (2 players, one keyboard)")
    while True:
        choice = input("\n  > ").strip()
        if choice == "1":
            return "solo"
        if choice == "2":
            return "coop"
        print("  Choose 1 or 2.")

def character_creation(prompt="Enter your hero's name: "):
    while True:
        name = input(f"\n  {prompt}").strip()
        if name:
            break
        print("  A hero needs a name.")

    print(f"\n  Choose your class, {Fore.CYAN}{name}{Style.RESET_ALL}:\n")
    print(f"  1. {Fore.RED}Warrior{Style.RESET_ALL}  — High HP and DEF. Power Strike, Shield Bash, War Cry.")
    print(f"  2. {Fore.GREEN}Rogue{Style.RESET_ALL}    — Fast and deadly. Backstab, Smoke Bomb, Poison Blade.")
    print(f"  3. {Fore.BLUE}Mage{Style.RESET_ALL}     — Powerful spells. Fireball, Frost Nova, Arcane Burst.")

    while True:
        choice = input("\n  > ").strip()
        if choice == "1":
            char_class = "Warrior"
            break
        elif choice == "2":
            char_class = "Rogue"
            break
        elif choice == "3":
            char_class = "Mage"
            break
        print("  Choose 1, 2 or 3.")

    player = Player(name, char_class)
    print(f"\n  Welcome, {Fore.CYAN}{name} the {char_class}{Style.RESET_ALL}.")
    print("  The Wandering Flagon waits at the dungeon's edge.")
    print("  The stranger in the corner watches you arrive.")
    return player

def show_floor_intro(floor, bosses_beaten):
    zone = get_current_zone(floor)
    boss_floor = is_boss_floor(floor)

    print(f"\n  {Fore.YELLOW}=========================================={Style.RESET_ALL}")
    if boss_floor:
        print(f"  {Fore.RED}FLOOR {floor} — BOSS FLOOR{Style.RESET_ALL}")
    else:
        print(f"  {Fore.CYAN}FLOOR {floor} — {zone.upper()}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}=========================================={Style.RESET_ALL}")

    if boss_floor and floor == 1000:
        print(f"  {Fore.RED}The air is still. Something waits at the end of everything.{Style.RESET_ALL}")
    elif boss_floor:
        print(f"  {Fore.RED}You feel a presence. Something powerful stirs ahead.{Style.RESET_ALL}")
    else:
        print(f"  You descend into {Fore.CYAN}{zone}{Style.RESET_ALL}.")

def handle_loot_drop(player, floor):
    roll = random.randint(1, 100)
    if roll <= 60:
        item = drop_loot(floor)
        if item:
            colour = rarity_colour(item)
            print(f"\n  {'='*40}")
            print(f"  {Fore.YELLOW}ITEM DROP!{Style.RESET_ALL}")
            print(f"  {colour}{item['name']}{Style.RESET_ALL}")
            print(f"  {colour}{item.get('rarity','').capitalize()} {item['slot'].capitalize()}{Style.RESET_ALL}")
            bonuses = ", ".join(f"+{v} {k}" for k, v in item.get("bonus", {}).items())
            if bonuses:
                print(f"  Bonuses: {colour}{bonuses}{Style.RESET_ALL}")
            if item.get("special"):
                print(f"  Special: {colour}{item['special'].replace('_', ' ').title()}{Style.RESET_ALL}")
            print(f"  {'='*40}")
            player.inventory.append(item)
    elif roll <= 75:
        item = drop_consumable()
        if item:
            print(f"\n  {'='*40}")
            print(f"  {Fore.GREEN}CONSUMABLE DROP!{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}{item['name']}{Style.RESET_ALL}")
            print(f"  {item['desc']}")
            print(f"  {'='*40}")
            player.inventory.append(item)

def handle_set_bonus_room(player):
    set_name, set_data = get_equipped_set(player)
    if set_name and set_data["bonus"] == "heart_of_the_forest":
        restore = int(player.max_hp * 0.05)
        player.hp = min(player.hp + restore, player.max_hp)
        print(f"  {Fore.GREEN}Heart of the Forest: restored {restore} HP.{Style.RESET_ALL}")

def run_floor(player, floor, bosses_beaten):
    show_floor_intro(floor, bosses_beaten)

    boss_floor = is_boss_floor(floor)

    if boss_floor:
        print("\n  You enter the boss chamber.")
        handle_set_bonus_room(player)

        if floor != 1000 and getattr(player, 'skip_next_combat', False):
            print(f"  {Fore.YELLOW}Void Incarnate! The boss senses your power and retreats... for now.{Style.RESET_ALL}")
            print("  (Boss skipped — floor cleared)")
            player.skip_next_combat = False
            bosses_beaten.add(get_current_zone(floor))
            return "cleared"

        enemy = spawn_boss(floor)
        if enemy is None:
            print("  The floor is empty. You pass through.")
            return "cleared"

        print(f"\n  {'='*40}")
        if floor == 1000:
            print(f"  {Fore.RED}The hooded stranger stands at the bottom of everything.{Style.RESET_ALL}")
        else:
            print(f"  {Fore.RED}BOSS: {enemy.name}{Style.RESET_ALL}")
            print(f"  HP: {Fore.RED}{enemy.hp}{Style.RESET_ALL} | ATK: {Fore.RED}{enemy.atk}{Style.RESET_ALL} | DEF: {enemy.defense}")
        print(f"  {'='*40}")

        result = combat(player, enemy)

        if result == "dead":
            return "dead"
        elif result == "victory_final":
            return "victory_final"
        else:
            print(f"\n  {Fore.GREEN}The boss has been defeated!{Style.RESET_ALL}")
            bosses_beaten.add(get_current_zone(floor))
            handle_loot_drop(player, floor)
            handle_loot_drop(player, floor)
            return "cleared"

    else:
        for room in range(1, ROOMS_PER_FLOOR + 1):
            print(f"\n  {Fore.CYAN}-- Room {room} of {ROOMS_PER_FLOOR} --{Style.RESET_ALL}")
            handle_set_bonus_room(player)

            if getattr(player, 'skip_next_combat', False):
                print(f"  {Fore.YELLOW}Void Incarnate! The enemy flees before you.{Style.RESET_ALL}")
                player.skip_next_combat = False
                handle_loot_drop(player, floor)
                continue

            enemy = spawn_enemy(floor)
            result = combat(player, enemy)

            if result == "dead":
                return "dead"

            handle_loot_drop(player, floor)

            if room < ROOMS_PER_FLOOR:
                print("\n  You press deeper into the floor...")
                player.show_stats()

        print(f"\n  {Fore.GREEN}Floor {floor} cleared!{Style.RESET_ALL}")
        return "cleared"

def death_screen(player, floor):
    print(f"\n  {Fore.RED}=========================================={Style.RESET_ALL}")
    print(f"  {Fore.RED}YOU HAVE FALLEN{Style.RESET_ALL}")
    print(f"  {Fore.RED}=========================================={Style.RESET_ALL}")
    print(f"\n  {Fore.CYAN}{player.name} the {player.char_class}{Style.RESET_ALL}")
    print(f"  Reached floor: {Fore.YELLOW}{floor}{Style.RESET_ALL}")
    print(f"  Level: {Fore.YELLOW}{player.level}{Style.RESET_ALL}")
    print(f"  Gold collected: {Fore.YELLOW}{player.gold}g{Style.RESET_ALL}")
    print("\n  The dungeon claims another.")
    print(f"  {Fore.RED}=========================================={Style.RESET_ALL}")

def victory_screen(player, floor):
    print(f"\n  {Fore.YELLOW}=========================================={Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}THE DUNGEON HAS BEEN DEFEATED.{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}=========================================={Style.RESET_ALL}")
    print(f"\n  {Fore.CYAN}{player.name} the {player.char_class}{Style.RESET_ALL}")
    print(f"  Reached floor: {Fore.YELLOW}{floor}{Style.RESET_ALL}")
    print(f"  Level: {Fore.YELLOW}{player.level}{Style.RESET_ALL}")
    print(f"  Gold collected: {Fore.YELLOW}{player.gold}g{Style.RESET_ALL}")
    print("\n  You are the first. You are the last.")
    print("  The dungeon is silent.")
    print(f"  {Fore.YELLOW}=========================================={Style.RESET_ALL}")

def play_again():
    while True:
        choice = input("\n  Play again? (y/n): ").strip().lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        print("  Enter y or n.")

def play_solo():
    player = character_creation()
    floor = 1
    bosses_beaten = set()

    print(f"\n  You push open the door to the {Fore.YELLOW}Wandering Flagon{Style.RESET_ALL}.")
    print("  The fire crackles. A hooded figure sits in the corner.")
    print("  The barkeep looks up.")
    tavern(player, floor, bosses_beaten)

    while True:
        result = run_floor(player, floor, bosses_beaten)

        if result == "dead":
            death_screen(player, floor)
            break

        if result == "victory_final":
            victory_screen(player, floor)
            break

        print("\n  You find the passage back to the surface.")
        print(f"  The {Fore.YELLOW}Wandering Flagon{Style.RESET_ALL} waits.")
        tavern(player, floor, bosses_beaten)

        floor += 1

def standing(heroes):
    return [hero for hero in heroes if hero.hp > 0]

def coop_loot(heroes, floor):
    for hero in heroes:
        print(f"\n  {Fore.CYAN}{hero.name}{Style.RESET_ALL} searches the room.")
        handle_loot_drop(hero, floor)

def take_coop_skip(heroes):
    for hero in heroes:
        if getattr(hero, 'skip_next_combat', False):
            hero.skip_next_combat = False
            return True
    return False

def run_coop_floor(heroes, floor, bosses_beaten):
    show_floor_intro(floor, bosses_beaten)

    if is_boss_floor(floor):
        print("\n  You enter the boss chamber.")
        for hero in standing(heroes):
            handle_set_bonus_room(hero)

        if floor != 1000 and take_coop_skip(heroes):
            print(f"  {Fore.YELLOW}Void Incarnate! The boss senses your power and retreats... for now.{Style.RESET_ALL}")
            print("  (Boss skipped — floor cleared)")
            bosses_beaten.add(get_current_zone(floor))
            return "cleared"

        enemy = spawn_boss(floor)
        if enemy is None:
            print("  The floor is empty. You pass through.")
            return "cleared"

        print(f"\n  {'='*40}")
        if floor == 1000:
            print(f"  {Fore.RED}The hooded stranger stands at the bottom of everything.{Style.RESET_ALL}")
        else:
            enemy.hp = enemy.max_hp = enemy.max_hp * COOP_ENEMY_HP_MULTIPLIER
            print(f"  {Fore.RED}BOSS: {enemy.name}{Style.RESET_ALL}")
            print(f"  HP: {Fore.RED}{enemy.hp}{Style.RESET_ALL} | ATK: {Fore.RED}{enemy.atk}{Style.RESET_ALL} | DEF: {enemy.defense}")
        print(f"  {'='*40}")

        result = coop_combat(heroes, enemy)
        if result in ("dead", "victory_final"):
            return result

        print(f"\n  {Fore.GREEN}The boss has been defeated!{Style.RESET_ALL}")
        bosses_beaten.add(get_current_zone(floor))
        coop_loot(heroes, floor)
        coop_loot(heroes, floor)
        return "cleared"

    for room in range(1, ROOMS_PER_FLOOR + 1):
        print(f"\n  {Fore.CYAN}-- Room {room} of {ROOMS_PER_FLOOR} --{Style.RESET_ALL}")
        for hero in standing(heroes):
            handle_set_bonus_room(hero)

        if take_coop_skip(heroes):
            print(f"  {Fore.YELLOW}Void Incarnate! The enemy flees before you.{Style.RESET_ALL}")
            coop_loot(heroes, floor)
            continue

        enemy = spawn_enemy(floor)
        enemy.hp = enemy.max_hp = enemy.max_hp * COOP_ENEMY_HP_MULTIPLIER
        if coop_combat(heroes, enemy) == "dead":
            return "dead"

        coop_loot(heroes, floor)

        if room < ROOMS_PER_FLOOR:
            print("\n  You press deeper into the floor...")
            for hero in heroes:
                hero.show_stats()

    print(f"\n  {Fore.GREEN}Floor {floor} cleared!{Style.RESET_ALL}")
    return "cleared"

def coop_tavern(heroes, floor, bosses_beaten):
    for hero in heroes:
        print(f"\n  {Fore.CYAN}{hero.name}'s turn at the tavern.{Style.RESET_ALL}")
        tavern(hero, floor, bosses_beaten)

def play_coop():
    heroes = [
        character_creation("Player 1, enter your hero's name: "),
        character_creation("Player 2, enter your hero's name: "),
    ]
    floor = 1
    bosses_beaten = set()

    print(f"\n  You push open the door to the {Fore.YELLOW}Wandering Flagon{Style.RESET_ALL} together.")
    print("  The fire crackles. A hooded figure sits in the corner.")
    print("  The barkeep looks up.")
    coop_tavern(heroes, floor, bosses_beaten)

    while True:
        result = run_coop_floor(heroes, floor, bosses_beaten)

        if result == "dead":
            for hero in heroes:
                death_screen(hero, floor)
            break

        if result == "victory_final":
            for hero in heroes:
                victory_screen(hero, floor)
            break

        print("\n  You find the passage back to the surface.")
        for hero in heroes:
            if hero.hp <= 0:
                hero.hp = max(1, int(hero.max_hp * 0.25))
                print(f"  {Fore.GREEN}{hero.name} is carried back and revived with {hero.hp} HP.{Style.RESET_ALL}")
        print(f"  The {Fore.YELLOW}Wandering Flagon{Style.RESET_ALL} waits.")
        coop_tavern(heroes, floor, bosses_beaten)

        floor += 1

def game_loop():
    while True:
        show_title()
        if choose_mode() == "coop":
            play_coop()
        else:
            play_solo()

        if not play_again():
            print("\n  Farewell, adventurer.")
            print(f"  {Fore.RED}The dungeon remains.{Style.RESET_ALL}")
            break
