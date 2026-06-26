"""
Main visualizer controller.

This module handles:
- Pygame event loop
- Maze generation
- Algorithm selection
- Algorithm execution
- Keyboard controls
- Passing algorithm state to the renderer
"""

from __future__ import annotations

import pygame

from src.algorithms.astar import AStar
from src.algorithms.bfs import BreadthFirstSearch
from src.algorithms.dijkstra import Dijkstra
from src.algorithms.greedy import GreedyBestFirstSearch
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

        self.algorithms = {
            pygame.K_1: AStar,
            pygame.K_2: BreadthFirstSearch,
            pygame.K_3: Dijkstra,
            pygame.K_4: GreedyBestFirstSearch,
        }

        self.selected_algorithm = AStar

        self.reset()

    def reset(self):
        """
        Generate a new maze and reset the selected algorithm.
        """

        self.maze, self.start, self.end = generate_maze()
        self.create_algorithm()

        self.paused = False
        self.last_step_time = pygame.time.get_ticks()

    def restart_same_maze(self):
        """
        Restart the selected algorithm on the current maze.
        """

        self.create_algorithm()
        self.paused = False
        self.last_step_time = pygame.time.get_ticks()

    def create_algorithm(self):
        """
        Create a fresh instance of the selected algorithm.
        """

        self.algorithm = self.selected_algorithm(
            self.maze,
            self.start,
            self.end
        )

    def select_algorithm(self, algorithm_class):
        """
        Change the active algorithm and restart on the same maze.
        """

        self.selected_algorithm = algorithm_class
        self.restart_same_maze()

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
            self.restart_same_maze()

        elif key in self.algorithms:
            self.select_algorithm(self.algorithms[key])

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
        print("1      - Select A*")
        print("2      - Select Breadth-First Search")
        print("3      - Select Dijkstra")
        print("4      - Select Greedy Best-First Search")
        print("SPACE  - Pause / Resume")
        print("R      - Generate new maze")
        print("ENTER  - Restart current maze")
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

        if hasattr(self.algorithm, "path_cost"):
            print(f"Path cost      : {self.algorithm.path_cost:.3f}")

        print(f"Runtime        : {self.algorithm.runtime_ms:.2f} ms")

        if self.algorithm.has_path:
            print("Status         : PATH FOUND")
        else:
            print("Status         : NO PATH FOUND")

        print("=====================================\n")