import boxed

from ..border import draw_boundary


def print_authors(authors: dict[str, str]) -> None:
    """Prints a list of authors with links from a dictionary of authors and links."""
    print(boxed.terminal.move_y(boxed.terminal.height // 2 - len(authors) // 2), end="")

    for author in authors:
        print(boxed.terminal.move_right(2), end="")
        print(
            boxed.terminal.link(
                authors[author],
                boxed.terminal.white_bold + author + boxed.terminal.normal + " - " + authors[author]
            )
        )  # Not all terminals support links so it also prints the url next to the author

    print(
        boxed.terminal.move(boxed.terminal.height - 3, boxed.terminal.width - 20)
        + f"Press {boxed.terminal.white_bold}B{boxed.terminal.normal} to go back"
    )
    draw_boundary()


def show_credits(authors: dict[str, str]) -> None:
    """
    Displays a list of authors who contributed to this project.

    Args:
        authors (dict): A dictionary containing the author and their github page url
    """
    with boxed.terminal.fullscreen() and boxed.terminal.hidden_cursor():
        print(boxed.terminal.clear)
        print_authors(authors)

        terminal_size = boxed.terminal.width, boxed.terminal.height

        while True:
            with boxed.terminal.cbreak():
                key = boxed.terminal.inkey(timeout=0.1)

                # Resize border if the terminal size gets changed
                if (boxed.terminal.width, boxed.terminal.height) != terminal_size:
                    print(boxed.terminal.clear)
                    print_authors(authors)
                    draw_boundary()
                    terminal_size = boxed.terminal.width, boxed.terminal.height

                if key == "b":
                    break


def load_screen(authors: dict[str, str]) -> None:
    """Callback for loading a screen."""
    show_credits(authors)
