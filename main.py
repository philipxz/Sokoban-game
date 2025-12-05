import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT, LEVEL_LAYOUT
from state import parse_level
from renderer import draw_grid, init_renderer
from input_handler import handle_input


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sokoban")

    init_renderer()

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)


    initial_state = parse_level(LEVEL_LAYOUT)
    sokoban_state = parse_level(LEVEL_LAYOUT)

    while True:
        command = handle_input(sokoban_state)
        if command == "reset":
            sokoban_state = parse_level(LEVEL_LAYOUT)

        solved = sokoban_state.is_solved()
        draw_grid(screen, sokoban_state, font, solved)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
