"""Pygame visualization for the autonomous navigation system."""

from pathlib import Path

import pygame

from .config import (
    ROWS,
    COLS,
    CELL_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND,
    GRID_COLOR,
    OBSTACLE_COLOR,
    PATH_COLOR,
    START_COLOR,
    GOAL_COLOR,
    ROBOT_COLOR,
    TEXT_COLOR,
    PANEL_COLOR,
)


class NavigationView:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption(
            "AI-Based Autonomous Navigation System"
        )

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18)
        self.small_font = pygame.font.SysFont("consolas", 14)

        self.grid_x = 20
        self.grid_y = 80
        self.grid_width = COLS * CELL_SIZE
        self.grid_height = ROWS * CELL_SIZE

    def draw_text(self, text, x, y, color=TEXT_COLOR, small=False):
        font = self.small_font if small else self.font
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw(self, environment, controller, path, paused=False):
        self.screen.fill(BACKGROUND)

        self.draw_text(
            "AI-Based Autonomous Navigation System",
            20,
            20,
        )
        self.draw_text(
            "A* path planning | 2D grid simulation",
            20,
            48,
            small=True,
        )

        # Draw map cells and obstacles.
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(
                    self.grid_x + col * CELL_SIZE,
                    self.grid_y + row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )

                color = (
                    OBSTACLE_COLOR
                    if environment.grid[row, col] == 1
                    else (255, 255, 255)
                )

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

        # Draw the planned path.
        for row, col in path:
            rect = pygame.Rect(
                self.grid_x + col * CELL_SIZE + 5,
                self.grid_y + row * CELL_SIZE + 5,
                CELL_SIZE - 10,
                CELL_SIZE - 10,
            )
            pygame.draw.rect(self.screen, PATH_COLOR, rect, border_radius=4)

        self._draw_cell(environment.start, START_COLOR)
        self._draw_cell(environment.goal, GOAL_COLOR)

        # Draw the robot as a blue circle.
        row, col = controller.position
        center = (
            self.grid_x + col * CELL_SIZE + CELL_SIZE // 2,
            self.grid_y + row * CELL_SIZE + CELL_SIZE // 2,
        )
        pygame.draw.circle(
            self.screen,
            ROBOT_COLOR,
            center,
            CELL_SIZE // 3,
        )

        # Right-side status panel.
        panel_x = 770
        pygame.draw.rect(
            self.screen,
            PANEL_COLOR,
            (panel_x, 80, 210, 540),
            border_radius=10,
        )

        self.draw_text("NAVIGATION STATUS", panel_x + 12, 100)

        if controller.finished:
            status = "GOAL REACHED"
        elif not controller.has_path:
            status = "NO VALID PATH"
        elif paused:
            status = "PAUSED"
        else:
            status = "NAVIGATING"

        self.draw_text(status, panel_x + 12, 140)

        self.draw_text("Start: " + str(environment.start),
                       panel_x + 12, 190, small=True)
        self.draw_text("Goal: " + str(environment.goal),
                       panel_x + 12, 220, small=True)
        self.draw_text("Robot: " + str(controller.position),
                       panel_x + 12, 250, small=True)

        path_length = max(0, len(path) - 1)
        self.draw_text(
            f"Route steps: {path_length}",
            panel_x + 12,
            290,
            small=True,
        )
        self.draw_text(
            f"Collision attempts: {controller.collision_attempts}",
            panel_x + 12,
            320,
            small=True,
        )

        self.draw_text("CONTROLS", panel_x + 12, 380)
        self.draw_text("SPACE: Pause/resume", panel_x + 12, 420, small=True)
        self.draw_text("R: Restart simulation", panel_x + 12, 450, small=True)
        self.draw_text("S: Save screenshot", panel_x + 12, 480, small=True)
        self.draw_text("ESC: Exit", panel_x + 12, 510, small=True)

        pygame.display.flip()

    def _draw_cell(self, position, color):
        row, col = position
        rect = pygame.Rect(
            self.grid_x + col * CELL_SIZE + 3,
            self.grid_y + row * CELL_SIZE + 3,
            CELL_SIZE - 6,
            CELL_SIZE - 6,
        )
        pygame.draw.rect(self.screen, color, rect, border_radius=5)

    def save_screenshot(self, filename="outputs/navigation_demo.png"):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        pygame.image.save(self.screen, str(path))
        print(f"Screenshot saved: {path.resolve()}")

    def close(self):
        pygame.quit()