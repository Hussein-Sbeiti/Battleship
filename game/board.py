# game/board.py
# Battleship Project - Board data + placement validation
# Created: 2026-02-06

# game/game_board.py
from dataclasses import dataclass, field
from typing import List, Tuple

GRID_SIZE = 10


@dataclass
class Board:
    grid: List[List[int]] = field(default_factory=lambda: [[0] * GRID_SIZE for _ in range(GRID_SIZE)])

    def clear(self) -> None:
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    def can_place(self, row: int, col: int, length: int, orientation: str) -> bool:
        cells = self._cells_for_ship(row, col, length, orientation)
        if not cells:
            return False
        return all(self.grid[r][c] == 0 for r, c in cells)

    def place(self, row: int, col: int, length: int, orientation: str) -> List[Tuple[int, int]]:
        cells = self._cells_for_ship(row, col, length, orientation)
        for r, c in cells:
            self.grid[r][c] = 1
        return cells

    def _cells_for_ship(self, row: int, col: int, length: int, orientation: str):
        if orientation not in ("H", "V"):
            return []
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return []
        if length <= 0:
            return []

        if orientation == "H":
            if col + length - 1 >= GRID_SIZE:
                return []
            return [(row, col + i) for i in range(length)]

        if row + length - 1 >= GRID_SIZE:
            return []
        return [(row + i, col) for i in range(length)]