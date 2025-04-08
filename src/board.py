# board.py:
# Author: Julien Devol

import pygame
from typing import List, Tuple, Optional

# The logic so far moves from Board -> Square -> Piece.
# Board handles the high-level logic, Square handles individual cell behavior, and Piece defines how 

class Board:
    DIMENSIONS: int = 6
    SCALE_MODIFIER: float = 0.80
    WHITE: Tuple[int, int, int] = (240, 217, 181)
    BLACK: Tuple[int, int, int] = (181, 136, 99)

    # __init__(): Constructor, sets up board info using the passed screen dimensions
    def __init__(self, screen):
        screen_width: int = screen.get_width()
        screen_height: int = screen.get_height()

        self.board_size: float = min(screen_width, screen_height) * self.SCALE_MODIFIER
        self.cell_size: float = self.board_size / 6
        self.margin_x: float = (screen_width - self.board_size) / 2
        self.margin_y: float = (screen_height - self.board_size) / 2

        self.squares: List[List[Square]] = []
        self.draw()

    # draw(): Determines where to place squares, and then creates them.
    def draw(self):
        for row in range(self.DIMENSIONS):
            square_row: List[Square] = []
            for col in range(self.DIMENSIONS):
                is_even = (row + col) % 2 == 0
                color = self.WHITE if is_even else self.BLACK
                new_square: Square = Square(row, col, color)
                square_row.append(new_square)
                # We probably want to initialize each Square with its proper Piece here.
                # e.g rename this function to "init_squares"
                # Maybe we pass squares an "anchor coordinate"? They can use row & col to calculate where to place themselves based on that

            self.squares.append(square_row)

        pygame.display.flip()

class Square:
    # __init__(): Constructor
    def __init__(self, row: int, col: int, color):
        self.row: int = row
        self.col: int = col
        self.color: Tuple[int, int, int] = color
        self.piece: Optional[Piece] = None
        self.is_selected: bool = False
        # Call the square's draw function here
        
    # draw(): Draws a single square to the screen at the specified coordinates
    def draw(self, screen, x: int, y: int, size: float):
        pygame.draw.rect(screen, self.color, (x, y, size, size))
        # Check if this square has a piece. If so, call that piece's draw function

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.type = None
        self.sprite = None

    def draw(self, screen):
        try:
            path = f'assets/{self.color}_king.png' # Temporary
            self.sprite = pygame.image.load(path).convert_alpha()
            screen.blit(self.sprite,(0,0))
        except pygame.error as err:
            print(f"Error loading image. {err}")