# main.py:
# Author: Julien Devol

import pygame
from src.camera import Camera
from src.board import Board

def main():
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running: bool = True
    delta: float = 0

    pygame.display.set_caption("Los Alamos Chess")
    camera = Camera(screen)
    board = Board(screen, camera)

    camera.position[0] = (SCREEN_WIDTH / 2) - (board.board_size / 2)
    camera.position[1] = (SCREEN_HEIGHT / 2) - (board.board_size / 2)
    
    while running:
        screen.fill((0, 0, 0)) # Clear the last frame

        for event in pygame.event.get():
            match(event.type):
                case pygame.QUIT:
                    running = False

                case pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_square = board.getSquareAt(pos)
                    if clicked_square:
                        clicked_square.select()

        keys = pygame.key.get_pressed()
        dir_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dir_y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        delta = clock.tick(60) / 1000
        camera.move(dir_x, dir_y, delta)
        board.draw(camera)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main() # Only execute main() if this file is run directly
    

    




    


