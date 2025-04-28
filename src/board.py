# board.py:
# Author: Julien Devol

import pygame
from typing import List, Tuple, Optional

DIMENSIONS: int = 6
pygame.font.init()
arial = pygame.font.SysFont('Times New Roman', 32, bold = True)

class Board:
    SCALE_MODIFIER: float = 0.80
    WHITE: Tuple[int, int, int] = (240, 217, 181)
    BLACK: Tuple[int, int, int] = (181, 136, 99)

    screen_xy: Tuple[int, int] = (0, 0)
    turn: int = 1

    # __init__(): Constructor, sets up board info using the passed screen
    def __init__(self, screen, camera) -> None:
        self.screen = screen
        self.camera = camera
        self.squares: List[List[Square]] = []

        self.board_size: float = min(self.camera.getWidth(), self.camera.getHeight()) * self.SCALE_MODIFIER
        self.square_size: float = self.board_size / 6
        Board.screen_xy = (self.camera.getWidth(), self.camera.getHeight())

        self.initSquares()
        self.draw(camera)

    # initSquares(): Initializes every square's values and its position in the board
    def initSquares(self) -> None:
        for row in range(DIMENSIONS):
            square_row: List[Square] = []
            for col in range(DIMENSIONS):
                is_even = (row + col) % 2 == 0
                color = self.WHITE if is_even else self.BLACK
                new_square: Square = Square(row, col, self.square_size, color)
                self.initializePiece(new_square, row, col)
                square_row.append(new_square)
        
            self.squares.append(square_row)

    # draw(): Draws the board by calling draw on each square
    #         TODO: Preferably, in the future, render the board as a single .png.
    #               Calling draw on every square every frame is pretty dumb.
    def draw(self, camera) -> None:
        for row in range(len(self.squares)):
            for col in range(len(self.squares[row])):
                self.squares[row][col].draw(camera.getScreen(), camera.getX(), camera.getY())

        text_surface = arial.render(f'Turn {Board.turn}', False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = camera.getWidth() / 2
        text_rect.top = camera.getHeight() / 24

        camera.getScreen().blit(text_surface, text_rect)

    # getSquareAt(): Get a reference to the square underneath the current mouse_pos
    #                TODO: Change the way this is calculated now that Squares have (x,y) coords
    def getSquareAt(self, mouse_pos_xy: Tuple[float, float]) -> 'Square':
        row = int((mouse_pos_xy[1] - self.camera.getY()) // self.square_size)
        col = int((mouse_pos_xy[0] - self.camera.getX()) // self.square_size)

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
    current_selected: 'Square' = None # Currently selected piece
    highlighted: List['Square'] = [] # Currently highlighted squares

    # __init__(): Constructor
    def __init__(self, row: int, col: int, size, color) -> None:
        self.x: float = 0
        self.y: float = 0
        self.size = size
        self.row: int = row
        self.col: int = col
        self.color: Tuple[int, int, int] = color
        self.base_color: Tuple[int, int, int] = color
        self.highlighted_color: Tuple[int, int, int] = color
        self.piece: Optional[Piece] = None
        self.is_highlighted: bool = False
        
        self.updatePosition()

    def highlight(self):
        self.is_highlighted = True
        if self.piece is None:
            self.color = (144, 238, 144)
        else:
            self.color = (255, 128, 128)

        Square.highlighted.append(self)

    def unhighlight(self):
        self.is_highlighted = False
        self.color = self.base_color

    @staticmethod
    def unhighlight_all(self):
        for square in Square.highlighted:
            square.unhighlight()
        Square.highlighted.clear()
        
    # draw(): Draws a square to the screen at the specified coordinates
    def draw(self, screen, cam_x = 0, cam_y = 0) -> None:
        offset_x = self.x + cam_x
        offset_y = self.y + cam_y

        pygame.draw.rect(screen, self.color, (offset_x, offset_y, self.size, self.size))
        if self.piece is not None:
            self.piece.draw(screen, cam_x, cam_y)

    # setPiece()
    def setPiece(self, piece: Optional["Piece"]) -> None:
        self.piece = piece
        self.draw()

    # getPiece()
    def getPiece(self):
        return self.piece

    # updatePosition(): Updates the x, y position of this square
    def updatePosition(self) -> None:
        self.x = self.size * self.col
        self.y = self.size * self.row
    
    # select(): Select this square
    def select(self):
        if Square.current_selected == self:
            self.unselect() # Unselect yourself if selected twice
            return
        
        if Square.current_selected is None:
            if self.piece is not None:
                Square.current_selected = self
            return
        
        if Square.current_selected.piece is None:
            self.unselect()
            return
            
        from_piece = Square.current_selected.piece
        to_piece = self.piece

        # TODO: Preferably clean this up at some point, it's a bit boilerplate right now
        if from_piece is not None and to_piece is not None:
            if from_piece.color != to_piece.color:
                # Capture to_piece with from_piece
                self.piece = from_piece
                from_piece.parent = self
                Square.current_selected.piece = None
            else:
                # Swap with same-color piece
                Square.current_selected.piece = to_piece
                self.piece = from_piece

                from_piece.parent = self
                to_piece.parent = Square.current_selected

        else:
            # Swap with an empty square
            Square.current_selected.piece = to_piece
            self.piece = from_piece

            if from_piece is not None:
                from_piece.parent = self
            if to_piece is not None:
                to_piece.parent = Square.current_selected

        self.unselect()
        Board.turn += 1
        print(Board.turn)

    # unselect(): Unselect this square
    def unselect(self):
        Square.current_selected = None

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
    def draw(self, screen, cam_x = 0, cam_y = 0) -> None:
        if self.type is None or self.sprite is None:
            return
    
        square_size = self.parent.size

        piece_x = self.parent.x + (square_size - self.sprite.get_width()) / 2
        piece_y = self.parent.y + (square_size - self.sprite.get_height()) / 2

        offset_x = piece_x + cam_x
        offset_y = piece_y + cam_y

        screen.blit(self.sprite, (offset_x, offset_y))

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

class Pawn(Piece):
    def getType(self) -> str:
        return "pawn"
    
    def isValidMove(self, from_square: 'Square', to_square: 'Square') -> bool:
        pass