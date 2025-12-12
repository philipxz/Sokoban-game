import heapq
from itertools import permutations
from scipy.optimize import linear_sum_assignment
import numpy as np
from collections import deque
from config import GRID_WIDTH, GRID_HEIGHT

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


# DEADLOCK HELPERS
# Returns a set of squares where a non target box is always dead. We want better deadlock check, earlier detection -> the earlier the search space is pruned
def compute_dead_squares(walls, targets):

    reachable_positions = set()
    queue = deque()

    # Start from all target positions
    for target_pos in targets:
        reachable_positions.add(target_pos)
        queue.append(target_pos)

    while queue:
        box_x, box_y = queue.popleft()

        for dx, dy in POSSIBLE_MOVES:

            # Reverse push: from goal to possible box/player pos
            prev_box_x, prev_box_y = box_x - dx, box_y - dy
            player_x, player_y = box_x - 2*dx, box_y - 2*dy

            if not (0 <= prev_box_x < GRID_WIDTH and 0 <= prev_box_y < GRID_HEIGHT):
                continue
            if not (0 <= player_x < GRID_WIDTH and 0 <= player_y < GRID_HEIGHT):
                continue

            if (prev_box_x, prev_box_y) in walls or (player_x, player_y) in walls:
                continue

            if (prev_box_x, prev_box_y) not in reachable_positions:
                reachable_positions.add((prev_box_x, prev_box_y))
                queue.append((prev_box_x, prev_box_y))

    dead_squares = set()

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pos = (x, y)
            if pos in walls or pos in targets:
                continue

            if pos not in reachable_positions:
                dead_squares.add(pos)

    return dead_squares

# Corner check for deadlocks
def is_corner_deadlock(box, state):

    if box in state.targets:
        return False

    x, y = box
    cant_move_up    = (x, y-1) in state.walls
    cant_move_down  = (x, y+1) in state.walls
    cant_move_left  = (x-1, y) in state.walls
    cant_move_right = (x+1, y) in state.walls

    if ((cant_move_up and cant_move_left) or
        (cant_move_up and cant_move_right) or
        (cant_move_down and cant_move_left) or
        (cant_move_down and cant_move_right)):
        return True

    return False


# CHECKS IF A BOX IS STUCK IN A CORNER / DEAD SQUARE
def is_deadlock(state, dead_squares, deadlock_cache):
    
    # dead_squares: precomputed set of permanently dead cells (not the target).
    # deadlock_cache: dict[frozenset(boxes)] ~ bool
    
    box_key = frozenset(state.boxes)

    # Cache lookup: same box layout (player pos doesnt matter)
    if box_key in deadlock_cache:
        return deadlock_cache[box_key]

    # static dead squares
    for box in state.boxes:
        if box not in state.targets and box in dead_squares:
            deadlock_cache[box_key] = True
            return True

    # corner patterns 
    for box in state.boxes:
        if is_corner_deadlock(box, state):
            deadlock_cache[box_key] = True
            return True

    # Not a deadlock
    deadlock_cache[box_key] = False
    return False


def solve_using_A_STAR(starting_board_layout, heuristic_function):
    
    initial_board = starting_board_layout
    start_snapshot = initial_board.get_snapshot_of_boxes_and_player()
    
    dead_squares = compute_dead_squares(initial_board.walls, initial_board.targets)
    deadlock_cache = {}
    
    # Makes sure that a level isnt treated as dead if a starting box is on a 'dead square'. level 8 is treated as unsolvable without this
    start_boxes_on_dead = [b for b in initial_board.boxes if b in dead_squares and b not in initial_board.targets]
    if start_boxes_on_dead:
        dead_squares = set()   # disable static dead squares
        deadlock_cache.clear() 

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
                    if not is_deadlock(new_state, dead_squares, deadlock_cache):
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
