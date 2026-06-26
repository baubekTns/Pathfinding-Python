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
    MAZE_GENERATOR,
    DFS_LOOP_ATTEMPTS,
    DFS_DEAD_END_PASSES,
    DFS_WIDEN_PASSES,
    DFS_CENTRAL_CROSS,
)
from src.maze_generators.dfs_maze import generate_dfs_maze


def generate_maze(
    rows=ROWS,
    cols=COLS,
    density=OBSTACLE_DENSITY,
    generator_type=MAZE_GENERATOR,
):
    """
    Generate a maze and choose start/end positions.

    0 = walkable
    1 = wall
    """

    if generator_type == "dfs":
        maze = generate_dfs_maze(
            rows,
            cols,
            loop_attempts=DFS_LOOP_ATTEMPTS,
            dead_end_passes=DFS_DEAD_END_PASSES,
            widen_passes=DFS_WIDEN_PASSES,
            central_cross=DFS_CENTRAL_CROSS,
        )
    else:
        maze = generate_random_obstacle_grid(
            rows,
            cols,
            density,
        )

    start, end = choose_start_and_end(maze)

    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0

    return maze, start, end


def generate_random_obstacle_grid(rows, cols, density):
    """
    Generate the original random obstacle grid.

    This is kept as a fallback generator.
    """

    return [
        [
            1 if random.random() < density else 0
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]


def choose_start_and_end(maze):
    """
    Pick two walkable cells that are reasonably far apart.
    """

    walkable_cells = get_walkable_cells(maze)

    if len(walkable_cells) < 2:
        raise ValueError("Maze does not contain enough walkable cells.")

    start = random.choice(walkable_cells)

    end = max(
        walkable_cells,
        key=lambda cell: manhattan_distance(start, cell),
    )

    return start, end


def get_walkable_cells(maze):
    """
    Return all walkable cells in the maze.
    """

    cells = []

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 0:
                cells.append((row, col))

    return cells


def manhattan_distance(a, b):
    """
    Manhattan distance between two cells.
    """

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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
    Return True if the position is not a wall.
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