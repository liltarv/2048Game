import random
import Direction

class Strategy:
    
    @staticmethod
    def next_move_direction(board):
        # Placeholder strategy: always move random
        possible_directions = {Direction.Direction.UP, Direction.Direction.DOWN, Direction.Direction.LEFT, Direction.Direction.RIGHT}
        return random.choice(list(possible_directions))