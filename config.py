# Configuration settings for the Sokoban game 
# Tile and grid dimensions
from levels import *

LEVEL_LAYOUT = LEVEL_13

TILE_SIZE = 60
GRID_HEIGHT = len(LEVEL_LAYOUT)
GRID_WIDTH = max(len(row) for row in LEVEL_LAYOUT)

WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE

BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (230, 230, 230)

# TIME BETWEEN AI MOVEMENTS FOR GUI
AI_DELAY = 300

ASSET_PATHS = {
    "player": "assets/player.png",
    "wall": "assets/wall.png",
    "floor": "assets/floor.png",
    "target": "assets/target.png",
    "box": "assets/box.png",
    "box_on_target": "assets/box_on_target.png"
}


