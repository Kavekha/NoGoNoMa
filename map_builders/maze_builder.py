from random import randint

from map_builders.builder_map import InitialMapBuilder
from gmap.gmap_enums import TileType


class MazeBuilder(InitialMapBuilder):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def __init__(self):
        super().__init__()
        self.noise_areas = list()

    def build_initial_map(self, build_data):
        print(f'---- Maze builder in action! -----')

        maze = Grid((build_data.map.width // 2) - 2, (build_data.map.height // 2) - 2)
        maze.generate_maze(build_data.map, build_data)


class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.walls = {MazeBuilder.TOP: True,
                      MazeBuilder.RIGHT: True,
                      MazeBuilder.BOTTOM: True,
                      MazeBuilder.LEFT: True}
        self.visited = False

    def remove_walls(self, next_cell):
        x = self.column - next_cell.column
        y = self.row - next_cell.row

        if x == 1:
            self.walls[MazeBuilder.LEFT] = False
            next_cell.walls[MazeBuilder.RIGHT] = False
        elif x == -1:
            self.walls[MazeBuilder.RIGHT] = False
            next_cell.walls[MazeBuilder.LEFT] = False
        elif y == 1:
            self.walls[MazeBuilder.TOP] = False
            next_cell.walls[MazeBuilder.BOTTOM] = False
        elif y == -1:
            self.walls[MazeBuilder.BOTTOM] = False
            next_cell.walls[MazeBuilder.TOP] = False


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = list()
        self.backtrace = list()
        self.current = 0

        for row in range(0, self.height):
            for column in range(0, self.width):
                self.cells.append(Cell(row, column))

    def calculate_index(self, row, column):
        if row < 0 or column < 0 or column > self.width - 1 or row > self.height - 1:
            return False
        else:
            return column + (row * self.width)

    def get_available_neighbors(self):
        neighbors = list()
        current_row = self.cells[self.current].row
        current_column = self.cells[self.current].column

        neighbor_indices = [
            self.calculate_index(current_row - 1, current_column),
            self.calculate_index(current_row, current_column + 1),
            self.calculate_index(current_row + 1, current_column),
            self.calculate_index(current_row, current_column - 1)
        ]

        for neighbor in neighbor_indices:
            if neighbor and not self.cells[neighbor].visited:
                neighbors.append(neighbor)
        return neighbors

    def find_next_cell(self):
        neighbors = self.get_available_neighbors()
        if neighbors:
            if len(neighbors) == 1:
                return neighbors[0]
            else:
                rand = randint(0, len(neighbors) - 1)
                return neighbors[rand]
        return None

    def generate_maze(self, gmap, build_data):
        iteration = 0
        while True:
            self.cells[self.current].visited = True
            next_cell_idx = self.find_next_cell()

            if next_cell_idx:
                self.cells[next_cell_idx].visited = True
                self.backtrace.append(self.current)
                next_cell = self.cells[next_cell_idx]
                current_cell = self.cells[self.current]
                current_cell.remove_walls(next_cell)
                self.current = next_cell_idx
            else:
                if self.backtrace:
                    self.current = self.backtrace[len(self.backtrace) - 1]
                    self.backtrace.remove(self.current)
                else:
                    break

            if iteration % 50 == 0:
                self.copy_to_map(gmap)
                build_data.take_snapshot()
            iteration += 1

    def copy_to_map(self, gmap):
        for i, tile in enumerate(gmap.tiles):
            gmap.tiles[i] = TileType.WALL

        for cell in self.cells:
            x = cell.column + 1
            y = cell.row + 1
            idx = gmap.xy_idx(x * 2, y * 2)

            gmap.tiles[idx] = TileType.FLOOR

            if not cell.walls.get(MazeBuilder.TOP):
                gmap.tiles[idx - gmap.width] = TileType.FLOOR
            if not cell.walls.get(MazeBuilder.RIGHT):
                gmap.tiles[idx + 1] = TileType.FLOOR
            if not cell.walls.get(MazeBuilder.BOTTOM):
                gmap.tiles[idx + gmap.width] = TileType.FLOOR
            if not cell.walls.get(MazeBuilder.LEFT):
                gmap.tiles[idx - 1] = TileType.FLOOR
