"""Grid environment and obstacle management."""

import numpy as np

from .config import ROWS, COLS, START, GOAL


class GridEnvironment:
    """A grid where 0 represents free space and 1 represents an obstacle."""

    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.grid = np.zeros((self.rows, self.cols), dtype=np.uint8)

        self.start = START
        self.goal = GOAL

        self._create_obstacles()

    def _create_obstacles(self):
        """Create deterministic walls with gaps for navigation."""

        # Horizontal wall with a gap at column 7.
        for col in range(2, 19):
            if col != 7:
                self.grid[4, col] = 1

        # Another wall with a gap at column 15.
        for col in range(5, 23):
            if col != 15:
                self.grid[9, col] = 1

        # Vertical wall with a gap at row 12.
        for row in range(5, 15):
            if row != 12:
                self.grid[row, 11] = 1

        # Small obstacle group.
        self.grid[13, 4:8] = 1
        self.grid[14, 7] = 1

        # Ensure the start and goal remain traversable.
        self.grid[self.start] = 0
        self.grid[self.goal] = 0

    def in_bounds(self, position):
        """Return True if a position lies inside the grid."""

        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_walkable(self, position):
        """Check bounds and obstacle occupancy."""

        return (
            self.in_bounds(position)
            and self.grid[position] == 0
        )

    def get_neighbors(self, position):
        """Return valid four-directional neighbors."""

        row, col = position

        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        return [
            point
            for point in candidates
            if self.is_walkable(point)
        ]