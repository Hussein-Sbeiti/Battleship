# ui_screen.py
# Battleship Project - UI screens
# Created: 2026-02-06

'''
This is the largest and most important UI file, containing all three game screens and nearly all player interaction.

WelcomeScreen lets the user choose how many ships to play with and initializes the game state accordingly.

PlacementScreen handles ship placement for both players, enforcing turn order, ship sizes, orientation toggling, overlap rules, and allowing ships to be removed by clicking them again.

BattleScreen manages the actual gameplay: selecting targets, firing shots, displaying hits/misses/sinks, switching turns with a delay, updating the scoreboard, and detecting win conditions.

This file focuses on UI behavior and flow, while delegating rule enforcement (hits, sinks, remaining ships) to the game.rules module

'''

import tkinter as tk
from tkinter import ttk, messagebox
from game.rules import fire_shot, ships_remaining, ship_hit_counters, UNKNOWN, MISS, HIT
from game.coords import col_to_letter, row_to_number


MIN_SHIPS = 1
MAX_SHIPS = 5
GRID_SIZE = 10

ACTIVE_BG = "#ffffff"
COVER_BG = "#2b2b2b"

P1_SHIP_BG = "#2ecc71"
P2_SHIP_BG = "#e67e22"

MISS_BG = "#95a5a6"
HIT_BG = "#c0392b"

