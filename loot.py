import random
from colorama import Fore, Style

RARITY_COLOURS = {
    "common":    Style.RESET_ALL,
    "uncommon":  Fore.GREEN,
    "rare":      Fore.BLUE,
    "legendary": Fore.YELLOW,
}

def rarity_colour(item):
    rarity = item.get("rarity", "common")
    return RARITY_COLOURS.get(rarity, Style.RESET_ALL)

CONSUMABLES = {
    "Health Potion": {
        "slot": "consumable",
        "rarity": "common",
        "bonus": {"hp": 0.33},
        "desc": "Restores 33% of your max HP",
    },
    "Mana Potion": {
        "slot": "consumable",
        "rarity": "common",
        "bonus": {"mp": 0.33},
        "desc": "Restores 33% of your max MP",
    },
    "Elixir": {
        "slot": "consumable",
        "rarity": "uncommon",
        "bonus": {"hp": 0.33, "mp": 0.33},
        "desc": "Restores 33% HP and 33% MP",
    },
    "Strength Potion": {
        "slot": "consumable",
        "rarity": "uncommon",
        "bonus": {"atk_up": 5},
        "desc": "Boosts ATK by 5 for 3 turns",
    },
    "Defense Potion": {
        "slot": "consumable",
        "rarity": "uncommon",
        "bonus": {"def_up": 5},
        "desc": "Boosts DEF by 5 for 3 turns",
    },
    "Speed Potion": {
        "slot": "consumable",
        "rarity": "uncommon",
        "bonus": {"spd_up": 5},
        "desc": "Boosts SPD by 5 for 3 turns",
    },
    "Poison Flask": {
        "slot": "consumable",
        "rarity": "rare",
        "bonus": {"poison": True},
        "desc": "Applies 2 poison stacks to the enemy",
    },
    "Napalm Flask": {
        "slot": "consumable",
        "rarity": "rare",
        "bonus": {"burn": True},
        "desc": "Applies 2 burn stacks to the enemy (weak/immune system applies)",
    },
    "Metal Jawed Termite": {
        "slot": "consumable",
        "rarity": "rare",
        "bonus": {"def_down": 3},
        "desc": "Applies 2 DEF down stacks to the enemy",
    },
    "Grand Elixir": {
        "slot": "consumable",
        "rarity": "legendary",
        "bonus": {"hp": 1.0, "mp": 1.0},
        "desc": "Fully restores HP and MP",
    },
    "Crimson Dew": {
        "slot": "consumable",
        "rarity": "rare",
        "bonus": {"hp_set": 0.20},
        "desc": "A dark red drink sold by the barkeep. What could go wrong?",
    },
}

