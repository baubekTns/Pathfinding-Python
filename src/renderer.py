from constants import *
import pygame

# ==============================
# DRAWING
# ==============================

def draw(
    screen,
    maze,
    start,
    end,
    open_set,
    closed_set,
    path,
    stats=None
):

    screen.fill(WHITE)

    # Maze
    for r in range(ROWS):

        for c in range(COLS):

            rect = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            color = WHITE

            if maze[r][c] == 1:
                color = BLACK

            pygame.draw.rect(screen, color, rect)

    # Closed set
    for position in closed_set:

        r, c = position

        pygame.draw.rect(
            screen,
            CLOSED,
            (
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # Open set
    for position in open_set:

        r, c = position

        pygame.draw.rect(
            screen,
            OPEN,
            (
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # Final path
    for r, c in path:

        pygame.draw.rect(
            screen,
            PATH,
            (
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # Start
    pygame.draw.rect(
        screen,
        START,
        (
            start[1] * CELL_SIZE,
            start[0] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

    # End
    pygame.draw.rect(
        screen,
        END,
        (
            end[1] * CELL_SIZE,
            end[0] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

    # Grid
    for r in range(ROWS + 1):

        pygame.draw.line(
            screen,
            GRID,
            (0, r * CELL_SIZE),
            (WINDOW_WIDTH, r * CELL_SIZE)
        )

    for c in range(COLS + 1):

        pygame.draw.line(
            screen,
            GRID,
            (c * CELL_SIZE, 0),
            (c * CELL_SIZE, WINDOW_HEIGHT)
        )

    pygame.display.flip()