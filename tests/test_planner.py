"""Automated tests for the A* path planner."""

from src.autonomous_nav.environment import GridEnvironment
from src.autonomous_nav.planner import astar


def test_path_exists():
    env = GridEnvironment()
    path = astar(env, env.start, env.goal)

    assert path
    assert path[0] == env.start
    assert path[-1] == env.goal


def test_path_never_crosses_obstacles():
    env = GridEnvironment()
    path = astar(env, env.start, env.goal)

    assert path

    for position in path:
        assert env.is_walkable(position)


def test_path_uses_adjacent_cells():
    env = GridEnvironment()
    path = astar(env, env.start, env.goal)

    for first, second in zip(path, path[1:]):
        distance = (
            abs(first[0] - second[0])
            + abs(first[1] - second[1])
        )
        assert distance == 1


def test_blocked_goal_has_no_path():
    env = GridEnvironment()
    env.grid[env.goal] = 1

    assert astar(env, env.start, env.goal) == []


def test_start_equals_goal():
    env = GridEnvironment()

    path = astar(env, env.start, env.start)

    assert path == [env.start]