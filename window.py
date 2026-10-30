"""Terminal Descent in a desktop window, with a story log, choice buttons, HP/MP bars and enemy art.

Run with: python window.py
"""
import os
import queue
import re
import sys
import threading
import tkinter as tk
import traceback
from tkinter import font as tkfont

import ui_bridge
from enemy_art import get_enemy_art

BG = "#14161a"
PANEL = "#1d2026"
BUTTON = "#2a2f38"
BUTTON_ACTIVE = "#3a4150"
TEXT = "#d8d8d8"
MUTED = "#8a8f98"
COLOURS = {
    "red": "#ff6b6b", "green": "#7bd88f", "yellow": "#f5c542",
    "blue": "#6ab0ff", "magenta": "#d68cff", "cyan": "#5fd7d7",
}
BAR_WIDTH = 300
MAX_LOG_LINES = 4000

ENCOUNTER = re.compile(r"(?:A (.+) appears!|BOSS: (.+))$")
ENEMY_INTRO_HP = re.compile(r"^\s*HP: (\d+) \| ATK")
ENEMY_HP = re.compile(r"^\s*HP: (-?\d+)/(\d+)$")
PLAYER_HIT = re.compile(r"You attack for \d+ damage! \((-?\d+)/(\d+) HP remaining\)")
ENEMY_GONE = re.compile(r"You defeated |defeated by |The boss has been defeated|YOU HAVE FALLEN")
TURN_HEADER = re.compile(r"^\s*(.+?) \| HP: (-?\d+)/(\d+) \| MP: (-?\d+)/(\d+)$")
SHEET = re.compile(r"^\s*(.+?) the (Warrior|Rogue|Mage) — Level (\d+)$")
SHEET_HP = re.compile(r"^\s*HP:\s+(-?\d+)/(\d+)(?: \| MP: (-?\d+)/(\d+))?$")
SHEET_MP = re.compile(r"^\s*MP:\s+(-?\d+)/(\d+)$")
PARTY = re.compile(r"^\s*Party: (.+)$")
PARTY_MEMBER = re.compile(r"^(.+) (-?\d+)/(\d+) HP$")


