"""
A* pathfinding algorithm implementation.

This class follows the common SearchAlgorithm interface so it can be
used interchangeably with other algorithms such as BFS, DFS, Dijkstra,
and Greedy Best-First Search.
"""

from __future__ import annotations

import heapq
import math
import time

from src.algorithms.base import SearchAlgorithm
from src.constants import ASTAR
from src.maze import get_neighbors, movement_cost
from src.node import Node


class AStar(SearchAlgorithm):
    """
    A* pathfinding algorithm.

    A* uses the formula:

        f(n) = g(n) + h(n)

    where:
    - g(n) is the cost from the start node to the current node
    - h(n) is the estimated cost from the current node to the end node
    - f(n) is the total estimated cost
    """

    name = ASTAR

    def __init__(self, maze, start, end):
        super().__init__(maze, start, end)

        self.nodes = {}
        self.open_heap = []

        self.start_time = None
        self.end_time = None

        self.reset()

    def reset(self):
        """
        Reset A* to its initial state.
        """

        self.nodes = {}

        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                position = (row, col)
                self.nodes[position] = Node(position=position)

        self.open_heap = []

        self.open_set = set()
        self.closed_set = set()
        self.path = []

        self.current = None

        self.finished = False
        self.path_found = False

        self.nodes_explored = 0

        self.start_time = time.perf_counter()
        self.end_time = None

        start_node = self.nodes[self.start]
        start_node.g = 0
        start_node.h = self.heuristic(self.start, self.end)
        start_node.f = start_node.g + start_node.h

        heapq.heappush(self.open_heap, start_node)
        self.open_set.add(self.start)

    def step(self):
        """
        Perform one A* search step.

        This method is called once per frame by the visualizer.
        """

        if self.finished:
            return

        if not self.open_heap:
            self.finished = True
            self.path_found = False
            self.end_time = time.perf_counter()
            return

        current_node = heapq.heappop(self.open_heap)
        current_position = current_node.position

        if current_position in self.closed_set:
            return

        self.current = current_position
        self.open_set.discard(current_position)
        self.closed_set.add(current_position)
        self.nodes_explored += 1

        if current_position == self.end:
            self.finished = True
            self.path_found = True
            self.end_time = time.perf_counter()
            self.reconstruct_path()
            return

        for neighbour_position in get_neighbors(current_position, self.maze):

            if neighbour_position in self.closed_set:
                continue

            neighbour_node = self.nodes[neighbour_position]

            tentative_g = (
                current_node.g
                + movement_cost(current_position, neighbour_position)
            )

            if tentative_g < neighbour_node.g:
                neighbour_node.parent = current_position
                neighbour_node.g = tentative_g
                neighbour_node.h = self.heuristic(
                    neighbour_position,
                    self.end
                )
                neighbour_node.f = neighbour_node.g + neighbour_node.h

                heapq.heappush(self.open_heap, neighbour_node)
                self.open_set.add(neighbour_position)

    def reconstruct_path(self):
        """
        Reconstruct the final path from end to start.
        """

        path = []
        current = self.end

        while current is not None:
            path.append(current)
            current = self.nodes[current].parent

        path.reverse()
        self.path = path

    def heuristic(self, current, goal):
        """
        Euclidean distance heuristic.
        """

        return math.sqrt(
            (current[0] - goal[0]) ** 2
            + (current[1] - goal[1]) ** 2
        )

    @property
    def runtime_ms(self):
        """
        Return runtime in milliseconds.
        """

        if self.start_time is None:
            return 0.0

        if self.end_time is not None:
            return (self.end_time - self.start_time) * 1000

        return (time.perf_counter() - self.start_time) * 1000

    @property
    def path_length(self):
        """
        Return the number of cells in the final path.
        """

        return len(self.path)