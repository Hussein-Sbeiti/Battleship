# ui_app.py
# Battleship Project - Tkinter app + screen manager
# Created: 2026-02-06

import tkinter as tk
from app.app_models import GameState
from app.ui_screen import WelcomeScreen, PlacementScreen, BattleScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Battleship")
        self.state = GameState()

        self._container = tk.Frame(self)
        self._container.pack(fill="both", expand=True)

        # Allow screens to expand
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        self.screens = {}
        for Screen in (WelcomeScreen, PlacementScreen, BattleScreen):
            self._add_screen(Screen)

        self.show_screen("WelcomeScreen")

        # Fullscreen
        self.attributes("-fullscreen", True)

        # ESC exits fullscreen (dev convenience)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

    def _add_screen(self, ScreenClass):
        screen = ScreenClass(parent=self._container, app=self)
        self.screens[ScreenClass.__name__] = screen
        screen.grid(row=0, column=0, sticky="nsew")

    def show_screen(self, name: str):
        self.screens[name].tkraise()