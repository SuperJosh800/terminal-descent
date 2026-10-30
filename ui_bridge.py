"""Runs the terminal game behind a graphical front end without changing the game code.

The game talks to the player with print() and input(). run_game() redirects both:
printed text goes to write(text), and each input() call asks ask(prompt, choices)
for an answer, where choices are the options of the menu the game printed just before.
"""
import builtins
import re
import sys

ANSI = re.compile(r"\x1b\[(\d+)m")
COLOURS = {"31": "red", "32": "green", "33": "yellow", "34": "blue", "35": "magenta", "36": "cyan"}
MENU_LINE = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")


def split_colours(text, colour=None):
    """Splits text with ANSI colour codes into (text, colour) pieces.

    Returns the pieces and the colour still active at the end, to pass in with the next chunk.
    """
    pieces = []
    pos = 0
    for match in ANSI.finditer(text):
        if match.start() > pos:
            pieces.append((text[pos:match.start()], colour))
        colour = COLOURS.get(match.group(1))
        pos = match.end()
    if pos < len(text):
        pieces.append((text[pos:], colour))
    return pieces, colour


def menu_choices(output, prompt):
    """Returns [(answer, label)] for the numbered menu printed right before an input prompt."""
    if "(y/n)" in prompt:
        return [("y", "Yes"), ("n", "No")]
    choices = []
    for line in reversed(ANSI.sub("", output).splitlines()):
        match = MENU_LINE.match(line)
        if match:
            choices.append((match.group(1), " ".join(match.group(2).split())))
        elif choices or line.strip():
            break
    return choices[::-1]


class _Output:
    def __init__(self, write):
        self.write = write

    def flush(self):
        pass


def run_game(write, ask):
    from game import game_loop

    recent = []

    def capture(text):
        recent.append(text)
        write(text)
        return len(text)

    def answer_input(prompt=""):
        output = "".join(recent)
        recent.clear()
        write(prompt)
        answer = ask(prompt.strip(), menu_choices(output, prompt))
        write(answer + "\n")
        return answer

    saved = sys.stdout, builtins.input
    sys.stdout, builtins.input = _Output(capture), answer_input
    try:
        game_loop()
    finally:
        sys.stdout, builtins.input = saved
