# Battleship (Python)

A two-player Battleship game implemented in Python using a graphical interface.  
The game follows the classic Battleship rules with configurable ship counts and turn-based gameplay.

---

## Project Overview

This project is a Python implementation of the Battleship board game.  
Players place ships on a 10×10 grid and take turns firing shots at the opponent’s board.  
The first player to sink all opposing ships wins.

The game is built using **Tkinter** for the user interface and is structured into logical components to separate UI and game logic.

---

## Features (Current & Planned)

### Implemented
- Graphical welcome screen
- Ship count selection (1–5 ships)
- Automatic ship sizing:
  - 1 ship → 1×1
  - 2 ships → 1×1, 1×2
  - 3 ships → 1×1, 1×2, 1×3
  - …
- Shared configuration for both players
- Git version control with GitHub integration

### Planned
- Ship placement screen (10×10 grid)
- Turn-based firing system
- Hit / miss / sunk detection
- Separate tracking and ship boards per player
- Win screen with replay option

---

## Game Rules

- Board size: **10 × 10**
- Number of ships: **1–5**
- Ships are placed horizontally or vertically
- Ships may not overlap
- Players take turns firing one shot at a time
- A hit is recorded if a ship occupies the target square
- A ship is sunk when all its squares are hit
- The game ends when one player sinks all opponent ships

---

## Project Structure

## Project Structure

```text
Battleship/
├── main.py        # Program entry point
├── models.py      # Game state and shared data
├── ui_app.py      # Main application window and screen manager
├── ui_screen.py   # UI screens (welcome, placement, battle, win)
├── README.md      # Project documentation
└── .gitignore     # Ignored files and folders



### File Responsibilities

- **main.py**  
  Starts the application.

- **models.py**  
  Stores shared game state (e.g., number of ships, player data).

- **ui_app.py**  
  Manages the main Tkinter window and screen transitions.

- **ui_screen.py**  
  Contains all UI screens and user interaction logic.

---

## Requirements

- Python 3.8+
- Tkinter (included with standard Python installs)

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Hussein-Sbeiti/Battleship.git
   cd Battleship
   python3 main.py
