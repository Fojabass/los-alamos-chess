# game.py: Defines all game interactions, such as the board, its squares, its pieces, and how these pieces are defined.
# Author: Julien Devol

import pygame
from typing import List, Tuple, Optional

DIMENSIONS: int = 6
pygame.font.init()
game_font = pygame.font.SysFont('Times New Roman', 32, bold = True)

class Board:
	SCALE_MODIFIER: float = 0.80
	WHITE: Tuple[int, int, int] = (240, 217, 181)
	BLACK: Tuple[int, int, int] = (181, 136, 99)

	turn: int = 1
	game_over: bool = False
	winner: str = None

	# __init__(): Constructor, sets up board info using the passed screen
	def __init__(self, screen, camera) -> None:
		self.screen = screen
		self.camera = camera
		self.squares: List[List[Square]] = []
		self.move_history: List[Move] = []
		self.current_history_index: int = -1
		Board.game_over = False
		Board.winner = None
		Board.turn = 1

		self.board_size: float = min(self.camera.getWidth(), self.camera.getHeight()) * self.SCALE_MODIFIER
		self.square_size: float = self.board_size / 6

		self.initSquares()
		self.draw(camera)
		
	# makeMove(): Adds a move to history and executes it
	def makeMove(self, move: 'Move') -> None:
		if Board.game_over:
			return # Don't allow moves if the game is over!
		
		# If you aren't at the end of your move history, remove all future moves since you're currently changing that history
		if self.current_history_index < len(self.move_history) - 1:
			self.move_history = self.move_history[:self.current_history_index + 1]
			
		self.move_history.append(move)
		self.current_history_index = len(self.move_history) - 1
		move.execute()
		
	# undoMove(): Goes back one move in the history
	def undoMove(self) -> None:
		if self.current_history_index >= 0:
			# If game was over (a king was captured), set it back to active
			Board.game_over = False
			Board.winner = None
			
			self.move_history[self.current_history_index].undo()
			self.current_history_index -= 1
			
	# redoMove(): Goes forward one move in the history
	def redoMove(self) -> None:
		if self.current_history_index < len(self.move_history) - 1:
			self.current_history_index += 1
			self.move_history[self.current_history_index].execute()
			
			# Make sure to check if this redo resulted in a king capture
			move = self.move_history[self.current_history_index]
			if move.captured_piece is not None and move.captured_piece.type == "king":
				winner = "White" if move.captured_piece.color == 'b' else "Black"
				self.endGame(winner)
			
	# endGame(): Ends the game and declares a winner!
	def endGame(self, winner: str) -> None:
		Board.game_over = True
		Board.winner = winner
		
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

	# draw(): Draws the squares that compose the board and the upper UI.
	def draw(self, camera) -> None:
		for row in range(len(self.squares)):
			for col in range(len(self.squares[row])):
				self.squares[row][col].draw(camera.getScreen(), camera.getX(), camera.getY())

		if Board.game_over:
			message = f"Game Over. {Board.winner} wins!"
			text_color = (255, 215, 0) # Gold
		else:
			# Determine current player based on turn #
			current_player = "White" if Board.turn % 2 == 1 else "Black"
			message = f'Turn {Board.turn} - {current_player}\'s Turn'
			text_color = (255, 255, 255) # White
			
		text_surface = game_font.render(message, False, text_color)
		text_rect = text_surface.get_rect()
		text_rect.centerx = camera.getWidth() / 2
		text_rect.top = camera.getHeight() / 24

		camera.getScreen().blit(text_surface, text_rect)

	# getSquareAt(): Get a reference to the square underneath the current mouse_pos_xy.
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

		# Determine piece type based on position
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

		# Create piece using the factory method
		if piece_type:
			square.piece = Piece.createPiece(color, piece_type, self.screen, square)


