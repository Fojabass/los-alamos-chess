# main.py:
# Author: Julien Devol

import pygame
from src.board import Board

def main():
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    delta = 0

    pygame.display.set_caption("Los Alamos Chess")
    board = Board(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        board.draw()
        delta = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main() # Only execute main() if this file is run directly
    

    




    


