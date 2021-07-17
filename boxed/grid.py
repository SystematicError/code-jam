from __future__ import annotations

import collections.abc
import enum
import typing

import boxed
from boxed.constants import WBorder

WIDTH_MULTIPLIER = 3


class Direction(enum.IntEnum):  # noqa: D101
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(self) -> Direction:
        """Get the direction opposite of `self`."""
        return Direction((self-2) % 4)


class GridDimensions(typing.NamedTuple):
    """Hold data about the dimensions of a grid."""

    cell_size: int
    width: int
    height: int

    @property
    def char_height(self) -> int:
        """Character height of the grid."""
        return (self.cell_size + 1) * self.height + 1

    @property
    def char_width(self) -> int:
        """Character width of the grid."""
        return (self.cell_size * WIDTH_MULTIPLIER + 1) * self.width + 1


class CellOpenings:
    """Provide an interface for openings of a cell with the ability to rotate them and check for their presence."""

    def __init__(self):
        self._openings = collections.deque((False, False, False, False))
        self.rotatable = True

    def reset_openings(self) -> None:
        """Reset all openings to the closed state."""
        self._openings = collections.deque((False, False, False, False))

    def reverse_opening(self, opening: Direction) -> None:
        """Reverse the current state of `opening`."""
        if self.rotatable:
            self._openings[opening] = not self._openings[opening]

    def rotate(self, n: int = 1) -> None:
        """Rotate the openings by `n` rotations clockwise."""
        if self.rotatable:
            self._openings.rotate(n)

    def __contains__(self, item: Direction):
        return self._openings[item]

    def __repr__(self):
        return "".join(
            (
                "<CellOpenings ",
                ", ".join(f"{dir_.name}={self._openings[dir_]}" for dir_ in Direction),
                ">",
            )
        )


