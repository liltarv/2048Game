import pygame
from pygame import draw, display

# Initialize pygame
pygame.init()

# Game clock for FPS control
clock = pygame.time.Clock()
FPS = 60

#init Game
game = Game()


#update display
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # ✅ handles close button 
            running = False
    

    display.flip()


pygame.quit()