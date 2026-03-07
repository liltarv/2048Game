from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def opposite(self):
        return opposites[self]
    
    def adjacent_90(self):
        return adjacent_90s[self]
    
    def is_vertical(self):
        return self == Direction.UP or self == Direction.DOWN
    
    def get_endpoint(self, board):
        if (self.is_vertical()):
            return 0 if self == Direction.UP else board.vars.BOARD_ROWS - 1
        else:
            return 0 if self == Direction.LEFT else board.vars.BOARD_COLS - 1

    def get_1D_delta(self):
        return deltas[self]

opposites = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

adjacent_90s = {
    Direction.UP: Direction.LEFT,
    Direction.RIGHT: Direction.UP,
    Direction.DOWN: Direction.RIGHT,
    Direction.LEFT: Direction.DOWN,
}

deltas = {
    Direction.UP: -1,
    Direction.DOWN: 1,
    Direction.LEFT: -1,
    Direction.RIGHT: 1,
}