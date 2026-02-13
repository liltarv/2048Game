from collections import defaultdict

class Controller:
    
    def __init__(self, board):
        self.board = board

    def move(self, direction):
        moved = False
        hasBeenMergedInto = defaultdict(bool)
        for a in range (direction.adjacent_90().get_endpoint(self.board), direction.adjacent_90().opposite().get_endpoint(self.board) - direction.adjacent_90().get_1D_delta(), -1 * direction.adjacent_90().get_1D_delta()):
            for b in range(direction.get_endpoint(self.board), direction.opposite().get_endpoint(self.board) - direction.get_1D_delta(), -1 * direction.get_1D_delta()):
                 moveLoc_1D = self.move_getMoveLoc(direction, a, b, hasBeenMergedInto)
                 curr_1D_ind = self.board.index2D_to_1D(b, a) if direction.is_vertical() else self.board.index2D_to_1D(a, b)
                 if (self.board.boardList[curr_1D_ind] == 0):
                    continue
                 if (moveLoc_1D == curr_1D_ind):
                    continue
                 if (self.board.boardList[moveLoc_1D] != 0):
                    hasBeenMergedInto[moveLoc_1D] = True
                 self.board.boardList[moveLoc_1D] = self.board.boardList[curr_1D_ind] if self.board.boardList[moveLoc_1D] == 0 else self.board.boardList[moveLoc_1D] + 1
                 self.board.boardList[curr_1D_ind] = 0
                 moved = True
        return moved

    

    def move_getMoveLoc(self, direction, a, b, hasBeenMergedInto):
        moveLoc = direction.get_endpoint(self.board)
        curr_1D_ind = self.board.index2D_to_1D(b, a) if direction.is_vertical() else self.board.index2D_to_1D(a, b)
        for c in range(b + direction.get_1D_delta(), direction.get_endpoint(self.board) + direction.get_1D_delta(), direction.get_1D_delta()):
            if (direction.is_vertical()):
                row = c
                col = a
            else:
                row = a
                col = c
            potMoveInd = self.board.index2D_to_1D(row, col)
            if (self.board.boardList[potMoveInd] != 0):
                moveLoc = c - (direction.get_1D_delta() if ((self.board.boardList[potMoveInd] != self.board.boardList[curr_1D_ind]) or hasBeenMergedInto[potMoveInd]) else 0)
                break
        return self.board.index2D_to_1D(moveLoc, a) if direction.is_vertical() else self.board.index2D_to_1D(a, moveLoc)