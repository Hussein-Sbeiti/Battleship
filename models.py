# models.py
# Battleship Project - shared game state
# Created: 2026-02-06

from dataclasses import dataclass
from typing import Optional

@dataclass
class GameState:
    num_ships: Optional[int] = None
