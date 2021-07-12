from blessed import Terminal


def print_options(selection: int, options: list, terminal: Terminal) -> None:
    """
    Prints the options provided and highlights the active selection

    Args:
        selection (int): A zero indexed integer representing the current selection
        options (list): The list of options to print
        terminal (Terminal): A blessed.Terminal object
    """
    print(terminal.clear)
    print(terminal.move_y(terminal.height // 2), end="")

    for idx, option in enumerate(options):
        if idx == selection:
            print(terminal.black + terminal.on_white + option + terminal.normal)
        else:
            print(option)


def get_selection(options: list, terminal: Terminal) -> int:
    """
    An interactive prompt for the user to select an option from a list of options

    Args:
        options (list): List of options for the user choose from
        terminal (Terminal): A blessed.Terminal object

    Returns:
        int: A zero indexed integer representing the chosen selection
    """
    selection = 0

    with terminal.fullscreen() and terminal.hidden_cursor():
        print_options(selection, options, terminal)

        while True:
            with terminal.cbreak():  # Without terminal.cbreak, the terminal cannot take in any input
                key = terminal.inkey()

                if key.name == "KEY_UP":
                    selection -= 1 if selection != 0 else 0
                    print_options(selection, options, terminal)

                elif key.name == "KEY_DOWN":
                    selection += 1 if selection != (len(options) - 1) else 0
                    print_options(selection, options, terminal)

                elif key.name == "KEY_ENTER":
                    return selection


def on_screen_load(options: list, terminal: Terminal) -> int:
    """Callback for loading a screen"""
    return get_selection(options, terminal)
