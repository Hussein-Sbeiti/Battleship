'''
battleship/
  main.py
  ui/
    app.py
    screens.py
    widgets.py
  game/
    models.py
    board.py
    ships.py
    rules.py
  utils/
    coords.py
'''
# main.py
# Battleship Project - entry point
# Created: 2026-02-06

from ui_app import App

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
