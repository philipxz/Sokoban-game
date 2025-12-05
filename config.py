# Configuration settings for the Sokoban game 
# Tile and grid dimensions

TILE_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 8

WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE

BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (230, 230, 230)

ASSET_PATHS = {
    "player": "assets/player.png",
    "wall": "assets/wall.png",
    "floor": "assets/floor.png",
    "target": "assets/target.png",
    "box": "assets/box.png",
    "box_on_target": "assets/box_on_target.png"
}

LEVEL_LAYOUT = [
    "##########",
    "#        #",
    "#  .$    #",
    "#  .$ @  #",
    "#        #",
    "#        #",
    "#        #",
    "##########",
]
