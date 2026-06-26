from constants import *
from renderer import draw
from node import Node
from maze import get_neighbors
import time
import pygame
import math
import heapq

# HEURISTIC

def heuristic(a, b):
    """
    Euclidean distance.
    """

    return math.sqrt(
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2
    )

# PATH RECONSTRUCTION

def reconstruct_path(nodes, end):

    path = []

    current = end

    while current is not None:
        path.append(current)
        current = nodes[current].parent

    path.reverse()

    return path


# A* SEARCH

def astar(screen, maze, start, end):

    start_time = time.perf_counter()

    # Create nodes
    nodes = {}

    for r in range(ROWS):
        for c in range(COLS):
            nodes[(r, c)] = Node((r, c))

    start_node = nodes[start]

    start_node.g = 0
    start_node.h = heuristic(start, end)
    start_node.f = start_node.h

    # Priority queue
    open_heap = []

    heapq.heappush(
        open_heap,
        (start_node.f, start)
    )

    open_set = {start}
    closed_set = set()

    explored = 0

    clock = pygame.time.Clock()

    while open_heap:

        # Keep window responsive
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                return [], {}

        _, current = heapq.heappop(open_heap)

        if current in closed_set:
            continue

        open_set.discard(current)
        closed_set.add(current)

        explored += 1

        # Goal reached
        if current == end:

            elapsed = (
                time.perf_counter() -
                start_time
            ) * 1000

            path = reconstruct_path(nodes, end)

            stats = {
                "time": elapsed,
                "visited": explored,
                "length": len(path)
            }

            # Animate path
            animated_path = []

            for position in path:

                animated_path.append(position)

                draw(
                    screen,
                    maze,
                    start,
                    end,
                    open_set,
                    closed_set,
                    animated_path
                )

                pygame.time.delay(40)

            return path, stats

        current_node = nodes[current]

        # Explore neighbours
        for dr, dc in get_neighbors(current):

            nr = current[0] + dr
            nc = current[1] + dc

            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue

            if maze[nr][nc] == 1:
                continue

            neighbour = (nr, nc)

            if neighbour in closed_set:
                continue

            # Diagonal movement costs slightly more
            if dr != 0 and dc != 0:
                movement_cost = 1.414
            else:
                movement_cost = 1

            tentative_g = (
                current_node.g +
                movement_cost
            )

            neighbour_node = nodes[neighbour]

            if tentative_g < neighbour_node.g:

                neighbour_node.parent = current

                neighbour_node.g = tentative_g

                neighbour_node.h = heuristic(
                    neighbour,
                    end
                )

                neighbour_node.f = (
                    neighbour_node.g +
                    neighbour_node.h
                )

                if neighbour not in open_set:

                    open_set.add(neighbour)

                    heapq.heappush(
                        open_heap,
                        (
                            neighbour_node.f,
                            neighbour
                        )
                    )

        # Draw current frame
        draw(
            screen,
            maze,
            start,
            end,
            open_set,
            closed_set,
            []
        )

        pygame.time.delay(SEARCH_DELAY)

        clock.tick(FPS)

    # No path found
    elapsed = (
        time.perf_counter() -
        start_time
    ) * 1000

    stats = {
        "time": elapsed,
        "visited": explored,
        "length": 0
    }

    return [], stats