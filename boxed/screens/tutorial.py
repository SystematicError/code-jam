from pathlib import Path
from threading import Thread
from typing import List

from playsound import playsound

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
            print(boxed.terminal.move_down(1) + boxed.terminal.move_x(2), end="", flush=True)


def load_screen(file: Path) -> None:
    """Callback for loading screen"""
    tutorial_text = file.read_text(encoding="utf8").splitlines()
    terminal_size = 0, 0
    with boxed.terminal.hidden_cursor():
        with boxed.terminal.cbreak():
            while True:
                if terminal_size != (boxed.terminal.width, boxed.terminal.height):
                    display_tutorial(tutorial_text)
                    terminal_size = (boxed.terminal.width, boxed.terminal.height)

                if boxed.terminal.inkey(timeout=0.1) == "b":
                    Thread(
                        target=lambda: playsound("music/up-down.wav"), daemon=True
                    ).start()
                    return
