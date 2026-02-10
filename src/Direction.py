from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def opposite(self):
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[self]
    
    def is_vertical(self):
        return self in {Direction.UP, Direction.DOWN}
    
    def get_endpoint(self):
        if (self.is_vertical()):
            return 0 if self == Direction.UP else self.board.vars.BOARD_ROWS - 1
        else:
            return 0 if self == Direction.LEFT else self.board.vars.BOARD_COLS - 1

    def get_1D_delta(self):
        deltas = {
            Direction.UP: -1,
            Direction.DOWN: 1,
            Direction.LEFT: -1,
            Direction.RIGHT: 1,
        }
        return deltas[self]

