import Globals
import Board
import Controller
import Visualizer
import Simulator
import Reporter
import pygame
import Direction
import Strategy
from pygame import display

class Game:
    def __init__(self):
        self.globals = Globals.Globals()
        self.board = Board.Board(self.globals)
        self.strategy = Strategy.Strategy(self.board)
        self.reporter = Reporter.Reporter(self.board)
        self.controller = Controller.Controller(self.board, self.reporter)
        self.visualizer = Visualizer.Visualizer(self.board, self.globals)
        self.simulator = Simulator.Simulator(self.board, self.controller, self.strategy)
        
        self.moved_this_tick = False
    
    def handleKeyBoardInput(self, event):
        key_to_direction = {
            pygame.K_UP: Direction.Direction.UP,
            pygame.K_DOWN: Direction.Direction.DOWN,
            pygame.K_LEFT: Direction.Direction.LEFT,
            pygame.K_RIGHT: Direction.Direction.RIGHT,
        }

        if (event.key == pygame.K_SPACE):
            self.simulator.continuously_simulating = not self.simulator.continuously_simulating
            return 

        if (not self.simulator.continuously_simulating and event.key == pygame.K_o):
            self.moved_this_tick = self.simulator.simulate_one_move()
            return

        if (event.key in key_to_direction):
            self.moved_this_tick = self.controller.move(key_to_direction[event.key])

    def tick_handler(self):
        if (self.globals.GAME_OVER):
            return
        if (self.simulator.continuously_simulating):
            self.moved_this_tick = self.simulator.simulate_one_move()
        if (self.moved_this_tick):
            self.board.fillEmptySquares(1)
            self.reporter.print_board()
        if (self.board.noAvailableMoves()):
            self.globals.GAME_OVER = True
        self.moved_this_tick = False
        self.visualizer.draw()
        display.flip()
        