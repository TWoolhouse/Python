from src.log import log
from src.states import State
from src.properties import Properties
import src.game_window

import libs
import gui

class Window:
    def __init__(self, name="Chess"):
        log.debug("Creating Window: %s", name)
        self.window = gui.Window(name, parent=self)
        self.window.winfo_toplevel().protocol("WM_DELETE_WINDOW", lambda: State(State.Game, State.Game.Quit))
        self.game = src.game_window.Window(name)
        PageMainMenu(self.window, "main_menu")
        PageGameMenu(self.window, "game_menu")
        self.window.show_page("main_menu")

    def update(self):
        self.window.update()
        self.game.update()

class PageMainMenu(gui.Page):
    def setup(self):
        self.add(gui.tk.Label(self, text="Welcome to Chess!\n[FLAVOUR TEXT HERE]"), row=1, column=1, pady=15)
        self.add(gui.tk.Button(self, text="Play!", command=gui.cmd(self.show_page, "game_menu")), row=2, column=1, pady=5)

class PageGameMenu(gui.Page):
    def setup(self):
        self.add(gui.tk.Button(self, text="Menu", command=gui.cmd(self.show_page, "main_menu")), row=1, column=1, pady=15)
        self.add(gui.tk.Button(self, text="Open Board", command=gui.cmd(self.parent.parent.game.open)), row=2, column=1, pady=5)