class GameWindow:
    def __init__(self, root):
        self.root = root
        self.events = queue.Queue()
        self.answers = queue.Queue()
        self.waiting = False
        self.colour = None
        self.partial_line = ""
        self.sheet_hero = None
        self.heroes = {}
        self.enemy = None

        root.title("Terminal Descent")
        root.geometry("1180x780")
        root.minsize(900, 600)
        root.configure(bg=BG)

        self.mono = tkfont.nametofont("TkFixedFont").copy()
        self.mono.configure(size=11)
        self.ui_font = tkfont.nametofont("TkDefaultFont").copy()
        self.ui_font.configure(size=11)
        self.title_font = self.ui_font.copy()
        self.title_font.configure(size=13, weight="bold")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        log_frame = tk.Frame(root, bg=BG)
        log_frame.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=(12, 6))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.log = tk.Text(
            log_frame, wrap="word", bg=BG, fg=TEXT, font=self.mono, borderwidth=0,
            highlightthickness=0, padx=8, pady=8, state="disabled", cursor="arrow",
        )
        self.log.grid(row=0, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(
            log_frame, command=self.log.yview, bg=BUTTON, activebackground=BUTTON_ACTIVE,
            troughcolor=BG, highlightthickness=0, borderwidth=0, elementborderwidth=0, relief="flat",
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=scrollbar.set)
        for name, hex_colour in COLOURS.items():
            self.log.tag_configure(name, foreground=hex_colour)

        side = tk.Frame(root, bg=PANEL, width=BAR_WIDTH + 40)
        side.grid(row=0, column=1, rowspan=2, sticky="ns", padx=(6, 12), pady=12)
        side.grid_propagate(False)
        side.columnconfigure(0, weight=1)

        self.enemy_frame = tk.Frame(side, bg=PANEL)
        self.enemy_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))
        self.enemy_name = tk.Label(self.enemy_frame, bg=PANEL, fg=COLOURS["red"], font=self.title_font, anchor="w")
        self.enemy_name.pack(fill="x")
        self.enemy_art = tk.Label(self.enemy_frame, bg=PANEL, fg=COLOURS["red"], font=self.mono, justify="left", anchor="w")
        self.enemy_art.pack(fill="x", pady=(8, 8))
        self.enemy_bar = tk.Canvas(self.enemy_frame, width=BAR_WIDTH, height=20, bg=PANEL, highlightthickness=0)
        self.enemy_bar.pack(anchor="w")

        tk.Frame(side, bg=BUTTON, height=1).grid(row=1, column=0, sticky="ew", padx=20, pady=12)
        self.heroes_frame = tk.Frame(side, bg=PANEL)
        self.heroes_frame.grid(row=2, column=0, sticky="ew", padx=20)

        prompt_frame = tk.Frame(root, bg=BG)
        prompt_frame.grid(row=1, column=0, sticky="ew", padx=(12, 6), pady=(0, 12))
        prompt_frame.columnconfigure(0, weight=1)
        self.prompt_label = tk.Label(prompt_frame, bg=BG, fg=COLOURS["yellow"], font=self.ui_font, anchor="w")
        self.prompt_label.grid(row=0, column=0, sticky="ew")
        self.buttons_frame = tk.Frame(prompt_frame, bg=BG)
        self.buttons_frame.grid(row=1, column=0, sticky="ew", pady=6)
        self.buttons_frame.columnconfigure((0, 1), weight=1, uniform="buttons")
        entry_row = tk.Frame(prompt_frame, bg=BG)
        entry_row.grid(row=2, column=0, sticky="ew")
        entry_row.columnconfigure(0, weight=1)
        self.entry = tk.Entry(
            entry_row, bg=PANEL, fg=TEXT, insertbackground=TEXT, font=self.mono,
            relief="flat", highlightthickness=1, highlightbackground=BUTTON, highlightcolor=COLOURS["cyan"],
        )
        self.entry.grid(row=0, column=0, sticky="ew", ipady=6)
        self.entry.bind("<Return>", lambda event: self.submit_entry())
        self.send_button = self.make_button(entry_row, "Send", self.submit_entry)
        self.send_button.grid(row=0, column=1, padx=(8, 0))

        self.render_enemy()
        self.render_heroes()
        self.entry.focus_set()

        threading.Thread(target=self.run_game, daemon=True).start()
        self.root.after(30, self.poll)

    def make_button(self, parent, text, command):
        return tk.Button(
            parent, text=text, command=command, bg=BUTTON, fg=TEXT, activebackground=BUTTON_ACTIVE,
            activeforeground=TEXT, relief="flat", borderwidth=0, highlightthickness=0, font=self.ui_font, anchor="w",
            justify="left", padx=12, pady=7, cursor="hand2", wraplength=360,
        )

    # Game thread

    def run_game(self):
        try:
            ui_bridge.run_game(lambda text: self.events.put(("text", text)), self.ask)
        except Exception:
            self.events.put(("text", "\n" + traceback.format_exc()))
        self.events.put(("done",))

    def ask(self, prompt, choices):
        self.events.put(("ask", prompt, choices))
        return self.answers.get()

    # UI thread

    def poll(self):
        while True:
            try:
                event = self.events.get_nowait()
            except queue.Empty:
                break
            if event[0] == "text":
                self.append(event[1])
            elif event[0] == "ask":
                self.show_prompt(event[1], event[2])
            else:
                self.show_finished()
        self.root.after(30, self.poll)

    def append(self, text):
        pieces, self.colour = ui_bridge.split_colours(text, self.colour)
        self.log.configure(state="normal")
        for piece, colour in pieces:
            self.log.insert("end", piece, colour or ())
        lines = int(self.log.index("end-1c").split(".")[0])
        if lines > MAX_LOG_LINES:
            self.log.delete("1.0", f"{lines - MAX_LOG_LINES}.0")
        self.log.configure(state="disabled")
        self.log.see("end")

        self.partial_line += ui_bridge.ANSI.sub("", text)
        *lines, self.partial_line = self.partial_line.split("\n")
        for line in lines:
            self.read_status(line)

    def show_prompt(self, prompt, choices):
        self.waiting = True
        if prompt == ">":
            prompt = "Choose an option, or type its number:"
        self.prompt_label.configure(text=prompt)
        for child in self.buttons_frame.winfo_children():
            child.destroy()
        for i, (answer, label) in enumerate(choices):
            text = label if answer in ("y", "n") else f"{answer}. {label}"
            button = self.make_button(self.buttons_frame, text, lambda a=answer: self.send(a))
            button.grid(row=i // 2, column=i % 2, sticky="ew", padx=3, pady=3)
        self.root.update_idletasks()  # the buttons just took space from the log
        self.log.see("end")
        self.entry.focus_set()

    def submit_entry(self):
        if self.waiting:
            answer = self.entry.get()
            self.entry.delete(0, "end")
            self.send(answer)

    def send(self, answer):
        if not self.waiting:
            return
        self.waiting = False
        for child in self.buttons_frame.winfo_children():
            child.destroy()
        self.prompt_label.configure(text="")
        self.answers.put(answer)

    def show_finished(self):
        self.prompt_label.configure(text="The dungeon remains. Close the window to exit.")
        self.entry.configure(state="disabled")
        self.send_button.configure(state="disabled")
        self.make_button(self.buttons_frame, "Quit", self.root.destroy).grid(row=0, column=0, sticky="ew", padx=3)

    # Status panel

    def read_status(self, line):
        if "Choose a mode:" in line:
            self.heroes.clear()
            self.enemy = None
        elif match := ENCOUNTER.search(line):
            name = match.group(1) or match.group(2)
            self.enemy = {"name": name, "hp": None, "max_hp": None}
        elif "The hooded stranger rises" in line:
            self.enemy = {"name": "???", "hp": None, "max_hp": None}
        elif ENEMY_GONE.search(line):
            self.enemy = None
        elif self.enemy and (match := ENEMY_INTRO_HP.match(line)):
            self.enemy["hp"] = self.enemy["max_hp"] = int(match.group(1))
        elif self.enemy and (match := PLAYER_HIT.search(line)):
            self.enemy["hp"], self.enemy["max_hp"] = int(match.group(1)), int(match.group(2))
        elif match := TURN_HEADER.match(line):
            self.update_hero(match.group(1), hp=match.group(2), max_hp=match.group(3), mp=match.group(4), max_mp=match.group(5))
        elif match := SHEET.match(line):
            self.sheet_hero = match.group(1)
            self.update_hero(self.sheet_hero, char_class=match.group(2), level=match.group(3))
            return
        elif self.sheet_hero and (match := SHEET_HP.match(line)):
            self.update_hero(self.sheet_hero, hp=match.group(1), max_hp=match.group(2))
            if match.group(3):
                self.update_hero(self.sheet_hero, mp=match.group(3), max_mp=match.group(4))
            else:
                return  # show_stats prints MP on the next line
        elif self.sheet_hero and (match := SHEET_MP.match(line)):
            self.update_hero(self.sheet_hero, mp=match.group(1), max_mp=match.group(2))
        elif self.enemy and (match := ENEMY_HP.match(line)):
            self.enemy["hp"], self.enemy["max_hp"] = int(match.group(1)), int(match.group(2))
        elif match := PARTY.match(line):
            for part in match.group(1).split(" | "):
                if member := PARTY_MEMBER.match(part):
                    self.update_hero(member.group(1), hp=member.group(2), max_hp=member.group(3))
                elif part.endswith(" DOWN"):
                    self.update_hero(part[:-len(" DOWN")], hp=0)
        else:
            self.sheet_hero = None
            return
        self.sheet_hero = None
        self.render_enemy()
        self.render_heroes()

    def update_hero(self, name, **stats):
        hero = self.heroes.setdefault(name, {})
        hero.update({key: value if key == "char_class" else int(value) for key, value in stats.items()})

    def render_enemy(self):
        if not self.enemy:
            self.enemy_name.configure(text="No enemy", fg=MUTED)
            self.enemy_art.configure(text="")
            self.enemy_bar.delete("all")
            return
        self.enemy_name.configure(text=self.enemy["name"], fg=COLOURS["red"])
        self.enemy_art.configure(text="\n".join(get_enemy_art(self.enemy["name"])))
        self.enemy_bar.delete("all")
        if self.enemy["max_hp"]:
            draw_bar(self.enemy_bar, "HP", self.enemy["hp"], self.enemy["max_hp"], COLOURS["red"], self.ui_font)

    def render_heroes(self):
        for child in self.heroes_frame.winfo_children():
            child.destroy()
        if not self.heroes:
            tk.Label(self.heroes_frame, text="No heroes yet", bg=PANEL, fg=MUTED, font=self.ui_font, anchor="w").pack(fill="x")
        for name, hero in self.heroes.items():
            title = name
            if "char_class" in hero:
                title += f" the {hero['char_class']}"
            if "level" in hero:
                title += f"  ·  Lv {hero['level']}"
            down = hero.get("hp", 1) <= 0
            tk.Label(
                self.heroes_frame, text=title + ("  ·  DOWN" if down else ""), bg=PANEL,
                fg=MUTED if down else COLOURS["cyan"], font=self.title_font, anchor="w",
            ).pack(fill="x", pady=(8, 4))
            for label, key, colour in (("HP", "hp", COLOURS["green"]), ("MP", "mp", COLOURS["blue"])):
                if hero.get(f"max_{key}"):
                    bar = tk.Canvas(self.heroes_frame, width=BAR_WIDTH, height=20, bg=PANEL, highlightthickness=0)
                    bar.pack(anchor="w", pady=2)
                    draw_bar(bar, label, hero.get(key, 0), hero[f"max_{key}"], colour, self.ui_font)


def draw_bar(canvas, label, value, maximum, colour, font):
    fraction = max(0.0, min(1.0, value / maximum))
    canvas.create_rectangle(0, 0, BAR_WIDTH, 20, fill=BUTTON, width=0)
    if fraction:
        canvas.create_rectangle(0, 0, int(BAR_WIDTH * fraction), 20, fill=colour, width=0)
    canvas.create_text(8, 10, text=f"{label} {max(0, value)}/{maximum}", anchor="w", fill="#101215" if fraction > 0.3 else TEXT, font=font)


def main():
    root = tk.Tk()
    window = GameWindow(root)
    # CI sets this to check that a build opens the window and reaches the first menu.
    self_test = os.environ.get("TERMINAL_DESCENT_SELF_TEST")
    if self_test:
        root.after(5000, root.destroy)
    root.mainloop()
    if self_test and not window.waiting:
        sys.exit("Self-test failed: the game never asked for input.")


if __name__ == "__main__":
    main()
