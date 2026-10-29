import random
from colorama import Fore, Style
from player import Player, CLASS_ABILITIES
from enemy import Enemy, BURN_IMMUNE, BURN_WEAK, FINAL_BOSS_TURN_TEXT
from loot import get_equipped_set, SETS
from enemy_art import get_enemy_art

RARITY_COLOURS = {
    "common":    Style.RESET_ALL,
    "uncommon":  Fore.GREEN,
    "rare":      Fore.BLUE,
    "legendary": Fore.YELLOW,
}

def rarity_colour(item):
    rarity = item.get("rarity", "common")
    return RARITY_COLOURS.get(rarity, Style.RESET_ALL)

def apply_status(target, effect, value, max_stacks):
    if not hasattr(target, 'status_effects'):
        target.status_effects = {}
    current = target.status_effects.get(effect, {})
    stacks = min(current.get('stacks', 0) + 1, max_stacks)
    target.status_effects[effect] = {
        'stacks': stacks,
        'value': value,
        'turns': current.get('turns', 0) + 5 if effect == 'poison' else current.get('turns', 0) + 3,
    }
    print(f"  {Fore.MAGENTA}{effect.upper()} applied! ({stacks} stack(s)){Style.RESET_ALL}")

def apply_burn(enemy, stacks=2, ignore_immune=False):
    if enemy.name in BURN_IMMUNE and not ignore_immune:
        print(f"  {Fore.RED}{enemy.name} is immune to burn! The flask fizzles out.{Style.RESET_ALL}")
        return False
    multiplier = 2 if enemy.name in BURN_WEAK else 1
    value = 10 * multiplier
    for _ in range(stacks):
        apply_status(enemy, 'burn', value, 3)
    if multiplier == 2:
        print(f"  {Fore.RED}{enemy.name} is weak to fire! The flames spread violently!{Style.RESET_ALL}")
    return True

def tick_statuses(target, eternal_inferno=False):
    if not hasattr(target, 'status_effects'):
        return
    expired = []
    for effect, data in list(target.status_effects.items()):
        if effect == 'poison':
            dmg = int(data['value'] * data['stacks'])
            target.hp -= dmg
            print(f"  {Fore.MAGENTA}Poison deals {dmg} damage! ({data['stacks']} stack(s)){Style.RESET_ALL}")
        elif effect == 'burn':
            dmg = int(data['value'] * data['stacks'])
            target.hp -= dmg
            print(f"  {Fore.MAGENTA}Burn deals {dmg} damage! ({data['stacks']} stack(s)){Style.RESET_ALL}")
        data['turns'] -= 1
        if data['turns'] <= 0 and not (effect == 'burn' and eternal_inferno):
            expired.append(effect)
    for effect in expired:
        del target.status_effects[effect]
        print(f"  {Fore.MAGENTA}{effect.upper()} has worn off.{Style.RESET_ALL}")

ABILITIES = {
    "Power Strike":  {"cost": 15, "type": "damage",  "multiplier": 2.0, "status": None},
    "Shield Bash":   {"cost": 25, "type": "damage",  "multiplier": 1.0, "status": ("atk_down", 5, 3)},
    "War Cry":       {"cost": 40, "type": "buff",    "multiplier": 0,   "status": ("atk_up", 5, 3)},
    "Backstab":      {"cost": 15, "type": "damage",  "multiplier": 2.5, "status": None},
    "Smoke Bomb":    {"cost": 25, "type": "buff",    "multiplier": 0,   "status": ("spd_up", 0, 2)},
    "Poison Blade":  {"cost": 40, "type": "damage",  "multiplier": 1.0, "status": ("poison", 0, 5)},
    "Fireball":      {"cost": 15, "type": "damage",  "multiplier": 2.0, "status": None},
    "Frost Nova":    {"cost": 25, "type": "damage",  "multiplier": 1.0, "status": ("def_down", 3, 3)},
    "Arcane Burst":  {"cost": 40, "type": "double",  "multiplier": 1.0, "status": None},
}

