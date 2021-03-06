import time
from pathlib import Path

import blessed

import boxed
from boxed.screens import credits, game, main_menu, tutorial, victory
from boxed.utils import get_int_input

boxed.terminal = blessed.Terminal()
try:
    import msvcrt

    # Add a small sleep to blessed's windows terminal kbhit to prevent high CPU usage from the tight loop
    def _kbhit_patch(self, timeout=None):  # noqa: ANN
        end = time.time() + (timeout or 0)
        while True:
            if msvcrt.kbhit():
                return True

            if timeout is not None and end < time.time():
                break
            time.sleep(0.01)

        return False

    blessed.win_terminal.Terminal.kbhit = _kbhit_patch
except ModuleNotFoundError:
    pass


menu_options = ["Play", "How to play", "Credits", "Quit"]

authors = {
    "Aaris-Kazi": "https://github.com/Aaris-Kazi",
    "Abhishek10351": "https://github.com/Abhishek10351",
    "DrokoDomi": "https://github.com/DrokoDomi",
    "Numerlor": "https://github.com/Numerlor",
    "ShanTen": "https://github.com/ShanTen",
    "SystematicError": "https://github.com/SystematicError",
}

try:
    while True:
        action = main_menu.load_screen(menu_options)

        if action == 0:    # Level selector
            cell_size = get_int_input("Enter cell size: ", 10, boxed.terminal.height//2)
            width = get_int_input("Enter grid width: ", 10, boxed.terminal.height//2)
            height = get_int_input("Enter grid height: ", 10, boxed.terminal.height//2)
            recursive_elements = get_int_input(
                "Enter difficulty (number of recursive cells on main puzzle): ",
                10,
                boxed.terminal.height//2
            )
            if game.load_screen(cell_size, width, height, recursive_elements):    # Returns true when game is won
                victory.load_screen()

        elif action == 1:    # Tutorial
            tutorial.load_screen(Path("tutorial.txt"))

        elif action == 2:    # Credits
            credits.load_screen(authors)

        elif action == 3:    # Quit Menu
            raise KeyboardInterrupt()


except KeyboardInterrupt:
    print(boxed.terminal.move_xy(0, boxed.terminal.height), end="")
    print(boxed.terminal.clear, end="")
