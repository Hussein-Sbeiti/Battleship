# game/board.py
# Battleship Project - Board data + placement validation
# Created: 2026-02-06

'''
This file defines a lightweight Board class that represents a 10×10 grid and provides helper methods for ship placement. 
It knows how to check whether a ship can be placed (can_place), how to place it (place), 
and how to compute which cells a ship would occupy based on position, length, and orientation. 
The board itself does not know about players, turns, or hits — it strictly manages grid validity. 
This separation keeps placement logic clean and reusable.
'''
from dataclasses import dataclass, field
from typing import List, Tuple

GRID_SIZE = 10


@dataclass
class Board:
    # 2D grid representing the board
    # 0 = empty cell
    # 1 = ship occupies cell
    grid: List[List[int]] = field(default_factory=lambda: [[0] * GRID_SIZE for _ in range(GRID_SIZE)])

    def clear(self) -> None:
        """
        Reset the board to an empty state.
        Used when starting a new game.
        """
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    def can_place(self, row: int, col: int, length: int, orientation: str) -> bool:
        """
        Check whether a ship can be placed at the given position.
        Returns True if the ship fits on the board and does not overlap.
        """
        cells = self._cells_for_ship(row, col, length, orientation) # Get all cells the ship would occupy
        if not cells: # Invalid placement (out of bounds or bad input)
            return False
        return all(self.grid[r][c] == 0 for r, c in cells) # Ensure all target cells are empty

    def place(self, row: int, col: int, length: int, orientation: str) -> List[Tuple[int, int]]:
        """
        Place a ship on the board.
        Marks the grid cells and returns the ship's coordinates.
        """
        cells = self._cells_for_ship(row, col, length, orientation) # Get the ship's cells
        for r, c in cells: # Mark cells as occupied by a ship
            self.grid[r][c] = 1
        return cells

    def _cells_for_ship(self, row: int, col: int, length: int, orientation: str):
        """
        Internal helper:
        Calculates the list of board cells a ship would occupy.
        Returns an empty list if placement is invalid.
        """
        if orientation not in ("H", "V"): # Orientation must be horizontal or vertical
            return []
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE): # Starting position must be on the board
            return []
        if length <= 0: # Ship length must be positive
            return []

        if orientation == "H": # Horizontal placement and Check right boundary
            if col + length - 1 >= GRID_SIZE:
                return []
            return [(row, col + i) for i in range(length)]

        if row + length - 1 >= GRID_SIZE: # Vertical placement and Check right boundary 
            return []
        return [(row + i, col) for i in range(length)]