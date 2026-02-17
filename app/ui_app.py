# ui_app.py
# Battleship Project - Tkinter app + screen manager
# Created: 2026-02-06

import tkinter as tk
from app.app_models import GameState
from app.ui_screen import WelcomeScreen, PlacementScreen, BattleScreen, WinScreen

'''
This file defines the main Tkinter application class, App, which acts as the screen manager. 
It creates the root window, initializes the shared GameState, and loads all screens (WelcomeScreen, PlacementScreen, and BattleScreen) 
into a single container frame. The app controls which screen is visible using tkraise(), allowing smooth screen transitions without destroying widgets. 
It also configures fullscreen behavior and provides a single place for screens to access shared state.
'''

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Battleship")
        self.state = GameState()

        self._container = tk.Frame(self)
        self._container.pack(fill="both", expand=True)

        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        self.screens = {}
        for Screen in (WelcomeScreen, PlacementScreen, BattleScreen, WinScreen):
            self._add_screen(Screen)

        self.show_screen("WelcomeScreen")

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

    def _add_screen(self, ScreenClass):
        screen = ScreenClass(parent=self._container, app=self)
        self.screens[ScreenClass.__name__] = screen
        screen.grid(row=0, column=0, sticky="nsew")

    def show_screen(self, name: str):
        self.screens[name].tkraise()

    def new_game(self):
        self.state.reset_for_new_game()
        self.state.num_ships = None

        # cancel any delayed BattleScreen callbacks from the previous game
        battle = self.screens.get("BattleScreen")
        if battle is not None:
            battle.after_cancel(getattr(battle, "_pending_after", ""))
            battle._pending_after = None

        self.show_screen("WelcomeScreen")