WEAPONS = {
    # The Forest (floors 1-10)
    "Worn Hatchet":        {"slot": "weapon", "rarity": "common",    "zone": (1,10),   "bonus": {"atk": 2}},
    "Hunter's Blade":      {"slot": "weapon", "rarity": "common",    "zone": (1,10),   "bonus": {"atk": 3}},
    "Goblin Stabber":      {"slot": "weapon", "rarity": "common",    "zone": (1,10),   "bonus": {"atk": 3}},
    "Forester's Axe":      {"slot": "weapon", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"atk": 5}},
    "Fang Blade":          {"slot": "weapon", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"atk": 4, "spd": 1}},
    "Wolf's Tooth Dagger": {"slot": "weapon", "rarity": "rare",      "zone": (1,10),   "bonus": {"atk": 6, "spd": 2}},
    "Thornwood Staff":     {"slot": "weapon", "rarity": "rare",      "zone": (1,10),   "bonus": {"atk": 7, "max_mp": 10}},
    "Sylvan Blade":        {"slot": "weapon", "rarity": "legendary", "zone": (1,10),   "bonus": {"atk": 9, "spd": 3}},

    # The Mines (floors 11-20)
    "Miner's Pick":        {"slot": "weapon", "rarity": "common",    "zone": (11,20),  "bonus": {"atk": 4}},
    "Crude Iron Sword":    {"slot": "weapon", "rarity": "common",    "zone": (11,20),  "bonus": {"atk": 5}},
    "Kobold Cleaver":      {"slot": "weapon", "rarity": "common",    "zone": (11,20),  "bonus": {"atk": 5}},
    "Reinforced Pickaxe":  {"slot": "weapon", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"atk": 7}},
    "Cave Iron Sword":     {"slot": "weapon", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"atk": 8}},
    "Spider Fang Blade":   {"slot": "weapon", "rarity": "rare",      "zone": (11,20),  "bonus": {"atk": 9, "spd": 2}, "on_hit": "poison_half"},
    "Golem Shard Blade":   {"slot": "weapon", "rarity": "rare",      "zone": (11,20),  "bonus": {"atk": 10, "def": 2}},
    "Earthcleaver":        {"slot": "weapon", "rarity": "legendary", "zone": (11,20),  "bonus": {"atk": 13, "def": 3}},

    # The Crypt (floors 21-30)
    "Bone Sword":          {"slot": "weapon", "rarity": "common",    "zone": (21,30),  "bonus": {"atk": 7}},
    "Grave Dirk":          {"slot": "weapon", "rarity": "common",    "zone": (21,30),  "bonus": {"atk": 8}},
    "Ghoul Claw Blade":    {"slot": "weapon", "rarity": "common",    "zone": (21,30),  "bonus": {"atk": 8}},
    "Crypt Reaper":        {"slot": "weapon", "rarity": "uncommon",  "zone": (21,30),  "bonus": {"atk": 10}},
    "Souldrainer":         {"slot": "weapon", "rarity": "rare",      "zone": (21,30),  "bonus": {"atk": 9}, "on_kill": "atk_up_2"},
    "Banewraith Blade":    {"slot": "weapon", "rarity": "rare",      "zone": (21,30),  "bonus": {"atk": 12}, "on_hit": "def_down"},
    "Staff of the Dead":   {"slot": "weapon", "rarity": "rare",      "zone": (21,30),  "bonus": {"atk": 13}},
    "Eternal Dirge":       {"slot": "weapon", "rarity": "legendary", "zone": (21,30),  "bonus": {"atk": 16, "spd": 4}},

    # The Ruined Castle (floors 31-40)
    "Shattered Lance":     {"slot": "weapon", "rarity": "common",    "zone": (31,40),  "bonus": {"atk": 10}},
    "Guardsman's Sword":   {"slot": "weapon", "rarity": "common",    "zone": (31,40),  "bonus": {"atk": 11}},
    "Rusty Halberd":       {"slot": "weapon", "rarity": "common",    "zone": (31,40),  "bonus": {"atk": 11}, "on_hit": "self_damage_10"},
    "Knight's Blade":      {"slot": "weapon", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"atk": 13}},
    "Banshee Wail Staff":  {"slot": "weapon", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"atk": 12, "spd": 3}},
    "Oathbreaker":         {"slot": "weapon", "rarity": "rare",      "zone": (31,40),  "bonus": {"atk": 15}},
    "Royal Executioner":   {"slot": "weapon", "rarity": "rare",      "zone": (31,40),  "bonus": {"atk": 16}},
    "Igris's Honour Blade":{"slot": "weapon", "rarity": "legendary", "zone": (31,40),  "bonus": {"atk": 20, "def": 5}},

    # The Dark Mage School (floors 41-50)
    "Apprentice Wand":     {"slot": "weapon", "rarity": "common",    "zone": (41,50),  "bonus": {"atk": 13}},
    "Arcane Rod":          {"slot": "weapon", "rarity": "common",    "zone": (41,50),  "bonus": {"atk": 14}},
    "Spell Dagger":        {"slot": "weapon", "rarity": "common",    "zone": (41,50),  "bonus": {"atk": 14}},
    "Runed Blade":         {"slot": "weapon", "rarity": "uncommon",  "zone": (41,50),  "bonus": {"atk": 16}},
    "Corruption Staff":    {"slot": "weapon", "rarity": "rare",      "zone": (41,50),  "bonus": {"atk": 15, "spd": 4}, "on_hit": "poison_stack"},
    "Spellbreaker":        {"slot": "weapon", "rarity": "rare",      "zone": (41,50),  "bonus": {"atk": 18}},
    "Voss's Tome Blade":   {"slot": "weapon", "rarity": "rare",      "zone": (41,50),  "bonus": {"atk": 19}},
    "Staff of Unmaking":   {"slot": "weapon", "rarity": "legendary", "zone": (41,50),  "bonus": {"atk": 24, "spd": 6}},

    # The Underdark (floors 51-60)
    "Shadow Blade":            {"slot": "weapon", "rarity": "common",    "zone": (51,60),  "bonus": {"atk": 16}},
    "Duergar Axe":             {"slot": "weapon", "rarity": "common",    "zone": (51,60),  "bonus": {"atk": 17}},
    "Mind Spike":              {"slot": "weapon", "rarity": "common",    "zone": (51,60),  "bonus": {"atk": 17}},
    "Assassin's Edge":         {"slot": "weapon", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"atk": 19, "spd": 4}},
    "Flayer Staff":            {"slot": "weapon", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"atk": 18}},
    "Krakenbone Sword":        {"slot": "weapon", "rarity": "rare",      "zone": (51,60),  "bonus": {"atk": 22, "def": 4}},
    "Void Touched Blade":      {"slot": "weapon", "rarity": "rare",      "zone": (51,60),  "bonus": {"atk": 23}},
    "Blade of the Elder Mind": {"slot": "weapon", "rarity": "legendary", "zone": (51,60),  "bonus": {"atk": 28, "spd": 8}, "on_hit": "spd_up_0.1"},

    # The Core (floors 61-70)
    "Ember Sword":             {"slot": "weapon", "rarity": "common",    "zone": (61,70),  "bonus": {"atk": 20}},
    "Demon Iron Blade":        {"slot": "weapon", "rarity": "common",    "zone": (61,70),  "bonus": {"atk": 21}},
    "Ashen Spear":             {"slot": "weapon", "rarity": "common",    "zone": (61,70),  "bonus": {"atk": 21}},
    "Infernal Cleaver":        {"slot": "weapon", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"atk": 23}},
    "Drake Fang Blade":        {"slot": "weapon", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"atk": 22, "spd": 5}},
    "Hellforged Sword":        {"slot": "weapon", "rarity": "rare",      "zone": (61,70),  "bonus": {"atk": 26}},
    "Ignarath's Ember":        {"slot": "weapon", "rarity": "rare",      "zone": (61,70),  "bonus": {"atk": 28}},
    "The Eternal Flame Blade": {"slot": "weapon", "rarity": "legendary", "zone": (61,70),  "bonus": {"atk": 34, "spd": 10}, "on_hit": "burn_stack"},

    # The Abyss (floors 71+)
    "Void Shard":          {"slot": "weapon", "rarity": "common",    "zone": (71,999), "bonus": {"atk": 24}},
    "Soul Blade":          {"slot": "weapon", "rarity": "common",    "zone": (71,999), "bonus": {"atk": 25}},
    "Nightmare Edge":      {"slot": "weapon", "rarity": "common",    "zone": (71,999), "bonus": {"atk": 25}},
    "Abyssal Cleaver":     {"slot": "weapon", "rarity": "uncommon",  "zone": (71,999), "bonus": {"atk": 28}},
    "Wraith Fang":         {"slot": "weapon", "rarity": "uncommon",  "zone": (71,999), "bonus": {"atk": 27, "spd": 6}},
    "The Undying Blade":   {"slot": "weapon", "rarity": "rare",      "zone": (71,999), "bonus": {"atk": 32}},
    "Soul Eater's Fang":   {"slot": "weapon", "rarity": "rare",      "zone": (71,999), "bonus": {"atk": 34}},
    "Blade of the Abyss":  {"slot": "weapon", "rarity": "legendary", "zone": (71,999), "bonus": {"atk": 40, "spd": 12}, "on_hit": "instant_kill_1"},
}

