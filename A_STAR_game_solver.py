import heapq
from itertools import permutations
from scipy.optimize import linear_sum_assignment
import numpy as np
from collections import deque

POSSIBLE_MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]


# HEURISTICS

def heuristic_min_pushes(state):
    pushes = 0
    
    for box in state.boxes:
        if box not in state.targets:
            pushes += 1
            
            min_dist = min(abs(box[0] - t[0]) + abs(box[1] - t[1]) 
                          for t in state.targets)
            pushes += min_dist
    
    return pushes

# USES SUM OF MANHATTAN DISTANCES FROM EVERY BOX TO THE CLOEST TARGET POSITION
def heuristic_manhattan(state):
    total_dist = 0
    for box in state.boxes:
        min_dist = float('inf')
        for target in state.targets:
            dist = abs(box[0] - target[0]) + abs(box[1] - target[1])
            if dist < min_dist:
                min_dist = dist
        total_dist += min_dist
    return total_dist

# MATCHING 
def heuristic_matching(state):
    boxes = list(state.boxes)
    targets = list(state.targets)

    if not boxes:
        return 0
    best_total = float('inf')

    for perm in permutations(targets, len(boxes)):
        total = 0
        for (boxX, boxY), (targetX, targetY) in zip(boxes, perm):
            total += abs(boxX - targetX) + abs(boxY - targetY)
            if total >= best_total:
                break
        if total < best_total:
            best_total = total

    return best_total


# HUNGARIAN
def heuristic_hungarian(state):
    boxes = list(state.boxes)
    targets = list(state.targets)
    
    if not boxes:
        return 0
    
    cost_matrix = []
    for box in boxes:
        row = []
        for target in targets:
            dist = abs(box[0] - target[0]) + abs(box[1] - target[1])
            row.append(dist)
        cost_matrix.append(row)
    
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return sum(cost_matrix[i][j] for i, j in zip(row_ind, col_ind))



def heuristic_greedy_matching(state):
    boxes = list(state.boxes)
    targets = list(state.targets)
    

    all_pairs = []
    
    for b_idx, box in enumerate(boxes):
        for t_idx, target in enumerate(targets):
            dist = abs(box[0] - target[0]) + abs(box[1] - target[1])
            all_pairs.append((dist, b_idx, t_idx))
            

    all_pairs.sort(key=lambda x: x[0])
    
    total_dist = 0
    matched_boxes = set()
    matched_targets = set()
    
    for dist, b_idx, t_idx in all_pairs:
        if b_idx not in matched_boxes and t_idx not in matched_targets:
            total_dist += dist
            matched_boxes.add(b_idx)
            matched_targets.add(t_idx)
        if len(matched_boxes) == len(boxes):
            break
            
    return total_dist



# CHECKS IF A BOX IS STUCK IN A CORNER
def is_deadlock(state):
    for box in state.boxes:
        if box in state.targets:
            continue
            
        boxx, boxy = box
        cant_move_up = (boxx, boxy-1) in state.walls
        cant_move_down = (boxx, boxy+1) in state.walls
        cant_move_left = (boxx-1, boxy) in state.walls
        cant_move_right = (boxx+1, boxy) in state.walls
        

        if (cant_move_up and cant_move_left) or (cant_move_up and cant_move_right) or (cant_move_down and cant_move_left) or (cant_move_down and cant_move_right):
            return True
            
    return False


def solve_using_A_STAR(starting_board_layout, heuristic_function):
    
    initial_board = starting_board_layout
    start_snapshot = initial_board.get_snapshot_of_boxes_and_player()
    
    
    # PRIORITY QUEUE
    AI_potential_game_states = []
    tie_breaker = 0
    heapq.heappush(AI_potential_game_states, (heuristic_function(initial_board), 0, tie_breaker, initial_board, []))
    
    AI_visited_snapshots  = set()
    
    AI_visited_snapshots.add(start_snapshot)
    
    expanded_states = 0

    while AI_potential_game_states:
        total_cost, backward_cost, _, current_state, path = heapq.heappop(AI_potential_game_states)

        expanded_states += 1

        if current_state.is_solved():
            return path, expanded_states

        for move in POSSIBLE_MOVES:
            new_state = current_state.clone()
            valid_move = new_state.move_player(move)

            if valid_move:
                
                new_snapshot = new_state.get_snapshot_of_boxes_and_player()

                if new_snapshot not in AI_visited_snapshots:
                    if not is_deadlock(new_state):
                        AI_visited_snapshots.add(new_snapshot)
                        new_backward_cost = backward_cost + 1
                        new_heuristic = heuristic_function(new_state)
                        new_total_cost = new_backward_cost + new_heuristic
                        
                        tie_breaker += 1
                        heapq.heappush(AI_potential_game_states, (new_total_cost, new_backward_cost, tie_breaker, new_state, path + [move]))
    
    return None, expanded_states

def heuristic_ucs(state):
    return 0

def solve_using_UCS(starting_board_layout):
    return solve_using_A_STAR(starting_board_layout, heuristic_ucs)