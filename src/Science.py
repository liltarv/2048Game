import cProfile
import re
import copy
import Visualizer
import pygame
import Board

class Science:
    def __init__(self, simulator):
        self.simulator = simulator
        self.initSimulator = copy.copy(simulator)
        self.visualizer = Visualizer.Visualizer(self.simulator.board, self.simulator.board.vars)
        self.oldBoard = Board.Board()

    def run(self, num_iterations, visualize=True):
        for i in range(num_iterations):
            while (not self.simulator.board.noAvailableMoves()):
                moved = self.simulator.simulate_one_move()
                if moved:
                    self.simulator.board.fillEmptySquares(1)
                if visualize:
                    self.visualizer.draw()
                    pygame.display.flip()
            
            #reset game vars
            self.simulator = copy.copy(self.initSimulator)
            self.simulator.board = copy.deepcopy(self.oldBoard)
            self.visualizer.board = self.simulator.board
            print("reset")

    def profile(self, num_iterations):
        pr = cProfile.Profile()
        pr.enable()
        self.run(num_iterations, visualize=True)
        pr.disable()
        pr.print_stats(sort='time')
