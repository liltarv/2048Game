import random
import Direction 
import Controller
import Reporter

class Board:
    #The board is a 1d list of ints of length vars.BOARD_ROWS * vars.BOARD_COLS, where the 2^n value of the int is the value of the square. 
    #Example: [1, 2, 3, 0] represents a 4x4 board with a 2 in the top left, a 4 in the top right, and a 8 in the bottom left. The rest of the squares are empty.
    def __init__(self, globals, base_board = None):
        self.vars = globals
        self.boardList = base_board
        if (self.boardList == None):
            self.generate_startBoardList()
        

    '''INIT BOARD LOGIC'''

    def generate_startBoardList(self):
        self.boardList = [0] * (self.vars.BOARD_ROWS * self.vars.BOARD_COLS)
        self.fillEmptySquares(2)

    #fill numSquares number of empty squares on the board with either a 2 or a 4
    def fillEmptySquares(self, numSquares):
        #choose numSquares random empty squares from self.board
        emptySquareInds = self.getEmptySquareInds()
        assert len(emptySquareInds) >= numSquares, "Not enough empty squares to fill"

        chosenSquareInds = random.sample(emptySquareInds, numSquares)
        for i in chosenSquareInds:  
            self.boardList[i] = self.fillEmptySquares_determineFillValue()

    def fillEmptySquares_determineFillValue(self):
        randVal = random.random()
        if (randVal < .9):
            return 1
        else:
            return 2

    def getEmptySquareInds(self):
        emptySquareInds = []
        for i in range(len(self.boardList)):
            if (self.boardList[i] == 0):
                emptySquareInds.append(i)
        return emptySquareInds
    
    def index2D_to_1D(self, row, col):
        return row * self.vars.BOARD_COLS + col
    
    def index1D_to_2D(self, index):
        row = index // self.vars.BOARD_COLS
        col = index % self.vars.BOARD_COLS
        return (row, col)

    def noAvailableMoves(self):
        canMove = False
        #iterate through each direction and see if a move is possible
        currDirection = Direction.Direction.UP
        for _ in range(4):
            board_copy = Board(self.vars, self.boardList.copy())
            controller = Controller.Controller(board_copy, None)
            if (controller.move(currDirection)):
                canMove = True
                break
            currDirection = currDirection.adjacent_90()
        return not canMove


    
    