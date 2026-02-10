import Globals
import Board
import Controller
import Visualizer
import Simulator
import Reporter
  self.globals = Globals.Globals()
        self.board = Board.Board(self.globals)
        self.controller = Controller.Controller(self.board)
        self.visualizer = Visualizer.Visualizer(self.board, self.globals)
        self.simulator = Simulator.Simulator(self.board)
        self.reporter = Reporter.Reporter(self.board)
    
    def handleKeyBoardInput(self, event):
        if event.type == pygame.KEYDOWN:
        