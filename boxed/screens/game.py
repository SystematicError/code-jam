import collections.abc
import random
import typing

import more_itertools

import boxed
from boxed import grid
from boxed.border import draw_boundary

KEY_OFFSETS = {
    "KEY_DOWN": (0, 1),
    "KEY_UP": (0, -1),
    "KEY_LEFT": (-1, 0),
    "KEY_RIGHT": (1, 0),
}


class PathGenerator:
    """Generate and verify paths between points on `grid`."""

    def __init__(self, grid: grid.Grid):
        self.grid = grid
        self.visited_cells = set()

    def neighbours(self, cell: grid.Cell) -> collections.abc.Iterable[grid.Cell]:
        """Get all neighbours around `cell`."""
        for x_offset, y_offset in KEY_OFFSETS.values():
            neighbour_cell = self.grid.cell_at(
                cell.x_pos + x_offset, cell.y_pos + y_offset
            )
            if neighbour_cell is not None:
                yield neighbour_cell

    def generate_path(self, start: grid.Cell, end: grid.Cell) -> list[grid.Cell]:
        """
        Generate a random path between `start` and `end`.

        Both start and end are included in the resulting path
        """
        visited_cells = {start}
        path = [start]
        current_cell = start
        while current_cell != end:
            valid_neighbours = tuple(
                cell
                for cell in self.neighbours(current_cell)
                if cell not in visited_cells
            )

            if not valid_neighbours:
                for current_cell in reversed(path.copy()):
                    valid_neighbours = tuple(
                        cell
                        for cell in self.neighbours(current_cell)
                        if cell not in visited_cells
                    )
                    if valid_neighbours:
                        break
                    else:
                        path.pop()

            current_cell = random.choice(valid_neighbours)
            visited_cells.add(current_cell)
            path.append(current_cell)
        return path

    def verify_path(self, start: grid.Cell, end: grid.Cell) -> bool:
        """Valid path between start and end exists."""
        visited_cells = {start}
        path = [start]
        current_cell = start
        while current_cell != end:
            valid_neighbours = tuple(
                cell
                for cell in self.neighbours(current_cell)
                if cell not in visited_cells
                and self.grid.cells_connected(cell, current_cell)
            )
            if not valid_neighbours:
                for current_cell in reversed(path.copy()):
                    valid_neighbours = tuple(
                        cell
                        for cell in self.neighbours(current_cell)
                        if cell not in visited_cells
                        and self.grid.cells_connected(cell, current_cell)
                    )
                    if valid_neighbours:
                        break
                    else:
                        path.pop()
                else:
                    return False

            current_cell = min(
                valid_neighbours,
                key=lambda c: self.grid.distance_between(c, current_cell),
            )
            visited_cells.add(current_cell)
            path.append(current_cell)
        return True


