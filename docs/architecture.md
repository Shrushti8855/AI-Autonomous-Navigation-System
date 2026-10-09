# System Architecture

## Environment
A NumPy occupancy grid represents the map:
- 0: free cell
- 1: obstacle

## Planner
A* uses Manhattan distance and four-directional movement.

## Controller
The controller executes the route one cell at a time and
checks the next cell before moving.

## Visualization
Pygame renders the grid, obstacles, route, robot, and status.

## Limitations
This version uses a known map and static obstacles.
It does not yet implement camera perception, localization,
learned object detection, dynamic obstacle prediction, or
physical robot control.