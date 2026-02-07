# ui_screen.py
# Battleship Project - UI screens
# Created: 2026-02-06

import tkinter as tk
from tkinter import ttk, messagebox

MIN_SHIPS = 1
MAX_SHIPS = 5
GRID_SIZE = 10

FADED_BG = "#e8e8e8"
ACTIVE_BG = "#ffffff"
SHIP_BG = "#1f77b4"

P1_SHIP_BG = "#2ecc71"   # green
P2_SHIP_BG = "#e67e22"   # orange
HIDDEN_BG  = "#bdbdbd"   # hidden ship when it's not your turn
COVER_BG = "#2b2b2b"   # matches your dark theme


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        outer = tk.Frame(self)
        outer.pack(fill="both", expand=True)

        inner = tk.Frame(outer)
        inner.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(inner, text="Battleship", font=("Arial", 50, "bold")).pack(pady=(0, 18))
        tk.Label(inner, text="Choose how many ships you want (1–5)", font=("Arial", 12)).pack(pady=(0, 12))

        self.choice_var = tk.IntVar(value=MIN_SHIPS)

        row = tk.Frame(inner)
        row.pack(pady=(0, 12))
        tk.Label(row, text="Ships:", font=("Arial", 12)).pack(side="left", padx=8)

        ttk.Combobox(
            row,
            textvariable=self.choice_var,
            values=list(range(MIN_SHIPS, MAX_SHIPS + 1)),
            state="readonly",
            width=5,
            justify="center",
        ).pack(side="left")

        tk.Label(
            inner,
            text="Ship sizes are based on this number.\nExample: 3 ships means 1x1, 1x2, 1x3.",
            font=("Arial", 10),
            fg="#444",
            justify="center",
        ).pack(pady=(0, 18))

        tk.Button(inner, text="Continue →", width=18, command=self.on_continue).pack()

    def on_continue(self):
        n = int(self.choice_var.get())
        if not (MIN_SHIPS <= n <= MAX_SHIPS):
            messagebox.showerror("Invalid", "Pick a number from 1 to 5.")
            return

        self.app.state.num_ships = n
        self.app.state.reset_for_new_game()
        self.app.state.num_ships = n
        self.app.show_screen("PlacementScreen")


