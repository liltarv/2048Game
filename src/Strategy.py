import random
import Direction
import Board
import Controller

class Strategy:

    def __init__(self, board, heuristic_weights_1d=None):
        self.board = board
        if heuristic_weights_1d is not None:
            self.heuristic_weights_1d = heuristic_weights_1d
        else:
            # Heuristic weights for the 4x4 board, starting from top left and going row by row. Higher weights in the top left corner to encourage keeping high value tiles there.
            #powers of 3
            self.heuristic_weights_1d = [(4)**15, (4)**14, (4)**13, (4)**12, (4)**8, (4)**9, (4)**10, (4)**11, (4)**7, (4)**6, (4)**5, (4)**4, (4)**0, (4)**1, (4)**2, (4)**3]

    
    def next_move_direction(self, board):
        return self.greedy_search(board, 3)
    
    def printHeuristicWeights(self):
        print("Current Heuristic Weights:")
        for i in range(self.board.vars.BOARD_ROWS):
            row = self.heuristic_weights_1d[i*self.board.vars.BOARD_COLS:(i+1)*self.board.vars.BOARD_COLS]
            print(row)

    def greedy_search(self, board, depth):
        self.printHeuristicWeights()
        bestDirection = Direction.Direction.UP
        bestHeuristicScore = float('-inf')
        currDirection = Direction.Direction.UP
        baseHeuristicScore = self.heuristic_evaluation(board)
        currHeuristicScore = baseHeuristicScore
        for _ in range(4):
            newBoard = Board.Board(board.vars, board.boardList.copy())
            newController = Controller.Controller(newBoard, None)
            if (newController.move(currDirection)):
                newBoard.placeTileInWorstPossibleSpot()
                if (depth == 1):
                    currScore = self.heuristic_evaluation(newBoard)
                else:
                    childDir, currScore = self.greedy_search(newBoard, depth - 1)
                if (currScore > bestHeuristicScore):
                    bestHeuristicScore = currScore
                    bestDirection = currDirection
            currDirection = currDirection.adjacent_90();
            currScore = baseHeuristicScore
        return (bestDirection, bestHeuristicScore)
                
    
    def heuristic_evaluation(self, board):
        total = 0
        for i in range(len(board.boardList)):
            total += (board.boardList[i]) * (self.heuristic_weights_1d[i])
        return total