from blessed import Terminal


def show_credits(authors: list, terminal: Terminal) -> None:
    """Displays a list of authors who contributed to this project.

    Args:
        authors (list): A dictionary containing the author and their github page url
        terminal (Terminal): A blessed.Terminal object
    """
    print(terminal.clear, end="")
    print(terminal.move_y(terminal.height // 2 - len(authors) // 2), end="")

    with terminal.fullscreen() and terminal.hidden_cursor():
        for author in authors:
            print(
                terminal.white_bold + author + terminal.normal + " - " + authors[author]
            )

        print(
            terminal.move(terminal.height, terminal.width - 18)
            + f"Press {terminal.white_bold}B{terminal.normal} to go back"
        )

        with terminal.cbreak():
            while True:
                if terminal.inkey() == "b":
                    break


def load_screen(authors: list, terminal: Terminal) -> None:
    """Callback for loading a screen."""
    show_credits(authors, terminal)
