# models.py
# Battleship Project
# Shared data structures that represent the current game state.
# This file contains NO UI code and NO game rules.
# Created: 2026-02-06

from dataclasses import dataclass
from typing import Optional


@dataclass
class GameState:
    """
    Stores shared state for the entire game.

    This object is created once when the application starts and is
    passed to all screens. It acts as the single source of truth
    for configuration and game progress.
    """

    # Number of ships chosen at the welcome screen (1–5).
    # This value determines the ship sizes for both players:
    #   1 -> [1x1]
    #   2 -> [1x1, 1x2]
    #   ...
    num_ships: Optional[int] = None
