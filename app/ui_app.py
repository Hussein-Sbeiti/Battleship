# ui_app.py
# Battleship Project - Tkinter app + screen manager
# Created: 2026-02-06

import tkinter as tk
from app.app_models import GameState
from app.ui_screen import WelcomeScreen, PlacementScreen, BattleScreen

'''
This file defines the main Tkinter application class, App, which acts as the screen manager. 
It creates the root window, initializes the shared GameState, and loads all screens (WelcomeScreen, PlacementScreen, and BattleScreen) 
into a single container frame. The app controls which screen is visible using tkraise(), allowing smooth screen transitions without destroying widgets. 
It also configures fullscreen behavior and provides a single place for screens to access shared state.
'''

class App(tk.Tk):
    def __init__(self):
        # Initialize the main Tkinter window
        super().__init__()

        # Set window title
        self.title("Battleship")
        self.state = GameState()

        # Create the shared game state
        # All screeens read from and write to this object 
        self._container = tk.Frame(self)
        self._container.pack(fill="both", expand=True)

        # Allow screens to expand
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        # Dictionary to store screen instances
        # Key = screen class name, Value = screen object
        self.screens = {}
        for Screen in (WelcomeScreen, PlacementScreen, BattleScreen):
            self._add_screen(Screen)

        self.show_screen("WelcomeScreen")

        # Fullscreen
        self.attributes("-fullscreen", True)

        # ESC exits fullscreen (dev convenience)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

    def _add_screen(self, ScreenClass):
        """
        Create a screen instance and add it to the container.
        Screens are stacked using grid and raised when needed.
        """
        screen = ScreenClass(parent=self._container, app=self)
        self.screens[ScreenClass.__name__] = screen  # Store the screen using its class name
        screen.grid(row=0, column=0, sticky="nsew") # Place the screen in the container

    def show_screen(self, name: str):
        self.screens[name].tkraise()