"""Plays solo and co-op games with random input and fails if anything crashes or hangs.

Run from the repository root: python -m tests.smoke_test
"""
import builtins
import collections
import contextlib
import io
import random

import game
from player import Player

NORMAL_SEEDS = range(30)
STRONG_SEEDS = range(3)
STRONG_MAX_FLOOR = 110  # every zone, every boss up to Sael, and one Abyssal Lord
MAX_INPUTS = 100_000
CHOICES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "", "x"]


class Stop(Exception):
    pass


def fake_input(rng, counter):
    def _input(prompt=""):
        print(prompt)
        counter[0] += 1
        if counter[0] > MAX_INPUTS:
            raise RuntimeError(f"game still running after {MAX_INPUTS} inputs, likely stuck in a loop")
        if "name" in prompt:
            return "Tester"
        if "Play again" in prompt:
            return "n"
        return rng.choice(CHOICES)
    return _input


def make_strong(player):
    player.max_hp = player.hp = 10**9
    player.base_atk = player.atk = 10**6
    return player


def run(label, seed, play):
    rng = random.Random(seed)
    random.seed(seed)
    counter = [0]
    out = io.StringIO()
    original_input = builtins.input
    builtins.input = fake_input(rng, counter)
    try:
        with contextlib.redirect_stdout(out):
            play()
    except Stop:
        pass
    except Exception:
        tail = collections.deque(out.getvalue().splitlines(), maxlen=40)
        print(f"FAIL {label} seed={seed} after {counter[0]} inputs. Last output:")
        print("\n".join(tail))
        raise
    finally:
        builtins.input = original_input
    print(f"ok   {label} seed={seed} ({counter[0]} inputs)")


def capped(run_floor):
    def _run_floor(heroes, floor, bosses_beaten):
        if floor > STRONG_MAX_FLOOR:
            raise Stop
        return run_floor(heroes, floor, bosses_beaten)
    return _run_floor


def play_strong(mode):
    def play():
        saved = game.character_creation, game.run_floor, game.run_coop_floor, game.choose_mode
        original_creation = game.character_creation
        game.character_creation = lambda *args: make_strong(original_creation(*args))
        game.run_floor = capped(game.run_floor)
        game.run_coop_floor = capped(game.run_coop_floor)
        game.choose_mode = lambda: mode
        try:
            game.game_loop()
        finally:
            game.character_creation, game.run_floor, game.run_coop_floor, game.choose_mode = saved
    return play


def random_hero():
    return Player("Tester", random.choice(["Warrior", "Rogue", "Mage"]))


def play_final_boss():
    game.run_floor(random_hero(), 1000, set())


def play_coop_final_boss():
    game.run_coop_floor([random_hero(), random_hero()], 1000, set())


def main():
    for seed in NORMAL_SEEDS:
        run("normal game", seed, game.game_loop)
    for mode in ("solo", "coop"):
        for seed in STRONG_SEEDS:
            run(f"{mode} strong heroes to floor {STRONG_MAX_FLOOR}", seed, play_strong(mode))
    for seed in STRONG_SEEDS:
        run("solo final boss", seed, play_final_boss)
        run("coop final boss", seed, play_coop_final_boss)


if __name__ == "__main__":
    main()
