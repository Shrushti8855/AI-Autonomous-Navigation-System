"""Application entry point for the navigation simulation."""

import pygame

from .config import FPS, MOVE_INTERVAL_MS
from .environment import GridEnvironment
from .planner import astar
from .controller import NavigationController
from .visualization import NavigationView


def main():
    environment = GridEnvironment()

    path = astar(
        environment,
        environment.start,
        environment.goal,
    )

    if not path:
        print("No valid route found.")
        return

    print("A* planner initialized.")
    print(f"Start: {environment.start}")
    print(f"Goal: {environment.goal}")
    print(f"Planned route steps: {len(path) - 1}")

    controller = NavigationController(environment, path)
    view = NavigationView()

    running = True
    paused = False
    elapsed = 0

    try:
        while running:
            elapsed += view.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_SPACE:
                        paused = not paused

                    elif event.key == pygame.K_s:
                        view.save_screenshot()

                    elif event.key == pygame.K_r:
                        environment = GridEnvironment()
                        path = astar(
                            environment,
                            environment.start,
                            environment.goal,
                        )
                        controller = NavigationController(
                            environment,
                            path,
                        )
                        elapsed = 0
                        paused = False

            if not paused and not controller.finished:
                if elapsed >= MOVE_INTERVAL_MS:
                    controller.step()
                    elapsed = 0

            view.draw(
                environment,
                controller,
                path,
                paused=paused,
            )

            if controller.finished:
                # Print only once, after reaching the goal.
                if not getattr(controller, "success_reported", False):
                    print("SUCCESS: Robot reached the goal.")
                    print(
                        "Collision attempts:",
                        controller.collision_attempts,
                    )
                    controller.success_reported = True

    finally:
        view.close()



if __name__ == "__main__":
    main()