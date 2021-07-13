from blessed import Terminal

from .screens import credits, main_menu

terminal = Terminal()
menu_options = ["Play", "How to play", "Credits"]

authors = {"Aaris-Kazi": "https://github.com/Aaris-Kazi",
           "Abhishek10351": "https://github.com/Abhishek10351",
           "DrokoDomi": "https://github.com/DrokoDomi",
           "Numerlor": "https://github.com/Numerlor",
           "ShanTen": "https://github.com/ShanTen",
           "SystematicError": "https://github.com/SystematicError"}

try:
    while True:
        action = main_menu.load_screen(menu_options, terminal)

        if action == 0:    # Level selector
            break

        elif action == 1:    # Tutorial
            pass

        elif action == 2:    # Credits
            credits.load_screen(authors, terminal)

except KeyboardInterrupt:
    pass
