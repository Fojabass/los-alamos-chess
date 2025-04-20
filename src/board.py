# board.py:
# Author: Julien Devol

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
                new_square: Square = Square(row, col, self.square_size, color)
                self.initializePiece(new_square, row, col)
                square_row.append(new_square)
        
            self.squares.append(square_row)
            Board.update_display()

    # update_display(): Refreshes the display to show changes
    def update_display() -> None:
        pygame.display.flip()

    # getSquareAt(): Get a reference to the square underneath the current mouse_pos
    #                TODO: Change the way this is calculated now that Squares have (x,y) coords
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
    current_selected: 'Square' = None # The currently selected piece

    # __init__(): Constructor
    def __init__(self, row: int, col: int, size, color) -> None:
        self.x: float = 0
        self.y: float = 0
        self.size = size
        self.row: int = row
        self.col: int = col
        self.color: Tuple[int, int, int] = color
        self.piece: Optional[Piece] = None
        
        self.updatePosition()
        self.draw()
        
    # draw(): Draws a square to the screen at the specified coordinates
    def draw(self) -> None:
        screen = pygame.display.get_surface()

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        if self.piece is not None:
            self.piece.draw(screen)

    # setPiece()
    def setPiece(self, piece: Optional["Piece"]) -> None:
        self.piece = piece
        self.draw()

    # getPiece()
    def getPiece(self):
        return self.piece

    # updatePosition(): Updates the x, y position of this square
    def updatePosition(self) -> None:
        self.x = self.size * self.col + Board.margin_xy[0]
        self.y = self.size * self.row + Board.margin_xy[1]
    
    # select(): Select this square
    def select(self):
        if Square.current_selected == self:
                self.unselect() # Unselect yourself if selected twice
                return
        
        if Square.current_selected is None:
            if self.piece is not None:
                Square.current_selected = self
        else:
            moving_piece = Square.current_selected.piece
            target_piece = self.piece
            
            Square.current_selected.piece = target_piece
            self.piece = moving_piece

            if moving_piece is not None:
                moving_piece.parent = self
            if target_piece is not None:
                target_piece.parent = Square.current_selected

            Square.current_selected.draw()
            self.draw()

            print("A swap has occurred.")
            self.unselect()

        Board.update_display()

    # unselect(): Unselect this square
    def unselect(self):
        Square.current_selected = None
        print(f"Square at ({self.row} {self.col}) has been unselected.")

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
    
        square_size = self.parent.size

        piece_x = self.parent.x + (square_size - self.sprite.get_width()) / 2
        piece_y = self.parent.y + (square_size - self.sprite.get_height()) / 2
        screen.blit(self.sprite, (piece_x, piece_y))

    # loadSprite(): Loads a sprite to represent this Piece
    def loadSprite(self) -> None:
        if self.type is None:
            return

        try:
            path = f'assets/{self.color}_{self.type}.png'
            new_sprite = pygame.image.load(path).convert_alpha()

            scale_size = int(self.parent.size * self.SCALE_MODIFIER)
            self.sprite = pygame.transform.scale(new_sprite, (scale_size, scale_size))

        except pygame.error as err:
            print(f"Error loading image for {self.color}, {self.type}: {err}")