import pygame
from chess_game_agent import ChessAgent

# Initialising the PyGame environment
pygame.init()


# Classes to create the Chess Pieces
class ChessPiece:
    def __init__(self, x, y, color):
        self.location = [x, y]  # The location of the chess piece (1-8)
        self.color = color  # Defining the color of the piece
        self.actions = []


class Pawn(ChessPiece):
    def __init__(self, x, y, color):
        super.__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/pawn.jpg" if self.color == "White" else "./images/pawnBlack.jpg"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        # Defining the actions a pawn can make
        # NOTE : En Passant isn't included within the initial actions
        self.actions = [[0, 1]]


class Rook(ChessPiece):
    def __init__(self, x, y, color):
        super.__init__(x, y, color)
        self.moved = False  # Used to check for possible castle
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/rook.jpg" if self.color == "White" else "./images/rookBlack.jpg"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        # Defining the actions a rook can make
        self.actions = (
            [[i, 0] for i in range(1, 8)]  # Right
            + [[0, i] for i in range(1, 8)]  # Up
            + [[-i, 0] for i in range(1, 8)]  # Left
            + [[0, -i] for i in range(1, 8)]  # Down
        )


class Knight(ChessPiece):
    def __init__(self, x, y, color):
        super.__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/knight.jpg"
            if self.color == "White"
            else "./images/knightBlack.jpg"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        # Defining the actions a rook can make
        self.actions = [
            [x, y] for x in [-2, -1, 1, 2] for y in [-2, -1, 1, 2] if abs(x) != abs(y)
        ]


class Bishop(ChessPiece):
    def __init__(self, x, y, color):
        super.__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/bishop.jpg" if self.color == "White" else "./images/pawnBlack.jpg"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        # Defining the actions a rook can make
        self.actions = (
            [[i, i] for i in range(1, 8)]  # Up and Right
            + [[i, -i] for i in range(1, 8)]  # Down and Right
            + [[-i, i] for i in range(1, 8)]  # Up and Left
            + [[-i, -i] for i in range(1, 8)]  # Down and Left
        )


class Queen(ChessPiece):
    def __init__(self, x, y, color):
        super.__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/queen.jpg" if self.color == "White" else "./images/pawnBlack.jpg"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        # Defining the actions a rook can make
        # The Queen's possible actions are the bishops and rooks added together
        self.actions = (
            [[i, i] for i in range(1, 8)]
            + [[i, -i] for i in range(1, 8)]
            + [[-i, i] for i in range(1, 8)]
            + [[-i, -i] for i in range(1, 8)]
            + [[i, 0] for i in range(1, 8)]
            + [[0, i] for i in range(1, 8)]
            + [[-i, 0] for i in range(1, 8)]
            + [[0, -i] for i in range(1, 8)]
        )


class King(ChessPiece):
    def __init__(self, x, y, color):
        super.__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/king.jpg" if self.color == "White" else "./images/kingBlack.jpg"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        self.moved = False  # Used to check for possible Castle
        # Defining the actions a rook can make
        self.actions = [
            [x, y] for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == 0 and y == 0)
        ]


# Defining the Chess Game Environment
class ChessGame:
    # Initialising variables within the environment
    def __init__(
        self,
        player1,
        player2,
        windowSize=640,
    ):
        # Defining the height and width of the game window
        self.windowSize = windowSize
        # Setting the height of the outputted display
        self.display = pygame.display.set_mode((self.windowSize, self.windowSize))
        pygame.display.set_caption("Chess Game")
        # Calculating the heights and widths of the board spaces
        self.blockSize = windowSize // 8
        # Initialising the players within the game
        self.player1 = player1
        self.player2 = player2
        # Initialising the state of the game
        self.reset()

    # Function to reset the environment
    def reset(self):
        # Creating the pieces for each player
        player1.chessPieces = []
        # Initialising whose turn it is to play
        self.playerTurn = player1

    # Function to process an action on the board, and call the function to perform the move
    def play_step(self, action):
        pass

    # Function to update the outputted UI display
    def _update_ui(self):
        pass

    # Function to perform a move on the board
    def _move(self, action):
        pass


player1 = ChessAgent()
player2 = ChessAgent()
game = ChessGame(player1, player2)

if __name__ == "__main__":
    # Initialising the Players and the Game
    player1 = ChessAgent()
    player2 = ChessAgent()
    game = ChessGame(player1, player2)

    # Running the Game until Closed
    running = True
    while running:
        # Closing the Game if Closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