ARMOR = {
    # The Forest (floors 1-10)
    "Tattered Leathers":      {"slot": "armor", "rarity": "common",    "zone": (1,10),   "bonus": {"def": 2}},
    "Wolfskin Vest":          {"slot": "armor", "rarity": "common",    "zone": (1,10),   "bonus": {"def": 3}},
    "Bark Plating":           {"slot": "armor", "rarity": "common",    "zone": (1,10),   "bonus": {"def": 3}},
    "Ranger's Coat":          {"slot": "armor", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"def": 5}},
    "Thornweave Armour":      {"slot": "armor", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"def": 4, "max_hp": 10}},
    "Bearskin Mantle":        {"slot": "armor", "rarity": "rare",      "zone": (1,10),   "bonus": {"def": 7, "max_hp": 20}},
    "Druidic Plate":          {"slot": "armor", "rarity": "rare",      "zone": (1,10),   "bonus": {"def": 8}},
    "Armour of the Wild":     {"slot": "armor", "rarity": "legendary", "zone": (1,10),   "bonus": {"def": 11, "max_hp": 30}},

    # The Mines (floors 11-20)
    "Miner's Jerkin":         {"slot": "armor", "rarity": "common",    "zone": (11,20),  "bonus": {"def": 4}},
    "Stone Plating":          {"slot": "armor", "rarity": "common",    "zone": (11,20),  "bonus": {"def": 5}},
    "Kobold Hide":            {"slot": "armor", "rarity": "common",    "zone": (11,20),  "bonus": {"def": 5}},
    "Iron Layered Vest":      {"slot": "armor", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"def": 7}},
    "Golem Shell Fragment":   {"slot": "armor", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"def": 8, "max_hp": 15}},
    "Cave Iron Plate":        {"slot": "armor", "rarity": "rare",      "zone": (11,20),  "bonus": {"def": 10, "max_hp": 25}},
    "Stonehide Armour":       {"slot": "armor", "rarity": "rare",      "zone": (11,20),  "bonus": {"def": 11}},
    "Armour of the Deep":     {"slot": "armor", "rarity": "legendary", "zone": (11,20),  "bonus": {"def": 14, "max_hp": 40}},

    # The Crypt (floors 21-30)
    "Grave Wrappings":        {"slot": "armor", "rarity": "common",    "zone": (21,30),  "bonus": {"def": 7}},
    "Bone Plate":             {"slot": "armor", "rarity": "common",    "zone": (21,30),  "bonus": {"def": 8}},
    "Mummy Bindings":         {"slot": "armor", "rarity": "common",    "zone": (21,30),  "bonus": {"def": 8}},
    "Crypt Knight Armour":    {"slot": "armor", "rarity": "uncommon",  "zone": (21,30),  "bonus": {"def": 10}},
    "Shroud of the Dead":     {"slot": "armor", "rarity": "uncommon",  "zone": (21,30),  "bonus": {"def": 9, "max_hp": 20}},
    "Soulbound Plate":        {"slot": "armor", "rarity": "rare",      "zone": (21,30),  "bonus": {"def": 13, "max_hp": 30}},
    "Armour of Eternal Rest": {"slot": "armor", "rarity": "rare",      "zone": (21,30),  "bonus": {"def": 14}},
    "Deathless Shroud":       {"slot": "armor", "rarity": "legendary", "zone": (21,30),  "bonus": {"def": 18, "max_hp": 50}, "special": "death_save"},

    # The Ruined Castle (floors 31-40)
    "Rusted Plate":               {"slot": "armor", "rarity": "common",    "zone": (31,40),  "bonus": {"def": 10}},
    "Guardsman's Mail":           {"slot": "armor", "rarity": "common",    "zone": (31,40),  "bonus": {"def": 11}},
    "Shattered Shield Coat":      {"slot": "armor", "rarity": "common",    "zone": (31,40),  "bonus": {"def": 11}},
    "Knight's Plate":             {"slot": "armor", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"def": 13}},
    "Royal Guard Armour":         {"slot": "armor", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"def": 12, "max_hp": 25}},
    "Oathbound Plate":            {"slot": "armor", "rarity": "rare",      "zone": (31,40),  "bonus": {"def": 16, "max_hp": 35}},
    "Armour of the Fallen King":  {"slot": "armor", "rarity": "rare",      "zone": (31,40),  "bonus": {"def": 17}},
    "Igris's Unbroken Plate":     {"slot": "armor", "rarity": "legendary", "zone": (31,40),  "bonus": {"def": 22, "max_hp": 60}, "special": "evasion_10"},

    # The Dark Mage School (floors 41-50)
    "Apprentice Robes":       {"slot": "armor", "rarity": "common",    "zone": (41,50),  "bonus": {"def": 13}},
    "Arcane Plating":         {"slot": "armor", "rarity": "common",    "zone": (41,50),  "bonus": {"def": 14}},
    "Scholar's Coat":         {"slot": "armor", "rarity": "common",    "zone": (41,50),  "bonus": {"def": 14}},
    "Runed Plate":            {"slot": "armor", "rarity": "uncommon",  "zone": (41,50),  "bonus": {"def": 16}},
    "Corruption Weave":       {"slot": "armor", "rarity": "uncommon",  "zone": (41,50),  "bonus": {"def": 15, "max_hp": 30}},
    "Spellguard Armour":      {"slot": "armor", "rarity": "rare",      "zone": (41,50),  "bonus": {"def": 19, "max_hp": 40}},
    "Voss's Forbidden Robes": {"slot": "armor", "rarity": "rare",      "zone": (41,50),  "bonus": {"def": 20, "max_mp": 50}},
    "Armour of Unmaking":     {"slot": "armor", "rarity": "legendary", "zone": (41,50),  "bonus": {"def": 26, "max_hp": 70}},

    # The Underdark (floors 51-60)
    "Shadow Weave":               {"slot": "armor", "rarity": "common",    "zone": (51,60),  "bonus": {"def": 16}},
    "Duergar Mail":               {"slot": "armor", "rarity": "common",    "zone": (51,60),  "bonus": {"def": 17}},
    "Flayer Hide":                {"slot": "armor", "rarity": "common",    "zone": (51,60),  "bonus": {"def": 17}},
    "Assassin's Plate":           {"slot": "armor", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"def": 19}},
    "Krakenscale Armour":         {"slot": "armor", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"def": 20, "max_hp": 35}},
    "Void Touched Plate":         {"slot": "armor", "rarity": "rare",      "zone": (51,60),  "bonus": {"def": 23, "max_hp": 50}},
    "Armour of the Elder Mind":   {"slot": "armor", "rarity": "rare",      "zone": (51,60),  "bonus": {"def": 24}},
    "Underdark Sovereign Plate":  {"slot": "armor", "rarity": "legendary", "zone": (51,60),  "bonus": {"def": 30, "max_hp": 80}},

    # The Core (floors 61-70)
    "Ember Plate":                    {"slot": "armor", "rarity": "common",    "zone": (61,70),  "bonus": {"def": 20}},
    "Demon Iron Mail":                {"slot": "armor", "rarity": "common",    "zone": (61,70),  "bonus": {"def": 21}},
    "Ashen Coat":                     {"slot": "armor", "rarity": "common",    "zone": (61,70),  "bonus": {"def": 21}},
    "Infernal Plate":                 {"slot": "armor", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"def": 23}},
    "Drake Scale Armour":             {"slot": "armor", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"def": 24, "max_hp": 40}},
    "Hellforged Plate":               {"slot": "armor", "rarity": "rare",      "zone": (61,70),  "bonus": {"def": 27, "max_hp": 55}},
    "Armour of the Eternal Flame":    {"slot": "armor", "rarity": "rare",      "zone": (61,70),  "bonus": {"def": 28}},
    "Ignarath's Ashen Plate":         {"slot": "armor", "rarity": "legendary", "zone": (61,70),  "bonus": {"def": 35, "max_hp": 90}},

    # The Abyss (floors 71+)
    "Void Plate":              {"slot": "armor", "rarity": "common",    "zone": (71,999), "bonus": {"def": 24}},
    "Soul Forged Mail":        {"slot": "armor", "rarity": "common",    "zone": (71,999), "bonus": {"def": 25}},
    "Nightmare Weave":         {"slot": "armor", "rarity": "common",    "zone": (71,999), "bonus": {"def": 25}},
    "Abyssal Plate":           {"slot": "armor", "rarity": "uncommon",  "zone": (71,999), "bonus": {"def": 28}},
    "Armour of the Undying":   {"slot": "armor", "rarity": "uncommon",  "zone": (71,999), "bonus": {"def": 29, "max_hp": 45}},
    "Void Sovereign Plate":    {"slot": "armor", "rarity": "rare",      "zone": (71,999), "bonus": {"def": 33, "max_hp": 60}},
    "Soul Eater's Carapace":   {"slot": "armor", "rarity": "rare",      "zone": (71,999), "bonus": {"def": 34}},
    "Armour of the Abyss":     {"slot": "armor", "rarity": "legendary", "zone": (71,999), "bonus": {"def": 42, "max_hp": 100}},
}

