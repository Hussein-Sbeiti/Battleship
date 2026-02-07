# ui_app.py
# Battleship Project - Tkinter app + screen manager
# This file owns the main window and handles switching between screens.
# Created: 2026-02-06

import tkinter as tk

# Shared game state (stores selections like num_ships, later boards/turns/etc.)
from app.models import GameState

# Import the screens this app can show
from app.ui_screen import WelcomeScreen, NextScreen


class App(tk.Tk):
    """
    The main application window.

    Responsibilities:
    - Create the Tk window
    - Hold the shared GameState (self.state)
    - Register screens (Frames) and switch between them
    """

    def __init__(self):
        super().__init__()

        # Window title shown by the OS/window manager
        self.title("Battleship")

        # One shared state object for the entire app lifetime
        self.state = GameState()

        # Container frame that will hold every screen (Frame).
        # Only one screen is raised (visible) at a time.
        self._container = tk.Frame(self)
        self._container.pack(fill="both", expand=True)

        # If you want screens to truly expand with the window/container,
        # these lines help when using grid() on the screens.
        # (Safe even if you're fullscreen.)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        # Dictionary of screen instances, keyed by class name
        self.screens = {}

        # Register screens here (add more later: PlacementScreen, BattleScreen, WinScreen)
        self._add_screen(WelcomeScreen)
        self._add_screen(NextScreen)

        # Show the first screen at startup
        self.show_screen("WelcomeScreen")

        # True fullscreen (borderless). Good for "game" feel.
        self.attributes("-fullscreen", True)

        # Escape exits fullscreen (helpful during development/testing)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

    def center_window(self):
        """
        Centers the window based on its requested size.
        Note: Not needed when using fullscreen, but useful if you switch to windowed mode.
        """
        # Ensure geometry values are up-to-date
        self.update_idletasks()

        # Requested size based on widget layout
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()

        # Screen dimensions
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # Compute centered position
        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)

        # Apply size + position
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _add_screen(self, ScreenClass):
        """
        Create one instance of a screen and store it in self.screens.
        All screens share the same parent container (self._container).
        """
        screen = ScreenClass(parent=self._container, app=self)
        name = ScreenClass.__name__

        # Store it so we can raise it later by name
        self.screens[name] = screen

        # Put every screen in the same grid cell;
        # whichever one is raised becomes visible.
        screen.grid(row=0, column=0, sticky="nsew")

    def show_screen(self, name: str):
        """
        Switch to a screen by raising it to the top.
        name must match the Screen class name (e.g., "WelcomeScreen").
        """
        self.screens[name].tkraise()
