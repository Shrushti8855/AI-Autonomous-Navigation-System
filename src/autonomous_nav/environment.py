
"""Grid environment and obstacle management."""

import numpy as np

from .config import ROWS, COLS, START, GOAL


class GridEnvironment:
    """A grid where 0 is free space and 1 is an obstacle."""

    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.grid = np.zeros(
            (self.rows, self.cols),
            dtype=np.uint8,
        )

        self.start = START
        self.goal = GOAL

        self._create_obstacles()

    def _create_obstacles(self):
        """Create a challenging zigzag obstacle course."""

        # Horizontal walls with alternating gaps.
        # These gaps force the robot to change direction.
        walls = {
            3: 5,
            6: 18,
            9: 7,
            12: 16,
            15: 20,
        }

        for row, gap_col in walls.items():
            for col in range(self.cols):
                if col != gap_col:
                    self.grid[row, col] = 1

        # Upper section: additional obstacles.
        self.grid[1, 8:12] = 1
        self.grid[2, 14:18] = 1

        self.grid[4, 8:12] = 1
        self.grid[5, 3:6] = 1

        # Middle section: create additional detours.
        self.grid[7, 3:6] = 1
        self.grid[8, 15:19] = 1

        self.grid[10, 9:13] = 1
        self.grid[11, 19:22] = 1

        # Lower section: obstacles near the final approach.
        self.grid[13, 3:7] = 1
        self.grid[14, 10:14] = 1

        # Always keep start and goal free.
        self.grid[self.start] = 0
        self.grid[self.goal] = 0

    def in_bounds(self, position):
        """Return True if a position is inside the grid."""

        row, col = position

        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
        )

    def is_walkable(self, position):
        """Check grid bounds and obstacle occupancy."""

        if not self.in_bounds(position):
            return False

        row, col = position
        return self.grid[row, col] == 0

    def get_neighbors(self, position):
        """Return walkable four-directional neighbors."""

        row, col = position

        candidates = [
            (row - 1, col),  # Up
            (row + 1, col),  # Down
            (row, col - 1),  # Left
            (row, col + 1),  # Right
        ]

        return [
            point
            for point in candidates
            if self.is_walkable(point)
        ]

    def validate_path(self, path):
        """Check that a path is safe and connects start to goal."""

        if not path:
            return False

        if path[0] != self.start or path[-1] != self.goal:
            return False

        for position in path:
            if not self.is_walkable(position):
                return False

        for current, following in zip(path, path[1:]):
            distance = (
                abs(current[0] - following[0])
                + abs(current[1] - following[1])
            )

            # Every move must go to an adjacent cell.
            if distance != 1:
                return False

        return True