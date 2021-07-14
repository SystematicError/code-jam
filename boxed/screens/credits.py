from blessed import Terminal

from ..border import draw_boundary


def show_credits(authors: list, terminal: Terminal) -> None:
    """Displays a list of authors who contributed to this project.

    Args:
        authors (list): A dictionary containing the author and their github page url
        terminal (Terminal): A blessed.Terminal object
    """
    with terminal.fullscreen() and terminal.hidden_cursor():
        print(terminal.clear, end="")
        draw_boundary(terminal)
        print(terminal.move_y(terminal.height // 2 - len(authors) // 2), end="")

        for author in authors:
            print(terminal.move_right(2), end="")
            print(
                terminal.white_bold + author + terminal.normal + " - " + authors[author]
            )

        print(
            terminal.move(terminal.height - 3, terminal.width - 20)
            + f"Press {terminal.white_bold}B{terminal.normal} to go back"
        )

        with terminal.cbreak():
            while True:
                if terminal.inkey() == "b":
                    break


def load_screen(authors: list, terminal: Terminal) -> None:
    """Callback for loading a screen."""
    show_credits(authors, terminal)
