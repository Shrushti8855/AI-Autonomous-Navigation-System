"""A* path planning implementation."""

import heapq


def heuristic(current, goal):
    """Manhattan distance between two grid positions."""

    return (
        abs(current[0] - goal[0])
        + abs(current[1] - goal[1])
    )


def astar(environment, start, goal):
    """
    Find a shortest path using A*.

    Returns:
        A list of (row, column) coordinates including start and goal.
        Returns [] when no valid path exists.
    """

    if not environment.is_walkable(start):
        return []

    if not environment.is_walkable(goal):
        return []

    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), 0, start))

    came_from = {start: None}
    cost_so_far = {start: 0}
    counter = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for neighbor in environment.get_neighbors(current):
            new_cost = cost_so_far[current] + 1

            if (
                neighbor not in cost_so_far
                or new_cost < cost_so_far[neighbor]
            ):
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current

                priority = new_cost + heuristic(neighbor, goal)
                counter += 1

                heapq.heappush(
                    frontier,
                    (priority, counter, neighbor),
                )

    if goal not in came_from:
        return []

    # Reconstruct the path from goal back to start.
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path