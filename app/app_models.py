# models.py
# Battleship Project
# Shared data structures that represent the current game state.
# This file contains NO UI code and NO game rules.
# Created: 2026-02-06

'''
This file defines the central game state using a dataclass called GameState. 
It stores everything needed to describe the current game at any moment: 
ship placement info, both players’ boards, shot tracking, ship coordinate lists, hit tracking, and turn management.
There is no UI code and no rules logic here, by design — this makes the state reusable and easy to reason about. 
The reset_for_new_game() method cleanly reinitializes all fields so a fresh game can start without restarting the app.
'''

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Set

UNKNOWN = 0
MISS = 1
HIT = 2

Coord = Tuple[int, int]

@dataclass
class GameState:
    num_ships: Optional[int] = None

    placing_player: int = 1
    placing_ship_len: int = 1
    placing_orientation: str = "H"

    # boards: 0 empty, 1 ship
    p1_board: List[List[int]] = field(default_factory=lambda: [[0] * 10 for _ in range(10)])
    p2_board: List[List[int]] = field(default_factory=lambda: [[0] * 10 for _ in range(10)])

    # battle
    current_turn: int = 1

    # outgoing shots (what I shot at opponent)
    p1_shots: List[List[int]] = field(default_factory=lambda: [[0] * 10 for _ in range(10)])
    p2_shots: List[List[int]] = field(default_factory=lambda: [[0] * 10 for _ in range(10)])

    # incoming shots (what opponent shot at me)
    p1_incoming: List[List[int]] = field(default_factory=lambda: [[0] * 10 for _ in range(10)])
    p2_incoming: List[List[int]] = field(default_factory=lambda: [[0] * 10 for _ in range(10)])

    # ships as coordinate lists (set later during placement)
    p1_ships: List[List[Coord]] = field(default_factory=list)
    p2_ships: List[List[Coord]] = field(default_factory=list)

    # hit coords on each player’s ships
    p1_hits: Set[Coord] = field(default_factory=set)
    p2_hits: Set[Coord] = field(default_factory=set)

    def reset_for_new_game(self) -> None:
        self.placing_player = 1
        self.placing_ship_len = 1
        self.placing_orientation = "H"

        self.p1_board = [[0] * 10 for _ in range(10)]
        self.p2_board = [[0] * 10 for _ in range(10)]

        self.current_turn = 1
        self.p1_shots = [[0] * 10 for _ in range(10)]
        self.p2_shots = [[0] * 10 for _ in range(10)]
        self.p1_incoming = [[0] * 10 for _ in range(10)]
        self.p2_incoming = [[0] * 10 for _ in range(10)]

        self.p1_ships = []
        self.p2_ships = []
        self.p1_hits = set()
        self.p2_hits = set()