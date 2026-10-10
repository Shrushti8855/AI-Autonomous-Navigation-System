
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
        self.font = pygame.font.SysFont("consolas", 18, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 14)
        self.label_font = pygame.font.SysFont("consolas", 10, bold=True)

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
            "AI-BASED AUTONOMOUS NAVIGATION",
            20,
            16,
        )
        self.draw_text(
            "A* PATH PLANNING  |  GRID-BASED ROBOT SIMULATION",
            20,
            48,
            small=True,
        )

        # Draw the grid and clearly visible obstacle cells.
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(
                    self.grid_x + col * CELL_SIZE,
                    self.grid_y + row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )

                if environment.grid[row, col] == 1:
                    color = OBSTACLE_COLOR
                else:
                    color = (255, 255, 255)

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

                # Add a subtle inset border to each obstacle.
                if environment.grid[row, col] == 1:
                    pygame.draw.rect(
                        self.screen,
                        (31, 41, 55),
                        rect,
                        2,
                    )

        # Draw the planned route as connected yellow lines.
        if len(path) > 1:
            centers = [
                (
                    self.grid_x + col * CELL_SIZE + CELL_SIZE // 2,
                    self.grid_y + row * CELL_SIZE + CELL_SIZE // 2,
                )
                for row, col in path
            ]

            pygame.draw.lines(
                self.screen,
                PATH_COLOR,
                False,
                centers,
                5,
            )

            # Keep route markers smaller than the obstacle cells.
            for center in centers:
                pygame.draw.circle(
                    self.screen,
                    PATH_COLOR,
                    center,
                    3,
                )

        # Draw the moving robot in blue.
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
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            center,
            CELL_SIZE // 3,
            2,
        )

        # Draw START and GOAL last so their labels stay visible.
        self._draw_marker(environment.start, START_COLOR, "S")
        self._draw_marker(environment.goal, GOAL_COLOR, "G")

        # Navigation status panel.
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
            status_color = (22, 163, 74)
        elif not controller.has_path:
            status = "NO VALID PATH"
            status_color = (220, 38, 38)
        elif paused:
            status = "PAUSED"
            status_color = (202, 138, 4)
        else:
            status = "NAVIGATING"
            status_color = (37, 99, 235)

        self.draw_text(status, panel_x + 12, 140, color=status_color)

        self.draw_text("LEGEND", panel_x + 12, 185)

        self._draw_legend_item(
            panel_x + 15, 225, START_COLOR, "S", "START POSITION"
        )
        self._draw_legend_item(
            panel_x + 15, 260, GOAL_COLOR, "G", "GOAL / DESTINATION"
        )
        self._draw_legend_item(
            panel_x + 15, 295, ROBOT_COLOR, "R", "ROBOT POSITION"
        )
        self._draw_legend_item(
            panel_x + 15, 330, PATH_COLOR, "", "PLANNED PATH"
        )
        self._draw_legend_item(
            panel_x + 15, 365, OBSTACLE_COLOR, "", "OBSTACLE / WALL"
        )

        self.draw_text("DETAILS", panel_x + 12, 410)

        self.draw_text(
            f"Start: {environment.start}",
            panel_x + 12, 445, small=True
        )
        self.draw_text(
            f"Goal:  {environment.goal}",
            panel_x + 12, 470, small=True
        )
        self.draw_text(
            f"Robot: {controller.position}",
            panel_x + 12, 495, small=True
        )
        self.draw_text(
            f"Route steps: {max(0, len(path) - 1)}",
            panel_x + 12, 520, small=True
        )
        self.draw_text(
            f"Collisions: {controller.collision_attempts}",
            panel_x + 12, 545, small=True
        )

        self.draw_text(
            "SPACE: Pause  |  R: Restart",
            panel_x + 12, 580, small=True
        )
        self.draw_text(
            "S: Screenshot  |  ESC: Exit",
            panel_x + 12, 600, small=True
        )

        pygame.display.flip()

    def _draw_marker(self, position, color, label):
        row, col = position

        rect = pygame.Rect(
            self.grid_x + col * CELL_SIZE + 3,
            self.grid_y + row * CELL_SIZE + 3,
            CELL_SIZE - 6,
            CELL_SIZE - 6,
        )

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=5,
        )

        text = self.font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def _draw_legend_item(self, x, y, color, marker, label):
        sample = pygame.Rect(x, y, 20, 20)

        if marker:
            pygame.draw.rect(
                self.screen, color, sample, border_radius=4
            )
            text = self.small_font.render(
                marker, True, (255, 255, 255)
            )
            self.screen.blit(text, text.get_rect(center=sample.center))
        else:
            pygame.draw.rect(self.screen, color, sample)

        self.draw_text(label, x + 28, y + 2, small=True)

    def save_screenshot(self, filename="outputs/navigation_demo.png"):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        pygame.image.save(self.screen, str(path))
        print(f"Screenshot saved: {path.resolve()}")

    def close(self):
        pygame.quit()