import random
from colorama import Fore, Style
from loot import equip_item, unequip_item

RARITY_COLOURS = {
    "common":    Style.RESET_ALL,
    "uncommon":  Fore.GREEN,
    "rare":      Fore.BLUE,
    "legendary": Fore.YELLOW,
}

def rarity_colour(item):
    rarity = item.get("rarity", "common")
    return RARITY_COLOURS.get(rarity, Style.RESET_ALL)

STRANGER_DIALOGUE = {
    "The Forest": {
        "current": "The forest... yes. It seems peaceful, doesn't it? The birds still sing. The light still filters through the canopy. But something old lives between those trees. Something that was here long before the goblins made it their home. I have seen men enter that forest full of courage. I have not seen all of them return.",
        "cleared": "You came back from the forest. I admit, I had my doubts. Gobzo does not fall easily, he has broken better warriors than most who sit in this tavern. But here you sit. Drink it in. The deeper floors will not be so... familiar.",
        "teaser": "The mines. You want to know about the mines. They were dug generations ago, for iron, they said. For wealth. But the miners found something else down there. Something that drove them mad. Grak rules what's left of them now. He is not the worst thing in those tunnels. He is simply the loudest.",
    },
    "The Mines": {
        "current": "The mines are loud in a way the forest never was. The dripping of water. The creak of ancient supports. The skittering of things that have never seen sunlight. Grak keeps order down there, if you can call it that. He is massive, brutal, and surprisingly patient. He will wait for you to make a mistake.",
        "cleared": "Grak is dead. I confess that surprises me. He has held those tunnels for longer than this tavern has stood. Whatever you are, adventurer, you are not ordinary. The miners' souls might rest a little easier tonight. Might.",
        "teaser": "The crypt lies beneath the mines, did you know that? Built before the mines were ever dug. Whoever built it did not want to be found. The dead there are not simply dead. They remember. They hunger. And Seraphine... she has had a very long time to grow powerful. Do not let her beauty deceive you.",
    },
    "The Crypt": {
        "current": "The crypt is cold in a way that has nothing to do with temperature. You feel it in your chest. In your thoughts. The dead here were not buried, they were imprisoned. There is a difference. Seraphine has ruled this place since before your grandfather's grandfather drew breath. She does not fear you. Not yet.",
        "cleared": "Seraphine... gone. I did not think I would live to see it. She was ancient when this dungeon was young. Whatever hunger drove her, whatever kept her bound to that place, you ended it. I wonder if she thanked you, at the end. She always did have a flair for the dramatic.",
        "teaser": "The ruined castle. Once a seat of power. Once filled with laughter and politics and the petty squabbles of kings. Now it is hollow. The king is long dead, no one remembers his name, which is perhaps fitting. But his guard remains. Commander Igris has not moved from that throne room in decades. He is still waiting for an order that will never come.",
    },
    "The Ruined Castle": {
        "current": "Igris was the finest soldier the kingdom ever produced. Loyal beyond reason. When the king died, suddenly, quietly, with no explanation, Igris refused to leave his post. He has been there ever since. The castle crumbled around him. His men fell one by one. He remains. I do not know whether that makes him admirable or tragic. Perhaps both.",
        "cleared": "You faced Igris. And you are sitting here, which means one of two things, either you are stronger than I thought, or he finally found something worth yielding to. I hope it was the former. He deserved a worthy end. The castle can crumble in peace now. Whatever the king's secret was, it dies with his last guardian.",
        "teaser": "The dark mage school. It was founded with good intentions, they always are. A place of learning. Of discovery. Headmaster Voss was brilliant, they say. Curious. Devoted. Then he found something in the lower archives that he was not supposed to find. The school has been sealed ever since. What remains inside is not what walked in.",
    },
    "The Dark Mage School": {
        "current": "Voss crossed a line that cannot be uncrossed. He sought power over death itself, not to cheat it, but to understand it. To catalogue it. What he found instead was something that understood him far better than he understood it. The school is his now, in a manner of speaking. He and it have become... difficult to separate.",
        "cleared": "Voss is gone. I wonder if any part of him is relieved. He spent so long being consumed by that place, by that knowledge, I am not sure there was much of him left to save. You did what needed doing. The archives should be burned. If you ever find yourself tempted to read what is written there, walk away. I am serious.",
        "teaser": "The Underdark. I will be honest with you, I have never been there myself. I know of it only through those who came back, and those who did not come back are far more numerous. It is a civilisation beneath a civilisation. Ancient, vast, and utterly indifferent to your existence. Zyx'ara rules the deepest part of it. She has been watching you since you entered the dungeon. She finds you interesting. That is not a compliment.",
    },
    "The Underdark": {
        "current": "You are deeper than most dare to go. The Underdark does not simply house monsters, it houses entire societies that have evolved in total darkness for millennia. They do not hate you. You are simply an anomaly. An insect that has wandered somewhere it does not belong. Zyx'ara will correct that, given the chance. She is patient in the way that only something truly ancient can be patient.",
        "cleared": "Zyx'ara. Dead. I need a moment with that. She has existed longer than written history. She has watched empires rise and fall from those tunnels without blinking. And you walked in and ended her. I do not know whether to be impressed or frightened. I think I am both. The Underdark will not forget this. Something down there will remember your name.",
        "teaser": "The Core. This is where I must choose my words carefully. What lies at the heart of this dungeon is not natural. The heat, the fire, the creatures, they are symptoms. Ignarath is the cause. He is not simply a demon. He is the reason this dungeon exists. Everything above, the forest, the mines, the crypt, it is all built on top of him. He has been burning at the centre of this place since before the first stone was laid. He will not be pleased to see you.",
    },
    "The Core": {
        "current": "You can feel it, can't you? Even up here. The heat. The pressure. The sense that something vast and ancient is aware of you. Ignarath does not need to look for you. He knows you are coming. He has always known. The dungeon was built around him, some say by him. Every creature you have fought, every floor you have descended, you have been walking towards him this entire time.",
        "cleared": "Ignarath is dead. The eternal flame, extinguished. I have sat in this tavern for a very long time and I did not believe this day would come. The dungeon should have collapsed without him at its core. The fact that it did not tells me something I find deeply unsettling. Something is holding it together. Something below even him. I think you already know what that means.",
        "teaser": "The Abyss. There is no story to tell you about the Abyss. No history. No names. No rulers who were once something else before the darkness took them. The Abyss simply is. It has always been. It will always be. Those who descend into it do not come back changed. They do not come back at all. And yet here you are, asking about it. I think, perhaps, that you were always going to end up there. Some people are just built for the dark.",
    },
    "The Abyss": {
        "current": "You are in the Abyss. You already know everything I could tell you, and it would not matter anyway. The Abyss does not follow rules. It does not follow logic. It simply consumes. All I can tell you is this, whatever you are fighting for, hold onto it. The Abyss will try to make you forget. Do not let it.",
        "cleared": "Still alive. Still descending. I stopped being surprised by you some time ago. I find myself checking the door each time it opens, wondering if it will be you again. It always is. Whatever is down there in the dark, it has not beaten you yet. I do not think it will. But I have been wrong before.",
        "teaser": None,
    },
}

