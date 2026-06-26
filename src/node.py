"""
Node representation used by pathfinding algorithms.
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(order=True)
class Node:
    """
    Represents a single grid cell.

    order=True allows Node objects to be compared by the first field
    (f), which lets heapq maintain a priority queue automatically.
    """

    # Used by heapq for sorting
    f: float = field(default=float("inf"))

    # Not used for comparisons
    position: Tuple[int, int] = field(compare=False, default=(0, 0))
    g: float = field(compare=False, default=float("inf"))
    h: float = field(compare=False, default=0.0)
    parent: Optional[Tuple[int, int]] = field(compare=False, default=None)

    def reset(self) -> None:
        """
        Reset node costs before running another search.
        """

        self.f = float("inf")
        self.g = float("inf")
        self.h = 0.0
        self.parent = None