from __future__ import annotations

import collections.abc
import random
import typing
from threading import Thread

import more_itertools
from playsound import playsound

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

    def __init__(self, grid: grid.Grid, rec_child_count: int):
        self.grid = grid
        self._path_gen = PathGenerator(self.grid)
        self.path = None
        self.start = None
        self.end = None
        self.recursive_cells = None
        self.current_selection = None
        self._selection_colour = boxed.terminal.black_on_white
        self.recursive_child_count = rec_child_count
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
        self.start.openings.rotatable = False
        self.end.openings.rotatable = False
        self.start.openings.reverse_opening(grid.Direction.LEFT)
        self.end.openings.reverse_opening(grid.Direction.RIGHT)
        self._generate_game()
        self.current_selection = self.grid.cell_at(0, 0)
        self.recursive_cells = random.sample(
            self.path[1:-1], min(self.recursive_cells, 2)
        )
        self.recursive_cells.extend(
            random.sample(
                list(set(more_itertools.flatten(self.grid.cells)).difference(self.path)),
                min(self.recursive_child_count - 2, 0)
            )
        )

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

    def display(self, depth: int) -> None:
        """Display the whole grid and highlight exits and selection."""
        print(boxed.terminal.clear, end="")
        draw_boundary()
        print(
            boxed.terminal.move(boxed.terminal.height - 4, boxed.terminal.width - 26)
            + f"Current depth: {depth}"
            + boxed.terminal.move(boxed.terminal.height - 3, boxed.terminal.width - 26)
            + f"Press {boxed.terminal.white_bold}S{boxed.terminal.normal} to stop the game"
        )
        if self.grid.print_grid():
            self.path[0].render(boxed.terminal.red_on_black)
            self.path[-1].render(boxed.terminal.red_on_black)
            for cell in self.recursive_cells:
                cell.render(boxed.terminal.yellow_on_black)
            self.display_selection()

    def display_selection(
        self, colour: typing.Optional[typing.Callable] = None
    ) -> None:
        """Display the current selection with `colour` or black on white."""
        for cell in self.recursive_cells:
            cell.render(boxed.terminal.yellow)
        if self.current_selection is self.start or self.current_selection is self.end:
            self.current_selection.render(colour or boxed.terminal.bold_red)
        elif self.current_selection in self.recursive_cells:
            self.current_selection.render(boxed.terminal.bright_yellow)
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
        while self.solved(cache=False):
            for cell in set(more_itertools.flatten(self.grid.cells)).difference(
                self.path
            ):
                if random.random() < 0.80:
                    for opening_dir in random.sample(
                        list(grid.Direction), random.randrange(2, 5)
                    ):
                        cell.openings.reverse_opening(opening_dir)
                        if (
                            (
                                neighbour := self.grid.cell_in_direction(
                                    cell, opening_dir
                                )
                            )
                            is not None
                            and neighbour is not self.start
                            and neighbour is not self.end
                        ):
                            neighbour.openings.reverse_opening(opening_dir.opposite())

            # rotate ells randomly
            for cell in more_itertools.flatten(self.grid.cells):
                cell.openings.rotate(random.randrange(0, 4))


class GameTracker:
    """Keep track of a game and the parent trackers which generated this tracker."""

    def __init__(self, game: Game, parent: typing.Optional[GameTracker], cell_size: int):
        self.parent = parent
        self.game = game
        self._children = {}
        self._cell_size = cell_size

    def child_tracker(self, cell: grid.Cell) -> GameTracker:
        """Create a tracker instance based on `cell`."""
        if cell not in self._children:
            game = Game(
                grid.Grid(grid.GridDimensions(self._cell_size, 4, 4)),
                int(self.game.recursive_child_count // 2.5),
            )
            game.start_game()
            self._children[cell] = game
        return GameTracker(self._children[cell], self, self._cell_size)

    def get_depth(self) -> int:
        """Get the depth of this tracker's game."""
        count = 0
        parent = self.parent
        while parent is not None:
            parent = parent.parent
            count += 1
        return count


def load_screen(cell_size: int, game_width: int, game_height: int, recursive_elements: int) -> bool:
    """
    Display and start a game.

    return True if the user won the game, False if they exited
    """
    game_tracker = GameTracker(
        Game(
            grid.Grid(
                grid.GridDimensions(cell_size, game_width, game_height)
            ),
            recursive_elements
        ),
        None,
        cell_size
    )

    terminal_size = 0, 0
    game_tracker.game.start_game()
    while True:
        with boxed.terminal.hidden_cursor():
            with boxed.terminal.cbreak():
                key = boxed.terminal.inkey(timeout=0.1)

                # Resize border if the terminal size gets changed
                if (boxed.terminal.width, boxed.terminal.height) != terminal_size:

                    game_tracker.game.display(game_tracker.get_depth())
                    terminal_size = boxed.terminal.width, boxed.terminal.height

                if key == "s":
                    if game_tracker.parent is None:
                        return False
                    else:
                        game_tracker = game_tracker.parent
                        game_tracker.game.display(game_tracker.get_depth())
                    Thread(target=lambda: playsound("music/up-down.wav"), daemon=True).start()

                elif key == "h":
                    game_tracker.game.display_generated_path()
                    Thread(target=lambda: playsound("music/up-down.wav"), daemon=True).start()

                elif (
                    key.name
                    and (direction := key.name.removeprefix("KEY_"))
                    in grid.Direction.__members__
                ):
                    game_tracker.game.move_selection(grid.Direction[direction])

                elif key == " ":
                    Thread(target=lambda: playsound("music/up-down.wav"), daemon=True).start()
                    if (
                        game_tracker.game.current_selection
                        in game_tracker.game.recursive_cells
                    ):
                        child_tracker = game_tracker.child_tracker(
                            game_tracker.game.current_selection
                        )
                        if not child_tracker.game.solved():
                            game_tracker = child_tracker
                            game_tracker.game.display(game_tracker.get_depth())
                        else:
                            game_tracker.game.current_selection.openings.rotate()
                            game_tracker.game.display_selection()
                    else:
                        game_tracker.game.current_selection.openings.rotate()
                        if game_tracker.game.solved():
                            if game_tracker.parent is None:
                                return True
                            else:
                                game_tracker = game_tracker.parent
                                game_tracker.game.display(game_tracker.get_depth())
                        game_tracker.game.display_selection()