STRANGER_FINAL = "So. You actually made it. I have been sitting in this chair for a very long time, watching adventurers come and go. Most do not make it past the forest. A few reach the mines. One or two have stood where you are standing now, at the edge of everything. None of them came back. I will see you soon. It has been a pleasure watching you descend."

STRANGER_LOCKED = "That is not something I can speak of yet. Some knowledge has to be earned. Come back when the path ahead is clearer. Or when the bodies behind you are."

BRAM_HINTS = [
    "That hooded fellow in the corner... he was here when I started working this place. Never seen him eat. Never seen him sleep.",
    "I asked him his name once. He just smiled. I didn't ask again.",
    "My father ran this tavern before me. He told me never to ask the stranger to leave. I never have.",
    "Sometimes I find his cup empty before I've even poured anything. I've stopped trying to explain it.",
    "He ordered the same drink the night this tavern opened. I know because my grandfather wrote it down. I found the ledger last winter.",
    "I don't think he's waiting for anything. I think he's just... watching. For what, I couldn't tell you.",
]

VENDOR_GREETINGS = {
    "Bram": [
        "What'll it be? We've got ale and... well, mostly ale.",
        "Back again. The dungeon not killed you yet then.",
        "Take a seat. You look like you've seen things.",
        "Rough down there, is it? Aye. It always is.",
    ],
    "Sister Maren": [
        "The light protect you, traveller. What do you need?",
        "I have potions and salves. Take what you need, pay what you can.",
        "You look wounded. Let me help.",
        "Rest here a moment. Then tell me what you need.",
    ],
    "Aldric the Grey": [
        "Ah, a customer with taste. What takes your fancy?",
        "Fresh stock in. Nasty stuff, all of it. You'll love it.",
        "Don't shake the termites. They bite.",
        "I won't ask what you're planning. Less I know the better.",
    ],
    "Sera": [
        "Looking to get stronger? You've come to the right place.",
        "I deal in potential. What are you lacking?",
        "Speed, strength, endurance. I've got all three.",
        "Back again. Good. Means you survived last time.",
    ],
}