HIGHLIGHT_BG = "#f1c40f"
TURN_DELAY_MS = 3000


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

        # Top-left empty corner
        tk.Label(frame, text="", width=4).grid(row=0, column=0)

        # Column headers A–J
        for c in range(GRID_SIZE):
            tk.Label(
                frame,
                text=col_to_letter(c),
                font=("Arial", 12, "bold")
            ).grid(row=0, column=c + 1)

        # Row headers + cells
        for r in range(GRID_SIZE):
            tk.Label(
                frame,
                text=row_to_number(r),
                font=("Arial", 12, "bold")
            ).grid(row=r + 1, column=0)

            for c in range(GRID_SIZE):
                cell = tk.Label(
                    frame,
                    text="",
                    width=6,
                    height=3,
                    bg=ACTIVE_BG,
                    relief="solid",
                    borderwidth=1,
                )
                cell.grid(row=r + 1, column=c + 1, padx=1, pady=1)

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

        if player != s.placing_player:
            return

        if s.num_ships is None:
            return

        board = self._board_for_player(player)
        ships_list = self._ships_list_for_player(player)

        # If clicking an occupied cell: remove that whole ship
        if board[row][col] == 1:
            for i, ship in enumerate(ships_list):
                if (row, col) in ship:
                    # clear cells from board
                    for rr, cc in ship:
                        board[rr][cc] = 0
                    # remove from ships list
                    ships_list.pop(i)
                    self.refresh_ui()
                    return

        # Otherwise place the next required length ship
        length = self._next_required_length(player)
        if length > s.num_ships:
            return  # all ships already placed

        orient = s.placing_orientation

        if not self.can_place(board, row, col, length, orient):
            messagebox.showerror("Invalid placement", "That ship doesn't fit there or overlaps another ship.")
            return

        coords = self.place_ship(board, row, col, length, orient)
        ships_list.append(coords)

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
        coords = []
        if orient == "H":
            for i in range(length):
                board[row][col + i] = 1
                coords.append((row, col + i))
        else:
            for i in range(length):
                board[row + i][col] = 1
                coords.append((row + i, col))
        return coords

    def on_ready(self):
        s = self.app.state
        if s.num_ships is None:
            return

        # must place all ships first
        ships_list = self._ships_list_for_player(s.placing_player)
        if len(ships_list) < s.num_ships:
            remaining = s.num_ships - len(ships_list)
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

        next_len = self._next_required_length(s.placing_player)
        if next_len <= s.num_ships:
            self.status_lbl.config(
                text=f"Placement — Player {s.placing_player}: place ship length {next_len}"
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
                    
    def _ships_list_for_player(self, player: int):
        s = self.app.state
        return s.p1_ships if player == 1 else s.p2_ships

    def _board_for_player(self, player: int):
        s = self.app.state
        return s.p1_board if player == 1 else s.p2_board

    def _next_required_length(self, player: int) -> int:
        s = self.app.state
        if s.num_ships is None:
            return 1
        placed_lengths = {len(ship) for ship in self._ships_list_for_player(player)}
        for L in range(1, s.num_ships + 1):
            if L not in placed_lengths:
                return L
        return s.num_ships + 1  # means "done"



class BattleScreen(tk.Frame):
    """
    Battle Phase:
    - Left: current player's own board (ships visible) + incoming marks (what opponent did to you)
    - Right: opponent board hidden except your shots (hit/miss shown)
    - Click selects a target cell (highlight only)
    - FIRE confirms the shot
    - Show big HIT/MISS/SINK, then switch turns after TURN_DELAY_MS
    - Scoreboard shows both players stats and ships remaining
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.selected = None        # (row, col) selection on target board
        self.input_locked = False   # lock input during result delay

        root = tk.Frame(self)
        root.pack(fill="x", expand=True)
        self.after(50, lambda: self.score_lbl.config(wraplength=self.winfo_width() - 80))

        header = tk.Frame(root)
        header.pack(fill="x", expand=True)

        self.turn_lbl = tk.Label(header, text="", font=("Arial", 22, "bold"), anchor="center")
        self.turn_lbl.pack(fill="x")


        self.result_lbl = tk.Label(
            header,
            text="",
            font=("Arial", 32, "bold"),
            anchor="center",
        )
        self.result_lbl.pack(fill="x", expand=True, pady=(10, 10))



        controls = tk.Frame(root)
        controls.pack(fill="x", pady=(0, 12))

        self.fire_btn = tk.Button(
            controls,
            text="FIRE",
            font=("Arial", 18, "bold"),
            width=10,
            command=self.on_fire_pressed,
        )
        self.fire_btn.pack()

        boards = tk.Frame(root)
        boards.pack(fill="both", expand=True)

        # Left panel: Own board
        left = tk.Frame(boards)
        left.pack(side="left", expand=True, padx=(0, 25))
        self.left_title = tk.Label(left, text="Your Board", font=("Arial", 14, "bold"))
        self.left_title.pack(pady=(0, 8))
        self.own_grid = tk.Frame(left)
        self.own_grid.pack()

        # Right panel: Target board
        right = tk.Frame(boards)
        right.pack(side="left", expand=True, padx=(25, 0))
        self.right_title = tk.Label(right, text="Opponent Board", font=("Arial", 14, "bold"))
        self.right_title.pack(pady=(0, 8))
        self.target_grid = tk.Frame(right)
        self.target_grid.pack()

        # Cell matrices
        self.own_cells = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.target_cells = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]

        self._make_grid(self.own_grid, self.own_cells, clickable=False)
        self._make_grid(self.target_grid, self.target_cells, clickable=True)

        # Scoreboard
        self.score_lbl = tk.Label(
            root,
            text="",
            font=("Arial", 16, "bold"),
            justify="center",
            anchor="center",
        )
        self.score_lbl.pack(pady=(14, 0), fill="x")



    def tkraise(self, aboveThis=None):
        self.refresh_ui()
        super().tkraise(aboveThis)

    def _make_grid(self, frame, cells, clickable: bool):

        tk.Label(frame, text="", width=4).grid(row=0, column=0)

        # Column headers
        for c in range(GRID_SIZE):
            tk.Label(
                frame,
                text=col_to_letter(c),
                font=("Arial", 12, "bold")
            ).grid(row=0, column=c + 1)

        for r in range(GRID_SIZE):
            tk.Label(
                frame,
                text=row_to_number(r),
                font=("Arial", 12, "bold")
            ).grid(row=r + 1, column=0)

            for c in range(GRID_SIZE):
                cell = tk.Label(
                    frame,
                    text="",
                    width=5,
                    height=2,
                    bg=ACTIVE_BG,
                    relief="solid",
                    borderwidth=1,
                    font=("Arial", 16, "bold"),
                )
                cell.grid(row=r + 1, column=c + 1, padx=1, pady=1)

                if clickable:
                    def handler(event, rr=r, cc=c):
                        self.on_select(rr, cc)

                    cell._click_handler = handler
                    cell.bind("<Button-1>", cell._click_handler)

                cells[r][c] = cell

    def on_select(self, row: int, col: int):
        if self.input_locked:
            return
        self.selected = (row, col)
        self.refresh_ui()

    def on_fire_pressed(self):
        if self.input_locked:
            return
        if self.selected is None:
            self.result_lbl.config(text="SELECT A CELL")
            return

        s = self.app.state
        row, col = self.selected
        turn = s.current_turn

        # Pick boards by attacker turn
        if turn == 1:
            attacker_shots = s.p1_shots
            defender_incoming = s.p2_incoming
            defender_ships = s.p2_ships
            defender_hits = s.p2_hits
        else:
            attacker_shots = s.p2_shots
            defender_incoming = s.p1_incoming
            defender_ships = s.p1_ships
            defender_hits = s.p1_hits

        result = fire_shot(attacker_shots, defender_incoming, defender_ships, defender_hits, row, col)

        if result == "already":
            self.result_lbl.config(text="ALREADY SHOT")
            return

        # Show result big
        self.result_lbl.config(text=result.upper())
        
        # Win check (after a valid shot)
        if turn == 1:
            defender_ships = s.p2_ships
            defender_hits = s.p2_hits
            winner = 1
        else:
            defender_ships = s.p1_ships
            defender_hits = s.p1_hits
            winner = 2

        if ships_remaining(defender_ships, defender_hits) == 0:
            self.result_lbl.config(text=f"PLAYER {winner} WINS!")
            self.input_locked = True
            self.fire_btn.config(state="disabled")

            # restart back to welcome after short pause
            def restart():
                s.reset_for_new_game()
                s.num_ships = None
                self.app.show_screen("WelcomeScreen")

            self.after(2500, restart)
            return

        # Lock input + disable fire during delay
        self.input_locked = True
        self.fire_btn.config(state="disabled")

        # Clear selection so it doesn't carry over
        self.selected = None

        # Switch turns after delay
        self.after(TURN_DELAY_MS, self._switch_turn)

        # Refresh now so you see the shot marks immediately
        self.refresh_ui()

    def _switch_turn(self):
        s = self.app.state
        s.current_turn = 2 if s.current_turn == 1 else 1

        self.result_lbl.config(text="")
        self.input_locked = False
        self.cell_font = ("Arial", 16, "bold")   # normal
        self.mark_font = ("Arial", 26, "bold")   # X / O only
        self.fire_btn.config(state="normal")

        self.refresh_ui()

    def refresh_ui(self):
        s = self.app.state
        turn = s.current_turn
        self.turn_lbl.config(text=f"Player {turn}'s turn")

        # Define what the current player sees
        if turn == 1:
            own_ship_board = s.p1_board
            own_incoming = s.p1_incoming
            own_color = P1_SHIP_BG

            my_shots = s.p1_shots

            p1_stats = self._stats(s.p1_shots, s.p1_ships, s.p1_hits)
            p2_stats = self._stats(s.p2_shots, s.p2_ships, s.p2_hits)
        else:
            own_ship_board = s.p2_board
            own_incoming = s.p2_incoming
            own_color = P2_SHIP_BG

            my_shots = s.p2_shots

            p1_stats = self._stats(s.p1_shots, s.p1_ships, s.p1_hits)
            p2_stats = self._stats(s.p2_shots, s.p2_ships, s.p2_hits)

        # Render own board (ships visible + incoming marks)
        self._render_own_board(self.own_cells, own_ship_board, own_incoming, own_color)

        # Render target board (opponent hidden except my shots)
        self._render_target_board(self.target_cells, my_shots)

        p1_ship_counters = ship_hit_counters(s.p1_ships, s.p1_hits)
        p2_ship_counters = ship_hit_counters(s.p2_ships, s.p2_hits)

        p1_ship_line = ", ".join(p1_ship_counters) if p1_ship_counters else "-"
        p2_ship_line = ", ".join(p2_ship_counters) if p2_ship_counters else "-"


        # Scoreboard (both players)
        self.score_lbl.config(
            text=(
                f"P1 → Shots: {p1_stats['shots']} | Hits: {p1_stats['hits']} | "
                f"Misses: {p1_stats['misses']} | Ships: {p1_stats['ships']} | "
                f"Ship hits: {p1_ship_line}\n"
                f"P2 → Shots: {p2_stats['shots']} | Hits: {p2_stats['hits']} | "
                f"Misses: {p2_stats['misses']} | Ships: {p2_stats['ships']} | "
                f"Ship hits: {p2_ship_line}"
            )
        )

        



        # Highlight selected cell on target board if valid
        if self.selected is not None:
            r, c = self.selected
            if my_shots[r][c] == UNKNOWN and not self.input_locked:
                self.target_cells[r][c].config(bg=HIGHLIGHT_BG)

        # Disable selection clicks if locked
        if self.input_locked:
            # prevent selecting during delay
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    self.target_cells[r][c].unbind("<Button-1>")
        else:
            # restore bindings
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    self.target_cells[r][c].bind("<Button-1>", self.target_cells[r][c]._click_handler)

    def _render_own_board(self, cells, ship_board, incoming_board, ship_color: str):
        """
        Own view:
        - ships are colored
        - incoming MISS -> gray 'O'
        - incoming HIT  -> red  'X'
        """
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                # base (ship visible)
                if ship_board[r][c] == 1:
                    cells[r][c].config(bg=ship_color, fg="white", text="")
                else:
                    cells[r][c].config(bg=ACTIVE_BG, fg="black", text="")

                # overlay incoming marks
                v = incoming_board[r][c]
                if v == MISS:
                    cells[r][c].config(bg=MISS_BG, fg="black", text="O")
                elif v == HIT:
                    cells[r][c].config(bg=HIT_BG, fg="white", text="X")

    def _render_target_board(self, cells, shots_board):
        """
        Target view:
        - opponent ships hidden (white)
        - your shots show:
          MISS -> gray 'O'
          HIT  -> red  'X'
        """
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                v = shots_board[r][c]
                if v == UNKNOWN:
                    cells[r][c].config(bg=ACTIVE_BG, fg="black", text="")
                elif v == MISS:
                    cells[r][c].config(bg=MISS_BG, fg="black", text="O")
                else:
                    cells[r][c].config(bg=HIT_BG, fg="white", text="X")

    def _stats(self, shots_board, ships_list, hits_set):
        hits = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if shots_board[r][c] == HIT)
        misses = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if shots_board[r][c] == MISS)
        shots = hits + misses
        ships_left = ships_remaining(ships_list, hits_set)
        return {"shots": shots, "hits": hits, "misses": misses, "ships": ships_left}