BOOTS = {
    # The Forest (floors 1-10)
    "Worn Leather Boots":      {"slot": "boots", "rarity": "common",    "zone": (1,10),   "bonus": {"spd": 2}},
    "Hunter's Treads":         {"slot": "boots", "rarity": "common",    "zone": (1,10),   "bonus": {"spd": 2}},
    "Mudwalkers":              {"slot": "boots", "rarity": "common",    "zone": (1,10),   "bonus": {"spd": 3}},
    "Boots of the Hare":       {"slot": "boots", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"spd": 4}},
    "Boots of the Giant":      {"slot": "boots", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"atk": 3}},
    "Boots of Hermes":         {"slot": "boots", "rarity": "rare",      "zone": (1,10),   "bonus": {"spd": 6}},
    "Ironsoled Stompers":      {"slot": "boots", "rarity": "rare",      "zone": (1,10),   "bonus": {"atk": 3, "def": 2}},
    "Boots of the Sylvan God": {"slot": "boots", "rarity": "legendary", "zone": (1,10),   "bonus": {"spd": 8, "atk": 4}, "special": "evasion_5"},

    # The Mines (floors 11-20)
    "Mineworker's Boots":      {"slot": "boots", "rarity": "common",    "zone": (11,20),  "bonus": {"spd": 2}},
    "Iron Toe Caps":           {"slot": "boots", "rarity": "common",    "zone": (11,20),  "bonus": {"def": 3}},
    "Kobold Kickers":          {"slot": "boots", "rarity": "common",    "zone": (11,20),  "bonus": {"spd": 3}},
    "Deepwalker Boots":        {"slot": "boots", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"spd": 5}},
    "Stonegrip Treads":        {"slot": "boots", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"def": 4}},
    "Boots of the Rock Golem": {"slot": "boots", "rarity": "rare",      "zone": (11,20),  "bonus": {"def": 5, "atk": 3}},
    "Swiftmine Treads":        {"slot": "boots", "rarity": "rare",      "zone": (11,20),  "bonus": {"spd": 7}},
    "Boots of the Deep Earth": {"slot": "boots", "rarity": "legendary", "zone": (11,20),  "bonus": {"spd": 9, "def": 5}, "special": "evasion_5"},

    # The Crypt (floors 21-30)
    "Grave Treads":            {"slot": "boots", "rarity": "common",    "zone": (21,30),  "bonus": {"spd": 3}},
    "Bone Stompers":           {"slot": "boots", "rarity": "common",    "zone": (21,30),  "bonus": {"def": 3}},
    "Mummy Wraps":             {"slot": "boots", "rarity": "common",    "zone": (21,30),  "bonus": {"spd": 4}},
    "Boots of the Restless":   {"slot": "boots", "rarity": "uncommon",  "zone": (21,30),  "bonus": {"spd": 6}},
    "Ghoul Treads":            {"slot": "boots", "rarity": "uncommon",  "zone": (21,30),  "bonus": {"def": 4, "spd": 2}},
    "Boots of the Undying":    {"slot": "boots", "rarity": "rare",      "zone": (21,30),  "bonus": {"spd": 8}},
    "Soulstepper Boots":       {"slot": "boots", "rarity": "rare",      "zone": (21,30),  "bonus": {"def": 5, "spd": 4}},
    "Boots of Eternal Night":  {"slot": "boots", "rarity": "legendary", "zone": (21,30),  "bonus": {"spd": 11, "def": 6}, "special": "evasion_5"},

    # The Ruined Castle (floors 31-40)
    "Guardsman's Boots":       {"slot": "boots", "rarity": "common",    "zone": (31,40),  "bonus": {"spd": 3}},
    "Rusted Sabatons":         {"slot": "boots", "rarity": "common",    "zone": (31,40),  "bonus": {"def": 4}},
    "Castle Treads":           {"slot": "boots", "rarity": "common",    "zone": (31,40),  "bonus": {"spd": 4}},
    "Knight's Sabatons":       {"slot": "boots", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"spd": 6}},
    "Boots of the Fallen":     {"slot": "boots", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"def": 5, "spd": 3}},
    "Oathbound Sabatons":      {"slot": "boots", "rarity": "rare",      "zone": (31,40),  "bonus": {"spd": 9}},
    "Royal Guard Treads":      {"slot": "boots", "rarity": "rare",      "zone": (31,40),  "bonus": {"def": 6, "spd": 5}},
    "Igris's Iron Boots":      {"slot": "boots", "rarity": "legendary", "zone": (31,40),  "bonus": {"spd": 13, "def": 7}, "special": "evasion_5"},

    # The Dark Mage School (floors 41-50)
    "Apprentice Slippers":     {"slot": "boots", "rarity": "common",    "zone": (41,50),  "bonus": {"spd": 4}},
    "Arcane Treads":           {"slot": "boots", "rarity": "common",    "zone": (41,50),  "bonus": {"spd": 5}},
    "Scholar's Boots":         {"slot": "boots", "rarity": "common",    "zone": (41,50),  "bonus": {"spd": 5}},
    "Runed Sabatons":          {"slot": "boots", "rarity": "uncommon",  "zone": (41,50),  "bonus": {"spd": 7}},
    "Boots of the Corrupted":  {"slot": "boots", "rarity": "uncommon",  "zone": (41,50),  "bonus": {"def": 6, "spd": 4}},
    "Spellstrider Boots":      {"slot": "boots", "rarity": "rare",      "zone": (41,50),  "bonus": {"spd": 10}},
    "Voss's Forbidden Treads": {"slot": "boots", "rarity": "rare",      "zone": (41,50),  "bonus": {"def": 7, "spd": 6}},
    "Boots of Unmaking":       {"slot": "boots", "rarity": "legendary", "zone": (41,50),  "bonus": {"spd": 15, "def": 8}, "special": "evasion_5"},

    # The Underdark (floors 51-60)
    "Shadow Treads":               {"slot": "boots", "rarity": "common",    "zone": (51,60),  "bonus": {"spd": 5}},
    "Duergar Stompers":            {"slot": "boots", "rarity": "common",    "zone": (51,60),  "bonus": {"def": 6}},
    "Flayer Slippers":             {"slot": "boots", "rarity": "common",    "zone": (51,60),  "bonus": {"spd": 6}},
    "Assassin's Treads":           {"slot": "boots", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"spd": 9}},
    "Krakenscale Boots":           {"slot": "boots", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"def": 7, "spd": 5}},
    "Void Touched Treads":         {"slot": "boots", "rarity": "rare",      "zone": (51,60),  "bonus": {"spd": 12}},
    "Boots of the Elder Mind":     {"slot": "boots", "rarity": "rare",      "zone": (51,60),  "bonus": {"def": 8, "spd": 7}},
    "Underdark Sovereign Boots":   {"slot": "boots", "rarity": "legendary", "zone": (51,60),  "bonus": {"spd": 17, "def": 10}, "special": "evasion_5"},

    # The Core (floors 61-70)
    "Ember Treads":                  {"slot": "boots", "rarity": "common",    "zone": (61,70),  "bonus": {"spd": 6}},
    "Demon Iron Boots":              {"slot": "boots", "rarity": "common",    "zone": (61,70),  "bonus": {"def": 7}},
    "Ashen Stompers":                {"slot": "boots", "rarity": "common",    "zone": (61,70),  "bonus": {"spd": 7}},
    "Infernal Sabatons":             {"slot": "boots", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"spd": 10}},
    "Drake Scale Boots":             {"slot": "boots", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"def": 8, "spd": 6}},
    "Hellforged Treads":             {"slot": "boots", "rarity": "rare",      "zone": (61,70),  "bonus": {"spd": 14}},
    "Boots of the Eternal Flame":    {"slot": "boots", "rarity": "rare",      "zone": (61,70),  "bonus": {"def": 9, "spd": 9}},
    "Ignarath's Ashen Treads":       {"slot": "boots", "rarity": "legendary", "zone": (61,70),  "bonus": {"spd": 20, "def": 12}, "special": "evasion_5"},

    # The Abyss (floors 71+)
    "Void Treads":             {"slot": "boots", "rarity": "common",    "zone": (71,999), "bonus": {"spd": 7}},
    "Soul Stompers":           {"slot": "boots", "rarity": "common",    "zone": (71,999), "bonus": {"def": 8}},
    "Nightmare Slippers":      {"slot": "boots", "rarity": "common",    "zone": (71,999), "bonus": {"spd": 8}},
    "Abyssal Sabatons":        {"slot": "boots", "rarity": "uncommon",  "zone": (71,999), "bonus": {"spd": 12}},
    "Undying Treads":          {"slot": "boots", "rarity": "uncommon",  "zone": (71,999), "bonus": {"def": 9, "spd": 7}},
    "Void Sovereign Treads":   {"slot": "boots", "rarity": "rare",      "zone": (71,999), "bonus": {"spd": 16}},
    "Soul Eater's Stompers":   {"slot": "boots", "rarity": "rare",      "zone": (71,999), "bonus": {"def": 11, "spd": 10}},
    "Boots of the Abyss":      {"slot": "boots", "rarity": "legendary", "zone": (71,999), "bonus": {"spd": 22, "def": 14}, "special": "evasion_5"},
}

