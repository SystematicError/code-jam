from blessed import Terminal

import boxed

from .screens import credits, grid, main_menu

boxed.terminal = Terminal()
menu_options = ["Play", "How to play", "Credits", "Quit"]

authors = {"Aaris-Kazi": "https://github.com/Aaris-Kazi",
           "Abhishek10351": "https://github.com/Abhishek10351",
           "DrokoDomi": "https://github.com/DrokoDomi",
           "Numerlor": "https://github.com/Numerlor",
           "ShanTen": "https://github.com/ShanTen",
           "SystematicError": "https://github.com/SystematicError"}

try:
    while True:
        action = main_menu.load_screen(menu_options)

        if action == 0:  # Level selector
            grid.load_screen(cell_size=4, width=5, height=5)

        elif action == 1:  # Tutorial
            pass

        elif action == 2:  # Credits
            credits.load_screen(authors)

        elif action == 3:
            raise KeyboardInterrupt()

except KeyboardInterrupt:
    print(boxed.terminal.clear)
