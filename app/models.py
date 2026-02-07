# models.py
# Battleship Project
# Shared data structures that represent the current game state.
# This file contains NO UI code and NO game rules.
# Created: 2026-02-06

# models.py
# Battleship Project - shared game state
# Created: 2026-02-06

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class GameState:
    """
    Shared state for the game. Screens read/write this object.
    """

    # Selected from welcome screen (1–5)
    num_ships: Optional[int] = None

    # Placement phase
    placing_player: int = 1            # 1 or 2
    placing_ship_len: int = 1          # next ship length to place (1..num_ships)
    placing_orientation: str = "H"     # "H" or "V"

    # Boards: 0 = empty, 1 = ship
    p1_board: List[List[int]] = field(default_factory=lambda: [[0] * 10 for _ in range(10)])
    p2_board: List[List[int]] = field(default_factory=lambda: [[0] * 10 for _ in range(10)])

    def reset_for_new_game(self) -> None:
        """Reset placement + boards for a new game."""
        self.placing_player = 1
        self.placing_ship_len = 1
        self.placing_orientation = "H"
        self.p1_board = [[0] * 10 for _ in range(10)]
        self.p2_board = [[0] * 10 for _ in range(10)]