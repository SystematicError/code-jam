from blessed import Terminal

from boxed.constants import WBorder


def draw_boundary(terminal: Terminal) -> None:
    """
    Prints a border around the app.

    Args:
        terminal (Terminal): A blessed.Terminal object.
    """
    # Upper edge
    print(terminal.move_xy(0, 0), WBorder.HORIZONTAL * (terminal.width - 1))

    # Left and Right edges
    for row in range(terminal.height - 2):
        print(WBorder.VERTICAL, terminal.move_right(terminal.width - 4), WBorder.VERTICAL)

    # Bottom edge
    print(terminal.move_xy(0, terminal.height - 2), WBorder.HORIZONTAL * (terminal.width - 1))

    # Top left corner
    print(terminal.move_xy(0, 0) + WBorder.DOWN_AND_RIGHT)

    # Top right corner
    print(terminal.move_xy(terminal.width - 1, 0) + WBorder.DOWN_AND_LEFT)

    # Bottom left corner
    print(terminal.move_xy(0, terminal.height - 2) + WBorder.UP_AND_RIGHT)

    # Bottom right corner
    print(terminal.move_xy(terminal.width - 1, terminal.height - 2) + WBorder.UP_AND_LEFT)
