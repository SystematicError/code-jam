# To prevent playsound() from blocking, the threading library is required
# The block parameter instead as it is not cross platform
from threading import Thread

from playsound import playsound

import boxed
from boxed.art import BANNER
from boxed.border import draw_boundary


def print_options(selection: int, options: list) -> None:
    """
    Prints the options provided and highlights the active selection.

    Args:
        selection (int): A zero indexed integer representing the current selection
        options (list): The list of options to print
    """
    print(boxed.terminal.clear, end="")
    draw_boundary()

    print(
        boxed.terminal.move_y(
            (boxed.terminal.height - len(BANNER.split("\n")) - len(options) - 1) // 2
        ),
        end="",
    )

    for line in BANNER.split("\n"):
        print(boxed.terminal.move_right(2), end="")
        print(line)

    print()

    for idx, option in enumerate(options):
        print(
            boxed.terminal.move_right(2), end=""
        )  # Move 2 right to not interfere with border

        if option == "Quit" and idx != selection:
            print(boxed.terminal.red + "Quit" + boxed.terminal.normal)

        elif option == "Quit" and idx == selection:
            print(
                boxed.terminal.black
                + boxed.terminal.on_red
                + "Quit"
                + boxed.terminal.normal
            )

        elif idx == selection:
            print(
                boxed.terminal.black
                + boxed.terminal.on_green
                + option
                + boxed.terminal.normal
            )

        else:
            print(boxed.terminal.green + option + boxed.terminal.normal)

    print(
        boxed.terminal.move(boxed.terminal.height - 3, boxed.terminal.width - 29)
        + f"Use {boxed.terminal.white_bold}UP{boxed.terminal.normal} and "
        f"{boxed.terminal.white_bold}DOWN{boxed.terminal.normal} to navigate"
    )

    print(
        boxed.terminal.move(boxed.terminal.height - 4, boxed.terminal.width - 23)
        + f"Press {boxed.terminal.white_bold}ENTER{boxed.terminal.normal} to select"
    )


def get_selection(options: list) -> int:
    """
    An interactive prompt for the user to select an option from a list of options.

    Args:
        options (list): List of options for the user choose from

    Returns:
        int: A zero indexed integer representing the chosen selection
    """
    selection = 0

    with boxed.terminal.fullscreen() and boxed.terminal.hidden_cursor():
        terminal_size = boxed.terminal.width, boxed.terminal.height

        print(boxed.terminal.clear)

        print_options(selection, options)
        while True:
            with boxed.terminal.cbreak():  # Without boxed.terminal.cbreak, the terminal cannot take in any input
                key = boxed.terminal.inkey(timeout=0.1)

                # Resize border if the terminal size gets changed
                if (boxed.terminal.width, boxed.terminal.height) != terminal_size:
                    print(boxed.terminal.clear)

                    # Draw the content first to avoid content overflow
                    print_options(selection, options)
                    draw_boundary()

                    terminal_size = boxed.terminal.width, boxed.terminal.height

                if key.name == "KEY_UP":
                    selection = (selection - 1) % len(options)
                    print_options(selection, options)
                    Thread(target=lambda: playsound("music/up-down.wav"), daemon=True).start()

                elif key.name == "KEY_DOWN":
                    selection = (selection + 1) % len(options)
                    print_options(selection, options)
                    Thread(target=lambda: playsound("music/up-down.wav"), daemon=True).start()

                elif key.name == "KEY_ENTER":
                    Thread(target=lambda: playsound("music/up-down.wav"), daemon=True).start()
                    return selection


def load_screen(options: list) -> int:
    """Callback for loading a screen."""
    return get_selection(options)
