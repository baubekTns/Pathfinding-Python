import pygame
import random
import time

# Define constants
WIDTH = 20  # Increase grid width
HEIGHT = 20  # Increase grid height
CELL_SIZE = 30  # Increase cell size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
OPEN_COLOR = (0, 0, 255)
CLOSED_COLOR = (255, 255, 0)

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, draw):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [  # 8 Directions (including diagonals)
            (0, -1),  
            (0, 1),   
            (-1, 0),  
            (1, 0),   
            (-1, -1), 
            (-1, 1),  
            (1, -1),  
            (1, 1),   
        ]:
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[0]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loop through children
        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

        # Update the visualization
        draw(maze, open_list, closed_list)
        pygame.display.update() 
        time.sleep(0.1)  

    return []


def plot_maze_with_path(maze, path, start, end):
    """Visualizes the maze and the found path"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
    pygame.display.set_caption("A* Pathfinding")

    # Colors for grid and nodes
    colors = {0: WHITE, 1: BLACK}

    # Function to draw the grid and the path
    def draw_grid(maze, open_list, closed_list):
        screen.fill(WHITE)
        for i in range(HEIGHT):
            for j in range(WIDTH):
                color = colors[maze[i][j]]
                pygame.draw.rect(screen, color, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for node in open_list:
            pygame.draw.rect(screen, OPEN_COLOR, pygame.Rect(node.position[1] * CELL_SIZE, node.position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for node in closed_list:
            pygame.draw.rect(screen, CLOSED_COLOR, pygame.Rect(node.position[1] * CELL_SIZE, node.position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw start and end with different colors
        pygame.draw.rect(screen, GREEN, pygame.Rect(start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Start
        pygame.draw.rect(screen, RED, pygame.Rect(end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # End

        for (x, y) in path:
            pygame.draw.rect(screen, RED, pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    return draw_grid


def generate_random_maze(width, height, obstacle_density=0.3):
    """Generates a random maze with obstacles"""
    maze = []
    for i in range(height):
        row = []
        for j in range(width):
            if random.random() < obstacle_density:
                row.append(1)  # obstacle
            else:
                row.append(0)  # empty space
        maze.append(row)

    # Ensure start and end positions are free (0)
    start = None
    end = None

    while not start:
        start = (random.randint(0, height - 1), random.randint(0, width - 1))
        if maze[start[0]][start[1]] != 0:  # Make sure start is not on an obstacle
            start = None

    while not end:
        end = (random.randint(0, height - 1), random.randint(0, width - 1))
        if maze[end[0]][end[1]] != 0 or end == start:  # Ensure end is not on an obstacle or the same as start
            end = None

    maze[start[0]][start[1]] = 0  # start
    maze[end[0]][end[1]] = 0  # end

    return maze, start, end


def main():
    maze, start, end = generate_random_maze(WIDTH, HEIGHT)
    print(f"Start: {start}, End: {end}")

    path = astar(maze, start, end, draw=plot_maze_with_path(maze, [], start, end))
    print("Path:", path)

    # Event loop to keep the window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':
    main()
