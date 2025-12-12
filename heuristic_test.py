import time
from config import LEVEL_LAYOUT
from state import parse_level
from A_STAR_game_solver import solve_using_A_STAR, heuristic_manhattan, heuristic_matching, heuristic_hungarian, heuristic_greedy_matching, heuristic_ucs, heuristic_min_pushes
from levels import LEVELS

def run_benchmark():
    heuristics_to_test = [
        ("UCS (Baseline)", heuristic_ucs),
        ("Manhattan", heuristic_manhattan),
        ("Matching (Permutations)", heuristic_matching),
        ("Hungarian", heuristic_hungarian),
        ("Greedy", heuristic_greedy_matching),
        ("Min pushes", heuristic_min_pushes)


        
    
    ]


    for name, level in LEVELS.items():
        print("\n")
        for heuristic_name, heuristic_function in heuristics_to_test:
            sokoban_state = parse_level(level)

            start_time = time.time()
            path, expanded_count = solve_using_A_STAR(sokoban_state, heuristic_function)
            end_time = time.time()
            elapsed_time = end_time - start_time
            step_count = len(path) if path is not None else "No Sol"
            print(f"{name:<25}{heuristic_name:<25} | Elapsed Time - {elapsed_time:<10.4f} | States Expanded - {expanded_count:<10} | Solution Steps count - {step_count:<10}")

if __name__ == "__main__":
    run_benchmark()