# AI-Based Autonomous Navigation System

A Python-based autonomous navigation simulation that demonstrates grid-based path planning, obstacle-aware movement, and interactive visualization using the A* search algorithm.

## Overview

This project simulates a robot navigating a two-dimensional environment from a starting position to a target while avoiding static obstacles.

The project demonstrates core concepts in robotics software, search algorithms, environment representation, movement validation, software testing, and simulation.

**Current implementation:** Classical A* path planning with a custom Pygame simulation. It does not yet include a trained machine-learning model or camera-based object detection.

## Problem Statement

Autonomous robots need to identify traversable space, find suitable routes, and move toward destinations without colliding with obstacles. This project implements a simplified virtual environment to explore the planning and navigation components of that problem.

## Features

* Interactive 2D grid-based simulation
* Start and destination configuration
* Static obstacle representation
* A* path planning with Manhattan distance
* Collision checks before each movement
* Live visualization of the robot and planned route
* Pause, restart, and screenshot controls
* Automated unit tests

## Technology Stack

* Python 3.12
* Pygame
* NumPy
* A* search algorithm
* pytest

## Architecture

1. Environment: represents free cells and obstacles.
2. Planner: calculates a route using A*.
3. Controller: follows the route with safety checks.
4. Visualization: displays the map, robot, route, and status.
5. Tests: verify route validity and important edge cases.

## Project Structure

```text
src/autonomous_nav/  Application modules
tests/               Automated tests
outputs/             Generated simulation outputs
images/              README screenshots
videos/              Demo recordings
docs/                Architecture documentation
main.py              Application entry point
requirements.txt     Python dependencies
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Simulation

```bash
python main.py
```

Controls:

* SPACE: Pause/resume
* R: Restart
* S: Save a screenshot
* ESC: Exit

## Run Tests

```bash
python -m pytest -v
```

## Simulation Demo

Add a screenshot of your actual successful run here:

![Navigation simulation](images/navigation_demo.png)

## Results

Record results from actual executions:

* Goal reached: [record observed result]
* Route length: [record measured steps]
* Collision attempts: [record observed value]
* Automated tests: [record passing/total tests]

Do not report unmeasured performance values.

## Limitations

* Known map rather than camera-derived perception
* Static obstacles in the default scenario
* Grid-based movement rather than physical vehicle dynamics
* No trained object detection or machine-learning model
* No ROS integration or hardware control

## Future Improvements

* Dynamic obstacles and automatic replanning
* OpenCV-based visual perception
* Webots or ROS 2 integration
* Multiple path-planning algorithms for comparison
* Robot motion and sensor simulation
* Performance benchmarks and additional test scenarios

## Learning Outcomes

* A* search and heuristic functions
* Grid maps and environment representation
* Modular Python application design
* Interactive simulation with Pygame
* Automated testing with pytest
* Git, GitHub, and technical documentation

## Author

**Shrushti Shewale**

GitHub: [Shrushti8855](https://github.com/Shrushti8855)

This is an educational software simulation developed to explore autonomous navigation and robotics concepts.
