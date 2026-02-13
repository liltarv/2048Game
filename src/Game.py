import Globals
import Board
import Controller
import Visualizer
import Simulator
import Reporter
import pygame
import Direction

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
            pygame.K_UP: Direction.Direction.UP,
            pygame.K_DOWN: Direction.Direction.DOWN,
            pygame.K_LEFT: Direction.Direction.LEFT,
            pygame.K_RIGHT: Direction.Direction.RIGHT,
        }
        if (event.key in key_to_direction):
            self.reporter.report_input_info(key_to_direction[event.key])
            moved = self.controller.move(key_to_direction[event.key])
            if moved:
                self.board.fillEmptySquares(1)
            self.reporter.report_on_move()
        