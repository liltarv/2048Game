import Globals
import Board
import Controller
import Visualizer
import Simulator
import Reporter

class Game:
    def __init__(self):
        self.globals = Globals.Globals()
        self.board = Board.Board(self.globals)
        self.controller = Controller.Controller(self.board)
        self.visualizer = Visualizer.Visualizer(self.board, self.globals)
        self.simulator = Simulator.Simulator(self.board)
        self.reporter = Reporter.Reporter(self.board)
    
    def handleKeyBoardInput(self, event):
        key_to_direction = {
            event.key.UP: self.globals.DIRECTION_UP,
            event.key.DOWN: self.globals.DIRECTION_DOWN,
            event.key.LEFT: self.globals.DIRECTION_LEFT,
            event.key.RIGHT: self.globals.DIRECTION_RIGHT,
        }
        if (event.key in key_to_direction):
            self.controller.move(key_to_direction[event.key])
            self.board.fillEmptySquares(1)
        