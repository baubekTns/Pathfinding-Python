"""
Global configuration and colour definitions.
Changing values here affects the whole application.
"""

# =========================
# Grid
# =========================

ROWS = 20
COLS = 20
CELL_SIZE = 30

GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE

HUD_WIDTH = 280

WINDOW_WIDTH = GRID_WIDTH + HUD_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT

# =========================
# Visualisation
# =========================

FPS = 60
SEARCH_DELAY = 25
ALLOW_DIAGONALS = True

SHOW_HUD = True

# =========================
# Maze
# =========================

OBSTACLE_DENSITY = 0.30

# =========================
# Colours
# =========================

WHITE = (245, 245, 245)
BLACK = (35, 35, 35)

GRID = (210, 210, 210)

START = (40, 200, 40)
END = (220, 60, 60)

OPEN = (70, 130, 255)
CLOSED = (255, 220, 0)

PATH = (160, 50, 255)

CURRENT = (255, 140, 0)

TEXT = (40, 40, 40)

HUD_BACKGROUND = (255, 255, 255)
HUD_BORDER = (180, 180, 180)

BACKGROUND = WHITE

# =========================
# Algorithm names
# =========================

ASTAR = "A*"
BFS = "Breadth-First Search"
DFS = "Depth-First Search"
DIJKSTRA = "Dijkstra"
GREEDY = "Greedy Best-First Search"