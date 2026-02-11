import pygame

class Visualizer:
    def __init__(self, board, globals):
        self.vars = globals
        self.board = board
    
    #draws the board to the screen of the 2048 Game
    def draw(self):
        self.vars.screen.fill(self.vars.BACKGROUND_COLOR)
        for row in range(self.vars.BOARD_ROWS):
            for col in range(self.vars.BOARD_COLS):
                value = self.board.boardList[self.board.index2D_to_1D(row, col)]
                if value != 0:
                    pygame.draw.rect(self.vars.screen, self.vars.TILE_COLORS[2**value], self.getTileRect(row, col))
                    self.drawTileValue(2**value, row, col)
        pygame.display.flip()
    
    def drawTileValue(self, value, row, col):
        font = pygame.font.SysFont(self.vars.FONT_NAME, self.vars.FONT_SIZE)
        text = font.render(str(value), True, self.vars.FONT_COLOR)
        text_rect = text.get_rect(center=self.getTileRect(row, col).center)
        self.vars.screen.blit(text, text_rect)

    def getTileRect(self, row, col):
        x = self.vars.BOARD_PADDING + col * (self.vars.TILE_SIZE + self.vars.BOARD_PADDING)
        y = self.vars.BOARD_PADDING + row * (self.vars.TILE_SIZE + self.vars.BOARD_PADDING)
        return pygame.Rect(x, y, self.vars.TILE_SIZE, self.vars.TILE_SIZE)
        