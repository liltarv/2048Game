import cProfile
import re
import copy
import Visualizer
import pygame
import Board
import Controller


class Science:
    def __init__(self, board):
        self.board = board
        

    def run(self, num_iterations, visualize=True):
        for i in range(num_iterations):
            self.board = Board.Board(self.board.vars)
            controller = Controller.Controller(self.board, None)
            visualizer = Visualizer.Visualizer(self.board, self.board.vars)
            simulator = Simulator.Simulator(self.board, self.controller, self.strategy)
            while (not self.simulator.board.noAvailableMoves()):
                moved = self.simulator.simulate_one_move()
                print(moved)
                if moved:
                    self.simulator.board.fillEmptySquares(1)
                if visualize:
                    self.visualizer.draw()
                    pygame.display.flip()

            print("reset")

    def profile(self, num_iterations):
        pr = cProfile.Profile()
        pr.enable()
        self.run(num_iterations, visualize=True)
        pr.disable()
        pr.print_stats(sort='time')