class Square:
	current_selected: 'Square' = None # Currently selected piece
	highlighted: List['Square'] = [] # Currently highlighted squares
	HIGHLIGHT_EMPTY: Tuple[int, int, int] = (144, 238, 144)  # Light green
	HIGHLIGHT_CAPTURE: Tuple[int, int, int] = (255, 128, 128)  # Light red
	HIGHLIGHT_SELECTED: Tuple[int, int, int] = (100, 149, 237)  # Cornflower blue

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
		self.is_selected: bool = False
		
		self.updatePosition()

	# highlight(): Highlight this square as a potential move
	def highlight(self):
		self.is_highlighted = True
		# Change the square's background color slightly
		if self.piece is None:
			# For empty squares - light green tint
			r, g, b = self.base_color
			self.color = (r * 0.8 + 50, g * 0.8 + 50, b * 0.8)
		else:
			# For capture squares - light red tint
			r, g, b = self.base_color
			self.color = (r * 0.8 + 50, g * 0.8, b * 0.8)

		Square.highlighted.append(self)

	# unhighlight(): Remove move highlighting from this square
	def unhighlight(self):
		self.is_highlighted = False
		if not self.is_selected:
			self.color = self.base_color

	# select_highlight(): Highlight this square as the selected piece
	def select_highlight(self):
		self.is_selected = True
		r, g, b = self.base_color
		self.color = (r * 0.6 + 40, g * 0.6 + 60, b * 0.6 + 90)  # Give it a bluish tint
		
	# unselect_highlight(): Removes the selected piece's highlighting
	def unselect_highlight(self):
		self.is_selected = False
		self.color = self.base_color # Reset the color

	# unhighlight_all(): Static method to unhighlight all highlighted squares
	@staticmethod
	def unhighlight_all():
		for square in Square.highlighted:
			square.unhighlight()
		Square.highlighted.clear()
		
	# draw(): Draws a square to the screen at the specified coordinates
	def draw(self, screen, cam_x = 0, cam_y = 0) -> None:
		offset_x = self.x + cam_x
		offset_y = self.y + cam_y

		pygame.draw.rect(screen, self.color, (offset_x, offset_y, self.size, self.size))
		
		# If this square is highlighted, draw a circle at the center
		if self.is_highlighted:
			circle_radius = self.size * 0.15
			circle_x = offset_x + self.size / 2
			circle_y = offset_y + self.size / 2
			
			if self.piece is None:
				circle_color = (50, 150, 50)  # Darker green circle for empty squares
			else:
				circle_color = (150, 50, 50)  # Darker red circle for capturable squares
				
			pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)
		
		# If this is the selected square, draw a thicker border!
		if self.is_selected:
			border_rect = pygame.Rect(offset_x, offset_y, self.size, self.size)
			pygame.draw.rect(screen, self.HIGHLIGHT_SELECTED, border_rect, 4)
			
		# Draw the piece on this square, if there is one
		if self.piece is not None:
			self.piece.draw(screen, cam_x, cam_y)

	# setPiece(): Set the piece on this square
	def setPiece(self, piece: Optional["Piece"]) -> None:
		self.piece = piece
		self.draw()

	# getPiece(): Return the piece on this square
	def getPiece(self):
		return self.piece

	# updatePosition(): Updates the x, y position of this square
	def updatePosition(self) -> None:
		self.x = self.size * self.col
		self.y = self.size * self.row
	
	# select(): Select this square
	def select(self, board):
		if Board.game_over:
			return # If the game is over, don't bother selecting anything.
		
		current_color = 'w' if Board.turn % 2 == 1 else 'b'
		
		# Unselect if clicked twice
		if Square.current_selected == self:
			self.unselect_highlight()
			self.unselect()
			Square.unhighlight_all()
			return
		
		# Clear previous selection and its highlighted squares
		if Square.current_selected is not None:
			Square.current_selected.unselect_highlight()
		
		# If no square is selected yet and this square has a piece of the current player's color
		if Square.current_selected is None:
			if self.piece is not None and self.piece.color == current_color:
				Square.current_selected = self
				self.select_highlight()
				self.show_legal_moves(board)
			return
		
		# If the selected square has no piece, unselect
		if Square.current_selected.piece is None:
			Square.current_selected.unselect_highlight()
			self.unselect()
			Square.unhighlight_all()
			return
		
		if self not in Square.highlighted:
			return # Not a legal move!
		
		# The attempted move is legal, so create and execute it
		from_square = Square.current_selected
		to_square = self
		captured_piece = self.piece  # Store the potentially captured piece
		
		move = Move(from_square, to_square, captured_piece)
		board.makeMove(move)
		
		if captured_piece is not None and captured_piece.type == "king":
			winner = "White" if captured_piece.color == 'b' else "Black"
			board.endGame(winner)
		
		from_square.unselect_highlight()
		self.unselect()
		Square.unhighlight_all()

	# unselect(): Unselect this square
	def unselect(self):
		Square.current_selected = None
		
	# show_legal_moves(): Show legal moves for the piece on this square
	def show_legal_moves(self, board):
		if self.piece is None:
			return
			
		# Unhighlight any previously highlighted squares
		Square.unhighlight_all()
		
		# Get legal moves from the piece
		moves = self.piece.get_moves(self, board.squares)
		
		# Highlight each legal move
		for move in moves:
			move.highlight()


class Piece:
	SCALE_MODIFIER = 0.8

	# __init__(): Base constructor for all pieces
	def __init__(self, color, type, screen, square) -> None:
		self.parent: 'Square' = square
		self.color: str = color
		self.type = type
		self.sprite = None
		self.loadSprite()
		self.draw(screen)

	# draw(): Draw the piece on the screen
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
			
	# get_moves(): Base method to be overridden by each piece type
	def get_moves(self, square: 'Square', board: List[List['Square']]) -> List['Square']:
		return []  # Base class returns no moves by default
		
	# createPiece(): Factory method to create the appropriate piece type
	@staticmethod
	def createPiece(color: str, piece_type: str, screen, square: 'Square') -> 'Piece':
		if piece_type == "pawn":
			return Pawn(color, piece_type, screen, square)
		elif piece_type == "rook":
			return Rook(color, piece_type, screen, square)
		elif piece_type == "knight":
			return Knight(color, piece_type, screen, square)
		elif piece_type == "queen":
			return Queen(color, piece_type, screen, square)
		elif piece_type == "king":
			return King(color, piece_type, screen, square)
		else:
			return Piece(color, piece_type, screen, square)
		
