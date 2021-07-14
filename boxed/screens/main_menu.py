from blessed import Terminal

from ..border import draw_boundary


def print_options(selection: int, options: list, terminal: Terminal) -> None:
    """
    Prints the options provided and highlights the active selection.

    Args:
        selection (int): A zero indexed integer representing the current selection
        options (list): The list of options to print
        terminal (Terminal): A blessed.Terminal object
    """
    print(terminal.clear, end="")
    draw_boundary(terminal)
    print(terminal.move_y(terminal.height // 2 - len(options) // 2), end="")

    for idx, option in enumerate(options):

        # Move the menu two chars to the side to not interfere with the border
        print(terminal.move_right(2), end="")

        if idx == selection:
            print(terminal.black + terminal.on_white + option + terminal.normal)
        else:
            print(option)


def get_selection(options: list, terminal: Terminal) -> int:
    """
    An interactive prompt for the user to select an option from a list of options.

    Args:
        options (list): List of options for the user choose from
        terminal (Terminal): A blessed.Terminal object

    Returns:
        int: A zero indexed integer representing the chosen selection
    """
    selection = 0

    with terminal.fullscreen() and terminal.hidden_cursor():
        terminal_size = terminal.width, terminal.height

        print(terminal.clear)

        print_options(selection, options, terminal)
        while True:
            with terminal.cbreak():  # Without terminal.cbreak, the terminal cannot take in any input
                key = terminal.inkey(timeout=0.1)

                # Resize border if the terminal size gets changed
                if (terminal.width, terminal.height) != terminal_size:
                    print(terminal.clear)

                    # Draw the content first to avoid content overflow
                    print_options(selection, options, terminal)
                    draw_boundary(terminal)

                    terminal_size = terminal.width, terminal.height

                if key.name == "KEY_UP":
                    selection = (selection - 1) % len(options)
                    print_options(selection, options, terminal)

                elif key.name == "KEY_DOWN":
                    selection = (selection + 1) % len(options)
                    print_options(selection, options, terminal)

                elif key.name == "KEY_ENTER":
                    return selection


def load_screen(options: list, terminal: Terminal) -> int:
    """Callback for loading a screen."""
    return get_selection(options, terminal)
