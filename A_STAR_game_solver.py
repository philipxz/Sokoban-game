import heapq
from itertools import permutations

POSSIBLE_MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]


# USES SUM OF MANHATTAN DISTANCES FROM EVERY BOX TO THE CLOEST TARGET POSITION
def heuristic_baseline(state):
    total_dist = 0
    for box in state.boxes:
        min_dist = float('inf')
        for target in state.targets:
            dist = abs(box[0] - target[0]) + abs(box[1] - target[1])
            if dist < min_dist:
                min_dist = dist
        total_dist += min_dist
    return total_dist

def heuristic_matching(state):
    boxes = list(state.boxes)
    targets = list(state.targets)

    if not boxes:
        return 0
    best_total = float('inf')

    # try all box->target pairings and take the minimum total distance
    for perm in permutations(targets, len(boxes)):
        total = 0
        for (boxX, boxY), (targetX, targetY) in zip(boxes, perm):
            total += abs(boxX - targetX) + abs(boxY - targetY)
            if total >= best_total:
                break
        if total < best_total:
            best_total = total

    return best_total

# CHECKS IF A BOX IS STUCK IN A CORNER
def is_deadlock(state):
    for box in state.boxes:
        if box in state.targets:
            continue
            
        x, y = box
        cant_move_up = (x, y-1) in state.walls
        cant_move_down = (x, y+1) in state.walls
        cant_move_left = (x-1, y) in state.walls
        cant_move_right = (x+1, y) in state.walls
        

        if (cant_move_up and cant_move_left) or (cant_move_up and cant_move_right) or (cant_move_down and cant_move_left) or (cant_move_down and cant_move_right):
            return True
            
    return False

# Choose which heuristic to use
heuristic = heuristic_baseline
#heuristic = heuristic_matching

def solve_using_A_STAR(starting_board_layout):
    
    initial_board = starting_board_layout
    start_snapshot = initial_board.get_snapshot_of_boxes_and_player()
    
    # PRIORITY QUEUE
    AI_potential_game_states = []
    tie_breaker = 0
    heapq.heappush(AI_potential_game_states, (heuristic(initial_board), 0, tie_breaker, initial_board, []))
    
    AI_visited_snapshots  = set()
    
    AI_visited_snapshots.add(start_snapshot)
    
    expanded_states = 0

    while AI_potential_game_states:
        total_cost, backward_cost, _, current_state, path = heapq.heappop(AI_potential_game_states)

        expanded_states += 1

        if current_state.is_solved():
            print(
                f"[{heuristic.__name__}] Expanded states: {expanded_states}, "
                f"solution length: {len(path)}"
            )
            return path

        for move in POSSIBLE_MOVES:
            new_state = current_state.clone()
            valid_move = new_state.move_player(move)

            if valid_move:
                
                new_snapshot = new_state.get_snapshot_of_boxes_and_player()

                if new_snapshot not in AI_visited_snapshots:
                    if not is_deadlock(new_state):
                        AI_visited_snapshots.add(new_snapshot)
                        new_backward_cost = backward_cost + 1
                        new_heuristic = heuristic(new_state)
                        new_total_cost = new_backward_cost + new_heuristic
                        
                        tie_breaker += 1
                        heapq.heappush(AI_potential_game_states, (new_total_cost, new_backward_cost, tie_breaker, new_state, path + [move]))
    
    return None