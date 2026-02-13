class Reporter:
    def __init__(self, board):
        self.board = board
    
    def report_on_move(self):
        print("Current Board State:")
        #print current board
        for i in range(self.board.vars.BOARD_ROWS):
            row = self.board.boardList[i*self.board.vars.BOARD_COLS:(i+1)*self.board.vars.BOARD_COLS]
            print(row)

    def report_input_info(self, direction):
        print(f"Moved {direction}")