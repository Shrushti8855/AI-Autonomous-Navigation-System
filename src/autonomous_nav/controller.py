"""Navigation controller for following a planned path."""


class NavigationController:
    """Moves one cell at a time along a planned route."""

    def __init__(self, environment, path):
        self.environment = environment
        self.path = path
        self.path_index = 0

        self.position = path[0] if path else environment.start
        self.collision_attempts = 0

    @property
    def finished(self):
        """True when the robot reaches the goal."""

        return (
            bool(self.path)
            and self.position == self.environment.goal
        )

    @property
    def has_path(self):
        return bool(self.path)

    def step(self):
        """Move to the next route cell after checking safety."""

        if not self.path or self.finished:
            return

        next_index = self.path_index + 1

        if next_index >= len(self.path):
            return

        next_position = self.path[next_index]

        # Safety check before every movement.
        if not self.environment.is_walkable(next_position):
            self.collision_attempts += 1
            self.path = []
            return

        self.position = next_position
        self.path_index = next_index