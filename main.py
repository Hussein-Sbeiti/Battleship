'''
Battleship/
  main.py
  app/
    __init__.py
    ui_app.py
    ui_screen.py
    models.py
  game/
    __init__.py
    game_board.py
    game_models.py
    ships.py
    rules.py        
    coords.py       
'''

# main.py
# Battleship Project - Program entry point
#
# This file is responsible only for starting the application.
# It should not contain any UI layout or game logic.
#
# Created: 2026-02-06

from app.ui_app import App

def main():
    """
    Entry point for the Battleship application.

    Creates the main App instance and starts the Tkinter
    event loop, which keeps the window running until the
    user closes the application.
    """
    app = App()
    app.mainloop()


# Ensures this file is only executed when run directly,
# and not when imported as a module.
if __name__ == "__main__":
    main()

