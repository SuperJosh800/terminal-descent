# Terminal Descent

A text-based roguelike dungeon crawler RPG playable entirely in your terminal, built in Python.

Descend through a seemingly endless dungeon, floor by floor. Fight enemies, collect loot, build your character and survive as you try to make it to, and defeat the final boss.

---

## Features

- **Three playable classes** — Warrior, Rogue, and Mage, each with unique stats and abilities
- **Endless dungeon** — floors go on forever, enemies scale endlessly with depth
- **Turn-based combat** — attack, use class abilities and consume items
- **RPG progression** — gain XP, level up, and watch your stats grow with every fight
- **Loot system** — weapons, armour, boots, rings, and consumables drop from enemies
- **Equipment slots** — equip and swap gear to shape your build
- **Boss encounters** — a powerful boss awaits every 10 floors cleared
- **Tavern hub** — clear a full floor to earn a rest; spend gold on healing and supplies before descending
- **Permadeath** — when you die, it's over. How deep can you go?

---

## Getting Started

### Download

Grab the executable for Windows, macOS (Apple Silicon) or Linux from the [latest release](https://github.com/superjosh800/terminal-descent/releases/latest) and run it in a terminal. No Python needed.

To run from source instead:

### Requirements

- Python 3.10+
- [colorama](https://pypi.org/project/colorama/) for coloured terminal output

### Installation

```bash
git clone https://github.com/vampcent/terminal-descent.git
cd terminal-descent
pip install -r requirements.txt
python main.py
```

### Development

```bash
pip install ruff
ruff check .                 # lint
python -m tests.smoke_test   # plays many random games and fails on any crash or hang
```

CI runs both on every push and pull request. To publish a release, push a version tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

This builds the executables, checks that they start, and attaches them to a new GitHub Release.

---

## How to Play

1. Create your hero - choose a name and class
2. Fight your way through every room on the floor
3. Clear the entire floor to unlock the tavern
4. Visit the tavern to rest, restock, and spend your gold
5. Descend to the next floor and repeat
6. Every 10 floors, face a boss - defeat it or die trying
7. Reach floor 1000 and defeat the final boss to win!

---

## Roadmap

- [ ] More classes (Paladin, Ranger, Necromancer)
- [ ] Passive skill trees per class
- [ ] Procedurally generated room descriptions
- [ ] Shrine rooms with risk/reward choices
- [ ] ASCII art for all characters and enemies
---

## Built With

- Python 3
- colorama

---

*A personal project built to learn Python, OOP, and game logic - and to have something fun to play in the terminal.*
