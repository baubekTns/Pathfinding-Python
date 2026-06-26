from constants import *
import random

# MAZE GENERATION

def generate_maze(rows, cols, density=0.30):

    maze = []

    for r in range(rows):

        row = []

        for c in range(cols):

            if random.random() < density:
                row.append(1)
            else:
                row.append(0)

        maze.append(row)

    while True:

        start = (
            random.randint(0, rows - 1),
            random.randint(0, cols - 1)
        )

        if maze[start[0]][start[1]] == 0:
            break

    while True:

        end = (
            random.randint(0, rows - 1),
            random.randint(0, cols - 1)
        )

        if maze[end[0]][end[1]] == 0 and end != start:
            break

    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0

    return maze, start, end


# NEIGHBOURS

def get_neighbors(position):

    if ALLOW_DIAGONALS:

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),

            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

    else:

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

    return directions
