class Reporter:
    def __init__(self, board):
        self.board = board
        self.reportingdata = []
    
    def print_board(self):
        print("Current Board State:")
        for i in range(self.board.vars.BOARD_ROWS):
            row = self.board.boardList[i*self.board.vars.BOARD_COLS:(i+1)*self.board.vars.BOARD_COLS]
            print(row)

    def collect_data(self, simulator):
        self.reportingdata = [
            simulator.gameNum,
            simulator.moveNum,
            simulator.deltaTime,
            simulator.predHeuristic,
            simulator.currHeuristic,
            simulator.lookahead
        ]
    
    #write data in datatable into eachGame.txt
    def output_eachGame_data(self, datatable):
        print("outputting data")
        with open("eachGame.txt", "w") as f:
            print("Game Number,Move Number,Time Taken, Predicted Heuristic, Current Heuristic, Lookahead", file=f)
            for gameNum in datatable.keys():
                for moveNum in datatable[gameNum].keys():
                    deltaTime, pHeuristic, cHeuristic, lookahead = tuple(datatable[gameNum][moveNum])
                    print(f"{gameNum},{moveNum},{deltaTime},{pHeuristic},{cHeuristic},{lookahead}", file=f)

    def report_on_move(self, direction):
        print(f"Moved {direction}")

    def report_input_info(self, direction):
        print(f"Moved {direction}")
