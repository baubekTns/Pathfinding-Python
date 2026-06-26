"""
Depth-First Search algorithm implementation.

DFS explores as far as possible along one path before backtracking.
It does not guarantee the shortest path, but it is useful for visualizing
a very different search strategy.
"""

from __future__ import annotations

import time

from src.algorithms.base import SearchAlgorithm
from src.constants import DFS
from src.maze import get_neighbors


class DepthFirstSearch(SearchAlgorithm):
    """
    Depth-First Search pathfinding algorithm.

    DFS uses a stack, meaning the most recently discovered node is explored
    first.
    """

    name = DFS

    def __init__(self, maze, start, end):
        super().__init__(maze, start, end)

        self.stack = []
        self.parents = {}

        self.start_time = None
        self.end_time = None

        self.reset()

    def reset(self):
        """
        Reset DFS to its initial state.
        """

        self.stack = [self.start]
        self.parents = {self.start: None}

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
        Perform one DFS search step.
        """

        if self.finished:
            return

        if not self.stack:
            self.finished = True
            self.path_found = False
            self.end_time = time.perf_counter()
            return

        current = self.stack.pop()

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
            self.stack.append(neighbour)
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