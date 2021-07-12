from os.path import dirname, join
from sys import path

from blessed import Terminal


def load_screen(screen: str, *args, **kwargs) -> None:
    """
    Loads a screen from the `screens` directory

    This function is merely a helper function to manage multiple screens.
    It requires the screens directory be on path otherwise
    python struggles to import it.

    Args:
        screen (str): The name of the screen to load
    """
    __import__(screen).on_screen_load(*args, **kwargs)


# Adds the screens folder to path temporarily otherwise python can't
# access your screens depending on the current directory
path.append(join(dirname(__file__), "screens"))

terminal = Terminal()
menu_options = ["Play", "How to play", "Credits"]

load_screen("main_menu", options=menu_options, terminal=terminal)
