from random import choice
from typing import List, Tuple

# ruff: noqa: E501

MAZE_COLS, MAZE_ROWS = 7, 7


def get_map_cell(cols: int, rows: int) -> List[bool]:
    """
    Generates a maze map represented as a list of boolean values.

    Parameters:
    - cols (int): The number of columns in the maze.
    - rows (int): The number of rows in the maze.

    Returns:
    - List[bool]: The maze map represented as a list of boolean values.

    Notes:
    - The maze is generated using a modified version of the Recursive Backtracking algorithm.
    - The map is represented as a list of boolean values, where True represents a wall and False represents a path.
    """

    class Cell:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y
            self.walls = {"top": True, "right": True, "bottom": True, "left": True}
            self.visited = False

        def check_cell(self, x: int, y: int) -> bool:
            """
            Checks if the neighboring cell at the specified coordinates is valid.

            Parameters:
            - x (int): The x-coordinate of the neighboring cell.
            - y (int): The y-coordinate of the neighboring cell.

            Returns:
            - bool: True if the neighboring cell is valid, False otherwise.
            """
            if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
                return False
            return grid_cell[x + y * cols]

        def check_neighbours(self):
            """
            Checks the valid neighboring cells of the current cell.

            Returns:
            - Cell or False: A randomly chosen neighboring cell if there are any, False otherwise.
            """
            neighbours = []

            top = self.check_cell(self.x, self.y - 1)
            right = self.check_cell(self.x + 1, self.y)
            bottom = self.check_cell(self.x, self.y + 1)
            left = self.check_cell(self.x - 1, self.y)

            if top and not top.visited:
                neighbours.append(top)
            if right and not right.visited:
                neighbours.append(right)
            if bottom and not bottom.visited:
                neighbours.append(bottom)
            if left and not left.visited:
                neighbours.append(left)

            return choice(neighbours) if neighbours else False

    def remove_walls(current_cell: Cell, next_cell: Cell):
        """
        Removes the walls between the current cell and the next cell.

        Parameters:
        - current_cell (Cell): The current cell.
        - next_cell (Cell): The next cell.
        """
        dx = current_cell.x - next_cell.x
        dy = current_cell.y - next_cell.y

        if dx == 1:
            current_cell.walls["left"] = False
            next_cell.walls["right"] = False
        if dx == -1:
            current_cell.walls["right"] = False
            next_cell.walls["left"] = False
        if dy == 1:
            current_cell.walls["top"] = False
            next_cell.walls["bottom"] = False
        if dy == -1:
            current_cell.walls["bottom"] = False
            next_cell.walls["top"] = False

    def check_wall(grid_cell: List[Cell], x: int, y: int) -> bool:
        """
        Checks if the wall at the specified coordinates exists.

        Parameters:
        - grid_cell (List[Cell]): The list of grid cells.
        - x (int): The x-coordinate of the wall.
        - y (int): The y-coordinate of the wall.

        Returns:
        - bool: True if the wall exists, False otherwise.
        """
        if x % 2 == 0 and y % 2 == 0:
            return False
        if x % 2 == 1 and y % 2 == 1:
            return True

        if x % 2 == 0:
            grid_x = x // 2
            grid_y = (y - 1) // 2
            return grid_cell[grid_x + grid_y * cols].walls["bottom"]
        else:
            grid_x = (x - 1) // 2
            grid_y = y // 2
            return grid_cell[grid_x + grid_y * cols].walls["right"]

    grid_cell = [Cell(x, y) for y in range(rows) for x in range(cols)]
    current_cell = grid_cell[0]
    current_cell.visited = True
    stack = []

    while True:
        next_cell = current_cell.check_neighbours()
        if next_cell:
            next_cell.visited = True
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
            stack.append(current_cell)
        elif stack:
            current_cell = stack.pop()
        else:
            break

    return [
        check_wall(grid_cell, x, y)
        for y in range(rows * 2 - 1)
        for x in range(cols * 2 - 1)
    ]


def get_map_str(map_cell: List[bool], player: Tuple[int, int]) -> str:
    """
    Generates a string representation of the maze grid.

    Parameters:
        map_cell (List[bool]): The maze grid represented as a list of boolean values.
        player (Tuple[int, int]): The current player's position as a tuple of x and y coordinates.

    Returns:
        str: A string representation of the maze grid with player's position marked as '🔴', walls as '⬛', and open paths as '⬜'.
    """
    map_str = ""
    for y in range(MAZE_ROWS * 2 - 1):
        for x in range(MAZE_COLS * 2 - 1):
            if map_cell[x + y * (MAZE_COLS * 2 - 1)]:
                map_str += "⬛"
            elif (x, y) == player:
                map_str += "🔴"
            else:
                map_str += "⬜"
        map_str += "\n"

    return map_str