RINGS = {
    # The Forest (floors 1-10)
    "Crude Wooden Ring":       {"slot": "ring", "rarity": "common",    "zone": (1,10),   "bonus": {"atk": 2}},
    "Hunter's Band":           {"slot": "ring", "rarity": "common",    "zone": (1,10),   "bonus": {"spd": 2}},
    "Goblin Trinket":          {"slot": "ring", "rarity": "common",    "zone": (1,10),   "bonus": {"def": 2}},
    "Ring of the Wolf":        {"slot": "ring", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"atk": 3, "spd": 2}},
    "Ranger's Signet":         {"slot": "ring", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"def": 3, "atk": 2}},
    "Ring of the Predator":    {"slot": "ring", "rarity": "rare",      "zone": (1,10),   "bonus": {"atk": 5, "spd": 3}},
    "Sylvan Signet":           {"slot": "ring", "rarity": "rare",      "zone": (1,10),   "bonus": {"def": 4, "atk": 4}},
    "Ring of the Forest God":  {"slot": "ring", "rarity": "legendary", "zone": (1,10),   "bonus": {"atk": 8, "spd": 5, "def": 3}},

    # The Mines (floors 11-20)
    "Miner's Band":            {"slot": "ring", "rarity": "common",    "zone": (11,20),  "bonus": {"atk": 3}},
    "Iron Loop":               {"slot": "ring", "rarity": "common",    "zone": (11,20),  "bonus": {"def": 3}},
    "Kobold Ring":             {"slot": "ring", "rarity": "common",    "zone": (11,20),  "bonus": {"spd": 3}},
    "Ring of the Deep":        {"slot": "ring", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"atk": 4, "def": 3}},
    "Stonegrip Band":          {"slot": "ring", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"def": 5, "atk": 2}},
    "Ring of the Cave":        {"slot": "ring", "rarity": "rare",      "zone": (11,20),  "bonus": {"atk": 6, "def": 4}},
    "Golem Core Ring":         {"slot": "ring", "rarity": "rare",      "zone": (11,20),  "bonus": {"def": 5, "atk": 5}},
    "Ring of the Deep Earth":  {"slot": "ring", "rarity": "legendary", "zone": (11,20),  "bonus": {"atk": 9, "def": 7, "spd": 3}},

    # The Crypt (floors 21-30)
    "Bone Ring":               {"slot": "ring", "rarity": "common",    "zone": (21,30),  "bonus": {"atk": 4}},
    "Grave Band":              {"slot": "ring", "rarity": "common",    "zone": (21,30),  "bonus": {"def": 4}},
    "Ghoul Trinket":           {"slot": "ring", "rarity": "common",    "zone": (21,30),  "bonus": {"spd": 4}},
    "Ring of the Crypt":       {"slot": "ring", "rarity": "uncommon",  "zone": (21,30),  "bonus": {"atk": 5, "def": 4}},
    "Soulbound Band":          {"slot": "ring", "rarity": "uncommon",  "zone": (21,30),  "bonus": {"def": 6, "spd": 3}},
    "Ring of the Undead":      {"slot": "ring", "rarity": "rare",      "zone": (21,30),  "bonus": {"atk": 8, "def": 5}},
    "Eternal Band":            {"slot": "ring", "rarity": "rare",      "zone": (21,30),  "bonus": {"def": 6, "atk": 6}},
    "Ring of Eternal Night":   {"slot": "ring", "rarity": "legendary", "zone": (21,30),  "bonus": {"atk": 11, "def": 8, "spd": 5}},

    # The Ruined Castle (floors 31-40)
    "Guardsman's Ring":        {"slot": "ring", "rarity": "common",    "zone": (31,40),  "bonus": {"atk": 5}},
    "Rusted Band":             {"slot": "ring", "rarity": "common",    "zone": (31,40),  "bonus": {"def": 5}},
    "Castle Signet":           {"slot": "ring", "rarity": "common",    "zone": (31,40),  "bonus": {"spd": 5}},
    "Knight's Ring":           {"slot": "ring", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"atk": 6, "def": 5}},
    "Oathbound Band":          {"slot": "ring", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"def": 7, "spd": 4}},
    "Ring of the Fallen King": {"slot": "ring", "rarity": "rare",      "zone": (31,40),  "bonus": {"atk": 10, "def": 6}},
    "Royal Signet":            {"slot": "ring", "rarity": "rare",      "zone": (31,40),  "bonus": {"def": 8, "atk": 7}},
    "Igris's Oath Ring":       {"slot": "ring", "rarity": "legendary", "zone": (31,40),  "bonus": {"atk": 13, "def": 10, "spd": 6}},

    # The Dark Mage School (floors 41-50)
    "Apprentice Band":         {"slot": "ring", "rarity": "common",    "zone": (41,50),  "bonus": {"atk": 6}},
    "Arcane Loop":             {"slot": "ring", "rarity": "common",    "zone": (41,50),  "bonus": {"def": 6}},
    "Scholar's Ring":          {"slot": "ring", "rarity": "common",    "zone": (41,50),  "bonus": {"spd": 6}},
    "Runed Band":              {"slot": "ring", "rarity": "uncommon",  "zone": (41,50),  "bonus": {"atk": 8, "def": 6}},
    "Corruption Ring":         {"slot": "ring", "rarity": "uncommon",  "zone": (41,50),  "bonus": {"def": 9, "spd": 5}},
    "Ring of Unmaking":        {"slot": "ring", "rarity": "rare",      "zone": (41,50),  "bonus": {"atk": 12, "def": 8}},
    "Spellbinder's Band":      {"slot": "ring", "rarity": "rare",      "zone": (41,50),  "bonus": {"def": 10, "atk": 9}},
    "Voss's Forbidden Ring":   {"slot": "ring", "rarity": "legendary", "zone": (41,50),  "bonus": {"atk": 16, "def": 12, "spd": 8}},

    # The Underdark (floors 51-60)
    "Shadow Band":             {"slot": "ring", "rarity": "common",    "zone": (51,60),  "bonus": {"atk": 7}},
    "Duergar Loop":            {"slot": "ring", "rarity": "common",    "zone": (51,60),  "bonus": {"def": 7}},
    "Flayer Ring":             {"slot": "ring", "rarity": "common",    "zone": (51,60),  "bonus": {"spd": 7}},
    "Assassin's Band":         {"slot": "ring", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"atk": 10, "spd": 7}},
    "Krakenscale Ring":        {"slot": "ring", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"def": 9, "atk": 6}},
    "Ring of the Elder Mind":  {"slot": "ring", "rarity": "rare",      "zone": (51,60),  "bonus": {"atk": 14, "def": 9}},
    "Void Touched Band":       {"slot": "ring", "rarity": "rare",      "zone": (51,60),  "bonus": {"def": 12, "atk": 10}},
    "Underdark Sovereign Ring":{"slot": "ring", "rarity": "legendary", "zone": (51,60),  "bonus": {"atk": 18, "def": 14, "spd": 10}},

    # The Core (floors 61-70)
    "Ember Band":              {"slot": "ring", "rarity": "common",    "zone": (61,70),  "bonus": {"atk": 8}},
    "Demon Iron Loop":         {"slot": "ring", "rarity": "common",    "zone": (61,70),  "bonus": {"def": 8}},
    "Ashen Ring":              {"slot": "ring", "rarity": "common",    "zone": (61,70),  "bonus": {"spd": 8}},
    "Infernal Band":           {"slot": "ring", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"atk": 12, "spd": 8}},
    "Drake Scale Ring":        {"slot": "ring", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"def": 11, "atk": 7}},
    "Ring of the Eternal Flame":{"slot": "ring","rarity": "rare",      "zone": (61,70),  "bonus": {"atk": 16, "def": 11}},
    "Hellforged Band":         {"slot": "ring", "rarity": "rare",      "zone": (61,70),  "bonus": {"def": 14, "atk": 12}},
    "Ignarath's Ember Ring":   {"slot": "ring", "rarity": "legendary", "zone": (61,70),  "bonus": {"atk": 22, "def": 16, "spd": 12}, "special": "fire_resist_10"},

    # The Abyss (floors 71+)
    "Void Band":               {"slot": "ring", "rarity": "common",    "zone": (71,999), "bonus": {"atk": 10}},
    "Soul Loop":               {"slot": "ring", "rarity": "common",    "zone": (71,999), "bonus": {"def": 10}},
    "Nightmare Ring":          {"slot": "ring", "rarity": "common",    "zone": (71,999), "bonus": {"spd": 10}},
    "Abyssal Band":            {"slot": "ring", "rarity": "uncommon",  "zone": (71,999), "bonus": {"atk": 14, "spd": 10}},
    "Ring of the Undying":     {"slot": "ring", "rarity": "uncommon",  "zone": (71,999), "bonus": {"def": 13, "atk": 8}},
    "Void Sovereign Band":     {"slot": "ring", "rarity": "rare",      "zone": (71,999), "bonus": {"atk": 19, "def": 13}},
    "Soul Eater's Loop":       {"slot": "ring", "rarity": "rare",      "zone": (71,999), "bonus": {"def": 16, "atk": 14}},
    "Ring of the Abyss":       {"slot": "ring", "rarity": "legendary", "zone": (71,999), "bonus": {"atk": 26, "def": 20, "spd": 15}},
}

