# A\* Pathfinding Visualizer

A Python application that visualizes the **A\* (A-Star) pathfinding algorithm** on a randomly generated grid. The program animates the search process, showing how the algorithm explores the grid before highlighting the shortest path between the start and end nodes.

## Features

- Random maze generation with configurable obstacle density
- Randomly generated start and end positions
- A\* pathfinding algorithm with diagonal movement support
- Animated visualization of the search process
- Displays open and closed node sets during execution
- Highlights the final shortest path
- Prints search statistics including:
  - Runtime
  - Nodes explored
  - Path length

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

| Key       | Action                          |
| --------- | ------------------------------- |
| **1**     | select A\*                      |
| **2**     | select BFS                      |
| **3**     | select Dijkstra                 |
| **4**     | select Greedy Best-First Search |
| **5**     | select DFS                      |
| **Space** | pauses/resumes                  |
| **R**     | Generate a new random maze      |
| **Esc**   | Exit the application            |

## Future Improvements

- Interactive wall placement with the mouse
- Custom start and end node selection
- Adjustable visualization speed
- Multiple heuristic options
- UI controls for maze generation and algorithm settings
