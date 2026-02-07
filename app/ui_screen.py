# ui_screen.py
# Battleship Project - UI screens (Frames)
# Each screen is a Tkinter Frame. The App shows one screen at a time.
# Created: 2026-02-06

import tkinter as tk
from tkinter import ttk, messagebox

# Allowed range for ship selection on the welcome screen.
MIN_SHIPS = 1
MAX_SHIPS = 5


class WelcomeScreen(tk.Frame):
    """
    Welcome/setup screen.
    User selects how many ships will be used for the game (1–5).
    That choice is saved into app.state and used later to build ship sizes.
    """

    def __init__(self, parent, app):
        # parent is the container frame created in ui_app.py
        # app is the main App instance (gives access to GameState + screen switching)
        super().__init__(parent)
        self.app = app

        # Main title
        title = tk.Label(self, text="Battleship", font=("Arial", 50, "bold"))
        title.pack(pady=18)

        # Short instruction line
        info = tk.Label(
            self,
            text="Choose how many ships you want (1–5)",
            font=("Arial", 12),
        )
        info.pack(pady=10)

        # Tk variable that stays synced with the combobox selection
        self.choice_var = tk.IntVar(value=MIN_SHIPS)

        # Row container for the label + dropdown
        row = tk.Frame(self)
        row.pack(pady=10)

        tk.Label(row, text="Ships:", font=("Arial", 12)).pack(side="left", padx=8)

        # Dropdown selection (readonly prevents free-typing invalid values)
        self.combo = ttk.Combobox(
            row,
            textvariable=self.choice_var,
            values=list(range(MIN_SHIPS, MAX_SHIPS + 1)),
            state="readonly",
            width=5,
            justify="center",
        )
        self.combo.pack(side="left")

        # Explanation of how the chosen number maps to ship sizes
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

        # Continue button: validate input, save to state, move to next screen
        btn = tk.Button(self, text="Continue →", width=18, command=self.on_continue)
        btn.pack(pady=18)

    def on_continue(self):
        """
        Button handler for 'Continue'.
        - Validates selection is 1–5
        - Stores selection in shared GameState
        - Switches to the next screen
        """
        n = int(self.choice_var.get())

        # Guard against unexpected values (defensive programming)
        if not (MIN_SHIPS <= n <= MAX_SHIPS):
            messagebox.showerror("Invalid", "Pick a number from 1 to 5.")
            return

        # Save the chosen ship count so other screens can use it
        self.app.state.num_ships = n

        # Navigate to the next screen (placeholder for now)
        self.app.show_screen("NextScreen")


class NextScreen(tk.Frame):
    """
    Placeholder screen shown after ship count selection.
    Later this will become the ship placement screen.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Simple title for the placeholder screen
        title = tk.Label(self, text="Next Screen", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Label that we update dynamically when the screen is shown
        self.msg = tk.Label(self, text="", font=("Arial", 12))
        self.msg.pack(pady=10)

        # Back button for testing navigation
        tk.Button(
            self,
            text="Back",
            command=lambda: app.show_screen("WelcomeScreen")
        ).pack(pady=16)

    def tkraise(self, aboveThis=None):
        """
        Runs every time this screen is brought to the front.
        We override tkraise so the text always reflects the latest state.
        """
        n = self.app.state.num_ships
        self.msg.config(
            text=f"You chose {n} ship(s).\nNext: placement screen will go here."
        )

        # Call the parent tkraise to actually show the frame
        super().tkraise(aboveThis)
