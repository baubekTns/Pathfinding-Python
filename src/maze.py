"""
Maze generation and utility functions.
"""

from __future__ import annotations

import random

from src.constants import (
    ROWS,
    COLS,
    ALLOW_DIAGONALS,
    OBSTACLE_DENSITY,
)


def generate_maze(
    rows: int = ROWS,
    cols: int = COLS,
    density: float = OBSTACLE_DENSITY,
):
    """
    Generate a random maze.

    0 = walkable
    1 = obstacle
    """

    maze = [
        [
            1 if random.random() < density else 0
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]

    start = random_empty_cell(maze)
    end = random_empty_cell(maze)

    while end == start:
        end = random_empty_cell(maze)

    return maze, start, end


def random_empty_cell(maze):
    """
    Return a random walkable position.
    """

    rows = len(maze)
    cols = len(maze[0])

    while True:

        position = (
            random.randint(0, rows - 1),
            random.randint(0, cols - 1),
        )

        if maze[position[0]][position[1]] == 0:
            return position


def in_bounds(position, maze):
    """
    Check whether a position lies inside the maze.
    """

    row, col = position

    return (
        0 <= row < len(maze)
        and
        0 <= col < len(maze[0])
    )


def is_walkable(position, maze):
    """
    Return True if the position is not an obstacle.
    """

    row, col = position

    return maze[row][col] == 0


def get_neighbors(position, maze):
    """
    Return all valid neighbouring cells.
    """

    row, col = position

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    if ALLOW_DIAGONALS:

        directions.extend([
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ])

    neighbours = []

    for dr, dc in directions:

        neighbour = (
            row + dr,
            col + dc,
        )

        if not in_bounds(neighbour, maze):
            continue

        if not is_walkable(neighbour, maze):
            continue

        neighbours.append(neighbour)

    return neighbours


def movement_cost(current, neighbour):
    """
    Cost of moving from one cell to another.
    """

    row_diff = abs(current[0] - neighbour[0])
    col_diff = abs(current[1] - neighbour[1])

    if row_diff == 1 and col_diff == 1:
        return 1.41421356237

    return 1.0