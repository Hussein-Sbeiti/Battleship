# Battleship (Python / Tkinter)

A two-player Battleship game built in Python using Tkinter.  
This project follows a multi-screen, turn-based design with hidden boards, ship placement, and full battle logic.

---

## 🎮 Game Overview

Battleship is a classic strategy game where two players place ships on a 10×10 grid and take turns firing shots at the opponent’s board.  
The goal is to sink all of the opponent’s ships first.

This implementation focuses on:
- Clear turn-based gameplay
- Fair hidden information
- Visual feedback for hits, misses, and sunk ships
- Clean code structure and extensibility

---

## 🧱 Project Structure
```Text
Battleship/
│
├── main.py                # Program entry point
│
├── app/
│   ├── init.py
│   ├── ui_app.py          # Main Tkinter app + screen manager
│   └── ui_screen.py       # All UI screens (welcome, placement, battle)
│
├── game/
│   ├── board.py           # Board-related helpers (placement validation)
│   ├── game_models.py     # Game data structures
│   ├── rules.py           # Game rules (fire, hit, miss, sink, win)
│   └── ships.py           # Ship definitions and helpers
│
├── README.md              # Project documentation
└── .gitignore
```
---

## 🖥️ Screens & Flow

### 1️⃣ Welcome Screen
- Player selects number of ships (1–5)
- Ship sizes are automatically:
  - 1 → 1×1
  - 2 → 1×1, 1×2
  - ...
  - 5 → 1×1 … 1×5

---

### 2️⃣ Placement Phase
- Player 1 places ships first, then Player 2
- Ships can be placed horizontally or vertically
- Ships can be **removed and repositioned** by clicking them
- Only the active player’s board is visible
- Opponent board is hidden/disabled
- Must place all ships before continuing

---

### 3️⃣ Battle Phase
- Both boards are visible at all times
- Active player:
  - Sees their own ships + incoming shots
  - Sees opponent board hidden except for their shots
- Gameplay flow:
  1. Select a target cell
  2. Press **FIRE**
  3. Result shown: **HIT / MISS / SINK**
  4. After a short delay, turn switches

#### Visual Indicators
- **X (red)** → hit
- **O (gray)** → miss
- Ships shown in:
  - Green (Player 1)
  - Orange (Player 2)

---

### 4️⃣ Scoreboard
Displayed below the boards:

P1 → Shots | Hits | Misses | Ships Remaining
P2 → Shots | Hits | Misses | Ships Remaining

---

### 5️⃣ Win Condition
- When all ships of one player are sunk:
  - Winner is announced
  - Game resets back to the welcome screen

---

## ⚙️ How to Run

```bash
python3 main.py

Requirements:
	•	Python 3.x
	•	Tkinter (included with most Python installations)

⸻

✅ Completed Features
	•	Multi-screen Tkinter UI
	•	10×10 grids
	•	Ship placement with undo
	•	Hidden information between players
	•	Turn-based firing with FIRE button
	•	Hit / Miss / Sink logic
	•	Scoreboard tracking
	•	Win detection and restart
	•	Git-based project structure

⸻

🔧 TODO / Remaining Improvements

These items are planned to fully match the project requirements and polish the game:
	•	Add row/column labels (A–J, 1–10) to grids (DONE)
	•	Display per-ship hit counters (e.g. 2/3 hits) (DONE)
	• 	Add delays in between actions x
	•	Add a dedicated Win Screen with:
	•	Play Again
	•	Exit
	•	Optional: sound effects for hit/miss/sink
	•	Optional: keyboard input for firing (e.g. “B7”)
	•	Code cleanup & documentation pass

⸻