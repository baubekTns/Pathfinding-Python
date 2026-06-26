# Pathfinding Algorithm Visualizer

A Python application that visualizes and compares multiple pathfinding algorithms on a randomly generated grid. The program animates the search process, showing how each algorithm explores the grid before highlighting the path between the start and end nodes.

## Features

- Procedural DFS maze generation with loops, dead-end reduction, and configurable layout settings
- Randomly generated start and end positions
- Multiple pathfinding algorithms:
  - A\* Search
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Dijkstra's Algorithm
  - Greedy Best-First Search

- Diagonal movement support
- Animated visualization of the search process
- Displays open and closed node sets during execution
- Highlights the final discovered path
- Keyboard controls for switching between algorithms
- On-screen HUD showing:
  - Active algorithm
  - Search status
  - Runtime
  - Nodes explored
  - Open and closed node counts
  - Path length
  - Path cost where applicable

## Technologies

- Python 3
- Pygame

## Project Structure

```
.
├── pathfinding.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Pathfinding-Python.git
cd Pathfinding-Python
```

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
```

**Windows**

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows (Command Prompt)**

```cmd
.venv\Scripts\activate
```

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Project

```bash
python main.py
```

## Controls

| Key       | Action                                |
| --------- | ------------------------------------- |
| **1**     | select A\*                            |
| **2**     | select BFS                            |
| **3**     | select Dijkstra                       |
| **4**     | select Greedy Best-First Search       |
| **5**     | select DFS                            |
| **Enter** | rerun selected algorithm on same maze |
| **Space** | pauses/resumes                        |
| **R**     | Generate a new random maze            |
| **Esc**   | Exit the application                  |

## Future Improvements

- Interactive wall placement with the mouse
- Custom start and end node selection
- Adjustable visualization speed
- Multiple heuristic options
- UI controls for maze generation and algorithm settings
