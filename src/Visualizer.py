class Visualizer:
    def __init__(self, board, globals):
        self.vars = globals
        self.board = board
    
    #draws the board to the screen of the 2048 Game
    #def draw(self):
    #    self.vars.screen.fill(self.vars.BACKGROUND_COLOR)
    #    for row in range(self.vars.BOARD_ROWS):
    #        for col in range(self.vars.BOARD_COLS):
    #            value = self.board.boardList[self.board.index2D_to_1D(row, col)]
    #            if value != 0:
    #                pygame.draw.rect(self.vars.screen, self.vars.TILE_COLORS[value], self.getTileRect(row, col))
    #                self.drawTileValue(value, row, col)
    #    pygame.display.flip()
        