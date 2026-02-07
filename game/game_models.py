# game/models.py
# Battleship Project - shared game state
# Created: 2026-02-06

# game/game_models.py
from dataclasses import dataclass
from typing import Optional

from game.game_board import Board


@dataclass
class GameState:
    num_ships: Optional[int] = None

    placing_player: int = 1
    placing_ship_len: int = 1
    placing_orientation: str = "H"

    p1_board: Board = Board()
    p2_board: Board = Board()

    def reset_for_new_game(self) -> None:
        self.placing_player = 1
        self.placing_ship_len = 1
        self.placing_orientation = "H"
        self.p1_board.clear()
        self.p2_board.clear()