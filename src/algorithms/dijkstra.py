"""
Dijkstra's pathfinding algorithm implementation.

Dijkstra explores the lowest-cost path first. Unlike A*, it does not use
a heuristic, so it behaves like A* with h(n) = 0.
"""

from __future__ import annotations

import heapq
import time

from src.algorithms.base import SearchAlgorithm
from src.constants import DIJKSTRA
from src.maze import get_neighbors, movement_cost


class Dijkstra(SearchAlgorithm):
    """
    Dijkstra's shortest path algorithm.

    Dijkstra guarantees the lowest-cost path when all movement costs are
    non-negative.
    """

    name = DIJKSTRA

    def __init__(self, maze, start, end):
        super().__init__(maze, start, end)

        self.distances = {}
        self.parents = {}
        self.open_heap = []
        self.counter = 0

        self.start_time = None
        self.end_time = None

        self.reset()

    def reset(self):
        """
        Reset Dijkstra to its initial state.
        """

        self.distances = {}
        self.parents = {}

        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                self.distances[(row, col)] = float("inf")
                self.parents[(row, col)] = None

        self.distances[self.start] = 0

        self.open_heap = []
        self.counter = 0

        heapq.heappush(
            self.open_heap,
            (0, self.counter, self.start)
        )

        self.open_set = {self.start}
        self.closed_set = set()
        self.path = []

        self.current = None

        self.finished = False
        self.path_found = False

        self.nodes_explored = 0

        self.start_time = time.perf_counter()
        self.end_time = None

    def step(self):
        """
        Perform one Dijkstra search step.

        This method is called once per frame by the visualizer.
        """

        if self.finished:
            return

        if not self.open_heap:
            self.finished = True
            self.path_found = False
            self.end_time = time.perf_counter()
            return

        current_distance, _, current = heapq.heappop(self.open_heap)

        if current in self.closed_set:
            return

        if current_distance > self.distances[current]:
            return

        self.current = current
        self.open_set.discard(current)
        self.closed_set.add(current)
        self.nodes_explored += 1

        if current == self.end:
            self.finished = True
            self.path_found = True
            self.end_time = time.perf_counter()
            self.reconstruct_path()
            return

        for neighbour in get_neighbors(current, self.maze):

            if neighbour in self.closed_set:
                continue

            new_distance = (
                self.distances[current]
                + movement_cost(current, neighbour)
            )

            if new_distance < self.distances[neighbour]:
                self.distances[neighbour] = new_distance
                self.parents[neighbour] = current

                self.counter += 1

                heapq.heappush(
                    self.open_heap,
                    (new_distance, self.counter, neighbour)
                )

                self.open_set.add(neighbour)

    def reconstruct_path(self):
        """
        Reconstruct the final path from end to start.
        """

        path = []
        current = self.end

        while current is not None:
            path.append(current)
            current = self.parents.get(current)

        path.reverse()
        self.path = path

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

    @property
    def path_cost(self):
        """
        Return the total cost of the final path.
        """

        if not self.path_found:
            return 0.0

        return self.distances[self.end]