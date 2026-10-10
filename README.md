# AI-Based Autonomous Navigation System

A grid-based autonomous navigation simulation built with Python, Pygame, and the A* pathfinding algorithm. The system plans a collision-free route around obstacles and simulates a robot navigating from a starting position to a destination.

## Overview

This project demonstrates the fundamentals of autonomous navigation, including environment modeling, obstacle avoidance, path planning, and robot movement in a 2D simulation.

The robot operates in a grid environment containing obstacles. The A* search algorithm calculates a valid route from the start to the goal, and the simulation visualizes the planned path and robot position.

## Features

* **A* Path Planning:** Finds a route from the start to the destination.
* **Obstacle Avoidance:** Plans paths that do not cross blocked grid cells.
* **2D Simulation:** Visualizes the environment using Pygame.
* **Robot Navigation:** Simulates movement along the planned route.
* **Navigation Visualization:** Displays the start, goal, robot, planned path, and obstacles.
* **Navigation Statistics:** Reports route length and collision attempts.
* **Automated Tests:** Validates pathfinding behavior and important edge cases.

## Technology Stack

* Python
* Pygame
* NumPy
* A* Search Algorithm
* Pytest
* Git and GitHub

## Project Architecture

```text
AI-Autonomous-Navigation-System/
├── src/
│   └── autonomous_nav/
│       ├── config.py
│       ├── controller.py
│       ├── environment.py
│       ├── main.py
│       ├── planner.py
│       └── visualization.py
├── tests/
│   └── test_planner.py
├── docs/
│   └── architecture.md
├── images/
├── outputs/
├── videos/
├── main.py
└── requirements.txt
```

### Main Components

* **Environment:** Creates the grid and defines obstacles, start, and goal positions.
* **Planner:** Uses A* to search for a valid route.
* **Controller:** Manages robot movement and navigation state.
* **Visualization:** Displays the grid, obstacles, route, robot, and navigation information.
* **Tests:** Check route validity, obstacle avoidance, adjacency, and edge cases.

## Getting Started

### Prerequisites

* Python 3.12 recommended
* pip
* Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/Shrushti8855/AI-Autonomous-Navigation-System.git
cd AI-Autonomous-Navigation-System
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the simulation

```bash
python main.py
```

The simulation displays the navigation environment and reports the planned route and navigation results in the terminal.

### 5. Run the tests

```bash
python -m pytest tests/test_planner.py -v
```

## Current Test Results

The current implementation passes all five planner tests:

| Test                     | Result |
| ------------------------ | ------ |
| Path exists              | Passed |
| Path avoids obstacles    | Passed |
| Path uses adjacent cells | Passed |
| Blocked goal has no path | Passed |
| Start equals goal        | Passed |

## Example Output

The current simulation run produced:

```text
A* planner initialized.
Start: (1, 1)
Goal: (16, 22)
Planned route steps: 36
SUCCESS: Robot reached the goal.
Collision attempts: 0
```

## Future Improvements

* Add interactive obstacle placement.
* Compare A* with Dijkstra's algorithm and other path planners.
* Add dynamic obstacles and re-planning.
* Record simulation videos and performance metrics.
* Explore integration with a realistic robotics simulator.

## Author

**Shrushti Shewale**

GitHub: [Shrushti8855](https://github.com/Shrushti8855)

---

*This project is an educational 2D navigation simulation and does not represent a complete real-world autonomous-driving system.*
