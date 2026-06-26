"""
Pygame renderer for the pathfinding visualizer.
"""

from __future__ import annotations

import pygame

from src.constants import (
    ROWS,
    COLS,
    CELL_SIZE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WHITE,
    BLACK,
    GRID,
    START,
    END,
    OPEN,
    CLOSED,
    PATH,
    CURRENT,
)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 18)

    def draw(self, maze, algorithm):
        """
        Draw the current visualization state.
        """

        self.screen.fill(WHITE)

        self.draw_maze(maze)
        self.draw_algorithm_state(algorithm)
        self.draw_grid()

        pygame.display.flip()

    def draw_maze(self, maze):
        """
        Draw obstacles and empty cells.
        """

        for row in range(ROWS):
            for col in range(COLS):

                rect = pygame.Rect(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                color = WHITE

                if maze[row][col] == 1:
                    color = BLACK

                pygame.draw.rect(self.screen, color, rect)

    def draw_algorithm_state(self, algorithm):
        """
        Draw open set, closed set, path, current node, start, end.
        """

        # Closed set
        for row, col in algorithm.closed_set:
            pygame.draw.rect(
                self.screen,
                CLOSED,
                (
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )

        # Open set
        for row, col in algorithm.open_set:
            pygame.draw.rect(
                self.screen,
                OPEN,
                (
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )

        # Path
        for row, col in algorithm.path:
            pygame.draw.rect(
                self.screen,
                PATH,
                (
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )

        # Current node
        if algorithm.current:
            row, col = algorithm.current

            pygame.draw.rect(
                self.screen,
                CURRENT,
                (
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )

        # Start
        row, col = algorithm.start
        pygame.draw.rect(
            self.screen,
            START,
            (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            ),
        )

        # End
        row, col = algorithm.end
        pygame.draw.rect(
            self.screen,
            END,
            (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            ),
        )

    def draw_grid(self):
        """
        Draw grid lines.
        """

        for row in range(ROWS + 1):
            pygame.draw.line(
                self.screen,
                GRID,
                (0, row * CELL_SIZE),
                (WINDOW_WIDTH, row * CELL_SIZE),
            )

        for col in range(COLS + 1):
            pygame.draw.line(
                self.screen,
                GRID,
                (col * CELL_SIZE, 0),
                (col * CELL_SIZE, WINDOW_HEIGHT),
            )