class Game:
    """Hold control over a game on `grid`."""

    def __init__(self, grid: grid.Grid):
        self.grid = grid
        self._path_gen = PathGenerator(self.grid)
        self.path = None
        self.start = None
        self.end = None
        self.current_selection = None
        self._selection_colour = boxed.terminal.black_on_white
        self.path_completed = False

    def start_game(self) -> None:
        """Start the game by picking exit points, generating a valid path and randomizing other cells."""
        for cell in more_itertools.flatten(self.grid.cells):
            cell.openings.reset_openings()
        self.start = self.grid.cell_at(0, random.randrange(self.grid.dimensions.height))
        self.end = self.grid.cell_at(
            self.grid.dimensions.width - 1,
            random.randrange(self.grid.dimensions.height),
        )

        self.start.openings.reverse_opening(grid.Direction.LEFT)
        self.end.openings.reverse_opening(grid.Direction.RIGHT)
        self._generate_game()
        self.current_selection = self.grid.cell_at(0, 0)

    def move_selection(self, direction: grid.Direction) -> None:
        """Move the current selection in `direction`"""
        if (
            target := self.grid.cell_in_direction(self.current_selection, direction)
        ) is not None:
            self.current_selection.render()
            self.current_selection = target
            self.display_selection()

    def display_generated_path(self) -> None:
        """Display the stored valid path."""
        for cell in self.path[1:]:
            cell.render(boxed.terminal.black_on_white)
        self.path[0].render(boxed.terminal.red_on_white)
        self.path[-1].render(boxed.terminal.red_on_white)

    def display(self) -> None:
        """Display the whole grid and highlight exits and selection."""
        print(boxed.terminal.clear, end="")
        draw_boundary()
        print(
            boxed.terminal.move(boxed.terminal.height - 3, boxed.terminal.width - 26)
            + f"Press {boxed.terminal.white_bold}S{boxed.terminal.normal} to stop the game"
        )
        if self.grid.print_grid():
            self.path[0].render(boxed.terminal.red_on_black)
            self.path[-1].render(boxed.terminal.red_on_black)
            self.display_selection()

    def display_selection(
        self, colour: typing.Optional[typing.Callable] = None
    ) -> None:
        """Display the current selection with `colour` or black on white."""
        if self.current_selection is self.start or self.current_selection is self.end:
            self.current_selection.render(colour or boxed.terminal.bold_red)
        else:
            self.start.render(boxed.terminal.red_on_black)
            self.end.render(boxed.terminal.red_on_black)
            self.current_selection.render(colour or boxed.terminal.bold_white)

    def solved(self, *, cache: bool = True) -> bool:
        """Verify if there's a valid paths between the ends"""
        if self.path_completed:
            return True
        else:
            completed = self._path_gen.verify_path(self.start, self.end)
            if cache:
                self.path_completed = completed
            return completed

    def _generate_game(self) -> None:
        """
        Generate a game from the current start and end points.

        The pregenerated path is stored in `self.path`
        """
        cell_count = self.grid.dimensions.height * self.grid.dimensions.width
        straight_distance = abs(self.start.x_pos - self.end.x_pos) + abs(
            self.start.y_pos - self.end.y_pos
        )

        self.path = self._path_gen.generate_path(self.start, self.end)
        # regenerate the path if it fills up too much space or is too straight
        while (
            len(self.path) > cell_count * 0.75
            or len(self.path) < straight_distance * 1.2
        ):
            self.path = self._path_gen.generate_path(self.start, self.end)

        for cell1, cell2 in more_itertools.windowed(self.path, 2):
            self.grid.create_cell_opening(cell1, cell2)

        # randomize openings of non path cells
        while not self.solved(cache=False):
            for cell in set(more_itertools.flatten(self.grid.cells)).difference(self.path):
                if random.random() < 0.80:
                    for opening_dir in random.sample(
                        list(grid.Direction), random.randrange(2, 5)
                    ):
                        cell.openings.reverse_opening(opening_dir)
                        if (
                            neighbour := self.grid.cell_in_direction(cell, opening_dir)
                        ) is not None:
                            neighbour.openings.reverse_opening(opening_dir.opposite())

        # rotate ells randomly
        for cell in more_itertools.flatten(self.grid.cells):
            cell.openings.rotate(random.randrange(0, 4))


def load_screen() -> bool:
    """
    Display and start a game.

    return True if the user won the game, False if they exited
    """
    game = Game(grid.Grid(grid.GridDimensions(1, 4, 4)))
    terminal_size = 0, 0
    game.start_game()
    while True:
        with boxed.terminal.hidden_cursor():
            with boxed.terminal.cbreak():
                key = boxed.terminal.inkey(timeout=0.1)

                # Resize border if the terminal size gets changed
                if (boxed.terminal.width, boxed.terminal.height) != terminal_size:
                    print(boxed.terminal.clear, end="")
                    draw_boundary()
                    game.display()
                    terminal_size = boxed.terminal.width, boxed.terminal.height

                if key == "s":
                    return False

                elif key == "h":
                    game.display_generated_path()

                elif (
                    key.name
                    and (direction := key.name.removeprefix("KEY_"))
                    in grid.Direction.__members__
                ):
                    game.move_selection(grid.Direction[direction])

                elif key == " ":
                    game.current_selection.openings.rotate()
                    game.display_selection()
                    if game.solved():
                        return True
