from blessed import Terminal


def draw_boundary(terminal: Terminal) -> None:
    """
    Prints a border around the app.

    Args:
        terminal (Terminal): A blessed.Terminal object.
    """
    VERTICAL_EDGE = "║"
    HORIZONTAL_EDGE = "═"
    TOP_LEFT_CORNER = "╔"
    TOP_RIGHT_CORNER = "╗"
    BOTTOM_LEFT_CORNER = "╚"
    BOTTOM_RIGHT_CORNER = "╝"

    # Upper edge
    print(terminal.move_xy(0, 0), HORIZONTAL_EDGE * (terminal.width - 1))

    # Left and Right edges
    for row in range(terminal.height - 2):
        print(VERTICAL_EDGE, terminal.move_right(terminal.width - 4), VERTICAL_EDGE)

    # Bottom edge
    print(
        terminal.move_xy(0, terminal.height - 2), HORIZONTAL_EDGE * (terminal.width - 1)
    )

    # Top left corner
    print(terminal.move_xy(0, 0) + TOP_LEFT_CORNER)

    # Top right corner
    print(terminal.move_xy(terminal.width - 1, 0) + TOP_RIGHT_CORNER)

    # Bottom left corner
    print(terminal.move_xy(0, terminal.height - 2) + BOTTOM_LEFT_CORNER)

    # Bottom right corner
    print(
        terminal.move_xy(terminal.width - 1, terminal.height - 2) + BOTTOM_RIGHT_CORNER
    )