ACCESSORIES = {
    # The Forest (floors 1-10)
    "Worn Shield Strap":       {"slot": "accessory", "rarity": "common",    "zone": (1,10),   "bonus": {"def": 3}},
    "Cloak of Shadows":        {"slot": "accessory", "rarity": "uncommon",  "zone": (1,10),   "bonus": {"spd": 4, "atk": 2}},
    "Sylvan Amulet":           {"slot": "accessory", "rarity": "rare",      "zone": (1,10),   "bonus": {"atk": 6, "max_mp": 15}},
    "Amulet of the Wild":      {"slot": "accessory", "rarity": "legendary", "zone": (1,10),   "bonus": {"atk": 10, "spd": 5, "max_hp": 30}, "special": "hp_restore_5_on_kill"},

    # The Mines (floors 11-20)
    "Miner's Buckler":         {"slot": "accessory", "rarity": "common",    "zone": (11,20),  "bonus": {"def": 4}},
    "Cloak of the Spider":     {"slot": "accessory", "rarity": "uncommon",  "zone": (11,20),  "bonus": {"spd": 5, "atk": 3}},
    "Crystal Amulet":          {"slot": "accessory", "rarity": "rare",      "zone": (11,20),  "bonus": {"atk": 7, "max_mp": 20}},
    "Shield of the Deep Earth":{"slot": "accessory", "rarity": "legendary", "zone": (11,20),  "bonus": {"def": 12, "max_hp": 40}, "special": "reflect_10"},

    # The Crypt (floors 21-30)
    "Bone Shield":             {"slot": "accessory", "rarity": "common",    "zone": (21,30),  "bonus": {"def": 5}},
    "Gravecloak":              {"slot": "accessory", "rarity": "uncommon",  "zone": (21,30),  "bonus": {"spd": 6, "atk": 4}},
    "Amulet of the Dead":      {"slot": "accessory", "rarity": "rare",      "zone": (21,30),  "bonus": {"atk": 9, "max_mp": 25}},
    "Shield of Eternal Night": {"slot": "accessory", "rarity": "legendary", "zone": (21,30),  "bonus": {"def": 15, "max_hp": 50}, "special": "hp_restore_15_on_kill"},

    # The Ruined Castle (floors 31-40)
    "Guardsman's Shield":      {"slot": "accessory", "rarity": "common",    "zone": (31,40),  "bonus": {"def": 6}},
    "Cloak of the Fallen":     {"slot": "accessory", "rarity": "uncommon",  "zone": (31,40),  "bonus": {"spd": 8, "atk": 5}},
    "Amulet of the Castle":    {"slot": "accessory", "rarity": "rare",      "zone": (31,40),  "bonus": {"atk": 11, "max_mp": 30}},
    "Igris's Oathbound Shield":{"slot": "accessory", "rarity": "legendary", "zone": (31,40),  "bonus": {"def": 18, "max_hp": 60}, "special": "block_first_hit"},

    # The Dark Mage School (floors 41-50)
    "Apprentice Shield":       {"slot": "accessory", "rarity": "common",    "zone": (41,50),  "bonus": {"def": 7}},
    "Cloak of Corruption":     {"slot": "accessory", "rarity": "uncommon",  "zone": (41,50),  "bonus": {"spd": 9, "atk": 6}},
    "Voss's Forbidden Amulet": {"slot": "accessory", "rarity": "rare",      "zone": (41,50),  "bonus": {"atk": 13, "max_mp": 35}},
    "Amulet of Unmaking":      {"slot": "accessory", "rarity": "legendary", "zone": (41,50),  "bonus": {"atk": 20, "max_mp": 70}, "special": "mp_cost_80"},

    # The Underdark (floors 51-60)
    "Shadow Shield":           {"slot": "accessory", "rarity": "common",    "zone": (51,60),  "bonus": {"def": 8}},
    "Cloak of the Assassin":   {"slot": "accessory", "rarity": "uncommon",  "zone": (51,60),  "bonus": {"spd": 11, "atk": 7}},
    "Amulet of the Underdark": {"slot": "accessory", "rarity": "rare",      "zone": (51,60),  "bonus": {"atk": 15, "max_mp": 40}},
    "Cloak of the Dark Sovereign":{"slot": "accessory", "rarity": "legendary", "zone": (51,60), "bonus": {"spd": 25, "atk": 15}, "special": "poison_on_hit_15"},

    # The Core (floors 61-70)
    "Ember Shield":            {"slot": "accessory", "rarity": "common",    "zone": (61,70),  "bonus": {"def": 9}},
    "Cloak of the Drake":      {"slot": "accessory", "rarity": "uncommon",  "zone": (61,70),  "bonus": {"spd": 13, "atk": 8}},
    "Amulet of the Core":      {"slot": "accessory", "rarity": "rare",      "zone": (61,70),  "bonus": {"atk": 17, "max_mp": 45}},
    "Ignarath's Ashen Shield": {"slot": "accessory", "rarity": "legendary", "zone": (61,70),  "bonus": {"def": 28, "max_hp": 90}, "special": "burn_resist_50"},

    # The Abyss (floors 71+)
    "Void Shield":             {"slot": "accessory", "rarity": "common",    "zone": (71,999), "bonus": {"def": 11}},
    "Cloak of the Nightmare":  {"slot": "accessory", "rarity": "uncommon",  "zone": (71,999), "bonus": {"spd": 16, "atk": 10}},
    "Amulet of the Void":      {"slot": "accessory", "rarity": "rare",      "zone": (71,999), "bonus": {"atk": 20, "max_mp": 55}},
    "Cloak of the Abyss":      {"slot": "accessory", "rarity": "legendary", "zone": (71,999), "bonus": {"spd": 30, "atk": 20}, "special": "skip_combat_5"},
}