class PlacementScreen(tk.Frame):
    """
    Two 10x10 grids:
    - Left = Player 1 placement
    - Right = Player 2 placement

    Player 1 places first, clicks Ready.
    Player 2 places next, clicks Ready.
    Then we move to BattleScreen (placeholder for now).
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        root = tk.Frame(self)
        root.pack(fill="both", expand=True, padx=30, pady=20)

        top = tk.Frame(root)
        top.pack(fill="x", pady=(0, 15))

        self.status_lbl = tk.Label(top, text="", font=("Arial", 16, "bold"))
        self.status_lbl.pack(side="left")

        self.orient_btn = tk.Button(top, text="Toggle (H)", command=self.toggle_orientation, width=14)
        self.orient_btn.pack(side="left", padx=(20, 0))

        self.ready_btn = tk.Button(top, text="Ready", command=self.on_ready, width=12)
        self.ready_btn.pack(side="right")

        boards = tk.Frame(root)
        boards.pack(fill="both", expand=True)

        # Player 1 panel
        p1_panel = tk.Frame(boards)
        p1_panel.pack(side="left", fill="both", expand=True, padx=(0, 25))
        tk.Label(p1_panel, text="Player 1", font=("Arial", 16, "bold")).pack(pady=(0, 10))
        self.p1_grid = tk.Frame(p1_panel)
        self.p1_grid.pack()

        # Player 2 panel
        p2_panel = tk.Frame(boards)
        p2_panel.pack(side="left", fill="both", expand=True, padx=(25, 0))
        tk.Label(p2_panel, text="Player 2", font=("Arial", 16, "bold")).pack(pady=(0, 10))
        self.p2_grid = tk.Frame(p2_panel)
        self.p2_grid.pack()

        self.p1_buttons = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.p2_buttons = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]

        self._make_grid(player=1)
        self._make_grid(player=2)

    def tkraise(self, aboveThis=None):
        self.refresh_ui()
        super().tkraise(aboveThis)

    def _make_grid(self, player: int):
        frame = self.p1_grid if player == 1 else self.p2_grid
        cells = self.p1_buttons if player == 1 else self.p2_buttons

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = tk.Label(
                    frame,
                    text="",
                    width=6,          # cell width
                    height=3,         # cell height
                    bg=ACTIVE_BG,
                    relief="solid",
                    borderwidth=1,
                )
                cell.grid(row=r, column=c, padx=1, pady=1)

                # click handler (stored so we can enable/disable later)
                def handler(event, rr=r, cc=c, pp=player):
                    self.on_cell_click(pp, rr, cc)

                cell._click_handler = handler
                cell.bind("<Button-1>", cell._click_handler)

                cells[r][c] = cell

    def toggle_orientation(self):
        s = self.app.state
        s.placing_orientation = "V" if s.placing_orientation == "H" else "H"
        self.orient_btn.config(text=f"Toggle ({s.placing_orientation})")
        self.refresh_ui()

    def on_cell_click(self, player: int, row: int, col: int):
        s = self.app.state

        # Ignore clicks when it's not that player's turn
        if player != s.placing_player:
            return
        
        if s.num_ships is None or s.placing_ship_len > s.num_ships:
            return

        length = s.placing_ship_len
        orient = s.placing_orientation
        board = s.p1_board if player == 1 else s.p2_board

        if not self.can_place(board, row, col, length, orient):
            messagebox.showerror("Invalid placement", "That ship doesn't fit there or overlaps another ship.")
            return

        self.place_ship(board, row, col, length, orient)
        s.placing_ship_len += 1
        self.refresh_ui()

    def can_place(self, board, row, col, length, orient) -> bool:
        if orient == "H":
            if col + length - 1 >= GRID_SIZE:
                return False
            cells = [(row, col + i) for i in range(length)]
        else:
            if row + length - 1 >= GRID_SIZE:
                return False
            cells = [(row + i, col) for i in range(length)]

        # overlap check
        return all(board[r][c] == 0 for r, c in cells)

    def place_ship(self, board, row, col, length, orient):
        if orient == "H":
            for i in range(length):
                board[row][col + i] = 1
        else:
            for i in range(length):
                board[row + i][col] = 1

    def on_ready(self):
        s = self.app.state
        if s.num_ships is None:
            return

        # must place all ships first
        if s.placing_ship_len <= s.num_ships:
            remaining = s.num_ships - (s.placing_ship_len - 1)
            messagebox.showinfo("Not ready", f"Place all ships first. Remaining: {remaining}")
            return

        if s.placing_player == 1:
            # switch to Player 2 placement
            s.placing_player = 2
            s.placing_ship_len = 1
            s.placing_orientation = "H"
            self.orient_btn.config(text="Toggle (H)")
            self.refresh_ui()
            return

        # Player 2 finished placement -> move to battle placeholder
        self.app.show_screen("BattleScreen")

    def refresh_ui(self):
        s = self.app.state
        if s.num_ships is None:
            self.status_lbl.config(text="Placement")
            return

        if s.placing_ship_len <= s.num_ships:
            self.status_lbl.config(
                text=f"Placement — Player {s.placing_player}: ship {s.placing_ship_len}/{s.num_ships} (length {s.placing_ship_len})"
            )
        else:
            self.status_lbl.config(
                text=f"Placement — Player {s.placing_player}: all ships placed. Click Ready."
            )

        p1_turn = (s.placing_player == 1)
        p2_turn = (s.placing_player == 2)

        self._render_board(self.p1_buttons, s.p1_board, show_ships=True, ship_color=P1_SHIP_BG, covered=not p1_turn)
        self._render_board(self.p2_buttons, s.p2_board, show_ships=True, ship_color=P2_SHIP_BG, covered=not p2_turn)

        self._set_active(self.p1_buttons, active=p1_turn)
        self._set_active(self.p2_buttons, active=p2_turn)

    def _render_board(self, cells, board, show_ships: bool, ship_color: str, covered: bool):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if covered:
                    # Completely hide the board
                    cells[r][c].config(bg=COVER_BG)
                    continue

                if board[r][c] == 1 and show_ships:
                    cells[r][c].config(bg=ship_color)
                else:
                    cells[r][c].config(bg=ACTIVE_BG)

    def _set_active(self, cells, active: bool):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if active:
                    cells[r][c].bind("<Button-1>", cells[r][c]._click_handler)
                else:
                    cells[r][c].unbind("<Button-1>")


class BattleScreen(tk.Frame):
    """Placeholder battle screen. Next step is turn-based firing."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        outer = tk.Frame(self)
        outer.pack(fill="both", expand=True)

        inner = tk.Frame(outer)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text="Battle Phase", font=("Arial", 22, "bold")).pack(pady=(0, 10))
        tk.Label(inner, text="Placement complete.\nNext: implement turn-based firing.", font=("Arial", 12)).pack(pady=(0, 16))

        tk.Button(inner, text="Back to Welcome", command=lambda: app.show_screen("WelcomeScreen")).pack()