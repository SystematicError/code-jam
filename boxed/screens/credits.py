from blessed import Terminal

from ..border import draw_boundary


def print_authors(authors: list, terminal: Terminal) -> None:
    """Prints a list of authors with links from a dictionary of authors and links."""
    print(terminal.move_y(terminal.height // 2 - len(authors) // 2), end="")

    for author in authors:
        print(terminal.move_right(2), end="")
        print(
            terminal.link(
                authors[author],
                terminal.white_bold
                + author
                + terminal.normal
                + " - "
                + authors[author],
            )
        )  # Not all terminals support links so it also prints the url next to the author

    print(
        terminal.move(terminal.height - 3, terminal.width - 20)
        + f"Press {terminal.white_bold}B{terminal.normal} to go back"
    )
    draw_boundary(terminal)


def show_credits(authors: list, terminal: Terminal) -> None:
    """
    Displays a list of authors who contributed to this project.

    Args:
        authors (list): A dictionary containing the author and their github page url
        terminal (Terminal): A blessed.Terminal object
    """
    with terminal.fullscreen() and terminal.hidden_cursor():
        print(terminal.clear)
        print_authors(authors, terminal)

        terminal_size = terminal.width, terminal.height

        while True:
            with terminal.cbreak():
                key = terminal.inkey(timeout=0.1)

                # Resize border if the terminal size gets changed
                if (terminal.width, terminal.height) != terminal_size:
                    print(terminal.clear)
                    print_authors(authors, terminal)
                    draw_boundary(terminal)
                    terminal_size = terminal.width, terminal.height

                if key == "b":
                    break


def load_screen(authors: list, terminal: Terminal) -> None:
    """Callback for loading a screen."""
    show_credits(authors, terminal)
