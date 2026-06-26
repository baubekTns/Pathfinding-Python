"""
Breadth-First Search algorithm implementation.

BFS explores nodes level by level. On an unweighted grid, BFS guarantees
the shortest path in terms of number of steps.
"""

from __future__ import annotations

import time
from collections import deque

from src.algorithms.base import SearchAlgorithm
from src.constants import BFS
from src.maze import get_neighbors


class BreadthFirstSearch(SearchAlgorithm):
    """
    Breadth-First Search pathfinding algorithm.

    BFS uses a queue to explore all neighbouring cells before moving
    deeper into the grid.
    """

    name = BFS

    def __init__(self, maze, start, end):
        super().__init__(maze, start, end)

        self.queue = deque()
        self.parents = {}

        self.start_time = None
        self.end_time = None

        self.reset()

    def reset(self):
        """
        Reset BFS to its initial state.
        """

        self.queue = deque([self.start])
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
        Perform one BFS search step.

        This method is called once per frame by the visualizer.
        """

        if self.finished:
            return

        if not self.queue:
            self.finished = True
            self.path_found = False
            self.end_time = time.perf_counter()
            return

        current = self.queue.popleft()

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
            self.queue.append(neighbour)
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