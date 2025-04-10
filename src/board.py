# board.py:
# Author: 

import pygame
from typing import List, Tuple, Optional

DIMENSIONS: int = 6

class Board:
    SCALE_MODIFIER: float = 0.80
    WHITE: Tuple[int, int, int] = (240, 217, 181)
    BLACK: Tuple[int, int, int] = (181, 136, 99)

    screen_xy: Tuple[int, int] = (0, 0)
    margin_xy: Tuple[float, float] = (0, 0)

    # __init__(): Constructor, sets up board info using the passed screen
    def __init__(self, screen) -> None:
        self.screen = screen # Temporary
        self.updateScreenInfo(screen)
        self.squares: List[List[Square]] = []
        self.draw()

    # updateScreenInfo(): Update the screen size and margins
    def updateScreenInfo(self, screen) -> None:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        self.board_size: float = min(screen_width, screen_height) * self.SCALE_MODIFIER
        self.square_size: float = self.board_size / 6
        margin_x: float = (screen_width - self.board_size) / 2
        margin_y: float = (screen_height - self.board_size) / 2

        Board.screen_xy = (screen_width, screen_height)
        Board.margin_xy = (margin_x, margin_y)

    # draw(): Determines where to place squares, and then creates them.
    def draw(self) -> None:
        for row in range(DIMENSIONS):
            square_row: List[Square] = []
            for col in range(DIMENSIONS):
                is_even = (row + col) % 2 == 0
                color = self.WHITE if is_even else self.BLACK
                new_square: Square = Square(self.square_size, row, col, color)
                self.initializePiece(new_square, row, col)
                square_row.append(new_square)
        
            self.squares.append(square_row)

        pygame.display.flip()

    # getSquareAt(): Get a reference to the square underneath the current mouse_pos
    def getSquareAt(self, mouse_pos_xy: Tuple[float, float]) -> 'Square':
        row = int((mouse_pos_xy[1] - Board.margin_xy[1]) // self.square_size)
        col = int((mouse_pos_xy[0] - Board.margin_xy[0]) // self.square_size)

        is_in_boundaries: bool = (0 <= row < DIMENSIONS) and (0 <= col < DIMENSIONS)
        if is_in_boundaries:
            return self.squares[row][col]
        
        return None

    # initializePiece(): Initializes pieces in their default positions
    def initializePiece(self, square: 'Square', row: int, col: int):
        if 2 <= row <= 3:
            return # No pieces in the middle two rows
        
        color = 'b' if row < 2 else 'w'
        piece_type = None

        # Temporary way of selecting piece types
        if row == 1 or row == 4:
            piece_type = "pawn"
        else:
            if col == 0 or col == 5:
                piece_type = "rook"
            if col == 1 or col == 4:
                piece_type = "knight"
            if col == 2:
                piece_type = "queen"
            if col == 3:
                piece_type = "king"

        square.piece = Piece(color, piece_type, self.screen, square)

class Square:
    # __init__(): Constructor
    def __init__(self, size, row: int, col: int, color) -> None:
        self.row: int = row
        self.col: int = col
        self.size = size
        self.color: Tuple[int, int, int] = color
        self.piece: Optional[Piece] = None
        self.is_selected: bool = False
        
        self.draw(color)
        
    # draw(): Draws a single square to the screen at the specified coordinates
    def draw(self, color) -> None:
        pos_xy = self.getPosition()

        pygame.draw.rect(pygame.display.get_surface(), color, (pos_xy[0], pos_xy[1], self.size, self.size))
        if self.piece is not None:
            self.piece.draw()

    # getPosition(): Returns the x, y position of this square
    #                I would like to move this logic and just *store* an x, y value
    def getPosition(self) -> Tuple[float, float]:
        margin_xy = Board.margin_xy
        x = self.size * self.col + margin_xy[0]
        y = self.size * self.row + margin_xy[1]
        return (x, y)
    
    # select(): Highlight this square
    def select():
        pass

    # unselect(): Unhighlight this square
    def unselect():
        pass

class Piece:
    SCALE_MODIFIER = 0.8

    # __init__(): 
    def __init__(self, color, type, screen, square) -> None:
        self.parent: 'Square' = square
        self.color: Tuple[int, int, int] = color
        self.type = type
        self.sprite = None
        self.loadSprite()
        self.draw(screen)

    # draw(): 
    def draw(self, screen) -> None:
        if self.type is None or self.sprite is None:
            return
    
        margin_xy = Board.margin_xy
        square_pos = self.parent.getPosition()
        square_size = self.parent.size

        piece_x = square_pos[0] + (square_size - self.sprite.get_width()) / 2
        piece_y = square_pos[1] + (square_size - self.sprite.get_height()) / 2
        screen.blit(self.sprite, (piece_x, piece_y))

    # loadSprite(): Loads a sprite to represent this Piece
    def loadSprite(self) -> None:
        if self.type is None:
            return

        try:
            path = f'assets/{self.color}_{self.type}.png' # Temporary
            new_sprite = pygame.image.load(path).convert_alpha()

            scale_size = int(self.parent.size * self.SCALE_MODIFIER)
            self.sprite = pygame.transform.scale(new_sprite, (scale_size, scale_size))

        except pygame.error as err:
            print(f"Error loading image for {self.color}, {self.type}: {err}")