# utils/coords.py
# Coordinate helpers for Battleship

LETTERS = "ABCDEFGHIJ"


def col_to_letter(col: int) -> str:
    return LETTERS[col]


def row_to_number(row: int) -> str:
    return str(row + 1)


def to_label(row: int, col: int) -> str:
    return f"{LETTERS[col]}{row + 1}"
