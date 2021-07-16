# To prevent playsound() from blocking, the threading library is required
# The block parameter instead as it is not cross platform
from threading import Thread

from blessed import Terminal
from playsound import playsound

from ..art import BANNER
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

    print(
        terminal.move_y(
            (terminal.height - len(BANNER.split("\n")) - len(options) - 1) // 2
        ),
        end="",
    )

    for line in BANNER.split("\n"):
        print(terminal.move_right(2), end="")
        print(line)

    print()

    for idx, option in enumerate(options):
        print(
            terminal.move_right(2), end=""
        )  # Move 2 right to not interfere with border

        if option == "Quit" and idx != selection:
            print(terminal.red + "Quit" + terminal.normal)

        elif option == "Quit" and idx == selection:
            print(terminal.black + terminal.on_red + "Quit" + terminal.normal)

        elif idx == selection:
            print(terminal.black + terminal.on_green + option + terminal.normal)

        else:
            print(terminal.green + option + terminal.normal)

    print(
        terminal.move(terminal.height - 3, terminal.width - 29)
        + f"Use {terminal.white_bold}UP{terminal.normal} and {terminal.white_bold}DOWN{terminal.normal} to navigate"
    )

    print(
        terminal.move(terminal.height - 4, terminal.width - 23)
        + f"Press {terminal.white_bold}ENTER{terminal.normal} to select"
    )


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
                    Thread(target=lambda: playsound("music/up-down.wav"), daemon=True).start()

                elif key.name == "KEY_DOWN":
                    selection = (selection + 1) % len(options)
                    print_options(selection, options, terminal)
                    Thread(target=lambda: playsound("music/up-down.wav"), daemon=True).start()

                elif key.name == "KEY_ENTER":
                    return selection


def load_screen(options: list, terminal: Terminal) -> int:
    """Callback for loading a screen."""
    return get_selection(options, terminal)
