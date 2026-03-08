import cProfile
import re
import copy
import Visualizer
import pygame
import Board
import Controller
import Simulator
import Controller
import Strategy
from collections import defaultdict


class Science:
    def __init__(self, board, reporter):
        self.board = board
        self.reporter = reporter
        #of the form: datatable[gameNum][moveNum] = [other data]
        self.datatable = defaultdict(lambda : defaultdict(list))
        self.aggregate_datatable = defaultdict(lambda : list)
        self.runningCalculationData = [
            0
        ]

    def run(self, num_iterations, visualize=True):
        for i in range(num_iterations):
            self.run_one_iteration(i+1, visualize)
            reportingdata = self.reporter.reportingdata.copy()
            gameNum = reportingdata.pop(0)
            self.aggregate_datatable[gameNum] = reportingdata
            self.aggregate_datatable[gameNum][6] = self.runningCalculationData[0] / reportingdata[0]
            print(i)
        self.reporter.output_eachGame_data(self.datatable)
        self.reporter.output_aggregate_data(self.aggregate_datatable)
        #print(self.datatable)
        #self.reporter.output_sumGames_data(datatable)

    #def fillAverageGame(self):
        #take the average values among all games for each entry

        
    
    def run_one_iteration(self, gameNum, visualize=True):
        self.board = Board.Board(self.board.vars)
        controller = Controller.Controller(self.board, None)
        if visualize: 
            visualizer = Visualizer.Visualizer(self.board, self.board.vars)
        strategy = Strategy.Strategy(self.board)
        simulator = Simulator.Simulator(self.board, controller, strategy, self.reporter)
        simulator.gameNum = gameNum
        self.runningCalculationData[0] = 0
        while (not simulator.board.noAvailableMoves()):
            moved = simulator.simulate_one_move()
            reportingdata = self.reporter.reportingdata.copy()
            gameNum = reportingdata.pop(0)
            moveNum = reportingdata.pop(0)
            self.runningCalculationData[0] += reportingdata[5]
            self.datatable[gameNum][moveNum] = reportingdata
            if visualize:
                visualizer.draw()
                pygame.display.flip()


    def profile(self, num_iterations, visualize):
        pr = cProfile.Profile()
        pr.enable()
        self.run(num_iterations, visualize)
        pr.disable()
        pr.print_stats(sort='time')
