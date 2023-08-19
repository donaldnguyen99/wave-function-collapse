import pygame
import os
import game
import random

def main():
    # Initialize
    pygame.init()

    # Set up display and clock
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pygame.time.Clock()

    # Set up game objects
    wave_func_col = game.Game(screen)

    # Event loop
    quit_status = False
    while not quit_status:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_status = True
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_status = True
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    print("Space pressed")
                    for i in range(10):
                        wave_func_col.draw()

        # Update display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()