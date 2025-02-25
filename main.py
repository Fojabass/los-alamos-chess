SIZE: int = 6
board = [[0] * SIZE] * SIZE

class Piece(Enum):
    Null = 0,
    Pawn = 1,
    Rook = 2,
    Knight = 3,
    King = 4,
    Queen = 5

def main():
    initialize_board()
    print(board)

def initialize_board():
    for i in range(SIZE):
        main_piece: int = Piece(((i + 1) % 4))
        board[0][i] = main_piece
        board[1][i] = Piece.Pawn
        board[5][i] = Piece.Pawn
        board[6][i] = main_piece

    


    

    




    


