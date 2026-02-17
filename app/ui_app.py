# ui_app.py
# Battleship Project - Tkinter app + screen manager
# Created: 2026-02-06

import tkinter as tk  # Tkinter GUI framework
from app.app_models import GameState  # Shared game state object
from app.ui_screen import WelcomeScreen, PlacementScreen, BattleScreen, WinScreen  # All screen classes


'''
This file defines the main Tkinter application class, App, which acts as the screen manager. 
It creates the root window, initializes the shared GameState, and loads all screens (WelcomeScreen, PlacementScreen, and BattleScreen) 
into a single container frame. The app controls which screen is visible using tkraise(), allowing smooth screen transitions without destroying widgets. 
It also configures fullscreen behavior and provides a single place for screens to access shared state.
'''

class App(tk.Tk):  # Main application window inherits from Tk
    def __init__(self):
        super().__init__()  # Initialize Tk base class
        self.title("Battleship")  # Set window title
        self.state = GameState()  # Create shared game state object

        self._container = tk.Frame(self)  # Container frame to hold all screens
        self._container.pack(fill="both", expand=True)  # Make container fill window

        self._container.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        self._container.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion

        self.screens = {}  # Dictionary to store screen instances

        # Create and register each screen
        for Screen in (WelcomeScreen, PlacementScreen, BattleScreen, WinScreen):
            self._add_screen(Screen)

        self.show_screen("WelcomeScreen")  # Show welcome screen first

        self.attributes("-fullscreen", True)  # Start in fullscreen mode
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))  # ESC exits fullscreen

    def _add_screen(self, ScreenClass):
        screen = ScreenClass(parent=self._container, app=self)  # Create screen instance
        self.screens[ScreenClass.__name__] = screen  # Store by class name
        screen.grid(row=0, column=0, sticky="nsew")  # Stack screens on top of each other

    def show_screen(self, name: str):
        self.screens[name].tkraise()  # Bring selected screen to the front

    def new_game(self):
        n = self.state.num_ships  # Remember selected ship count

        self.state.reset_for_new_game()  # Reset all boards, hits, shots, turns

        self.state.num_ships = n  # Restore ship count

        # Reset placement phase variables
        self.state.placing_player = 1       # Player 1 starts placement again
        self.state.placing_orientation = "H"  # Default orientation
        self.state.placing_ship_len = 1     # First ship size starts at 1

        self.show_screen("WelcomeScreen")  # Return to welcome screen

