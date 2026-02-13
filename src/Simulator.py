from Strategy import Strategy

class Simulator:
    def __init__(self, board, controller, strategy, continuously_simulating=False):
        self.board = board
        self.controller = controller
        self.strategy = strategy
        self.continuously_simulating = continuously_simulating

    def simulate_one_move(self):
        directionToMoveIn, heuristic = self.strategy.next_move_direction(self.board)
        print(f"Simulating move in direction {directionToMoveIn} with heuristic score {heuristic}")
        return self.controller.move(directionToMoveIn)
    
