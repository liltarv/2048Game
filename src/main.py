import pygame
import Game
from pygame import draw, display

# Initialize pygame
pygame.init()

# Game clock for FPS control
clock = pygame.time.Clock()
FPS = 60

#init Game
game = Game.Game()


#update display
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
        elif event.type == pygame.KEYDOWN:  
            game.handleKeyBoardInput(event)
            
    game.visualizer.draw()
    game.reporter.report()

    display.flip()

'''
Traceback (most recent call last):
  File "/workspaces/2048Game/src/main.py", line 25, in <module>
    game.handleKeyBoardInput(event)
  File "/workspaces/2048Game/src/Game.py", line 19, in handleKeyBoardInput
    event.key.UP: self.globals.DIRECTION_UP
'''

pygame.quit()