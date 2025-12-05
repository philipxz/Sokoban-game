import pygame
import sys

def handle_input(sokoban_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_UP:
                sokoban_state.move_player((0, -1))
            elif event.key == pygame.K_DOWN:
                sokoban_state.move_player((0, 1))
            elif event.key == pygame.K_LEFT:
                sokoban_state.move_player((-1, 0))
            elif event.key == pygame.K_RIGHT:
                sokoban_state.move_player((1, 0))

    return None