FINAL_BOSS_ABILITY_TEXT = {
    "Power Strike":  "You swing with everything you have. Your blade passes through him like smoke.",
    "Shield Bash":   "You charge forward. He does not move. You are the one who stumbles.",
    "War Cry":       "Your lungs fill with rage, but nothing escapes your mouth.",
    "Backstab":      "You move faster than thought. He is already looking at you when you arrive.",
    "Smoke Bomb":    "The smoke billows around you. When it clears, he is still there. Still watching.",
    "Poison Blade":  "The poison drips from your blade. He watches it fall to the floor with something like amusement.",
    "Fireball":      "The spell leaves your hand. It dies before it reaches him.",
    "Frost Nova":    "The air around him does not change. If anything, you feel colder.",
    "Arcane Burst":  "You pour everything into the cast. The magic unravels. He tilts his head slightly.",
}

def get_active_set_bonus(player):
    set_name, set_data = get_equipped_set(player)
    if set_data:
        return set_data["bonus"]
    return None

def handle_on_hit(player, enemy, weapon, set_bonus=None):
    if not weapon:
        return
    on_hit = weapon.get("on_hit")
    if not on_hit:
        return

    if on_hit == "poison_half":
        if not hasattr(player, 'poison_half_counter'):
            player.poison_half_counter = 0
        player.poison_half_counter += 1
        if player.poison_half_counter >= 2:
            player.poison_half_counter = 0
            poison_val = int(player.atk * 0.20)
            apply_status(enemy, 'poison', poison_val, 5)
            print(f"  {Fore.MAGENTA}Spider Fang Blade drips poison!{Style.RESET_ALL}")

    elif on_hit == "def_down":
        apply_status(enemy, 'def_down', 3, 3)
        print(f"  {Fore.MAGENTA}Banewraith Blade corrodes the enemy's armour!{Style.RESET_ALL}")

    elif on_hit == "poison_stack":
        poison_val = int(player.atk * 0.20)
        apply_status(enemy, 'poison', poison_val, 5)
        print(f"  {Fore.MAGENTA}Corruption Staff seeps poison!{Style.RESET_ALL}")

    elif on_hit == "self_damage_10":
        if random.randint(1, 100) <= 10:
            dmg = max(1, int(player.hp * 0.05))
            player.hp -= dmg
            print(f"  {Fore.RED}The Rusty Halberd cuts you for {dmg} damage!{Style.RESET_ALL}")

    elif on_hit == "spd_up_0.1":
        increment = 0.1
        if set_bonus == "mind_ascendant":
            increment = 0.2
        player.base_spd += increment
        player.spd = player.base_spd
        print(f"  {Fore.CYAN}Blade of the Elder Mind sharpens your reflexes! SPD +{increment:.1f}{Style.RESET_ALL}")

    elif on_hit == "burn_stack":
        eternal = set_bonus == "eternal_inferno"
        apply_burn(enemy, stacks=1, ignore_immune=eternal)
        print(f"  {Fore.MAGENTA}The Eternal Flame Blade ignites the enemy!{Style.RESET_ALL}")

    elif on_hit == "instant_kill_1":
        chance = 5 if set_bonus == "void_incarnate" else 1
        if random.randint(1, 100) <= chance:
            enemy.hp = 0
            print(f"  {Fore.YELLOW}The Blade of the Abyss tears through reality! Instant kill!{Style.RESET_ALL}")

def handle_on_kill(player, enemy, set_bonus=None):
    weapon = player.equipped.get("weapon")
    if weapon and weapon.get("on_kill") == "atk_up_2":
        player.base_atk += 2
        player.atk = player.base_atk
        print(f"  {Fore.YELLOW}Souldrainer feeds on the kill! ATK permanently +2!{Style.RESET_ALL}")

    if set_bonus == "reapers_pact":
        if player.hp <= int(player.max_hp * 0.30):
            player.base_atk += 2
            player.atk = player.base_atk
            print(f"  {Fore.YELLOW}Reaper's Pact! ATK permanently +2!{Style.RESET_ALL}")

