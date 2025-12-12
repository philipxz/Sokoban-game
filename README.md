# Sokoban Solver Using A*

This project implements a Sokoban game and an AI solving agent using the A* search algorithm.
The solver is designed to solve small to medium difficulty Sokoban levels

---

## Requirements
- Python
- Pygame
- NumPy

### Running the Game
  From the project directory, run: 
  python main.py

### Running Heuristic Benchmarks
  From the project directory, run: 
  python heuristic_test.py

## Player Controls

| Key        | Action            |
|------------|-------------------|
| Arrow Keys | Move player       |
| S          | Run A* solver     |
| R          | Reset level       |
| ESC        | Quit              |

---

## File and Folder Descriptions

### `main.py`
Game main entry point.
Initializes the game window, loads the level, handles input, and runs the solver.

### `config.py`
Stores global configuration settings such as tile size, window size, asset paths, and selected level.

### `renderer.py`
Handles all graphical rendering using Pygame, including drawing the grid, sprites, and messages.

### `input_handler.py`
Processes keyboard input for player movement, resetting the level, and triggering the AI solver.

### `state.py`
Defines the Sokoban game state.
Includes player movement, box pushing logic, collision handling, and state copying for AI simulation.

### `A_STAR_game_solver.py`
Implements the A* search algorithm and all heuristics:
- Manhattan distance
- Minimum pushes
- Permutation matching
- Hungarian algorithm
- Greedy matching

This file also includes deadlock detection and state pruning.

### `heuristic_test.py`
Benchmarking script for testing and comparing heuristic performance across levels.

### `levels.py`
Contains Sokoban level definitions using ASCII characters:
- `#` wall
- `$` box
- `.` goal
- `@` player start

### `assets/`
Contains sprite images for the player, walls, boxes, goals, and floor tiles.

