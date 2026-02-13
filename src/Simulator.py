from Strategy import Strategy

class Simulator:
    def __init__(self, board, controller, continuously_simulating=False):
        self.board = board
        self.controller = controller
        self.continuously_simulating = continuously_simulating

    def simulate_one_move(self):
        directionToMoveIn = Strategy.next_move_direction(self.board)
        return self.controller.move(directionToMoveIn)
    