SETS = {
    "The Sylvan God Set": {
        "pieces": [
            "Sylvan Blade", "Armour of the Wild", "Boots of the Sylvan God",
            "Ring of the Forest God", "Amulet of the Wild"
        ],
        "bonus": "heart_of_the_forest",
        "desc": "Regenerate 5% max HP at the start of every room",
    },
    "Set of the Deep Earth": {
        "pieces": [
            "Earthcleaver", "Armour of the Deep", "Boots of the Deep Earth",
            "Ring of the Deep Earth", "Shield of the Deep Earth"
        ],
        "bonus": "unyielding_stone",
        "desc": "Every hit you take has a 20% chance to deal 0 damage",
    },
    "The Deathless Set": {
        "pieces": [
            "Eternal Dirge", "Deathless Shroud", "Boots of Eternal Night",
            "Ring of Eternal Night", "Shield of Eternal Night"
        ],
        "bonus": "reapers_pact",
        "desc": "ATK increases by 2 permanently each time you kill an enemy while below 30% HP",
    },
    "The Oathbound Set": {
        "pieces": [
            "Igris's Honour Blade", "Igris's Unbroken Plate", "Igris's Iron Boots",
            "Igris's Oath Ring", "Igris's Oathbound Shield"
        ],
        "bonus": "last_stand",
        "desc": "When HP drops below 20%, ATK and DEF both double until end of combat",
    },
    "The Unmaking Set": {
        "pieces": [
            "Staff of Unmaking", "Armour of Unmaking", "Boots of Unmaking",
            "Voss's Forbidden Ring", "Amulet of Unmaking"
        ],
        "bonus": "forbidden_mastery",
        "desc": "All ability MP costs reduced by 80%. Every ability has a 15% chance to hit twice",
    },
    "The Dark Sovereign Set": {
        "pieces": [
            "Blade of the Elder Mind", "Underdark Sovereign Plate", "Underdark Sovereign Boots",
            "Underdark Sovereign Ring", "Cloak of the Dark Sovereign"
        ],
        "bonus": "mind_ascendant",
        "desc": "SPD bonus from Blade of the Elder Mind stacks twice as fast. Poison stacks deal 50% more damage",
    },
    "The Eternal Flame Set": {
        "pieces": [
            "The Eternal Flame Blade", "Ignarath's Ashen Plate", "Ignarath's Ashen Treads",
            "Ignarath's Ember Ring", "Ignarath's Ashen Shield"
        ],
        "bonus": "eternal_inferno",
        "desc": "Burn immune enemies take normal burn damage. Burn stacks never expire",
    },
    "The Abyss Set": {
        "pieces": [
            "Blade of the Abyss", "Armour of the Abyss", "Boots of the Abyss",
            "Ring of the Abyss", "Cloak of the Abyss"
        ],
        "bonus": "void_incarnate",
        "desc": "Instant kill chance becomes 5%. Combat skip chance becomes 15%",
    },
}

