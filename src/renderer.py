"""
Pygame renderer for the pathfinding visualizer.
"""

from __future__ import annotations

import pygame

from src.constants import (
    ROWS,
    COLS,
    CELL_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    HUD_WIDTH,
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
    TEXT,
    HUD_BACKGROUND,
    HUD_BORDER,
    SHOW_HUD,
)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 16)
        self.small_font = pygame.font.SysFont("Arial", 14)

    def draw(self, maze, algorithm):
        """
        Draw the current visualization state.
        """

        self.screen.fill(WHITE)

        self.draw_maze(maze)
        self.draw_algorithm_state(algorithm)
        self.draw_grid()

        if SHOW_HUD:
            self.draw_hud(algorithm)

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
                    CELL_SIZE,
                )

                color = WHITE

                if maze[row][col] == 1:
                    color = BLACK

                pygame.draw.rect(self.screen, color, rect)

    def draw_algorithm_state(self, algorithm):
        """
        Draw open set, closed set, path, current node, start, end.
        """

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
        Draw grid lines only over the maze area.
        """

        for row in range(ROWS + 1):
            pygame.draw.line(
                self.screen,
                GRID,
                (0, row * CELL_SIZE),
                (GRID_WIDTH, row * CELL_SIZE),
            )

        for col in range(COLS + 1):
            pygame.draw.line(
                self.screen,
                GRID,
                (col * CELL_SIZE, 0),
                (col * CELL_SIZE, GRID_HEIGHT),
            )

    def draw_hud(self, algorithm):
        """
        Draw on-screen information in a side panel.
        """

        panel_rect = pygame.Rect(
            GRID_WIDTH,
            0,
            HUD_WIDTH,
            WINDOW_HEIGHT,
        )

        pygame.draw.rect(
            self.screen,
            HUD_BACKGROUND,
            panel_rect,
        )

        pygame.draw.line(
            self.screen,
            HUD_BORDER,
            (GRID_WIDTH, 0),
            (GRID_WIDTH, WINDOW_HEIGHT),
            width=2,
        )

        padding = 18
        x = GRID_WIDTH + padding
        y = padding

        status = self.get_status_text(algorithm)

        lines = [
            "Pathfinding Visualizer",
            "",
            f"Algorithm: {algorithm.name}",
            f"Status: {status}",
            "",
            f"Visited: {algorithm.nodes_explored}",
            f"Open: {len(algorithm.open_set)}",
            f"Closed: {len(algorithm.closed_set)}",
            f"Path length: {algorithm.path_length}",
            f"Runtime: {algorithm.runtime_ms:.1f} ms",
        ]

        if hasattr(algorithm, "path_cost"):
            lines.append(f"Path cost: {algorithm.path_cost:.3f}")

        lines.extend([
            "",
            "Controls",
            "1 - A*",
            "2 - BFS",
            "3 - Dijkstra",
            "4 - Greedy",
            "5 - DFS",
            "",
            "R - New maze",
            "Enter - Restart maze",
            "Space - Pause/resume",
            "Esc - Quit",
        ])

        for index, line in enumerate(lines):
            if line == "":
                y += 12
                continue

            font = self.font if index == 0 else self.small_font

            text_surface = font.render(
                line,
                True,
                TEXT,
            )

            self.screen.blit(
                text_surface,
                (x, y),
            )

            y += 22

    def get_status_text(self, algorithm):
        """
        Convert algorithm state into a readable status label.
        """

        if not algorithm.is_finished:
            return "Running"

        if algorithm.has_path:
            return "Path found"

        return "No path found"