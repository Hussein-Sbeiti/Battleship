# game/rules.py
# Battleship Project - Core battle rules (shots, hit/miss)
# Created: 2026-02-07

'''
This file contains the core Battleship rules, completely independent of the UI. 
The fire_shot() function determines whether a shot is a hit, miss, sink, or already-fired location, 
and updates both the attacker’s shot board and the defender’s incoming board. 
It also tracks hits using a set so ship destruction can be detected efficiently. 
The ships_remaining() function counts how many ships are still afloat and is used to determine when the game is over.
'''
from typing import List, Tuple, Set

UNKNOWN = 0
MISS = 1
HIT = 2

Coord = Tuple[int, int]


def fire_shot(
    shots_board: List[List[int]],         # attacker tracking
    incoming_board: List[List[int]],      # defender incoming marks
    defender_ships: List[List[Coord]],    # defender ships (lists of coords)
    defender_hits: Set[Coord],            # defender hit set
    row: int,
    col: int,
) -> str:
    """
    Returns one of: "already", "miss", "hit", "sink"
    """
    if shots_board[row][col] != UNKNOWN:
        return "already"

    target = (row, col)

    ship_index = None
    for i, ship in enumerate(defender_ships):
        if target in ship:
            ship_index = i
            break

    if ship_index is None:
        shots_board[row][col] = MISS
        incoming_board[row][col] = MISS
        return "miss"

    shots_board[row][col] = HIT
    incoming_board[row][col] = HIT
    defender_hits.add(target)

    ship_coords = defender_ships[ship_index]
    if all(coord in defender_hits for coord in ship_coords):
        return "sink"

    return "hit"


def ships_remaining(defender_ships: List[List[Coord]], defender_hits: Set[Coord]) -> int:
    remaining = 0
    for ship in defender_ships:
        if not all(coord in defender_hits for coord in ship):
            remaining += 1
    return remaining