ZONE_ORDER = [
    "The Forest", "The Mines", "The Crypt", "The Ruined Castle",
    "The Dark Mage School", "The Underdark", "The Core", "The Abyss"
]

ZONE_FLOORS = {
    "The Forest":           (1, 10),
    "The Mines":            (11, 20),
    "The Crypt":            (21, 30),
    "The Ruined Castle":    (31, 40),
    "The Dark Mage School": (41, 50),
    "The Underdark":        (51, 60),
    "The Core":             (61, 70),
    "The Abyss":            (71, 999),
}

SHOP_ITEMS = {
    "Bram": [
        {"name": "Ale",         "base_price": 5,  "slot": "consumable", "bonus": {"atk_up": 1, "spd_down": 1}, "desc": "A frothy mug. Warms the blood.", "ale": True},
        {"name": "Crimson Dew", "base_price": 30, "slot": "consumable", "bonus": {"hp_set": 0.20}, "desc": "A dark red drink. What could go wrong?"},
    ],
    "Sister Maren": [
        {"name": "Health Potion", "base_price": 20,  "slot": "consumable", "bonus": {"hp": 0.33}, "desc": "Restores 33% of your max HP"},
        {"name": "Mana Potion",   "base_price": 20,  "slot": "consumable", "bonus": {"mp": 0.33}, "desc": "Restores 33% of your max MP"},
        {"name": "Elixir",        "base_price": 40,  "slot": "consumable", "bonus": {"hp": 0.33, "mp": 0.33}, "desc": "Restores 33% HP and 33% MP"},
        {"name": "Grand Elixir",  "base_price": 120, "slot": "consumable", "bonus": {"hp": 1.0, "mp": 1.0}, "desc": "Fully restores HP and MP"},
    ],
    "Aldric the Grey": [
        {"name": "Poison Flask",        "base_price": 50, "slot": "consumable", "bonus": {"poison": True}, "desc": "Applies 2 poison stacks to the enemy"},
        {"name": "Napalm Flask",        "base_price": 50, "slot": "consumable", "bonus": {"burn": True}, "desc": "Applies 2 burn stacks to the enemy"},
        {"name": "Metal Jawed Termite", "base_price": 40, "slot": "consumable", "bonus": {"def_down": 3}, "desc": "Applies 2 DEF down stacks to the enemy"},
    ],
    "Sera": [
        {"name": "Strength Potion", "base_price": 35, "slot": "consumable", "bonus": {"atk_up": 5}, "desc": "Boosts ATK by 5 for 3 turns"},
        {"name": "Defense Potion",  "base_price": 35, "slot": "consumable", "bonus": {"def_up": 5}, "desc": "Boosts DEF by 5 for 3 turns"},
        {"name": "Speed Potion",    "base_price": 35, "slot": "consumable", "bonus": {"spd_up": 5}, "desc": "Boosts SPD by 5 for 3 turns"},
    ],
}

SELL_PRICES = {
    "common":    20,
    "uncommon":  30,
    "rare":      100,
    "legendary": 300,
}

def get_price(base_price, floor):
    return int(base_price * (1 + floor * 0.05))

def get_current_zone(floor):
    for zone, (min_f, max_f) in ZONE_FLOORS.items():
        if min_f <= floor <= max_f:
            return zone
    return "The Abyss"

def get_zone_index(zone):
    return ZONE_ORDER.index(zone) if zone in ZONE_ORDER else 0

