"""
DFS maze generator.

Inspired by the previous Processing maze generator:
- start with a full wall grid
- carve corridors using depth-first search
- add random loops
- reduce some dead ends
- optionally carve a central cross
- reinforce the border
"""

from __future__ import annotations

import random


WALL = 1
FLOOR = 0


def generate_dfs_maze(
    rows,
    cols,
    loop_attempts=25,
    dead_end_passes=2,
    widen_passes=1,
    central_cross=True,
):
    """
    Generate a maze using recursive backtracking / DFS carving.

    Returns:
        maze: 2D list where 0 = walkable, 1 = wall
    """

    maze = create_wall_grid(rows, cols)

    carve_depth_first_maze(maze)

    add_random_loops(maze, loop_attempts)

    for _ in range(dead_end_passes):
        reduce_dead_ends(maze)

    for _ in range(widen_passes):
        widen_selected_intersections(maze)

    if central_cross:
        carve_central_cross(maze)

    reinforce_border(maze)

    return maze


def create_wall_grid(rows, cols):
    """
    Create a grid filled completely with walls.
    """

    return [
        [WALL for _ in range(cols)]
        for _ in range(rows)
    ]


def carve_depth_first_maze(maze):
    """
    Carve a maze through odd-indexed logical cells.
    """

    rows = len(maze)
    cols = len(maze[0])

    logical_rows = max(1, (rows - 1) // 2)
    logical_cols = max(1, (cols - 1) // 2)

    visited = [
        [False for _ in range(logical_cols)]
        for _ in range(logical_rows)
    ]

    start_row = random.randint(0, logical_rows - 1)
    start_col = random.randint(0, logical_cols - 1)

    stack = [(start_row, start_col)]
    visited[start_row][start_col] = True
    carve_logical_cell(maze, start_row, start_col)

    while stack:
        current_row, current_col = stack[-1]

        neighbours = get_unvisited_logical_neighbours(
            current_row,
            current_col,
            visited,
            logical_rows,
            logical_cols,
        )

        if not neighbours:
            stack.pop()
            continue

        next_row, next_col = random.choice(neighbours)

        visited[next_row][next_col] = True

        carve_logical_passage(
            maze,
            current_row,
            current_col,
            next_row,
            next_col,
        )

        stack.append((next_row, next_col))


def get_unvisited_logical_neighbours(row, col, visited, logical_rows, logical_cols):
    """
    Return unvisited neighbours in the logical maze grid.
    """

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    neighbours = []

    for dr, dc in directions:
        nr = row + dr
        nc = col + dc

        if not (0 <= nr < logical_rows and 0 <= nc < logical_cols):
            continue

        if visited[nr][nc]:
            continue

        neighbours.append((nr, nc))

    random.shuffle(neighbours)

    return neighbours


def actual_row(logical_row):
    return 1 + logical_row * 2


def actual_col(logical_col):
    return 1 + logical_col * 2


def carve_logical_cell(maze, logical_row, logical_col):
    """
    Convert a logical maze cell into a walkable grid cell.
    """

    row = actual_row(logical_row)
    col = actual_col(logical_col)

    if in_bounds(maze, row, col):
        maze[row][col] = FLOOR


def carve_logical_passage(maze, row1, col1, row2, col2):
    """
    Carve two cells and the wall between them.
    """

    r1 = actual_row(row1)
    c1 = actual_col(col1)

    r2 = actual_row(row2)
    c2 = actual_col(col2)

    maze[r1][c1] = FLOOR
    maze[r2][c2] = FLOOR

    wall_row = (r1 + r2) // 2
    wall_col = (c1 + c2) // 2

    maze[wall_row][wall_col] = FLOOR


def add_random_loops(maze, attempts):
    """
    Open some walls between corridors to create loops.

    A pure DFS maze is a perfect maze, meaning there is only one route
    between any two cells. Loops make the maze more interesting for
    comparing pathfinding algorithms.
    """

    rows = len(maze)
    cols = len(maze[0])

    for _ in range(attempts):
        row = random.randint(1, rows - 2)
        col = random.randint(1, cols - 2)

        if maze[row][col] != WALL:
            continue

        horizontal_open = 0
        vertical_open = 0

        if maze[row][col - 1] == FLOOR:
            horizontal_open += 1

        if maze[row][col + 1] == FLOOR:
            horizontal_open += 1

        if maze[row - 1][col] == FLOOR:
            vertical_open += 1

        if maze[row + 1][col] == FLOOR:
            vertical_open += 1

        connects_horizontal_corridor = (
            horizontal_open == 2 and vertical_open == 0
        )

        connects_vertical_corridor = (
            vertical_open == 2 and horizontal_open == 0
        )

        if connects_horizontal_corridor or connects_vertical_corridor:
            maze[row][col] = FLOOR


def reduce_dead_ends(maze):
    """
    Open one wall near each dead end to reduce overly linear corridors.
    """

    rows = len(maze)
    cols = len(maze[0])

    cells_to_open = []

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):

            if maze[row][col] != FLOOR:
                continue

            if count_open_neighbours(maze, row, col) != 1:
                continue

            wall_neighbours = []

            for nr, nc in get_cardinal_neighbours(row, col):
                if maze[nr][nc] == WALL:
                    wall_neighbours.append((nr, nc))

            if wall_neighbours:
                cells_to_open.append(random.choice(wall_neighbours))

    for row, col in cells_to_open:
        maze[row][col] = FLOOR


def widen_selected_intersections(maze):
    """
    Randomly widen some intersections to make the maze less cramped.
    """

    rows = len(maze)
    cols = len(maze[0])

    for row in range(2, rows - 2):
        for col in range(2, cols - 2):

            if maze[row][col] != FLOOR:
                continue

            if count_open_neighbours(maze, row, col) < 3:
                continue

            if random.random() > 0.18:
                continue

            for nr, nc in get_cardinal_neighbours(row, col):
                if maze[nr][nc] == WALL:
                    maze[nr][nc] = FLOOR


def carve_central_cross(maze):
    """
    Carve a small central cross to improve map connectivity.
    """

    rows = len(maze)
    cols = len(maze[0])

    mid_row = rows // 2
    mid_col = cols // 2

    arm = min(rows, cols) // 5

    for col in range(max(1, mid_col - arm), min(cols - 1, mid_col + arm + 1)):
        maze[mid_row][col] = FLOOR

    for row in range(max(1, mid_row - arm), min(rows - 1, mid_row + arm + 1)):
        maze[row][mid_col] = FLOOR


def reinforce_border(maze):
    """
    Keep the outer border as walls.
    """

    rows = len(maze)
    cols = len(maze[0])

    for col in range(cols):
        maze[0][col] = WALL
        maze[rows - 1][col] = WALL

    for row in range(rows):
        maze[row][0] = WALL
        maze[row][cols - 1] = WALL


def get_cardinal_neighbours(row, col):
    """
    Return four-directional neighbours.
    """

    return [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]


def count_open_neighbours(maze, row, col):
    """
    Count open neighbours in four directions.
    """

    count = 0

    for nr, nc in get_cardinal_neighbours(row, col):
        if in_bounds(maze, nr, nc) and maze[nr][nc] == FLOOR:
            count += 1

    return count


def in_bounds(maze, row, col):
    """
    Check whether a cell is inside the maze.
    """

    return (
        0 <= row < len(maze)
        and
        0 <= col < len(maze[0])
    )