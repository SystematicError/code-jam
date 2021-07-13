from blessed import Terminal

from .screens import main_menu

terminal = Terminal()
menu_options = ["Play", "How to play", "Credits"]

main_menu.load_screen(options=menu_options, terminal=terminal)