def handle_accessory_on_kill(player):
    accessory = player.equipped.get("accessory")
    if not accessory:
        return
    special = accessory.get("special", "")
    if special == "hp_restore_5_on_kill":
        restore = int(player.max_hp * 0.05)
        player.hp = min(player.hp + restore, player.max_hp)
        print(f"  {Fore.GREEN}Amulet of the Wild restores {restore} HP!{Style.RESET_ALL}")
    elif special == "hp_restore_15_on_kill":
        restore = int(player.max_hp * 0.15)
        player.hp = min(player.hp + restore, player.max_hp)
        print(f"  {Fore.GREEN}Shield of Eternal Night restores {restore} HP!{Style.RESET_ALL}")

def handle_sael(player, enemy):
    if enemy.name != "Sael, the Debt Collector":
        return
    drain = max(1, int(player.gold * 0.05))
    player.gold = max(0, player.gold - drain)
    print(f"  {Fore.YELLOW}Sael drains {drain}g from you. (Gold remaining: {player.gold}g){Style.RESET_ALL}")
    if player.gold == 0 and not enemy.enraged:
        enemy.atk = int(enemy.atk * 1.2)
        enemy.enraged = True
        print(f"  {Fore.RED}Sael: \"You have nothing left to give. Then I will take something else.\"{Style.RESET_ALL}")

