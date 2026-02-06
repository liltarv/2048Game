class Board:
    def __init__(self, globals, base_board = None):
        self.vars = globals
        self.board = base_board
        if (self.board = None):
            self.generate_startBoardList()

    def generate_startBoardList(self):
        pass