import collections.abc
import random

import more_itertools

import boxed
from boxed.screens import grid

KEY_OFFSETS = {
    "KEY_DOWN": (0, 1),
    "KEY_UP": (0, -1),
    "KEY_LEFT": (-1, 0),
    "KEY_RIGHT": (1, 0),
}


class PathGenerator:
    """Used to create random paths from a start point to a end point"""

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

    def validate_connection(self, start: grid.Cell, end: grid.Cell) -> list[grid.Cell]:
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
            try:
                current_cell = min(
                    valid_neighbours,
                    key=lambda c: self.grid.distance_between(c, current_cell),
                )
            except ValueError:
                return False
            visited_cells.add(current_cell)
            path.append(current_cell)
        print(end in path)
        return True


class Game:
    """Game instance"""

    def __init__(self, grid: grid.Grid):
        self.grid = grid
        self.path_gen = PathGenerator(self.grid)
        self.path = None
        self.start = None
        self.end = None

    def generate_game(self) -> None:
        """Displays the current game"""
        for cell in more_itertools.flatten(self.grid.cells):
            cell.openings.reset_openings()
        self.start = start = self.grid.cell_at(
            0, random.randrange(self.grid.dimensions.height)
        )
        self.end = end = self.grid.cell_at(
            self.grid.dimensions.width - 1,
            random.randrange(self.grid.dimensions.height),
        )

        start.openings.reverse_opening(grid.Direction.LEFT)
        end.openings.reverse_opening(grid.Direction.RIGHT)

        path = self.path_gen.generate_path(start, end)
        cell_count = self.grid.dimensions.height * self.grid.dimensions.width
        straight_dist = abs(start.x_pos - end.x_pos) + abs(start.y_pos - end.y_pos)

        # regenerate the path if it fills up too much space or is too straight
        # modifiers need adjustment to scale with square root of total grid size
        while len(path) > cell_count * 0.75 or len(path) < straight_dist * 1.2:
            path = self.path_gen.generate_path(start, end)

        for c1, c2 in more_itertools.windowed(path, 2):
            self.grid.create_cell_opening(c1, c2)

        # randomize openings of non path openings
        for cell in set(more_itertools.flatten(self.grid.cells)).difference(path):
            for opening_dir in random.sample(
                list(grid.Direction), random.randrange(2, 5)
            ):
                cell.openings.reverse_opening(opening_dir)
                if (c := self.grid.cell_in_direction(cell, opening_dir)) is not None:
                    c.openings.reverse_opening(opening_dir.opposite())

        # rotate cells randomly
        # we need to make sure the end and stat cells point to edges instead of only ending at them
        for cell in more_itertools.flatten(self.grid.cells):

            cell.openings.rotate(random.randrange(1, 5))

        self.grid.print_grid()

        # for cell in path[1:]:
        #     cell.render(boxed.terminal.black_on_white)
        path[0].render(boxed.terminal.red_on_white)
        path[-1].render(boxed.terminal.red_on_white)


def load_screen() -> None:
    """Callback to load screen"""
    game = Game(grid.Grid(grid.GridDimensions(1, 4, 4)))
    terminal_size = 0, 0
    color = boxed.terminal.black_on_white
    c = True
    while True:

        with boxed.terminal.cbreak():
            key = boxed.terminal.inkey(timeout=0.1)

            # Resize border if the terminal size gets changed
            if (boxed.terminal.width, boxed.terminal.height) != terminal_size:
                print(boxed.terminal.clear, end="")
                game.grid.print_grid()
                game.generate_game()
                terminal_size = boxed.terminal.width, boxed.terminal.height
                cell = game.grid.cell_at(0, 0)
                cell.render(boxed.terminal.black_on_white)

            if key == "b":
                break
            if key == "c":
                print(game.path_gen.verify_path(game.start, game.end))

            elif key == "r":
                game.grid.print_grid()
                game.generate_game()
                cell = game.grid.cell_at(0, 0)
                cell.render(color)

            elif (
                key.name
                and (direction := key.name.removeprefix("KEY_"))
                in grid.Direction.__members__
            ):
                new_cell = game.grid.cell_in_direction(cell, grid.Direction[direction])
                if new_cell is not None:
                    cell.render()  # blackout old cell
                    new_cell.render(color)

                    game.start.render(boxed.terminal.red_on_white)
                    game.end.render(boxed.terminal.red_on_white)

                    cell = new_cell
            elif key == "m":
                while True:
                    key = boxed.terminal.inkey()
                    if key.name is not None:
                        if key.name.removeprefix("KEY_") in grid.Direction.__members__:
                            cell.openings.reverse_opening(
                                grid.Direction[key.name.removeprefix("KEY_")]
                            )
                            cell.render(color)
                        elif key.name == "KEY_ENTER":
                            break

            elif key == " ":
                cell.openings.rotate()
                cell.render(boxed.terminal.black_on_white)
            elif key == "l":
                # trigger current cell highlight
                if c:
                    color = boxed.terminal.white_on_black
                else:
                    color = boxed.terminal.black_on_white
                c = not c
