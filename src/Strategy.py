import random
import Direction
import Board
import Controller
import Visualizer
import pygame
import copy

class Strategy:

    def __init__(self, board, heuristic_weights=None):
        self.board = board
        self.main_strategy = Strategy.Learning_Algo(board, heuristic_weights)
        
    def next_move_direction(self, board):
        return self.main_strategy.next_move_direction(board)
    
    def heuristic_evaluation(self, board):
        return self.main_strategy.heuristic_evaluation(board)

    class Learning_Algo():
        def __init__(self, board, heuristic_weights=None):
            self.board = board
            self.score = 0
            self.oldScore = 0
            self.oldBoard = None
            if heuristic_weights is not None:
                self.heuristic_weights = heuristic_weights
            else:
                self.heuristic_weights = {
                    Direction.Direction.UP: None,
                    Direction.Direction.DOWN: None,
                    Direction.Direction.LEFT: None,
                    Direction.Direction.RIGHT: None}
                self.fill_base_heuristic_weights()
            self.threshold = 0.50  #hyperparameter for counting a section as contributing to the heuristic score
            self.train(10)  #number of iterations to train the heuristic weights for. Can be adjusted for better performance, but keep in mind that training can take a long time, especially with more iterations.

        def updateOldBoard(self, board):
            self.oldBoard = Board.Board(board.vars, board.boardList.copy())

        #newScore = oldScore + (square value of each tile merged on that move)
        def updateScore(self):
            self.oldScore = self.score
            for i in range(len(self.board.boardList)):
                if (self.board.boardList[i] != 0 and self.oldBoard.boardList[i] != 0 and self.board.boardList[i] != self.oldBoard.boardList[i]):
                    #a merge has occurred at this index, so add the value of the merged tile to the score
                    self.score += (2)**(self.board.boardList[i])

        def train(self, num_iterations):
            base_weights = copy.deepcopy(self.heuristic_weights)
            curr_weights = copy.deepcopy(self.heuristic_weights)
            for i in range(num_iterations):
                print(f"Training iteration {i+1}/{num_iterations}")
                self.board = Board.Board(self.board.vars)
                self.score = 0
                controller = Controller.Controller(self.board, None)
                visualizer = Visualizer.Visualizer(self.board, self.board.vars)
                while not self.board.noAvailableMoves():
                    #print(curr_weights == base_weights)
                    moved = self.simulate_one_move(controller)
                    #print(self.heuristic_weights.equals(curr_weights)
                    if moved:
                        self.board.fillEmptySquares(1)
                    visualizer.draw()
                    pygame.display.flip()
                    curr_weights = self.heuristic_weights.copy()
                self.heuristic_weights = curr_weights
                self.printHeuristicWeights()
            self.printHeuristicWeights() 
        
        def simulate_one_move(self, controller):
            directionToMoveIn, heuristic = self.next_move_direction(self.board)
            if directionToMoveIn == None:
                return False
           # print(f"Simulating move in direction {directionToMoveIn} with heuristic score {heuristic}")
            moved = controller.move(directionToMoveIn)
            if moved:
                oldHeuristicWeights = self.heuristic_weights.copy()
                self.update_heuristic_weights(move_direction=directionToMoveIn)
                #print("e")
                #print(self.heuristic_weights == oldHeuristicWeights)
            return moved

        def update_heuristic_weights(self, move_direction):
            oldBoard = self.oldBoard
            newBoard = self.board
            old_score = self.oldScore
            self.updateScore()
            new_score = self.score
            ##print(-old_score + new_score)
            #print(oldBoard.boardList == newBoard.boardList)
            oldHeuristicWeights = copy.deepcopy(self.heuristic_weights)
            score_diff = new_score - old_score #the score difference observed after making the move, minus the value of the highest tile on the old board (to account for the fact that the heuristic evaluation is based on the current board state, so we want to isolate the score change that is not just due to having higher value tiles on the board)
            learning_rate = 10  #hyperparameter for how much to adjust the weights based on the observed score difference
            new_heuristic_weights = copy.deepcopy(self.heuristic_weights)
            for section_index in range(9):
                for square_index in range(4):
                    tile_value = oldBoard.boardList[self.weightTableIndiciesToBoardIndicies(section_index, square_index)]
                    weight = self.heuristic_weights[move_direction][section_index][square_index]
                    #adjust the weight based on the score difference and the tile value
                    new_heuristic_weights[move_direction][section_index][square_index] *= (1+oldBoard.getHighestTileValue() - new_heuristic_weights[move_direction][section_index][square_index] * tile_value) / (new_heuristic_weights[move_direction][section_index][square_index] + 1e-8)  #add a small value to the denominator to avoid division by zero
                    print(f"Updated weight for move {move_direction}, section {section_index}, square {square_index}: {new_heuristic_weights[move_direction][section_index][square_index]} by {new_heuristic_weights[move_direction][section_index][square_index] - weight}")
            self.heuristic_weights = new_heuristic_weights
            

        #the heuristic weights are based on the following:
        #First, split the board into 2x2 sections, indexed by the 1d index of the top left corner of the section.
        #Each square in that section is assigned a weight in that section
        #Repeat 4 times, one for each possible move direction
        #So, heuristic_weights is of the form 
        # heuristic_weights[move_direction][section_index][square_index_in_section], where heuristic_weights is a dictionary of 4 keys (one for each move direction), each key maps to a list of 9 sections (the 2x2 squares), and each section is a list of 4 weights for the 4 squares in that section.
        #the 2x2 squares do have overlap, so the same square will have different weights in different sections, depending on the move direction. This allows the learning algorithm to learn different heuristics for different move directions, which can be useful for learning to keep high value tiles in certain positions depending on the move direction.
        #the goal of the heuristic weights is to estimate the change in score that would result from making a move in a certain direction, based on the current board state. The learning algorithm can then adjust these weights over time based on the actual score changes observed after making moves, in order to improve its heuristic evaluation and ultimately make better move decisions.
        #now, there are 8 more sections that are the rows and columns of the board, to capture heuristics related to those as well. So, there are a total of 17 sections (the 9 2x2 squares, plus the 4 rows and 4 columns), and each section has 4 weights for the 4 squares in that section.
        #now, there are 4 more sections, each being a 3x3 square in the corner of the board, to capture heuristics related to those as well. So, there are a total of 21 sections (the 9 2x2 squares, plus the 4 rows and 4 columns, plus the 4 3x3 corner squares), and each section has 4 weights for the 4 squares in that section.
        def fill_base_heuristic_weights(self):
            total_squares = self.board.vars.BOARD_ROWS * self.board.vars.BOARD_COLS
            directions = [Direction.Direction.UP, Direction.Direction.DOWN, Direction.Direction.LEFT, Direction.Direction.RIGHT]
            for move_direction in directions:
                single_direction_weights = []
                for section_index in range(21):  # 9 2x2 sections + 4 rows + 4 columns + 4 3x3 corner squares
                    section_weights = []
                    for square_index in range(4 if section_index < 9 else self.board.vars.BOARD_COLS if section_index < 13 else self.board.vars.BOARD_ROWS if section_index < 17 else 9):  # 4 squares in a 2x2 section, or 4 squares in a row/column, or 4 squares in a 3x3 corner square
                        section_weights.append(1)  # Initialize with zero weights
                    single_direction_weights.append(section_weights)
                
                self.heuristic_weights[move_direction] = single_direction_weights


        #for each 2x2 section, calculate the heuristic score for that section by multiplying the tile values by the corresponding weights for that move direction, and summing them up.
        #if the value exceeds a certain threshold, then count that section as contributing to the heuristic score for that move direction. The threshold can be a hyperparameter that can be tuned for better performance.
        def heuristic_evaluation(self, board, move_direction):
            total_score = 0
            for section_index in range(21):  # 9 2x2 sections + 4 rows + 4 columns + 4 3x3 corner squares
                section_score = 0
                maxTileValueInSection = 0
                for square_index in range(4 if section_index < 9 else self.board.vars.BOARD_COLS if section_index < 13 else self.board.vars.BOARD_ROWS if section_index < 17 else 9):  # 4 squares in a 2x2 section, or 4 squares in a row/column, or 4 squares in a 3x3 corner square
                    tile_value = board.boardList[self.weightTableIndiciesToBoardIndicies(section_index, square_index)]
                    weight = self.heuristic_weights[move_direction][section_index][square_index]
                    section_score += tile_value * weight
                    if tile_value > maxTileValueInSection:
                        maxTileValueInSection = tile_value
                if section_score > self.threshold:
                    total_score += maxTileValueInSection  #add the value of the highest tile in that section to the total score, to encourage the algorithm to learn heuristics that keep high value tiles in certain positions on the board depending on the move direction. This is based on the idea that having high value tiles in certain positions can lead to better score outcomes, even if the immediate heuristic score for that section is not very high.
            return total_score
        
        def weightTableIndiciesToBoardIndicies(self, section_index, square_index):
            if (section_index < 9):
                #the section index corresponds to the 1d index of the top left corner of the 2x2 section on the board
                #the square index corresponds to the position within that 2x2 section, indexed from 0 to 3, starting from the top left and going row by row
                section_row = section_index // (self.board.vars.BOARD_COLS - 1)
                section_col = section_index % (self.board.vars.BOARD_COLS - 1)
                square_row = square_index // 2
                square_col = square_index % 2
                board_row = section_row + square_row
                board_col = section_col + square_col
                return self.board.index2D_to_1D(board_row, board_col)
            elif (section_index < 13):
                #the section index corresponds to the row index of the board, and the square index corresponds to the column index of the board
                row = section_index - 9
                col = square_index
                return self.board.index2D_to_1D(row, col)
            elif (section_index < 17):
                #the section index corresponds to the column index of the board, and the square index corresponds to the row index of the board
                col = section_index - 13
                row = square_index
                return self.board.index2D_to_1D(row, col)
            else:
                #the section index corresponds to the 3x3 corner squares, indexed from top left, top right, bottom left, bottom right, and the square index corresponds to the position within that 3x3 square, indexed from 0 to 8, starting from the top left and going row by row
                corner_index = section_index - 17
                square_row = square_index // 3
                square_col = square_index % 3
                if corner_index == 0:  # top left corner
                    board_row = square_row
                    board_col = square_col
                elif corner_index == 1:  # top right corner
                    board_row = square_row
                    board_col = self.board.vars.BOARD_COLS - 3 + square_col
                elif corner_index == 2:  # bottom left corner
                    board_row = self.board.vars.BOARD_ROWS - 3 + square_row
                    board_col = square_col
                else:  # bottom right corner
                    board_row = self.board.vars.BOARD_ROWS - 3 + square_row
                    board_col = self.board.vars.BOARD_COLS - 3 + square_col
                return self.board.index2D_to_1D(board_row, board_col)
            
        
        def printHeuristicWeights(self):
            print("Current Heuristic Weights:")
            for move_direction in [Direction.Direction.UP, Direction.Direction.DOWN, Direction.Direction.LEFT, Direction.Direction.RIGHT]:
                print(f"Move Direction: {move_direction}")
                for section_index in range(9):
                    print(f"Section {section_index}: {self.heuristic_weights[move_direction][section_index]}")

        def next_move_direction(self, board):
            direction_scores = []
            for move_direction in [Direction.Direction.UP, Direction.Direction.DOWN, Direction.Direction.LEFT, Direction.Direction.RIGHT]:
                if (Controller.Controller(board, None).canMove(move_direction)):
                    direction_scores.append((move_direction, self.heuristic_evaluation(board, move_direction)))
            #return best_direction, heuristic_score
            self.updateOldBoard(board)
            return max(direction_scores, key=lambda x: x[1]) if direction_scores else (None, 0)



            





    class Greedy():
        def __init__(self, board, heuristic_weights_1d=None):
            self.board = board
            if heuristic_weights_1d is not None:
                self.heuristic_weights_1d = heuristic_weights_1d
            else:
                 self.fill_base_heuristic_weights()

        #Heuristic weights for the 4x4 board, starting from top left and going row by row. Higher weights in the top left corner to encourage keeping high value tiles there.
        #powers of 4
        def fill_base_heuristic_weights(self):
            self.heuristic_weights_1d = [(4)**15, (4)**14, (4)**13, (4)**12, (4)**8, (4)**9, (4)**10, (4)**11, (4)**7, (4)**6, (4)**5, (4)**4, (4)**0, (4)**1, (4)**2, (4)**3]

        
        def next_move_direction(self, board):
            return self.greedy_search(board, 3)

        def printHeuristicWeights(self):
            print("Current Heuristic Weights:")
            for i in range(self.board.vars.BOARD_ROWS):
                row = self.heuristic_weights_1d[i*self.board.vars.BOARD_COLS:(i+1)*self.board.vars.BOARD_COLS]
                print(row)

        def greedy_search(self, board, depth):
            bestDirection = Direction.Direction.UP
            bestHeuristicScore = float('-inf')
            currDirection = Direction.Direction.UP
            baseHeuristicScore = self.heuristic_evaluation(board)
            currHeuristicScore = baseHeuristicScore
            canMove = False
            for _ in range(4):
                newBoard = Board.Board(board.vars, board.boardList.copy())
                newController = Controller.Controller(newBoard, None)
                if (newController.move(currDirection)):
                    canMove = True
                    newBoard.placeTileInBestPossibleSpot()
                    if (depth == 1):
                        currScore = self.heuristic_evaluation(newBoard)
                    else:
                        childDir, currScore = self.greedy_search(newBoard, depth - 1)
                    if (currScore > bestHeuristicScore):
                        bestHeuristicScore = currScore
                        bestDirection = currDirection
                currDirection = currDirection.adjacent_90();
                currScore = baseHeuristicScore
            return (bestDirection, bestHeuristicScore) if canMove else (None, baseHeuristicScore)
                    
        
        def heuristic_evaluation(self, board):
            total = 0
            for i in range(len(board.boardList)):
                total += (board.boardList[i]) * (self.heuristic_weights_1d[i])
            return total
        
        