class Game:
    def __init__():
        self.globals = Globals()
        self.board = Board(globals)
        self.controller = Controller(board)
        self.visualizer = Visualizer(board, globals)
        self.simulator = Simulator(board)
        self.reporter = Reporter()