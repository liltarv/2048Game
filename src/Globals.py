import pygame

class Globals:
    def __init__(self):
        self.BOARD_ROWS = 4
        self.BOARD_COLS = 4
        self.WINDOW_RES_X = 500
        self.WINDOW_RES_Y = 500
        self.screen = pygame.display.set_mode((self.WINDOW_RES_X, self.WINDOW_RES_Y))
        self.BACKGROUND_COLOR = (187, 173, 160)
        self.TILE_COLORS = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
            4096: (60, 58, 50),
            8192: (60, 58, 50),
        }
        self.FONT_NAME = 'Arial'
        self.FONT_SIZE = 40
        self.FONT_COLOR = (119, 110, 101)
        self.BOARD_PADDING = 10
        self.TILE_SIZE = (self.WINDOW_RES_X - (self.BOARD_COLS + 1) * self.BOARD_PADDING) // self.BOARD_COLS 
        self.GAME_OVER = False
        self.GAME_OVER_FONT_SIZE = 80
        self.GAME_OVER_FONT_COLOR = (255, 0, 0)   
