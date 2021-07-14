import boxed
from boxed.constants import WBorder


def draw_boundary() -> None:
    """
    Prints a border around the app.

    Args:
        terminal (Terminal): A blessed.Terminal object.
    """
    # Upper edge
    print(boxed.terminal.move_xy(0, 0), WBorder.HORIZONTAL * (boxed.terminal.width - 1))

    # Left and Right edges
    for row in range(boxed.terminal.height - 2):
        print(WBorder.VERTICAL, boxed.terminal.move_right(boxed.terminal.width - 4), WBorder.VERTICAL)

    # Bottom edge
    print(boxed.terminal.move_xy(0, boxed.terminal.height - 2), WBorder.HORIZONTAL * (boxed.terminal.width - 1))

    # Top left corner
    print(boxed.terminal.move_xy(0, 0) + WBorder.DOWN_AND_RIGHT)

    # Top right corner
    print(boxed.terminal.move_xy(boxed.terminal.width - 1, 0) + WBorder.DOWN_AND_LEFT)

    # Bottom left corner
    print(boxed.terminal.move_xy(0, boxed.terminal.height - 2) + WBorder.UP_AND_RIGHT)

    # Bottom right corner
    print(boxed.terminal.move_xy(boxed.terminal.width - 1, boxed.terminal.height - 2) + WBorder.UP_AND_LEFT)
