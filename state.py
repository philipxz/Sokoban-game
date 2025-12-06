from config import GRID_WIDTH, GRID_HEIGHT

class SokobanState:
    def __init__(self, walls, targets, boxes, player_position):
        self.walls = set(walls)
        self.targets = set(targets)
        self.boxes = set(boxes)
        self.player_position = player_position

    def is_free(self, pos):
        x, y = pos
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            return False
        if pos in self.walls:
            return False
        if pos in self.boxes:
            return False
        return True
    
    def move_player(self, direction):
        dx, dy = direction
        nx = self.player_position[0] + dx
        ny = self.player_position[1] + dy
        new_pos = (nx, ny)

        if new_pos in self.walls:
            return False

        if new_pos in self.boxes:
            box_new = (nx + dx, ny + dy)

            if self.is_free(box_new):
                self.boxes.remove(new_pos)
                self.boxes.add(box_new)
                self.player_position = new_pos
                return True 
            return False
        else:
            self.player_position = new_pos
            return True

    def is_solved(self):
        return self.targets.issubset(self.boxes)



    # CREATES CLONE OF THE SOKOBAN MAP SO A* CAN RUN SIMULATIONS WITHOUT ACTUALLY PLAYING THE GAME ON THE GUI
    def clone(self):
        return SokobanState(
            self.walls,
            self.targets,
            self.boxes,
            self.player_position
        )

    # RETURNS THE PLAYERS POSITION AND THE POSITION OF THE BOXES SO IT KNOWS WHERE IT HAS BEEN BEFORE
    def get_snapshot_of_boxes_and_player(self):
        list_of_boxes = list(self.boxes)
        list_of_boxes.sort()
        return (self.player_position, tuple(list_of_boxes))



def parse_level(layout):
    walls = set()
    targets = set()
    boxes = set()
    player_position = None

    for y, line in enumerate(layout):
        for x, c in enumerate(line):
            pos = (x, y)

            if c == '#':
                walls.add(pos)
            elif c == '.':
                targets.add(pos)
            elif c == '$':
                boxes.add(pos)
            elif c == '@':
                player_position = pos
            elif c == '*':      # box on target
                boxes.add(pos)
                targets.add(pos)
            elif c == '+':      # player on target
                player_position = pos
                targets.add(pos)
                


    return SokobanState(walls, targets, boxes, player_position)