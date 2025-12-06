import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT, LEVEL_LAYOUT, AI_DELAY
from state import parse_level
from renderer import draw_grid, init_renderer
from input_handler import handle_input
from A_STAR_game_solver import solve_using_A_STAR

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sokoban AI")

    init_renderer()

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    sokoban_state = parse_level(LEVEL_LAYOUT)
    
    # AI SOLVER SECTION
    
    # AI SOLUTION PATH AND KEEPING TRACK OF IF THE AI IS CURRENTLY SOLVING AND SHOULD IGNORE USER INPUTS
    AI_solution_path = []
    AI_is_solving = False

    while True:
        
        if len(AI_solution_path) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
        else:
            command = handle_input(sokoban_state)
            
            if command == "reset":
                sokoban_state = parse_level(LEVEL_LAYOUT)
                AI_solution_path = []
                AI_is_solving = False
            
            elif command == "solve_using_AI" and not AI_is_solving:
                AI_is_solving = True
                draw_grid(screen, sokoban_state, font, False)
                msg = font.render("SOLVING USING A* PLEASE WAIT", True, (255, 155, 0))
                screen.blit(msg, (10, 30))
                pygame.display.flip()
                
                # RUNS AI SOLVER
                path = solve_using_A_STAR(sokoban_state)
                AI_is_solving = False
                if path:
                    AI_solution_path = path
                    print(f"Solution found! {len(path)} steps.")
                else:
                    print("No solution found.")

        # DISPLAYS AI SOLVERS PATH STEP BY STEP IN GUI
        if len(AI_solution_path) != 0:
                move = AI_solution_path.pop(0)
                sokoban_state.move_player(move)
                pygame.time.wait(AI_DELAY)
                
        solved = sokoban_state.is_solved()
        draw_grid(screen, sokoban_state, font, solved)


        # DISPLAYS GAME
        pygame.display.flip()

if __name__ == "__main__":
    main()