class Move:
	# __init__(): Constructor
	def __init__(self, from_square: 'Square', to_square: 'Square', 
				 captured_piece: Optional['Piece'] = None) -> None:
		self.from_square = from_square
		self.to_square = to_square
		self.moved_piece = from_square.piece
		self.captured_piece = captured_piece
		self.turn_number = Board.turn

	# undo(): Reverts this move!
	def undo(self) -> None:
		# Move piece back to original square
		self.from_square.piece = self.moved_piece
		if self.moved_piece is not None:
			self.moved_piece.parent = self.from_square
		
		# Restore the captured piece (if any!)
		self.to_square.piece = self.captured_piece
		if self.captured_piece is not None:
			self.captured_piece.parent = self.to_square
		
		Board.turn = self.turn_number
		
	# execute(): Executes this move.
	def execute(self) -> None:
		# Store potentially captured piece
		self.captured_piece = self.to_square.piece
		
		# Move the piece to new square
		self.to_square.piece = self.moved_piece
		self.from_square.piece = None
		
		if self.moved_piece is not None:
			self.moved_piece.parent = self.to_square
		
		Board.turn += 1

class Pawn(Piece):
	# get_moves(): Returns all legal moves for this pawn.
	def get_moves(self, square: 'Square', board: List[List['Square']]) -> List['Square']:
		moves = []
		direction = -1 if self.color == 'w' else 1  # White moves up, black moves down
		
		# Forward move
		if 0 <= square.row + direction < DIMENSIONS:
			forward_square = board[square.row + direction][square.col]
			if forward_square.piece is None:
				moves.append(forward_square)
		
		# Diagonal captures
		for offset in [-1, 1]:
			if 0 <= square.row + direction < DIMENSIONS and 0 <= square.col + offset < DIMENSIONS:
				diagonal_square = board[square.row + direction][square.col + offset]
				if diagonal_square.piece and diagonal_square.piece.color != self.color:
					moves.append(diagonal_square)
		
		return moves


class Rook(Piece):
	# get_moves(): Returns all legal moves for this rook.
	def get_moves(self, square: 'Square', board: List[List['Square']]) -> List['Square']:
		moves = []
		directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, down, left, up
		
		for dr, dc in directions:
			r, c = square.row + dr, square.col + dc
			while 0 <= r < DIMENSIONS and 0 <= c < DIMENSIONS:
				target_square = board[r][c]
				if target_square.piece is None:
					moves.append(target_square)
				else:
					if target_square.piece.color != self.color:
						moves.append(target_square)
					break  # Stop in this direction after encountering a piece
				r += dr
				c += dc
		
		return moves


class Knight(Piece):
	# get_moves(): Returns all legal moves for this knight.
	def get_moves(self, square: 'Square', board: List[List['Square']]) -> List['Square']:
		moves = []

		offsets = [
			(-2, -1), (-2, 1), (-1, -2), (-1, 2),
			(1, -2), (1, 2), (2, -1), (2, 1)
		]
		
		for dr, dc in offsets:
			r, c = square.row + dr, square.col + dc
			if 0 <= r < DIMENSIONS and 0 <= c < DIMENSIONS:
				target_square = board[r][c]
				if target_square.piece is None or target_square.piece.color != self.color:
					moves.append(target_square)
		
		return moves


class Queen(Piece):
	# get_moves(): Returns all legal moves for this queen.
	def get_moves(self, square: 'Square', board: List[List['Square']]) -> List['Square']:
		moves = []

		diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
		straight_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
		
		for dr, dc in diagonal_directions + straight_directions:
			r, c = square.row + dr, square.col + dc
			while 0 <= r < DIMENSIONS and 0 <= c < DIMENSIONS:
				target_square = board[r][c]
				if target_square.piece is None:
					moves.append(target_square)
				else:
					if target_square.piece.color != self.color:
						moves.append(target_square)
					break  # Stop in this direction after encountering a piece
				r += dr
				c += dc
		
		return moves


class King(Piece):
	# get_moves(): Returns all legal moves for this king.
	def get_moves(self, square: 'Square', board: List[List['Square']]) -> List['Square']:
		moves = []
		offsets = [
			(-1, -1), (-1, 0), (-1, 1),
			(0, -1), (0, 1),
			(1, -1), (1, 0), (1, 1)
		]
		
		for dr, dc in offsets:
			r, c = square.row + dr, square.col + dc
			if 0 <= r < DIMENSIONS and 0 <= c < DIMENSIONS:
				target_square = board[r][c]
				if target_square.piece is None or target_square.piece.color != self.color:
					moves.append(target_square)
		
		return moves