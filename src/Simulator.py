from Strategy import Strategy

class Simulator:
    def __init__(self, board, controller, strategy, continuously_simulating=False):
        self.board = board
        self.controller = controller
        self.strategy = strategy
        self.continuously_simulating = continuously_simulating

    def simulate_one_move(self):
        directionToMoveIn, heuristic = self.strategy.next_move_direction(self.board)
        if directionToMoveIn == None:
            return False
        print(f"Simulating move in direction {directionToMoveIn} with heuristic score {heuristic}")
        moved = self.controller.move(directionToMoveIn)
        #if moved:
        #    self.strategy.main_strategy.update_heuristic_weights()
        return moved
    
