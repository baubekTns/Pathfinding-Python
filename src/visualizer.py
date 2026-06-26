"""
Main visualizer controller.

This module handles:
- Pygame event loop
- Maze generation
- Algorithm execution
- Keyboard controls
- Passing algorithm state to the renderer
"""

from __future__ import annotations

import pygame

from src.algorithms.astar import AStar
from src.constants import (
    FPS,
    SEARCH_DELAY,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
from src.maze import generate_maze
from src.renderer import Renderer


class Visualizer:
    """
    Controls the pathfinding visualization.
    """

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        pygame.display.set_caption(
            "Pathfinding Algorithm Visualizer"
        )

        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)

        self.running = True
        self.paused = False

        self.maze = None
        self.start = None
        self.end = None
        self.algorithm = None

        self.last_step_time = 0

        self.reset()

    def reset(self):
        """
        Generate a new maze and reset the algorithm.
        """

        self.maze, self.start, self.end = generate_maze()

        self.algorithm = AStar(
            self.maze,
            self.start,
            self.end
        )

        self.paused = False
        self.last_step_time = pygame.time.get_ticks()

    def run(self):
        """
        Main application loop.
        """

        self.print_controls()

        while self.running:
            self.clock.tick(FPS)

            self.handle_events()
            self.update()
            self.render()

        pygame.quit()

    def handle_events(self):
        """
        Handle keyboard and window events.
        """

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key):
        """
        Handle key press events.
        """

        if key == pygame.K_ESCAPE:
            self.running = False

        elif key == pygame.K_r:
            self.reset()

        elif key == pygame.K_SPACE:
            self.paused = not self.paused

        elif key == pygame.K_RETURN:
            self.reset()

    def update(self):
        """
        Advance the selected algorithm by one step.
        """

        if self.paused:
            return

        if self.algorithm.is_finished:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.last_step_time >= SEARCH_DELAY:
            self.algorithm.step()
            self.last_step_time = current_time

            if self.algorithm.is_finished:
                self.print_stats()

    def render(self):
        """
        Draw the current frame.
        """

        self.renderer.draw(
            self.maze,
            self.algorithm
        )

    def print_controls(self):
        """
        Print controls to the terminal.
        """

        print("\n======================================")
        print("PATHFINDING ALGORITHM VISUALIZER")
        print("======================================")
        print("Controls")
        print("--------------------------------------")
        print("SPACE  - Pause / Resume")
        print("R      - Generate new maze")
        print("ENTER  - Restart with new maze")
        print("ESC    - Quit")
        print("======================================\n")

    def print_stats(self):
        """
        Print algorithm statistics to the terminal.
        """

        print("\n========== Search Complete ==========")
        print(f"Algorithm      : {self.algorithm.name}")
        print(f"Start          : {self.start}")
        print(f"End            : {self.end}")
        print(f"Nodes explored : {self.algorithm.nodes_explored}")
        print(f"Path length    : {self.algorithm.path_length}")
        print(f"Runtime        : {self.algorithm.runtime_ms:.2f} ms")

        if self.algorithm.has_path:
            print("Status         : PATH FOUND")
        else:
            print("Status         : NO PATH FOUND")

        print("=====================================\n")