def use_item(player, enemy=None):
    consumables = [item for item in player.inventory if item["slot"] == "consumable"]
    if not consumables:
        print(f"  {Fore.RED}No items to use!{Style.RESET_ALL}")
        return
    print("\n  Choose an item:")
    for i, item in enumerate(consumables, 1):
        print(f"  {i}. {item['name']} — {item['desc']}")
    choice = input("\n  > ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(consumables)):
        print("  Invalid choice, no item used.")
        return
    item = consumables[int(choice) - 1]

    if "hp" in item["bonus"]:
        restore = int(player.max_hp * item["bonus"]["hp"])
        player.hp = min(player.hp + restore, player.max_hp)
        print(f"  {Fore.GREEN}Used {item['name']}! Restored {restore} HP.{Style.RESET_ALL}")
    if "mp" in item["bonus"]:
        restore = int(player.max_mp * item["bonus"]["mp"])
        player.mp = min(player.mp + restore, player.max_mp)
        print(f"  {Fore.BLUE}Used {item['name']}! Restored {restore} MP.{Style.RESET_ALL}")
    if "hp_set" in item["bonus"]:
        player.hp = max(1, int(player.max_hp * item["bonus"]["hp_set"]))
        print(f"  {Fore.RED}You drink the {item['name']}... your vision goes red.{Style.RESET_ALL}")
    if "atk_up" in item["bonus"]:
        apply_status(player, 'atk_up', item["bonus"]["atk_up"], 3)
        print(f"  {Fore.GREEN}Used {item['name']}! ATK increased!{Style.RESET_ALL}")
    if "def_up" in item["bonus"]:
        apply_status(player, 'def_up', item["bonus"]["def_up"], 3)
        print(f"  {Fore.GREEN}Used {item['name']}! DEF increased!{Style.RESET_ALL}")
    if "spd_up" in item["bonus"]:
        apply_status(player, 'spd_up', item["bonus"]["spd_up"], 3)
        print(f"  {Fore.GREEN}Used {item['name']}! SPD increased!{Style.RESET_ALL}")
    if "poison" in item["bonus"] and enemy:
        poison_val = int(player.atk * 0.20)
        for _ in range(2):
            apply_status(enemy, 'poison', poison_val, 5)
        print(f"  {Fore.MAGENTA}Used {item['name']}! Enemy poisoned!{Style.RESET_ALL}")
    if "burn" in item["bonus"] and enemy:
        apply_burn(enemy, stacks=2)
    if "def_down" in item["bonus"] and enemy:
        for _ in range(2):
            apply_status(enemy, 'def_down', item["bonus"]["def_down"], 3)
        print(f"  {Fore.MAGENTA}Used {item['name']}! Enemy defence reduced!{Style.RESET_ALL}")

    player.inventory.remove(item)

def choose_ability(player, enemy, set_bonus=None):
    abilities = CLASS_ABILITIES[player.char_class]
    print("\n  Choose an ability:")
    for i, ab in enumerate(abilities, 1):
        cost = ABILITIES[ab]["cost"]
        if set_bonus == "forbidden_mastery":
            cost = max(1, int(cost * 0.2))
        mp_note = "" if player.mp >= cost else f" {Fore.RED}(not enough MP){Style.RESET_ALL}"
        print(f"  {i}. {Fore.CYAN}{ab}{Style.RESET_ALL} ({Fore.BLUE}{cost} MP{Style.RESET_ALL}){mp_note}")
    choice = input("\n  > ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(abilities):
        ability = abilities[int(choice) - 1]
        use_ability(player, enemy, ability, set_bonus)
    else:
        print("  Invalid choice, you hesitate!")

def use_ability(player, enemy, ability, set_bonus=None):
    data = ABILITIES.get(ability)
    if not data:
        print("  Unknown ability!")
        return False

    cost = data["cost"]
    if set_bonus == "forbidden_mastery":
        cost = max(1, int(cost * 0.2))

    if player.mp < cost:
        print(f"  {Fore.RED}Not enough MP!{Style.RESET_ALL}")
        return False
    player.mp -= cost

    atype = data["type"]
    mult  = data["multiplier"]
    status = data["status"]

    def do_hit(multiplier):
        dmg = enemy.take_damage(int(player.atk * multiplier))
        weapon = player.equipped.get("weapon")
        if weapon:
            handle_on_hit(player, enemy, weapon, set_bonus)
        return dmg

    if atype == "damage":
        dmg = do_hit(mult)
        print(f"  {Fore.CYAN}{ability}!{Style.RESET_ALL} {Fore.GREEN}You deal {dmg} damage!{Style.RESET_ALL}")
        if set_bonus == "forbidden_mastery" and random.randint(1, 100) <= 15:
            dmg2 = do_hit(mult)
            print(f"  {Fore.YELLOW}Forbidden Mastery! The spell echoes for {dmg2} extra damage!{Style.RESET_ALL}")

    elif atype == "double":
        dmg1 = do_hit(mult)
        dmg2 = do_hit(mult)
        print(f"  {Fore.CYAN}{ability}!{Style.RESET_ALL} {Fore.GREEN}Two hits for {dmg1} and {dmg2} damage!{Style.RESET_ALL}")
        if set_bonus == "forbidden_mastery" and random.randint(1, 100) <= 15:
            dmg3 = do_hit(mult)
            print(f"  {Fore.YELLOW}Forbidden Mastery! A third strike for {dmg3} damage!{Style.RESET_ALL}")

    elif atype == "buff":
        print(f"  {Fore.CYAN}{ability}!{Style.RESET_ALL}")

    if status:
        effect, value, max_stacks = status
        if effect == "poison":
            value = int(player.atk * 0.20)
        elif effect == "spd_up":
            value = player.spd
        apply_status(enemy if effect in ("atk_down", "def_down", "poison") else player, effect, value, max_stacks)

    return True

def show_turn_header(player, enemy, set_bonus=None):
    abilities = CLASS_ABILITIES[player.char_class]
    consumables = [item for item in player.inventory if item["slot"] == "consumable"]

    print(f"\n  {'='*40}")
    print(f"  {Fore.RED}{enemy.name}{Style.RESET_ALL}")
    print(f"  HP: {Fore.RED}{enemy.hp}/{enemy.max_hp}{Style.RESET_ALL}")
    print(f"  {'='*40}")
    print(f"\n  {player.name} | {Fore.GREEN}HP: {player.hp}/{player.max_hp}{Style.RESET_ALL} | {Fore.BLUE}MP: {player.mp}/{player.max_mp}{Style.RESET_ALL}")

    if set_bonus:
        print(f"  {Fore.YELLOW}Set Bonus: {set_bonus.replace('_', ' ').title()}{Style.RESET_ALL}")

    print(f"\n  Abilities:")
    for ab in abilities:
        cost = ABILITIES[ab]["cost"]
        if set_bonus == "forbidden_mastery":
            cost = max(1, int(cost * 0.2))
        mp_note = "" if player.mp >= cost else f" {Fore.RED}(not enough MP){Style.RESET_ALL}"
        print(f"    - {Fore.CYAN}{ab}{Style.RESET_ALL} ({Fore.BLUE}{cost} MP{Style.RESET_ALL}){mp_note}")

    if consumables:
        print(f"\n  Inventory:")
        for item in consumables:
            colour = rarity_colour(item)
            print(f"    - {colour}{item['name']}{Style.RESET_ALL} — {item['desc']}")
    else:
        print(f"\n  Inventory: empty")

    print(f"\n  What will you do?")
    print(f"  1. Attack")
    print(f"  2. Ability")
    print(f"  3. Use Item")
    print(f"  4. Attack + Use Item")
    print(f"  5. Ability + Use Item")

def show_enemy_art(enemy):
    for line in get_enemy_art(enemy.name):
        print(f"  {Fore.RED}{line}{Style.RESET_ALL}")

def combat_final_boss(player, enemy):
    print()
    show_enemy_art(enemy)
    print(f"\n  {Fore.RED}The hooded stranger rises from his chair.{Style.RESET_ALL}")
    print(f"  {Fore.RED}\"So. You actually made it.\"{Style.RESET_ALL}")
    print(f"\n  HP:  {Fore.RED}???{Style.RESET_ALL}")
    print(f"  ATK: {Fore.RED}???{Style.RESET_ALL}")
    print(f"  DEF: {Fore.RED}???{Style.RESET_ALL}\n")

    turn_index = 0
    set_bonus = get_active_set_bonus(player)

    while player.hp > 0:
        print(f"\n  {'='*40}")
        print(f"  {Fore.RED}???{Style.RESET_ALL}")
        print(f"  HP: {Fore.RED}???{Style.RESET_ALL}")
        print(f"  {'='*40}")
        print(f"\n  {player.name} | {Fore.GREEN}HP: {player.hp}/{player.max_hp}{Style.RESET_ALL} | {Fore.BLUE}MP: {player.mp}/{player.max_mp}{Style.RESET_ALL}")

        abilities = CLASS_ABILITIES[player.char_class]
        print(f"\n  Abilities:")
        for ab in abilities:
            print(f"    - {Fore.CYAN}{ab}{Style.RESET_ALL}")

        consumables = [item for item in player.inventory if item["slot"] == "consumable"]
        if consumables:
            print(f"\n  Inventory:")
            for item in consumables:
                colour = rarity_colour(item)
                print(f"    - {colour}{item['name']}{Style.RESET_ALL} — {item['desc']}")
        else:
            print(f"\n  Inventory: empty")

        print(f"\n  What will you do?")
        print(f"  1. Attack")
        print(f"  2. Ability")
        print(f"  3. Use Item")
        print(f"  4. Attack + Use Item")
        print(f"  5. Ability + Use Item")

        action = input("\n  > ").strip()

        if action in ("1", "4"):
            weapon = player.equipped.get("weapon")
            if weapon and weapon.get("on_hit") == "instant_kill_1":
                chance = 5 if set_bonus == "void_incarnate" else 1
                if random.randint(1, 100) <= chance:
                    print(f"\n  {Fore.YELLOW}The Blade of the Abyss tears through reality!{Style.RESET_ALL}")
                    print(f"  {Fore.RED}???: \"...finally. Someone read the item description.\"{Style.RESET_ALL}")
                    print(f"\n  {Fore.YELLOW}*** THE DUNGEON HAS BEEN DEFEATED. ***{Style.RESET_ALL}")
                    return "victory_final"
            print(f"  You attack. Your strike lands but draws no reaction.")
            if action == "4":
                print(f"  You reach for your supplies. He watches patiently. Nothing seems to help.")

        elif action in ("2", "5"):
            print(f"\n  Choose an ability:")
            for i, ab in enumerate(abilities, 1):
                print(f"  {i}. {Fore.CYAN}{ab}{Style.RESET_ALL}")
            choice = input("\n  > ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(abilities):
                ability = abilities[int(choice) - 1]
                print(f"  {FINAL_BOSS_ABILITY_TEXT.get(ability, 'Nothing happens.')}")
            if action == "5":
                print(f"  You reach for your supplies. He watches patiently. Nothing seems to help.")

        elif action == "3":
            print(f"  You reach for your supplies. He watches patiently. Nothing seems to help.")

        else:
            print("  Invalid choice.")

        print(f"\n  {FINAL_BOSS_TURN_TEXT[turn_index % len(FINAL_BOSS_TURN_TEXT)]}")
        turn_index += 1

        dmg = int(player.max_hp * 0.20)
        player.hp = max(0, player.hp - dmg)
        print(f"  {Fore.RED}He reaches out. You lose {dmg} HP. ({player.hp}/{player.max_hp} HP remaining){Style.RESET_ALL}")

        if player.hp <= 0:
            print(f"\n  {Fore.RED}???: \"You were so close.\"{Style.RESET_ALL}")
            print(f"\n  {Fore.RED}You have been defeated by ???...{Style.RESET_ALL}")
            return "dead"

    return "dead"

def combat(player, enemy):
    if hasattr(enemy, 'is_boss') and enemy.name == "???":
        return combat_final_boss(player, enemy)

    print()
    show_enemy_art(enemy)
    print(f"\n  {Fore.RED}A {enemy.name} appears!{Style.RESET_ALL}")
    print(f"  HP: {Fore.RED}{enemy.hp}{Style.RESET_ALL} | ATK: {Fore.RED}{enemy.atk}{Style.RESET_ALL} | DEF: {enemy.defense}\n")

    set_bonus = get_active_set_bonus(player)
    eternal_inferno = set_bonus == "eternal_inferno"
    first_hit_blocked = False

    accessory = player.equipped.get("accessory")
    if accessory and accessory.get("special") == "block_first_hit":
        first_hit_blocked = True

    while player.hp > 0 and enemy.is_alive():

        tick_statuses(enemy, eternal_inferno=eternal_inferno)
        if not enemy.is_alive():
            break

        if 'def_down' in enemy.status_effects:
            reduction = enemy.status_effects['def_down']['value'] * enemy.status_effects['def_down']['stacks']
            enemy.defense = max(0, int(enemy.base_defense - reduction))
        else:
            enemy.defense = enemy.base_defense

        bonus_atk = 0
        bonus_def = 0
        bonus_spd = 0
        if player.status_effects:
            if 'atk_up' in player.status_effects:
                bonus_atk = player.status_effects['atk_up']['value'] * player.status_effects['atk_up']['stacks']
            if 'def_up' in player.status_effects:
                bonus_def = player.status_effects['def_up']['value'] * player.status_effects['def_up']['stacks']
            if 'spd_up' in player.status_effects:
                bonus_spd = player.status_effects['spd_up']['value'] * player.status_effects['spd_up']['stacks']

        player.atk = int(player.base_atk + bonus_atk)
        player.defense = int(player.base_defense + bonus_def)
        player.spd = int(player.base_spd + bonus_spd)

        if set_bonus == "last_stand" and player.hp <= int(player.max_hp * 0.20):
            player.atk *= 2
            player.defense *= 2
            print(f"  {Fore.YELLOW}Last Stand! ATK and DEF doubled!{Style.RESET_ALL}")

        show_turn_header(player, enemy, set_bonus)
        action = input("\n  > ").strip()

        if action == "1":
            dmg = enemy.take_damage(player.atk)
            print(f"  {Fore.GREEN}You attack for {dmg} damage! ({enemy.hp}/{enemy.max_hp} HP remaining){Style.RESET_ALL}")
            handle_on_hit(player, enemy, player.equipped.get("weapon"), set_bonus)

        elif action == "2":
            choose_ability(player, enemy, set_bonus)

        elif action == "3":
            use_item(player, enemy)

        elif action == "4":
            dmg = enemy.take_damage(player.atk)
            print(f"  {Fore.GREEN}You attack for {dmg} damage! ({enemy.hp}/{enemy.max_hp} HP remaining){Style.RESET_ALL}")
            handle_on_hit(player, enemy, player.equipped.get("weapon"), set_bonus)
            if not enemy.is_alive():
                break
            use_item(player, enemy)

        elif action == "5":
            choose_ability(player, enemy, set_bonus)
            if not enemy.is_alive():
                break
            use_item(player, enemy)

        else:
            print("  Invalid choice, you hesitate!")

        if not enemy.is_alive():
            handle_on_kill(player, enemy, set_bonus)
            handle_accessory_on_kill(player)
            break

        tick_statuses(player)
        print(f"\n  --- {Fore.RED}{enemy.name}'s turn{Style.RESET_ALL} ---")

        enemy_atk = enemy.atk
        if 'atk_down' in enemy.status_effects:
            reduction = enemy.status_effects['atk_down']['value'] * enemy.status_effects['atk_down']['stacks']
            enemy_atk = max(1, int(enemy.atk - reduction))

        ring = player.equipped.get("ring")
        if ring and ring.get("special") == "fire_resist_10" and enemy.name in BURN_IMMUNE:
            enemy_atk = int(enemy_atk * 0.9)

        handle_sael(player, enemy)

        if set_bonus == "unyielding_stone" and random.randint(1, 100) <= 20:
            print(f"  {Fore.CYAN}Unyielding Stone! You absorb the hit!{Style.RESET_ALL}")
        elif first_hit_blocked:
            print(f"  {Fore.CYAN}Igris's Oathbound Shield blocks the attack!{Style.RESET_ALL}")
            first_hit_blocked = False
        else:
            evade_chance = max(0, (player.spd / (player.spd + enemy.atk)) * 100 - 20)

            armor = player.equipped.get("armor")
            boots = player.equipped.get("boots")
            if armor and armor.get("special") == "evasion_10":
                evade_chance += 10
            if boots and boots.get("special") == "evasion_5":
                evade_chance += 5

            if random.randint(1, 100) <= evade_chance:
                print(f"  {Fore.CYAN}You dodge the {enemy.name}'s attack!{Style.RESET_ALL}")
            else:
                dmg = player.take_damage(enemy_atk)
                accessory = player.equipped.get("accessory")
                if accessory and accessory.get("special") == "burn_resist_50":
                    dmg = int(dmg * 0.5)
                    player.hp += int(dmg * 0.5)
                if player.hp <= 0:
                    armor = player.equipped.get("armor")
                    if armor and armor.get("special") == "death_save" and not armor.get("used"):
                        player.hp = 1
                        armor["used"] = True
                        print(f"  {Fore.YELLOW}The Deathless Shroud saves you! It crumbles to dust.{Style.RESET_ALL}")
                        player.equipped["armor"] = None
                    else:
                        print(f"  {Fore.RED}{enemy.name} strikes you for {dmg} damage! You have been slain.{Style.RESET_ALL}")
                        break
                else:
                    print(f"  {Fore.RED}{enemy.name} strikes you for {dmg} damage! ({player.hp}/{player.max_hp} HP remaining){Style.RESET_ALL}")

                accessory = player.equipped.get("accessory")
                if accessory and accessory.get("special") == "reflect_10":
                    reflect = max(1, int(dmg * 0.1))
                    enemy.hp -= reflect
                    print(f"  {Fore.GREEN}Reflected {reflect} damage!{Style.RESET_ALL}")

    if player.hp <= 0:
        print(f"\n  {Fore.RED}You have been defeated by {enemy.name}...{Style.RESET_ALL}")
        return "dead"
    else:
        print(f"\n  {Fore.GREEN}You defeated {enemy.name}!{Style.RESET_ALL}")
        player.gain_xp(enemy.xp)

        if enemy.name == "Sael, the Debt Collector":
            print(f"  {Fore.RED}Sael: \"The debt... is cleared.\"{Style.RESET_ALL}")
            player.gold += enemy.gold * 2
            print(f"  {Fore.YELLOW}Sael releases his collection. +{enemy.gold * 2}g{Style.RESET_ALL}")
        else:
            player.gold += enemy.gold
            print(f"  {Fore.YELLOW}+{enemy.xp} XP | +{enemy.gold} gold{Style.RESET_ALL}")

        if set_bonus == "void_incarnate" and random.randint(1, 100) <= 15:
            print(f"  {Fore.YELLOW}Void Incarnate! The next combat will be skipped.{Style.RESET_ALL}")
            player.skip_next_combat = True

        return "victory"