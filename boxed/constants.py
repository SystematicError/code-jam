import enum


class Border(str, enum.Enum):
    """Thin border characters."""

    VERTICAL = "│"
    HORIZONTAL = "─"
    DOWN_AND_RIGHT = "┌"
    DOWN_AND_HORIZONTAL = "┬"
    DOWN_AND_LEFT = "┐"
    VERTICAL_AND_RIGHT = "├"
    VERTICAL_AND_HORIZONTAL = "┼"
    VERTICAL_AND_LEFT = "┤"
    UP_AND_RIGHT = "└"
    UP_AND_HORIZONTAL = "┴"
    UP_AND_LEFT = "┘"

    def __str__(self):
        return str(self.value)


class WBorder(str, enum.Enum):
    """Wide border characters."""

    HORIZONTAL = "═"
    VERTICAL = "║"
    DOWN_AND_RIGHT = "╔"
    DOWN_AND_HORIZONTAL = "╦"
    DOWN_AND_LEFT = "╗"
    VERTICAL_AND_RIGHT = "╠"
    VERTICAL_AND_HORIZONTAL = "╬"
    VERTICAL_AND_LEFT = "╣"
    UP_AND_RIGHT = "╚"
    UP_AND_HORIZONTAL = "╩"
    UP_AND_LEFT = "╝"

    def __str__(self):
        return str(self.value)
