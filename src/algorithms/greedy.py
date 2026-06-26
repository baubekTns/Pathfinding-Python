"""
Greedy Best-First Search algorithm implementation.

Greedy Best-First Search prioritizes the node that appears closest to
the goal according to a heuristic. It is often fast, but it does not
guarantee the shortest path.
"""

from __future__ import annotations

import heapq
import math
import time

from src.algorithms.base import SearchAlgorithm
from src.constants import GREEDY
from src.maze import get_neighbors


class GreedyBestFirstSearch(SearchAlgorithm):
    """
    Greedy Best-First Search pathfinding algorithm.

    Unlike A*, Greedy Best-First Search only considers the heuristic
    distance to the goal:

        f(n) = h(n)

    It ignores the cost already travelled from the start.
    """

    name = GREEDY

    def __init__(self, maze, start, end):
        super().__init__(maze, start, end)

        self.open_heap = []
        self.parents = {}
        self.counter = 0

        self.start_time = None
        self.end_time = None

        self.reset()

    def reset(self):
        """
        Reset Greedy Best-First Search to its initial state.
        """

        self.open_heap = []
        self.parents = {self.start: None}
        self.counter = 0

        heapq.heappush(
            self.open_heap,
            (
                self.heuristic(self.start, self.end),
                self.counter,
                self.start,
            ),
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
        Perform one Greedy Best-First Search step.
        """

        if self.finished:
            return

        if not self.open_heap:
            self.finished = True
            self.path_found = False
            self.end_time = time.perf_counter()
            return

        _, _, current = heapq.heappop(self.open_heap)

        if current in self.closed_set:
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

            if neighbour in self.open_set:
                continue

            self.parents[neighbour] = current
            self.counter += 1

            heapq.heappush(
                self.open_heap,
                (
                    self.heuristic(neighbour, self.end),
                    self.counter,
                    neighbour,
                ),
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