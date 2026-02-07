# ui/screens.py
# Battleship Project - UI screens (Frames)
# Created: 2026-02-06

import tkinter as tk
from tkinter import ttk, messagebox

MIN_SHIPS = 1
MAX_SHIPS = 5

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title = tk.Label(self, text="Battleship", font=("Arial", 50, "bold"))
        title.pack(pady=18)

        info = tk.Label(
            self,
            text="Choose how many ships you want (1–5)",
            font=("Arial", 12),
        )
        info.pack(pady=10)

        self.choice_var = tk.IntVar(value=MIN_SHIPS)

        row = tk.Frame(self)
        row.pack(pady=10)

        tk.Label(row, text="Ships:", font=("Arial", 12)).pack(side="left", padx=8)

        self.combo = ttk.Combobox(
            row,
            textvariable=self.choice_var,
            values=list(range(MIN_SHIPS, MAX_SHIPS + 1)),
            state="readonly",
            width=5,
            justify="center",
        )
        self.combo.pack(side="left")

        rules = tk.Label(
            self,
            text=(
                "Ship sizes are based on this number.\n"
                "Example: 3 ships means 1x1, 1x2, 1x3."
            ),
            font=("Arial", 10),
            fg="#444",
        )
        rules.pack(pady=12)

        btn = tk.Button(self, text="Continue →", width=18, command=self.on_continue)
        btn.pack(pady=18)

    def on_continue(self):
        n = int(self.choice_var.get())
        if not (MIN_SHIPS <= n <= MAX_SHIPS):
            messagebox.showerror("Invalid", "Pick a number from 1 to 5.")
            return

        self.app.state.num_ships = n
        self.app.show_screen("NextScreen")


class NextScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title = tk.Label(self, text="Next Screen", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        self.msg = tk.Label(self, text="", font=("Arial", 12))
        self.msg.pack(pady=10)

        tk.Button(self, text="Back", command=lambda: app.show_screen("WelcomeScreen")).pack(pady=16)

    def tkraise(self, aboveThis=None):
        n = self.app.state.num_ships
        self.msg.config(text=f"You chose {n} ship(s).\nNext: placement screen will go here.")
        super().tkraise(aboveThis)
