import pygame
from chess_game_agent import ChessAgent

# Initialising the PyGame environment
pygame.init()


# Classes to create the Chess Pieces
class ChessPiece:
    def __init__(self, x, y, color):
        self.location = (x, y)  # The location of the chess piece (1-8)
        self.color = color  # Defining the color of the piece
        self.actions = []


class Pawn(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/pawn.png" if self.color == "white" else "./images/pawnBlack.png"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        # Defining the actions a pawn can make
        # NOTE : En Passant isn't included within the initial actions
        self.actions = [[0, 1]]


class Rook(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.moved = False  # Used to check for possible castle
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/rook.png" if self.color == "white" else "./images/rookBlack.png"
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
        super().__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/knight.png"
            if self.color == "white"
            else "./images/knightBlack.png"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        # Defining the actions a rook can make
        self.actions = [
            [x, y] for x in [-2, -1, 1, 2] for y in [-2, -1, 1, 2] if abs(x) != abs(y)
        ]


class Bishop(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/bishop.png"
            if self.color == "white"
            else "./images/bishopBlack.png"
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
        super().__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/queen.png" if self.color == "white" else "./images/queenBlack.png"
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
        super().__init__(x, y, color)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/king.png" if self.color == "white" else "./images/kingBlack.png"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        self.moved = False  # Used to check for possible Castle
        # Defining the actions a rook can make
        self.actions = [
            [x, y] for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == 0 and y == 0)
        ]


# Defining the different colours used throughout the game
LIGHT = (240, 217, 181)
DARK = (105, 170, 75)
HIGHLIGHT = (255, 239, 160)
CURRENTHIGHIGHLIGHT = (250, 250, 210)


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
        # Tracking the selectedPieces and the highlighted sqaures
        self.currentPiece = None
        self.highlightedSquares = []
        # Initialising the state of the game
        self.reset()

    # Function to reset the environment
    def reset(self):
        # Creating the pieces for each player
        self.generateChessPieces(player1, 1)
        self.generateChessPieces(player2, 2)
        # Initialising whose turn it is to play
        self.playerTurn = player2
        # Displaying the initial chess board
        self.displayInitialBoard()

    # Code to generate the chess pieces for each player, and assign them to the player
    def generateChessPieces(self, player, playerNmb):
        # Determing the rows which the pieces will initially be located
        if playerNmb == 1:
            baseRow = 8
            pawnRow = 7
            color = "white"
        else:
            baseRow = 1
            pawnRow = 2
            color = "black"

        # Defining the order of Pieces in the base row
        piece_classes = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        # Creating all of the Pieces, at the correct locations
        chessPieces = [
            pieceClass(x + 1, baseRow, color)
            for x, pieceClass in enumerate(piece_classes)
        ]
        # Adding a Pawn Piece in every square of the Pawn Row
        chessPieces.extend(Pawn(i, pawnRow, color) for i in range(1, 9))

        player.chessPieces = chessPieces

    # Code to display the initial board to the screen
    def displayInitialBoard(self):
        # The code to display the board background (the squares) is below
        current_x = 0
        current_y = 0
        # Looping through all the rows and columns of the board
        for i in range(0, 8):
            for j in range(0, 8):
                # Determining the color of the square
                # (i+j) % 2 == 0 can be used to determine whether the square is white or black, on a chess board
                current_color = LIGHT if (i + j) % 2 == 0 else DARK
                # Drawing the square to the screen
                pygame.draw.rect(
                    self.display,
                    current_color,
                    (current_x, current_y, self.blockSize, self.blockSize),
                )
                # Moving across the screen for each square
                current_x += self.blockSize
            # Updating the position values for the next row
            current_y += self.blockSize
            current_x = 0

        pygame.display.update()  # Updating the screen to display the squares drawn

        # The _update_ui() function is called to display the chess pieces to the screen
        self._update_ui()

    # Function to process an action on the board, and call the function to perform the move
    def play_step(self, click):
        # Converting the pixel number where the user has pressed into a position on the grid (1,1) --> (8,8)
        (x, y) = (click[0] // self.blockSize + 1, click[1] // self.blockSize + 1)
        # Getting the player's turn pieces
        playerPieces = self.playerTurn.chessPieces
        # Finding out if the player has pressed any of their own pieces
        for chessPiece in playerPieces:
            if chessPiece.location == (x, y):
                if self.currentPiece != chessPiece:
                    # If another piece was previously selected, revert its colour
                    if self.currentPiece is not None:
                        self.resetBoardDisplay()
                    # Marking the current piece as highlighted
                    self.currentPiece = chessPiece
                    self.changeGridSpaceColor(chessPiece.location, CURRENTHIGHIGHLIGHT)
                    self.highlightedSquares.append(chessPiece)
                else:
                    # Deselecting the current piece, and reverting its color
                    self.currentPiece = None
                    self.resetBoardDisplay()
                break
        # Code to update the UI once the action has been made
        self._update_ui()

    # Function to change the color of a rectangle at a positon in the chess grid to a specific colour
    def changeGridSpaceColor(self, gridSpace, color):
        pygame.draw.rect(
            self.display,
            color,
            (
                (gridSpace[0] - 1) * self.blockSize,
                (gridSpace[1] - 1) * self.blockSize,
                self.blockSize,
                self.blockSize,
            ),
        )

    # Function to revert all highlighted squares back to default
    def resetBoardDisplay(self):
        # Looping through all the highlighted squares
        for piece in self.highlightedSquares:
            # Resetting back to their original color
            newColor = (
                LIGHT if (piece.location[0] + piece.location[1]) % 2 == 0 else DARK
            )
            self.changeGridSpaceColor(piece.location, newColor)
            # Removing the square from highlighted squares
            self.highlightedSquares.remove(piece)

    # Function to update the outputted UI display
    def _update_ui(self):
        # Combining both players pieces into one array
        chessPieces = player1.chessPieces + player2.chessPieces
        # Looping through every chess piece and outputting them at their specified location
        for chessPiece in chessPieces:
            scaled_image = pygame.transform.scale(
                chessPiece.image, (self.blockSize - 8, self.blockSize - 8)
            )
            self.display.blit(
                scaled_image,
                (
                    (chessPiece.location[0] - 1) * self.blockSize + 4,
                    (chessPiece.location[1] - 1) * self.blockSize + 4,
                ),
            )
        # Updating the display to show the pieces
        pygame.display.update()

    # Function to perform a move on the board
    def _move(self, action):
        pass


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
            # Processing if the user presses any button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                game.play_step(
                    mouse_pos
                )  # Giving the play_step function where the user has pressed
    pygame.quit()
