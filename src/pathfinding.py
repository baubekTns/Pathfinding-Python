import math
import random
import time
import heapq

import pygame

# ==============================
# CONFIGURATION
# ==============================

ROWS = 20
COLS = 20
CELL_SIZE = 30

WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

FPS = 60
SEARCH_DELAY = 25  # milliseconds between search steps

OBSTACLE_DENSITY = 0.30
ALLOW_DIAGONALS = True

# ==============================
# COLORS
# ==============================

WHITE = (245, 245, 245)
BLACK = (35, 35, 35)

GRID = (210, 210, 210)

START = (0, 220, 0)
END = (220, 50, 50)

OPEN = (70, 130, 255)
CLOSED = (255, 220, 0)

PATH = (170, 0, 255)

TEXT = (40, 40, 40)

# ==============================
# NODE
# ==============================

class Node:
    def __init__(self, position):
        self.position = position

        self.g = float("inf")
        self.h = 0
        self.f = float("inf")

        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


# ==============================
# HEURISTIC
# ==============================

def heuristic(a, b):
    """
    Euclidean distance.
    """

    return math.sqrt(
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2
    )


# ==============================
# MAZE GENERATION
# ==============================

def generate_maze(rows, cols, density=0.30):

    maze = []

    for r in range(rows):

        row = []

        for c in range(cols):

            if random.random() < density:
                row.append(1)
            else:
                row.append(0)

        maze.append(row)

    while True:

        start = (
            random.randint(0, rows - 1),
            random.randint(0, cols - 1)
        )

        if maze[start[0]][start[1]] == 0:
            break

    while True:

        end = (
            random.randint(0, rows - 1),
            random.randint(0, cols - 1)
        )

        if maze[end[0]][end[1]] == 0 and end != start:
            break

    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0

    return maze, start, end


# ==============================
# NEIGHBOURS
# ==============================

def get_neighbors(position):

    if ALLOW_DIAGONALS:

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),

            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

    else:

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

    return directions


# ==============================
# DRAWING
# ==============================

def draw(
    screen,
    maze,
    start,
    end,
    open_set,
    closed_set,
    path,
    stats=None
):

    screen.fill(WHITE)

    # Maze
    for r in range(ROWS):

        for c in range(COLS):

            rect = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            color = WHITE

            if maze[r][c] == 1:
                color = BLACK

            pygame.draw.rect(screen, color, rect)

    # Closed set
    for position in closed_set:

        r, c = position

        pygame.draw.rect(
            screen,
            CLOSED,
            (
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # Open set
    for position in open_set:

        r, c = position

        pygame.draw.rect(
            screen,
            OPEN,
            (
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # Final path
    for r, c in path:

        pygame.draw.rect(
            screen,
            PATH,
            (
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # Start
    pygame.draw.rect(
        screen,
        START,
        (
            start[1] * CELL_SIZE,
            start[0] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

    # End
    pygame.draw.rect(
        screen,
        END,
        (
            end[1] * CELL_SIZE,
            end[0] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

    # Grid
    for r in range(ROWS + 1):

        pygame.draw.line(
            screen,
            GRID,
            (0, r * CELL_SIZE),
            (WINDOW_WIDTH, r * CELL_SIZE)
        )

    for c in range(COLS + 1):

        pygame.draw.line(
            screen,
            GRID,
            (c * CELL_SIZE, 0),
            (c * CELL_SIZE, WINDOW_HEIGHT)
        )

    pygame.display.flip()

# ==============================
# PATH RECONSTRUCTION
# ==============================

def reconstruct_path(nodes, end):

    path = []

    current = end

    while current is not None:
        path.append(current)
        current = nodes[current].parent

    path.reverse()

    return path


# ==============================
# A* SEARCH
# ==============================

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

# ==============================
# MAIN APPLICATION
# ==============================

def run_search(screen):

    maze, start, end = generate_maze(
        ROWS,
        COLS,
        OBSTACLE_DENSITY
    )

    draw(
        screen,
        maze,
        start,
        end,
        set(),
        set(),
        []
    )

    pygame.time.delay(300)

    path, stats = astar(
        screen,
        maze,
        start,
        end
    )

    # Draw final state
    draw(
        screen,
        maze,
        start,
        end,
        set(),
        set(path),
        path
    )

    print("\n========== A* Search ==========")
    print(f"Start: {start}")
    print(f"End: {end}")
    print(f"Nodes explored : {stats['visited']}")
    print(f"Path length    : {stats['length']}")
    print(f"Runtime        : {stats['time']:.2f} ms")

    if path:
        print("Status         : PATH FOUND")
    else:
        print("Status         : NO PATH FOUND")

    print("===============================\n")


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    pygame.display.set_caption(
        "A* Pathfinding Visualizer"
    )

    print("======================================")
    print("A* PATHFINDING VISUALIZER")
    print("======================================")
    print("Controls")
    print("--------------------------------------")
    print("SPACE - Generate new maze")
    print("R     - Generate new maze")
    print("ESC   - Quit")
    print("======================================")

    run_search(screen)

    clock = pygame.time.Clock()

    running = True

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    run_search(screen)

                elif event.key == pygame.K_SPACE:
                    run_search(screen)

    pygame.quit()


if __name__ == "__main__":
    main()