def talk_to_stranger(player, floor, bosses_beaten):
    current_zone = get_current_zone(floor)
    current_index = get_zone_index(current_zone)

    if floor >= 999:
        print(f"\n  {Fore.RED}???: \"{STRANGER_FINAL}\"{Style.RESET_ALL}")
        return

    print(f"\n  {Fore.RED}The hooded stranger turns to face you.{Style.RESET_ALL}")
    print("\n  Which zone would you like to ask about?")

    available = []
    for i, zone in enumerate(ZONE_ORDER):
        if i < current_index:
            available.append((zone, "cleared"))
        elif i == current_index:
            available.append((zone, "current"))
        elif i == current_index + 1 and current_zone in bosses_beaten:
            available.append((zone, "teaser"))

    for i, (zone, state) in enumerate(available, 1):
        tag = f" {Fore.GREEN}(cleared){Style.RESET_ALL}" if state == "cleared" else f" {Fore.CYAN}(current){Style.RESET_ALL}" if state == "current" else f" {Fore.YELLOW}(teaser){Style.RESET_ALL}"
        print(f"  {i}. {zone}{tag}")
    print(f"  {len(available)+1}. Never mind.")

    choice = input("\n  > ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(available)+1):
        print("  The stranger waits. You say nothing.")
        return
    if int(choice) == len(available)+1:
        print("  You nod and step away.")
        return

    zone, state = available[int(choice)-1]
    dialogue = STRANGER_DIALOGUE[zone][state]
    if dialogue:
        print(f"\n  {Fore.RED}???: \"{dialogue}\"{Style.RESET_ALL}")
    else:
        print(f"\n  {Fore.RED}???: \"{STRANGER_LOCKED}\"{Style.RESET_ALL}")

def visit_vendor(player, vendor_name, floor):
    greetings = VENDOR_GREETINGS[vendor_name]
    print(f"\n  {Fore.CYAN}{vendor_name}{Style.RESET_ALL}: \"{random.choice(greetings)}\"")

    if vendor_name == "Bram":
        if not hasattr(player, 'bram_visit_count'):
            player.bram_visit_count = 0
        player.bram_visit_count += 1
        if player.bram_visit_count % 3 == 0:
            hint_index = (player.bram_visit_count // 3 - 1) % len(BRAM_HINTS)
            print(f"\n  {Fore.CYAN}Bram{Style.RESET_ALL} leans in and lowers his voice.")
            print(f"  {Fore.CYAN}Bram{Style.RESET_ALL}: \"{Fore.RED}{BRAM_HINTS[hint_index]}{Style.RESET_ALL}\"")

    items = SHOP_ITEMS[vendor_name]
    while True:
        print(f"\n  {Fore.YELLOW}Gold: {player.gold}g{Style.RESET_ALL}")
        print(f"\n  {vendor_name}'s wares:")
        for i, item in enumerate(items, 1):
            price = get_price(item["base_price"], floor)
            affordable = Fore.YELLOW if player.gold >= price else Fore.RED
            print(f"  {i}. {item['name']} — {item['desc']} ({affordable}{price}g{Style.RESET_ALL})")
        print(f"  {len(items)+1}. Leave")

        choice = input("\n  > ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(items)+1):
            print("  Invalid choice.")
            continue
        if int(choice) == len(items)+1:
            break

        item = items[int(choice)-1]
        price = get_price(item["base_price"], floor)

        if player.gold < price:
            print(f"  {Fore.RED}Not enough gold! You need {price}g.{Style.RESET_ALL}")
            continue

        if item.get("ale"):
            already_has = any(i["name"] == "Ale" for i in player.inventory)
            if already_has:
                print(f"  {Fore.RED}You've had enough ale for now.{Style.RESET_ALL}")
                continue

        player.gold -= price
        bought = dict(item)
        player.inventory.append(bought)
        print(f"  {Fore.GREEN}Bought {item['name']} for {price}g.{Style.RESET_ALL}")

def view_equipment(player):
    print(f"\n  {'='*40}")
    print(f"  {Fore.CYAN}{player.name} the {player.char_class}{Style.RESET_ALL} — Level {Fore.YELLOW}{player.level}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}HP: {player.hp}/{player.max_hp}{Style.RESET_ALL} | {Fore.BLUE}MP: {player.mp}/{player.max_mp}{Style.RESET_ALL}")
    print(f"  ATK: {player.atk}  DEF: {player.defense}  SPD: {player.spd}")
    print(f"  XP: {player.xp}/{player.xp_next} | {Fore.YELLOW}Gold: {player.gold}g{Style.RESET_ALL}")
    print("\n  Equipped:")
    for slot, item in player.equipped.items():
        if item:
            colour = rarity_colour(item)
            print(f"    {slot.capitalize()}: {colour}{item['name']}{Style.RESET_ALL}")
        else:
            print(f"    {slot.capitalize()}: None")
    print(f"\n  Inventory ({len(player.inventory)} items):")
    if not player.inventory:
        print("    Empty")
    else:
        for i, item in enumerate(player.inventory, 1):
            colour = rarity_colour(item)
            print(f"    {i}. {colour}{item['name']}{Style.RESET_ALL} ({item.get('rarity','').capitalize()} {item['slot']})")

def manage_inventory(player):
    while True:
        view_equipment(player)
        print("\n  1. Equip an item")
        print("  2. Unequip a slot")
        print("  3. Sell an item")
        print("  4. Back")
        choice = input("\n  > ").strip()

        if choice == "1":
            equippable = [i for i in player.inventory if i["slot"] != "consumable"]
            if not equippable:
                print(f"  {Fore.RED}No equippable items in inventory.{Style.RESET_ALL}")
                continue
            print("\n  Choose an item to equip:")
            for i, item in enumerate(equippable, 1):
                colour = rarity_colour(item)
                bonuses = ", ".join(f"+{v} {k}" for k,v in item.get("bonus",{}).items())
                print(f"  {i}. {colour}{item['name']}{Style.RESET_ALL} ({bonuses})")
            print(f"  {len(equippable)+1}. Cancel")
            c = input("\n  > ").strip()
            if c.isdigit() and 1 <= int(c) <= len(equippable):
                equip_item(player, equippable[int(c)-1])

        elif choice == "2":
            slots = [s for s, i in player.equipped.items() if i is not None]
            if not slots:
                print(f"  {Fore.RED}Nothing equipped.{Style.RESET_ALL}")
                continue
            print("\n  Choose a slot to unequip:")
            for i, slot in enumerate(slots, 1):
                item = player.equipped[slot]
                colour = rarity_colour(item)
                print(f"  {i}. {slot.capitalize()} ({colour}{item['name']}{Style.RESET_ALL})")
            print(f"  {len(slots)+1}. Cancel")
            c = input("\n  > ").strip()
            if c.isdigit() and 1 <= int(c) <= len(slots):
                item = player.equipped[slots[int(c)-1]]
                unequip_item(player, item)
                player.inventory.append(item)

        elif choice == "3":
            sellable = [i for i in player.inventory if i["slot"] != "consumable"]
            if not sellable:
                print(f"  {Fore.RED}No items to sell. Unequip items first if needed.{Style.RESET_ALL}")
                continue
            print("\n  Choose an item to sell:")
            for i, item in enumerate(sellable, 1):
                rarity = item.get("rarity", "common")
                price = SELL_PRICES.get(rarity, 20)
                colour = rarity_colour(item)
                print(f"  {i}. {colour}{item['name']}{Style.RESET_ALL} ({rarity.capitalize()}) — {Fore.YELLOW}{price}g{Style.RESET_ALL}")
            print(f"  {len(sellable)+1}. Cancel")
            c = input("\n  > ").strip()
            if c.isdigit() and 1 <= int(c) <= len(sellable):
                item = sellable[int(c)-1]
                rarity = item.get("rarity", "common")
                price = SELL_PRICES.get(rarity, 20)
                player.inventory.remove(item)
                player.gold += price
                print(f"  {Fore.GREEN}Sold {item['name']} for {price}g.{Style.RESET_ALL}")

        elif choice == "4":
            break

def tavern(player, floor, bosses_beaten):
    print(f"\n  {Fore.YELLOW}=========================================={Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}The Wandering Flagon{Style.RESET_ALL}")
    print(f"  Floor {floor} | {Fore.YELLOW}Gold: {player.gold}g{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}=========================================={Style.RESET_ALL}")

    while True:
        print("\n  What would you like to do?")
        print(f"  1. Talk to {Fore.RED}???{Style.RESET_ALL} (Hooded Stranger)")
        print(f"  2. Visit {Fore.CYAN}Bram{Style.RESET_ALL} (Barkeep)")
        print(f"  3. Visit {Fore.CYAN}Sister Maren{Style.RESET_ALL} (Healer)")
        print(f"  4. Visit {Fore.CYAN}Aldric the Grey{Style.RESET_ALL} (Alchemist)")
        print(f"  5. Visit {Fore.CYAN}Sera{Style.RESET_ALL} (Merchant)")
        print("  6. View stats and equipment")
        print("  7. Head to the dungeon")

        choice = input("\n  > ").strip()

        if choice == "1":
            talk_to_stranger(player, floor, bosses_beaten)
        elif choice == "2":
            visit_vendor(player, "Bram", floor)
        elif choice == "3":
            visit_vendor(player, "Sister Maren", floor)
        elif choice == "4":
            visit_vendor(player, "Aldric the Grey", floor)
        elif choice == "5":
            visit_vendor(player, "Sera", floor)
        elif choice == "6":
            manage_inventory(player)
        elif choice == "7":
            ale = next((i for i in player.inventory if i.get("ale")), None)
            if ale:
                player.base_atk += 1
                player.atk = player.base_atk
                player.base_spd = max(1, player.base_spd - 1)
                player.spd = player.base_spd
                player.inventory.remove(ale)
                print(f"\n  {Fore.YELLOW}You down the ale. Your blood runs hot.{Style.RESET_ALL}")
            break
        else:
            print("  Invalid choice.")