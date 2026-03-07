from Strategy import Strategy
import time 

class Simulator:
    def __init__(self, board, controller, strategy, reporter=None, continuously_simulating=False):
        self.board = board
        self.controller = controller
        self.strategy = strategy
        self.reporter = reporter
        self.continuously_simulating = continuously_simulating
        self.gameNum = 1
        self.moveNum = 0
        self.deltaTime = 0
        self.predHeuristic = 0
        self.lookahead = 0
        self.currHeuristic = 0

    def simulate_one_move(self, printPerMove=False):
        self.moveNum += 1
        starttime = time.time()
        directionToMoveIn, self.predHeuristic, self.lookahead = self.strategy.next_move_direction(self.board)
        if directionToMoveIn == None:
            return False
        endtime = time.time()
        self.deltaTime = endtime - starttime
        self.currHeuristic = self.strategy.main_strategy.heuristic_evaluation(self.board)
        if (self.reporter != None):
            self.reporter.collect_data(self)
        if printPerMove: 
            print(f"Simulating move in direction {directionToMoveIn} with heuristic score {heuristic}")
        moved = self.controller.move(directionToMoveIn)
        if moved:
            self.board.fillEmptySquares(1)
        #if moved:
        #    self.strategy.main_strategy.update_heuristic_weights()
        return moved
    
