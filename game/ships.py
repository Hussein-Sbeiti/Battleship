# game/ships.py
# Battleship Project - ship configuration helpers
# Created: 2026-02-06

from dataclasses import dataclass
from typing import List


@dataclass
class Ship:
    """
    A ship is defined mainly by its length.
    We'll track its cells/hits later during gameplay.
    """
    length: int


def build_ship_set(num_ships: int) -> List[Ship]:
    """
    Convert the welcome-screen selection into a ship set.
    1 -> [1]
    2 -> [1,2]
    3 -> [1,2,3]
    ...
    """
    return [Ship(length=i) for i in range(1, num_ships + 1)]