import pygame
from config import (
    TILE_SIZE, GRID_WIDTH, GRID_HEIGHT,
    ASSET_PATHS, BACKGROUND_COLOR, TEXT_COLOR
)

# Manages loading and accessing sprites
class SpriteManager: 
    def __init__(self):
        self.sprites = {}
        self.load_sprites()

    def load_sprites(self):
        for key, path in ASSET_PATHS.items():
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.sprites[key] = img

    def get(self, key):
        return self.sprites[key]

sprite_manager = None


def init_renderer():
    global sprite_manager
    sprite_manager = SpriteManager()


def draw_grid(surface, state, font, solved):
    if sprite_manager is None:
        raise RuntimeError("Call init_renderer() before drawing.")

    surface.fill(BACKGROUND_COLOR)

    floor_sprite = sprite_manager.get("floor")
    target_sprite = sprite_manager.get("target")
    wall_sprite = sprite_manager.get("wall")

    # Draw floor
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            surface.blit(floor_sprite, (x * TILE_SIZE, y * TILE_SIZE))

    # Draw targets
    for (targetsx, targety) in state.targets:
        surface.blit(target_sprite, (targetsx * TILE_SIZE, targety * TILE_SIZE))

    # Draw walls
    for (wallx, wally) in state.walls:
        surface.blit(wall_sprite, (wallx * TILE_SIZE, wally * TILE_SIZE))

    # Draw boxes
    for (boxesx, boxesy) in state.boxes:
        if (boxesx, boxesy) in state.targets:
            sprite = sprite_manager.get("box_on_target")
        else:
            sprite = sprite_manager.get("box")
        surface.blit(sprite, (boxesx * TILE_SIZE, boxesy * TILE_SIZE))

    # Draw player
    playerx, playery = state.player_position
    surface.blit(sprite_manager.get("player"), (playerx * TILE_SIZE, playery * TILE_SIZE))

    msg = "Solved! R: reset | S: A* solve" if solved else "Arrows: move | R: reset | S: A* solve"
    surface.blit(font.render(msg, True, TEXT_COLOR), (GRID_WIDTH * TILE_SIZE // 2 - font.size(msg)[0] // 2, 10))