ALL_ITEMS = {**WEAPONS, **ARMOR, **BOOTS, **RINGS, **ACCESSORIES}

def get_equipped_set(player):
    equipped_names = [
        item["name"] for item in player.equipped.values() if item is not None
    ]
    for set_name, set_data in SETS.items():
        if all(piece in equipped_names for piece in set_data["pieces"]):
            return set_name, set_data
    return None, None

def equip_item(player, item):
    slot = item["slot"]
    if slot not in player.equipped:
        print(f"  {Fore.RED}Cannot equip {item['name']}!{Style.RESET_ALL}")
        return

    if player.equipped[slot] is not None:
        unequip_item(player, player.equipped[slot])

    player.equipped[slot] = item
    item["name"] = item.get("name", "Unknown")

    bonus = item.get("bonus", {})
    if "atk" in bonus:
        player.base_atk += bonus["atk"]
        player.atk = player.base_atk
    if "def" in bonus:
        player.base_defense += bonus["def"]
        player.defense = player.base_defense
    if "spd" in bonus:
        player.base_spd += bonus["spd"]
        player.spd = player.base_spd
    if "max_hp" in bonus:
        player.max_hp += bonus["max_hp"]
        player.hp = min(player.hp + bonus["max_hp"], player.max_hp)
    if "max_mp" in bonus:
        player.max_mp += bonus["max_mp"]
        player.mp = min(player.mp + bonus["max_mp"], player.max_mp)

    colour = rarity_colour(item)
    print(f"  {Fore.GREEN}Equipped {colour}{item['name']}{Style.RESET_ALL}{Fore.GREEN}!{Style.RESET_ALL}")

    set_name, set_data = get_equipped_set(player)
    if set_name:
        print(f"\n  {Fore.YELLOW}*** SET BONUS ACTIVATED: {set_name} ***{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}{set_data['desc']}{Style.RESET_ALL}")

def unequip_item(player, item):
    slot = item["slot"]
    player.equipped[slot] = None

    bonus = item.get("bonus", {})
    if "atk" in bonus:
        player.base_atk -= bonus["atk"]
        player.atk = player.base_atk
    if "def" in bonus:
        player.base_defense -= bonus["def"]
        player.defense = player.base_defense
    if "spd" in bonus:
        player.base_spd -= bonus["spd"]
        player.spd = player.base_spd
    if "max_hp" in bonus:
        player.max_hp -= bonus["max_hp"]
        player.hp = min(player.hp, player.max_hp)
    if "max_mp" in bonus:
        player.max_mp -= bonus["max_mp"]
        player.mp = min(player.mp, player.max_mp)

    colour = rarity_colour(item)
    print(f"  {Fore.RED}Unequipped {colour}{item['name']}{Style.RESET_ALL}{Fore.RED}.{Style.RESET_ALL}")

# A level-up gives +1 ATK, DEF and SPD, +10 max HP and +8 max MP, so weigh item stats the same way.
STAT_WEIGHTS = {"atk": 1, "def": 1, "spd": 1, "max_hp": 0.1, "max_mp": 0.125}
RARITY_RANK = {"common": 0, "uncommon": 1, "rare": 2, "legendary": 3}

def item_score(item):
    return sum(STAT_WEIGHTS.get(stat, 0) * value for stat, value in item.get("bonus", {}).items())

def recommended_gear(player):
    """Returns {slot: item} with the best gear the player owns.

    A complete set wins, for its set bonus. Otherwise each slot gets the item with the highest
    stat score; ties go to the rarer item (rarer items carry the special effects), then to
    whatever is already equipped.
    """
    owned = {id(item): item for item in player.inventory + list(player.equipped.values())
             if item and item["slot"] in player.equipped}.values()

    by_name = {item["name"]: item for item in owned}
    by_name.update({item["name"]: item for item in player.equipped.values() if item})  # keep equipped copies
    complete_sets = [data["pieces"] for data in SETS.values() if all(p in by_name for p in data["pieces"])]
    if complete_sets:
        pieces = max(complete_sets, key=lambda names: sum(item_score(by_name[n]) for n in names))
        return {by_name[n]["slot"]: by_name[n] for n in pieces}

    best = {}
    for item in owned:
        slot = item["slot"]
        rank = (item_score(item), RARITY_RANK.get(item.get("rarity"), 0), item is player.equipped[slot])
        if slot not in best or rank > best[slot][0]:
            best[slot] = (rank, item)
    return {slot: item for slot, (rank, item) in best.items()}

RARITY_WEIGHTS_EARLY = {
    "common": 80,
    "uncommon": 15,
    "rare": 4,
    "legendary": 1,
}

RARITY_WEIGHTS_LATE = {
    "common": 50,
    "uncommon": 30,
    "rare": 15,
    "legendary": 5,
}

def get_rarity_weights(floor):
    return RARITY_WEIGHTS_LATE if floor >= 36 else RARITY_WEIGHTS_EARLY

def pick_rarity(floor):
    weights = get_rarity_weights(floor)
    pool = []
    for rarity, weight in weights.items():
        pool.extend([rarity] * weight)
    return random.choice(pool)

def get_loot_pool(floor):
    eligible = []
    for name, item in ALL_ITEMS.items():
        min_floor, max_floor = item["zone"]
        if min_floor <= floor <= max_floor:
            eligible.append((name, item))
    return eligible

def drop_loot(floor):
    rarity = pick_rarity(floor)
    pool = get_loot_pool(floor)
    matching = [(name, item) for name, item in pool if item["rarity"] == rarity]

    if not matching:
        matching = [(name, item) for name, item in pool if item["rarity"] == "common"]

    if not matching:
        return None

    name, item = random.choice(matching)
    drop = dict(item)
    drop["name"] = name
    return drop

def drop_consumable():
    name = random.choice(list(CONSUMABLES.keys()))
    drop = dict(CONSUMABLES[name])
    drop["name"] = name
    return drop