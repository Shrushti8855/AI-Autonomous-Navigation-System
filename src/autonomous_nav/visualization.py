
"""Professional Pygame visualization for autonomous robot navigation."""

from pathlib import Path

import pygame

from .config import (
    ROWS,
    COLS,
    CELL_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)


# Professional dark robotics theme
BG = (10, 15, 28)
SURFACE = (17, 25, 43)
SURFACE_LIGHT = (24, 35, 56)
BORDER = (43, 58, 82)
GRID = (35, 48, 69)
FREE_CELL = (14, 22, 38)
OBSTACLE = (57, 72, 96)
OBSTACLE_EDGE = (79, 99, 127)
WHITE = (237, 244, 255)
MUTED = (139, 157, 185)
CYAN = (46, 221, 255)
CYAN_DARK = (20, 111, 143)
GREEN = (53, 235, 154)
RED = (255, 91, 115)
YELLOW = (255, 195, 73)
BLUE = (91, 151, 255)


class NavigationView:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption(
            "NAV-X | Autonomous Navigation Intelligence"
        )

        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont(
            "segoeui", 25, bold=True
        )
        self.font = pygame.font.SysFont(
            "segoeui", 16, bold=True
        )
        self.body_font = pygame.font.SysFont("segoeui", 14)
        self.small_font = pygame.font.SysFont("consolas", 12)
        self.tiny_font = pygame.font.SysFont("consolas", 10)

        self.grid_x = 20
        self.grid_y = 100
        self.grid_width = COLS * CELL_SIZE
        self.grid_height = ROWS * CELL_SIZE

        self.started_at = pygame.time.get_ticks()
        self.last_position = None
        self.position_history = []

    def draw_text(
        self,
        text,
        x,
        y,
        color=WHITE,
        font=None,
    ):
        font = font or self.body_font
        surface = font.render(str(text), True, color)
        self.screen.blit(surface, (x, y))
        return surface.get_width()

    def rounded_rect(
        self,
        color,
        rect,
        radius=10,
        width=0,
        border_color=None,
    ):
        pygame.draw.rect(
            self.screen,
            color,
            rect,
            width,
            border_radius=radius,
        )

        if border_color:
            pygame.draw.rect(
                self.screen,
                border_color,
                rect,
                1,
                border_radius=radius,
            )

    def cell_center(self, position):
        row, col = position
        return (
            self.grid_x + col * CELL_SIZE + CELL_SIZE // 2,
            self.grid_y + row * CELL_SIZE + CELL_SIZE // 2,
        )

    def draw_header(self, controller, paused):
        self.draw_text(
            "NAV",
            22,
            17,
            CYAN,
            self.title_font,
        )

        nav_width = self.draw_text(
            "-X",
            79,
            17,
            WHITE,
            self.title_font,
        )

        self.draw_text(
            "AUTONOMOUS NAVIGATION INTELLIGENCE",
            22,
            53,
            MUTED,
            self.small_font,
        )

        self.draw_text(
            "A* PATH PLANNING  /  2D ROBOTICS SIMULATION",
            22,
            72,
            CYAN,
            self.tiny_font,
        )

        if controller.finished:
            label, color = "MISSION COMPLETE", GREEN
        elif not controller.has_path:
            label, color = "PATH UNAVAILABLE", RED
        elif paused:
            label, color = "SIMULATION PAUSED", YELLOW
        else:
            label, color = "SYSTEM ONLINE", GREEN

        badge = pygame.Rect(
            SCREEN_WIDTH - 188, 26, 166, 32
        )
        self.rounded_rect(
            SURFACE_LIGHT,
            badge,
            radius=9,
            border_color=BORDER,
        )

        pygame.draw.circle(
            self.screen,
            color,
            (badge.x + 15, badge.centery),
            4,
        )

        self.draw_text(
            label,
            badge.x + 27,
            badge.y + 9,
            color,
            self.tiny_font,
        )

        pygame.draw.line(
            self.screen,
            BORDER,
            (20, 91),
            (SCREEN_WIDTH - 20, 91),
            1,
        )

    def draw_grid(self, environment):
        map_rect = pygame.Rect(
            self.grid_x - 1,
            self.grid_y - 1,
            self.grid_width + 2,
            self.grid_height + 2,
        )

        self.rounded_rect(
            SURFACE,
            map_rect,
            radius=7,
            border_color=BORDER,
        )

        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(
                    self.grid_x + col * CELL_SIZE,
                    self.grid_y + row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )

                is_obstacle = environment.grid[row, col] == 1

                self.rounded_rect(
                    OBSTACLE if is_obstacle else FREE_CELL,
                    rect,
                    radius=2,
                )

                pygame.draw.rect(
                    self.screen,
                    GRID,
                    rect,
                    1,
                )

                if is_obstacle:
                    inner = rect.inflate(-5, -5)
                    self.rounded_rect(
                        OBSTACLE_EDGE,
                        inner,
                        radius=2,
                    )

                    # Small highlight gives the wall depth.
                    pygame.draw.line(
                        self.screen,
                        (105, 124, 151),
                        (inner.x + 3, inner.y + 2),
                        (inner.right - 3, inner.y + 2),
                        1,
                    )

    def draw_path(self, path, controller):
        if not path:
            return

        centers = [self.cell_center(point) for point in path]

        # Dark halo underneath the route.
        if len(centers) > 1:
            pygame.draw.lines(
                self.screen,
                CYAN_DARK,
                False,
                centers,
                max(5, CELL_SIZE // 3),
            )

        # Determine how much of the route has been traversed.
        try:
            current_index = path.index(controller.position)
        except ValueError:
            current_index = 0

        if len(centers) > 1:
            pygame.draw.lines(
                self.screen,
                CYAN,
                False,
                centers,
                3,
            )

            # The completed section is highlighted in green.
            if current_index > 0:
                pygame.draw.lines(
                    self.screen,
                    GREEN,
                    False,
                    centers[: current_index + 1],
                    4,
                )

        # Small route nodes make the path easier to follow.
        for index, center in enumerate(centers):
            if index % 2 == 0:
                pygame.draw.circle(
                    self.screen,
                    CYAN,
                    center,
                    2,
                )

    def draw_marker(self, position, color, label):
        center = self.cell_center(position)
        radius = max(8, CELL_SIZE // 2 - 3)

        pygame.draw.circle(
            self.screen,
            color,
            center,
            radius + 2,
        )
        pygame.draw.circle(
            self.screen,
            SURFACE,
            center,
            radius - 2,
        )
        pygame.draw.circle(
            self.screen,
            color,
            center,
            radius - 4,
        )

        text = self.small_font.render(
            label, True, BG
        )
        self.screen.blit(
            text,
            text.get_rect(center=center),
        )

    def draw_robot(self, position):
        center = self.cell_center(position)
        radius = max(7, CELL_SIZE // 3)

        # Outer halo and robot body.
        pygame.draw.circle(
            self.screen,
            CYAN_DARK,
            center,
            radius + 5,
        )
        pygame.draw.circle(
            self.screen,
            WHITE,
            center,
            radius + 2,
        )
        pygame.draw.circle(
            self.screen,
            BLUE,
            center,
            radius,
        )
        pygame.draw.circle(
            self.screen,
            WHITE,
            center,
            3,
        )

    def draw_metric_card(self, x, y, width, label, value, accent):
        rect = pygame.Rect(x, y, width, 76)

        self.rounded_rect(
            SURFACE_LIGHT,
            rect,
            radius=9,
            border_color=BORDER,
        )

        pygame.draw.rect(
            self.screen,
            accent,
            (x + 1, y + 10, 3, 30),
            border_radius=2,
        )

        self.draw_text(
            label,
            x + 12,
            y + 12,
            MUTED,
            self.tiny_font,
        )

        self.draw_text(
            value,
            x + 12,
            y + 34,
            accent,
            self.font,
        )

    def draw_panel(self, environment, controller, path, paused):
        panel_x = self.grid_x + self.grid_width + 22
        panel_width = SCREEN_WIDTH - panel_x - 20

        panel = pygame.Rect(
            panel_x,
            self.grid_y,
            panel_width,
            self.grid_height,
        )

        self.rounded_rect(
            SURFACE,
            panel,
            radius=12,
            border_color=BORDER,
        )

        x = panel_x + 15
        content_width = panel_width - 30

        self.draw_text(
            "MISSION CONTROL",
            x,
            self.grid_y + 16,
            WHITE,
            self.font,
        )

        self.draw_text(
            "LIVE ROBOT TELEMETRY",
            x,
            self.grid_y + 40,
            MUTED,
            self.tiny_font,
        )

        if controller.finished:
            status, accent = "GOAL REACHED", GREEN
        elif not controller.has_path:
            status, accent = "NO VALID PATH", RED
        elif paused:
            status, accent = "PAUSED", YELLOW
        else:
            status, accent = "NAVIGATING", CYAN

        status_rect = pygame.Rect(
            x,
            self.grid_y + 66,
            content_width,
            35,
        )

        self.rounded_rect(
            SURFACE_LIGHT,
            status_rect,
            radius=7,
            border_color=BORDER,
        )

        pygame.draw.circle(
            self.screen,
            accent,
            (x + 13, status_rect.centery),
            4,
        )

        self.draw_text(
            status,
            x + 25,
            status_rect.y + 10,
            accent,
            self.small_font,
        )

        # Route progress and live metrics.
        route_steps = max(0, len(path) - 1)

        try:
            route_index = path.index(controller.position)
        except ValueError:
            route_index = 0

        progress = (
            route_index / route_steps
            if route_steps > 0
            else (1.0 if controller.finished else 0.0)
        )
        progress = max(0.0, min(1.0, progress))

        percent = int(progress * 100)

        self.draw_text(
            "ROUTE PROGRESS",
            x,
            self.grid_y + 119,
            MUTED,
            self.tiny_font,
        )

        self.draw_text(
            f"{percent}%",
            x + content_width - 39,
            self.grid_y + 116,
            CYAN,
            self.small_font,
        )

        bar = pygame.Rect(
            x,
            self.grid_y + 140,
            content_width,
            7,
        )

        self.rounded_rect(
            BORDER,
            bar,
            radius=4,
        )

        if percent > 0:
            filled = bar.copy()
            filled.width = max(
                4,
                int(bar.width * progress),
            )
            self.rounded_rect(
                GREEN if controller.finished else CYAN,
                filled,
                radius=4,
            )

        gap = 8
        card_width = (content_width - gap) // 2
        cards_y = self.grid_y + 163

        self.draw_metric_card(
            x,
            cards_y,
            card_width,
            "ROUTE STEPS",
            route_steps,
            CYAN,
        )

        self.draw_metric_card(
            x + card_width + gap,
            cards_y,
            card_width,
            "COLLISIONS",
            controller.collision_attempts,
            GREEN if controller.collision_attempts == 0 else RED,
        )

        # Coordinates and mission information.
        details_y = cards_y + 94

        self.draw_text(
            "POSITION DATA",
            x,
            details_y,
            MUTED,
            self.tiny_font,
        )

        details = [
            ("START", str(environment.start), GREEN),
            ("DESTINATION", str(environment.goal), RED),
            ("ROBOT", str(controller.position), BLUE),
        ]

        for index, (label, value, color) in enumerate(details):
            y = details_y + 24 + index * 30

            self.draw_text(
                label,
                x,
                y,
                MUTED,
                self.tiny_font,
            )

            self.draw_text(
                value,
                x + content_width - 85,
                y - 1,
                color,
                self.small_font,
            )

        # Compact legend.
        legend_y = details_y + 126

        pygame.draw.line(
            self.screen,
            BORDER,
            (x, legend_y),
            (x + content_width, legend_y),
            1,
        )

        self.draw_text(
            "MAP LEGEND",
            x,
            legend_y + 13,
            MUTED,
            self.tiny_font,
        )

        legend_items = [
            (CYAN, "Planned path"),
            (GREEN, "Completed path"),
            (OBSTACLE, "Obstacle"),
            (BLUE, "Robot"),
        ]

        for index, (color, label) in enumerate(legend_items):
            col = index % 2
            row = index // 2

            lx = x + col * (content_width // 2)
            ly = legend_y + 37 + row * 24

            pygame.draw.circle(
                self.screen,
                color,
                (lx + 5, ly + 6),
                4,
            )

            self.draw_text(
                label,
                lx + 14,
                ly,
                WHITE,
                self.tiny_font,
            )

        # Footer controls stay inside the panel.
        controls_y = self.grid_y + self.grid_height - 70

        pygame.draw.line(
            self.screen,
            BORDER,
            (x, controls_y - 9),
            (x + content_width, controls_y - 9),
            1,
        )

        self.draw_text(
            "SPACE  PAUSE / RESUME",
            x,
            controls_y,
            MUTED,
            self.tiny_font,
        )

        self.draw_text(
            "R  RESTART     S  SCREENSHOT",
            x,
            controls_y + 20,
            MUTED,
            self.tiny_font,
        )

    def draw_footer(self):
        footer_y = SCREEN_HEIGHT - 22

        self.draw_text(
            "NAV-X  /  AUTONOMOUS SYSTEMS LAB",
            22,
            footer_y,
            MUTED,
            self.tiny_font,
        )

        self.draw_text(
            "PYTHON  |  PYGAME  |  A* SEARCH",
            SCREEN_WIDTH - 260,
            footer_y,
            CYAN,
            self.tiny_font,
        )

    def draw(self, environment, controller, path, paused=False):
        self.screen.fill(BG)

        self.draw_header(controller, paused)
        self.draw_grid(environment)
        self.draw_path(path, controller)

        # Markers and robot are drawn after the route.
        self.draw_marker(environment.start, GREEN, "S")
        self.draw_marker(environment.goal, RED, "G")
        self.draw_robot(controller.position)

        self.draw_panel(
            environment,
            controller,
            path,
            paused,
        )

        self.draw_footer()

        pygame.display.flip()

    def save_screenshot(self, filename="outputs/navigation_demo.png"):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        pygame.image.save(self.screen, str(path))
        print(f"Screenshot saved: {path.resolve()}")

    def close(self):
        pygame.quit()