from pathlib import Path
from typing import List

import boxed
from boxed.border import draw_boundary


def display_tutorial(lines: List[str]) -> None:
    """Wraps and prints tutorial text"""
    print(boxed.terminal.clear, end="")
    print(
        boxed.terminal.move(boxed.terminal.height - 3, boxed.terminal.width - 20)
        + f"Press {boxed.terminal.white_bold}B{boxed.terminal.normal} to go back"
    )
    draw_boundary()
    print(boxed.terminal.move_xy(2, 2), end="")

    lines = [
        line.format(
            title=boxed.terminal.white_underline + boxed.terminal.bold,
            bold=boxed.terminal.bold,
            normal=boxed.terminal.normal,
            breakline=boxed.terminal.white_underline + boxed.terminal.normal,
        )
        for line in lines
    ]

    for line in lines:
        if line.startswith(boxed.terminal.white_underline):
            print(boxed.terminal.move_down(1) + boxed.terminal.move_x(2), end="")

        for wrapped_line in boxed.terminal.wrap(line, width=boxed.terminal.width - 4):
            print(wrapped_line, end="")
            print(boxed.terminal.move_down(1) + boxed.terminal.move_x(2), end="")


def load_screen(file: Path) -> None:
    """Callback for loading screen"""
    with boxed.terminal.hidden_cursor():
        display_tutorial(file.read_text(encoding="utf8").splitlines())
        input()
        # When i add the below lines it seems to break the code, nothing gets displayed

        # with boxed.terminal.cbreak():
        #     while True:
        #         if boxed.terminal.inkey() == "b":
        #             exit()
