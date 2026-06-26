"""
Abstract base class for all pathfinding algorithms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class SearchAlgorithm(ABC):
    """
    Base class for all pathfinding algorithms.

    Every algorithm should expose the same interface so the
    visualizer does not need to know which algorithm it is running.
    """

    def __init__(self, maze, start, end):

        self.maze = maze
        self.start = start
        self.end = end

        # Visualisation state
        self.open_set = set()
        self.closed_set = set()
        self.path = []

        self.current: Optional[tuple[int, int]] = None

        # Algorithm state
        self.finished = False
        self.path_found = False

        # Statistics
        self.nodes_explored = 0

    @abstractmethod
    def step(self):
        """
        Perform ONE iteration of the algorithm.

        Called once per frame by the visualizer.
        """
        pass

    @abstractmethod
    def reconstruct_path(self):
        """
        Construct the shortest path after the goal is reached.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset the algorithm to its initial state.
        """
        pass

    @property
    def is_finished(self) -> bool:
        return self.finished

    @property
    def has_path(self) -> bool:
        return self.path_found