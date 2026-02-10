# game/models.py
# Battleship Project - shared game state
# Created: 2026-02-06

'''
This is an earlier or alternate version of game state modeling that uses Board objects instead of raw lists. 
It tracks placement-related information such as which player is placing ships and the orientation, and it provides a reset method to clear boards between games. 
Compared to app/app_models.py, this version is more minimal and focused on setup rather than full gameplay. 
It’s likely retained for architectural clarity or future refactoring.
'''
from dataclasses import dataclass
from typing import Optional

from game.board import Board


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