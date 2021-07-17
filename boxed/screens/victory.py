import boxed
from boxed.art import TROPHY
from boxed.border import draw_boundary


def display_game_over() -> None:
    """Displayed when game successfully finished"""
    print(boxed.terminal.clear, end="")
    print(
        boxed.terminal.move(boxed.terminal.height - 3, boxed.terminal.width - 20)
        + f"Press {boxed.terminal.white_bold}B{boxed.terminal.normal} to go back"
    )
    print(boxed.terminal.yellow, end="")
    print(boxed.terminal.move_xy(boxed.terminal.width // 2 - 8, boxed.terminal.height // 2 - 8), end="")

    trophy_lines = TROPHY.splitlines()
    for row, line in enumerate(trophy_lines):
        print(
            boxed.terminal.move_xy(
                boxed.terminal.width // 2 - len(trophy_lines[0]) // 2,
                row+boxed.terminal.height // 2 - len(trophy_lines) // 2,
            ) + line,
            end="",
        )
    print(boxed.terminal.normal, end="")

    draw_boundary()


def load_screen() -> None:
    """Callback for loading screen"""
    with boxed.terminal.hidden_cursor():
        with boxed.terminal.cbreak():
            while boxed.terminal.inkey() != "b":
                display_game_over()
