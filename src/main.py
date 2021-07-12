from importlib.util import module_from_spec, spec_from_file_location
from os.path import dirname, join

from blessed import Terminal


def load_screen(screen_name: str, *args, **kwargs) -> None:
    """
    Loads a screen from the `screens` directory

    This function is merely a helper function to manage multiple screens.

    Args:
        screen_name (str): The name of the screen to load
    """
    spec = spec_from_file_location('screens', join(dirname(__file__), f'screens/{screen_name}.py'))
    screen = module_from_spec(spec)
    spec.loader.exec_module(screen)

    screen.on_screen_load(*args, **kwargs)


terminal = Terminal()
menu_options = ["Play", "How to play", "Credits"]

load_screen("main_menu", options=menu_options, terminal=terminal)
