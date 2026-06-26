from constants import *
from renderer import draw
from maze import generate_maze
from pathfinding import astar
import pygame

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