class Controller:
    
    def __init__(self, board):
        self.board = board

    def move(self, direction):
        for a in range (self.board.vars.BOARD_COLS if direction.is_vertical() else self.board.vars.BOARD_ROWS):
            for b in range(self.board.vars.BOARD_ROWS if direction.is_vertical() else self.board.vars.BOARD_COLS):
                 moveLoc = self.move_getMoveLoc(direction, a, b)
                 curr_1D_ind = self.board.index2D_to_1D(a, b) if direction.is_vertical() else self.board.index2D_to_1D(b, a)
                 if (moveLoc == curr_1D_ind):
                    continue
                 self.board.boardList[moveLoc] = self.board.boardList[curr_1D_ind] if self.board.boardList[moveLoc] == 0 else self.board.boardList[moveLoc] + 1
                 self.board.boardList[curr_1D_ind] = 0

    def move_getMoveLoc(self, direction, a, b):
        moveLoc = direction.get_endpoint()
        curr_1D_ind = self.board.index2D_to_1D(a, b) if direction.is_vertical() else self.board.index2D_to_1D(b, a)
        for c in range(direction.get_endpoint(), direction.opposite().get_endpoint(), -1 * direction.get_1D_delta()):
            if (direction.is_vertical()):
                row = c
                col = a
            else:
                row = a
                col = c
            potMoveInd = self.board.index2D_to_1D(row, col)
            if (self.board.boardList[potMoveInd] == 0 or self.board.boardList[potMoveInd] == self.board.boardList[curr_1D_ind]):
                moveLoc = c
                break
        return moveLoc