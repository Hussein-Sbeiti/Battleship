# ui/app.py
# Battleship Project - Tkinter app + screen manager
# Created: 2026-02-06

import tkinter as tk
from models import GameState
from ui_screen import WelcomeScreen, NextScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Battleship")

        self.state = GameState()

        self._container = tk.Frame(self)
        self._container.pack(fill="both", expand=True)

        self.screens = {}
        self._add_screen(WelcomeScreen)
        self._add_screen(NextScreen)

        self.show_screen("WelcomeScreen")

        # TRUE fullscreen (no borders)
        self.attributes("-fullscreen", True)

        # Optional: press ESC to exit fullscreen
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))


    def center_window(self):
        # Make sure Tk calculates final requested size
        self.update_idletasks()

        # Get the window’s requested size based on its contents
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()

        # Screen size
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # Center position
        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)

        # Set size + position in one shot
        self.geometry(f"{w}x{h}+{x}+{y}")


    def _add_screen(self, ScreenClass):
        screen = ScreenClass(parent=self._container, app=self)
        name = ScreenClass.__name__
        self.screens[name] = screen
        screen.grid(row=0, column=0, sticky="nsew")

    def show_screen(self, name: str):
        self.screens[name].tkraise()