class Cell:
    """Manage a single cell in a grid defined by `grid_dimensions`."""

    def __init__(self, x_pos: int, y_pos: int, grid: Grid):
        self.size = grid.dimensions.cell_size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.openings = CellOpenings()
        self._grid = grid

    def generate_cell_lines(self) -> collections.abc.Iterable[str]:
        """Create the text representation of the cell as individual lines."""
        top_left, top_right, bottom_left, bottom_right = self.get_corners()
        modifier_size = self.size * WIDTH_MULTIPLIER

        yield "".join(
            (
                top_left,
                WBorder.HORIZONTAL * (modifier_size // 2 - (1 - modifier_size % 2)),
                self.get_edge_center(Direction.UP),
                WBorder.HORIZONTAL * (modifier_size // 2),
                top_right,
            )
        )

        for _ in range(self.size // 2 - (1 - modifier_size % 2)):
            yield "".join((WBorder.VERTICAL, " " * modifier_size, WBorder.VERTICAL))

        yield "".join(
            (
                self.get_edge_center(Direction.LEFT),
                " " * modifier_size,
                self.get_edge_center(Direction.RIGHT),
            )
        )

        for _ in range(self.size // 2):
            yield "".join((WBorder.VERTICAL, " " * modifier_size, WBorder.VERTICAL))

        yield "".join(
            (
                bottom_left,
                WBorder.HORIZONTAL * (modifier_size // 2 - (1 - modifier_size % 2)),
                self.get_edge_center(Direction.DOWN),
                WBorder.HORIZONTAL * (modifier_size // 2),
                bottom_right,
            )
        )

    def render(self, colour: typing.Optional[typing.Callable] = None) -> None:
        """Render the cell at its position in the grid."""
        x, y = self.get_cell_start()
        if colour is None:
            colour = boxed.terminal.white_on_black
        for row, line in enumerate(self.generate_cell_lines()):
            print(boxed.terminal.move_xy(x, y + row), end="")
            print(colour("".join(line)))

    def get_cell_start(self) -> tuple[int, int]:
        """Get the coordinates of the left corner of cell."""
        x, y = grid_center_offset_coords(self._grid.dimensions)
        x += (self._grid.dimensions.cell_size * WIDTH_MULTIPLIER * self.x_pos) + self.x_pos
        y += (self._grid.dimensions.cell_size * self.y_pos) + self.y_pos
        return x, y

    def get_corners(self) -> tuple[WBorder, WBorder, WBorder, WBorder]:
        """Get the corner borders of the cell."""
        if self.x_pos == 0:
            if self.y_pos == 0:
                return (
                    WBorder.DOWN_AND_RIGHT,
                    WBorder.DOWN_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_RIGHT,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                )
            elif self.y_pos == self._grid.dimensions.height - 1:
                return (
                    WBorder.VERTICAL_AND_RIGHT,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.UP_AND_RIGHT,
                    WBorder.UP_AND_HORIZONTAL,
                )
            else:
                return (
                    WBorder.VERTICAL_AND_RIGHT,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_RIGHT,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                )

        elif self.x_pos == self._grid.dimensions.width - 1:
            if self.y_pos == 0:
                return (
                    WBorder.DOWN_AND_HORIZONTAL,
                    WBorder.DOWN_AND_LEFT,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_LEFT,
                )
            elif self.y_pos == self._grid.dimensions.height - 1:
                return (
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_LEFT,
                    WBorder.UP_AND_HORIZONTAL,
                    WBorder.UP_AND_LEFT,
                )
            else:
                return (
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_LEFT,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_LEFT,
                )
        else:
            if self.y_pos == 0:
                return (
                    WBorder.DOWN_AND_HORIZONTAL,
                    WBorder.DOWN_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                )
            elif self.y_pos == self._grid.dimensions.height - 1:
                return (
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.UP_AND_HORIZONTAL,
                    WBorder.UP_AND_HORIZONTAL,
                )
            else:
                return (
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                    WBorder.VERTICAL_AND_HORIZONTAL,
                )

    def get_edge_center(self, edge_loc: Direction) -> WBorder:
        """Get the required center piece of an edge with the openings defined by `self.openings`."""
        if edge_loc is Direction.UP:
            neighbour = self._grid.cell_in_direction(self, edge_loc)
            if edge_loc in self.openings and (neighbour is None or self._grid.cells_connected(self, neighbour)):
                return WBorder.VERTICAL_AND_HORIZONTAL
            elif edge_loc in self.openings:
                return WBorder.DOWN_AND_HORIZONTAL
            elif neighbour is not None and edge_loc.opposite() in neighbour.openings:
                return WBorder.UP_AND_HORIZONTAL
            else:
                return WBorder.HORIZONTAL

        elif edge_loc is Direction.DOWN:
            neighbour = self._grid.cell_in_direction(self, edge_loc)
            if edge_loc in self.openings and (neighbour is None or self._grid.cells_connected(self, neighbour)):
                return WBorder.VERTICAL_AND_HORIZONTAL
            elif edge_loc in self.openings:
                return WBorder.UP_AND_HORIZONTAL
            elif neighbour is not None and edge_loc.opposite() in neighbour.openings:
                return WBorder.DOWN_AND_HORIZONTAL
            else:
                return WBorder.HORIZONTAL

        elif edge_loc is Direction.LEFT:
            neighbour = self._grid.cell_in_direction(self, edge_loc)
            if edge_loc in self.openings and (neighbour is None or self._grid.cells_connected(self, neighbour)):
                return WBorder.VERTICAL_AND_HORIZONTAL
            elif edge_loc in self.openings:
                return WBorder.VERTICAL_AND_RIGHT
            elif neighbour is not None and edge_loc.opposite() in neighbour.openings:
                return WBorder.VERTICAL_AND_LEFT
            else:
                return WBorder.VERTICAL

        else:
            neighbour = self._grid.cell_in_direction(self, edge_loc)
            if edge_loc in self.openings and (neighbour is None or self._grid.cells_connected(self, neighbour)):
                return WBorder.VERTICAL_AND_HORIZONTAL
            elif edge_loc in self.openings:
                return WBorder.VERTICAL_AND_LEFT
            elif neighbour is not None and edge_loc.opposite() in neighbour.openings:
                return WBorder.VERTICAL_AND_RIGHT
            else:
                return WBorder.VERTICAL

    def __repr__(self):
        return f"<Cell x={self.x_pos}, y={self.y_pos}, size={self.size}, openings={self.openings}>"


class Grid:
    """A grid of `Cell`s defined by `dimensions`."""

    def __init__(self, dimensions: GridDimensions):
        self.dimensions = dimensions
        self.cells = []

        for y_pos in range(dimensions.height):
            row = []
            for x_pos in range(dimensions.width):
                row.append(Cell(x_pos, y_pos, self))
            self.cells.append(row)

    def print_grid(self) -> bool:
        """
        Print all cells in a centered grid.

        Return True if the grid was displayed, False otherwise.
        """
        print(
            boxed.terminal.move(boxed.terminal.height - 3, boxed.terminal.width - 26)
            + f"Press {boxed.terminal.white_bold}S{boxed.terminal.normal} to stop the game"
        )

        print(boxed.terminal.move_xy(boxed.terminal.width//2-18, boxed.terminal.height//2), end="")

        if self.dimensions.char_width > boxed.terminal.width - 2:
            print("Your terminal's width is too small!")
            return False

        elif self.dimensions.char_height > boxed.terminal.height - 2:
            print("Your terminal's height is too small!")
            return False

        lines = []
        x, y = grid_center_offset_coords(self.dimensions)
        for row, cells in enumerate(self.cells):
            for line_pos, iterables in enumerate(
                zip(*(cell.generate_cell_lines() for cell in cells))
            ):
                lines.append(
                    # Move cursor to start of line.
                    boxed.terminal.move_xy(
                        x, y + line_pos + row * (self.dimensions.cell_size + 1)
                    )
                    # After every cell, move one character left to overlap edges.
                    + boxed.terminal.move_left.join(iterables)
                )
        print("\n".join(lines))
        return True

    def cell_at(self, x: int, y: int) -> typing.Optional[Cell]:
        """Get call at `x` and `y`, or None if the cell is out of bounds."""
        if 0 <= x < self.dimensions.width and 0 <= y < self.dimensions.height:
            return self.cells[y][x]
        else:
            return None

    def cell_in_direction(self, start_cell: Cell, direction: Direction) -> typing.Optional[Cell]:
        """Get cell in `direction` from `start_cell`, or None if the cell is at an edge."""
        if direction is Direction.UP:
            return self.cell_at(start_cell.x_pos, start_cell.y_pos-1)
        elif direction is Direction.DOWN:
            return self.cell_at(start_cell.x_pos, start_cell.y_pos+1)
        elif direction is Direction.LEFT:
            return self.cell_at(start_cell.x_pos-1, start_cell.y_pos)
        elif direction is Direction.RIGHT:
            return self.cell_at(start_cell.x_pos+1, start_cell.y_pos)

    def cells_connected(self, cell1: Cell, cell2: Cell) -> bool:
        """Check if there is a full connection between `cell1` and `cell2`."""
        direction = self.get_direction_between(cell1, cell2)
        if direction is Direction.UP:
            return Direction.UP in cell1.openings and Direction.DOWN in cell2.openings
        elif direction is Direction.DOWN:
            return Direction.DOWN in cell1.openings and Direction.UP in cell2.openings
        elif direction is Direction.LEFT:
            return Direction.LEFT in cell1.openings and Direction.RIGHT in cell2.openings
        else:
            return Direction.RIGHT in cell1.openings and Direction.LEFT in cell2.openings

    def create_cell_opening(self, cell1: Cell, cell2: Cell) -> None:
        """Create an opening between two adjacent cells, on edges of both cells."""
        direction = self.get_direction_between(cell1, cell2)
        if direction is Direction.RIGHT:
            cell1.openings.reverse_opening(Direction.RIGHT)
            cell2.openings.reverse_opening(Direction.LEFT)
        elif direction is Direction.LEFT:
            cell1.openings.reverse_opening(Direction.LEFT)
            cell2.openings.reverse_opening(Direction.RIGHT)

        elif direction is Direction.DOWN:
            cell1.openings.reverse_opening(Direction.DOWN)
            cell2.openings.reverse_opening(Direction.UP)
        else:
            cell1.openings.reverse_opening(Direction.UP)
            cell2.openings.reverse_opening(Direction.DOWN)

    @staticmethod
    def get_direction_between(cell1: Cell, cell2: Cell) -> Direction:
        """Get the direction from `cell1` to `cell2`."""
        if cell1.y_pos == cell2.y_pos:
            if cell1.x_pos < cell2.x_pos:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        else:
            if cell1.y_pos < cell2.y_pos:
                return Direction.DOWN
            else:
                return Direction.UP

    @staticmethod
    def distance_between(cell1: Cell, cell2: Cell) -> int:
        """Get the manhattan distance between two cells."""
        return abs(cell1.x_pos - cell2.x_pos) + abs(cell1.y_pos - cell2.y_pos)


def grid_center_offset_coords(grid_dimensions: GridDimensions) -> tuple[int, int]:
    """Get coordinates of the top left corner of a centered grid with `grid_dimensions`."""
    x = boxed.terminal.width // 2 - grid_dimensions.char_width // 2
    y = boxed.terminal.height // 2 - grid_dimensions.char_height // 2
    return x, y
