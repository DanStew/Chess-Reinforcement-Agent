import pygame
from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess_game_popup import show_popup
import sys

# Initialising the PyGame environment
pygame.init()
clock = pygame.time.Clock()

# Defining the different colours used throughout the game
LIGHT = (240, 217, 181)
DARK = (105, 170, 75)
HIGHLIGHT = (255, 76, 78)
CURRENTHIGHIGHLIGHT = (205, 76, 78)


# Defining the Chess Game Environment
class ChessGameAI:
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
        # Tracking the selectedPieces, possible moves and the highlighted
        self.currentPiece = None
        self.possibleMoves = []
        self.allPlayer1Moves = []
        self.calculatedAllPlayer1Moves = False
        self.allPlayer2Moves = []
        self.calculatedAllPlayer2Moves = False
        self.highlightedSquares = []
        # Initialising the piece id for the new game
        self.chessPieceId = 1
        # Creating the pieces for each player
        self.generateChessPieces(self.player1, 1)
        self.generateChessPieces(self.player2, 2)
        # Initialising whose turn it is to play
        self.playerTurn = self.player1
        # Keeping track of the moveNmb within the game
        self.moveNmb = 1
        # Displaying the initial chess board
        self._update_ui(True)

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
            pieceClass(x + 1, baseRow, color, self.chessPieceId + x, self.blockSize)
            for x, pieceClass in enumerate(piece_classes)
        ]
        self.chessPieceId += 7
        # Adding a Pawn Piece in every square of the Pawn Row
        chessPieces.extend(
            Pawn(i, pawnRow, color, self.chessPieceId + i, self.blockSize)
            for i in range(1, 9)
        )
        self.chessPieceId += 8

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
                rect = pygame.Rect(current_x, current_y, self.blockSize, self.blockSize)
                # Draw filled rectangle
                pygame.draw.rect(self.display, current_color, rect)

                # Draw black border
                pygame.draw.rect(self.display, (0, 0, 0), rect, width=1)
                # Moving across the screen for each square
                current_x += self.blockSize
            # Updating the position values for the next row
            current_y += self.blockSize
            current_x = 0

        pygame.display.update()  # Updating the screen to display the squares

    # Function to process an action on the board, and call the function to perform the move
    def play_step(self, action):
        # Processing pygame events, if any
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        oldLocation = action[0].location

        # Storing who the currently player was
        currentPlayer = self.playerTurn
        # Getting the player's pieces
        playerPieces = currentPlayer.chessPieces
        # Getting the opponents pieces
        opponentPieces = (
            self.player2.chessPieces
            if self.playerTurn == self.player1
            else self.player1.chessPieces
        )

        # Setting the chosen piece to be the current piece
        self.currentPiece = action[0]
        reward = self._move(action[1], opponentPieces)  # Performing the move

        player_score = self.calculateScore(
            currentPlayer
        )  # Calculating the player's score
        opposition_score = self.calculateScore(
            self.playerTurn
        )  # Calculating the oppositions score
        score = self.plus_prefix(player_score - opposition_score)

        # Calculating all the moves the opponent can now make
        opposition_moves = self.playerTurn.calculateAllPossibleMoves(
            True, currentPlayer, playerPieces
        )

        checkmate = (
            True
            if opposition_moves == []
            or opposition_score < 800
            or opposition_score == player_score
            and player_score == 1000
            else False
        )

        # Code to update the UI once the action has been made
        self._update_ui(False, oldLocation, action)

        # Returning the reward from the move, the player's current score and whether checkmate or not
        return reward, checkmate, score

    # Function to update the outputted UI display
    def _update_ui(self, resetGrid, old_location=None, action=None):
        # Resetting the display of the board
        if resetGrid:
            self.display.fill((255, 255, 255))
            self.displayInitialBoard()

            # Combining both players pieces into one array
            chessPieces = self.player1.chessPieces + self.player2.chessPieces
            # Looping through every chess piece and outputting them at their specified location
            for chessPiece in chessPieces:
                self.display.blit(
                    chessPiece.scaled_image,
                    (
                        (chessPiece.location[0] - 1) * self.blockSize + 4,
                        (chessPiece.location[1] - 1) * self.blockSize + 4,
                    ),
                )
        else:
            xo, yo = old_location
            xn, yn = action[1]
            # Draw a rectangle, or the correct color, at the original squares location
            color = LIGHT if (xo + yo) % 2 == 0 else DARK
            xPixel = (xo - 1) * self.blockSize
            yPixel = (yo - 1) * self.blockSize
            # Draw filled rectangle
            rect = pygame.Rect(xPixel, yPixel, self.blockSize, self.blockSize)
            pygame.draw.rect(self.display, color, rect)
            # Draw black border
            pygame.draw.rect(self.display, (0, 0, 0), rect, width=1)
            # Draw the image of the piece at the new location
            rect = pygame.Rect(
                (xn - 1) * self.blockSize,
                (yn - 1) * self.blockSize,
                self.blockSize,
                self.blockSize,
            )
            color = LIGHT if (xn + yn) % 2 == 0 else DARK
            pygame.draw.rect(self.display, color, rect)
            # Draw black border
            pygame.draw.rect(self.display, (0, 0, 0), rect, width=1)
            self.display.blit(
                action[0].scaled_image,
                (
                    (xn - 1) * self.blockSize + 4,
                    (yn - 1) * self.blockSize + 4,
                ),
            )

        # Updating the display to show the pieces
        pygame.display.update()

    # Function to perform a move on the board
    def _move(self, action, opponentPieces):
        # Initialising reward to be returned later
        reward = 0
        # Defining how much movement happened
        movement = (
            action[0] - self.currentPiece.location[0],
            action[1] - self.currentPiece.location[1],
        )
        self.currentPiece.location = action  # Moving the piece to the location'

        # If the current piece tracks self.moved and hasn't been moved yet, update it
        if (
            isinstance(self.currentPiece, (Pawn, Rook, King))
            and not self.currentPiece.moved
        ):
            self.currentPiece.moved = True

        # If the pawn reaches the final rank, allow the piece for promotion
        if isinstance(self.currentPiece, Pawn):
            final_rank = (
                1 if self.currentPiece.color == "white" else 8
            )  # Finding that pieces final rank
            if self.currentPiece.location[1] == final_rank:
                # Making sure they select a valid option, by continuously showing the popup
                choice = "Queen"
                self.promote_pawn(choice)  # Promoting the pawn

        # If the king makes a castling move, move the rook aswell to the correct place
        if isinstance(self.currentPiece, King):
            if movement == (-2, 0):
                # Queenside castling
                rook = [
                    piece
                    for piece in self.playerTurn.chessPieces
                    if isinstance(piece, Rook)
                    and piece.location[0] == self.currentPiece.location[0] - 2
                ][0]
                rook.location = (
                    self.currentPiece.location[0] + 1,
                    self.currentPiece.location[1],
                )
            elif movement == (2, 0):
                # Kingside castling
                rook = [
                    piece
                    for piece in self.playerTurn.chessPieces
                    if isinstance(piece, Rook)
                    and piece.location[0] == self.currentPiece.location[0] + 1
                ][0]
                rook.location = (
                    self.currentPiece.location[0] - 1,
                    self.currentPiece.location[1],
                )

        # Checking whether the move has captured any pieces
        for chessPiece in opponentPieces:
            # If action == chessPiece.location, the piece should be captured
            if action == chessPiece.location:
                # Capturing the piece (taking it off the board)
                opponentPieces.remove(chessPiece)
                # Outputting the scroe as a result of the capture
                player1Score = self.calculateScore(self.player1)
                player2Score = self.calculateScore(self.player2)
                player1Diff = self.plus_prefix(player1Score - player2Score)
                player2Diff = self.plus_prefix(player2Score - player1Score)
                # Printing out the differences
                print(
                    "Player 1 : "
                    + str(player1Diff)
                    + ", Player 2 : "
                    + str(player2Diff)
                )
                reward = chessPiece.value

        # Resetting some of the environment attributes
        self.currentPiece = None
        self.possibleMoves = []
        self.calculatedAllPlayer1Moves = False
        self.calculatedAllPlayer2Moves = False
        self.highlightedSquares = []
        # Changing whose turn it is to play
        self.playerTurn = (
            self.player1 if self.playerTurn != self.player1 else self.player2
        )
        self.moveNmb += 1

        return reward

    # Function to calculate a players score
    def calculateScore(self, player):
        score = 0
        for piece in player.chessPieces:
            score += piece.value
        return score

    # Function to correctly format the outputted scores
    def plus_prefix(self, val):
        if val > 0:
            return "+" + str(val)
        return val

    # Allowing the user for Pawn Promotion, given the option they select
    def promote_pawn(self, piece_name):
        x, y = self.currentPiece.location
        color = self.currentPiece.color

        piece_classes = {
            "Queen": Queen,
            "Knight": Knight,
            "Rook": Rook,
            "Bishop": Bishop,
        }

        # Creating the new piece
        new_piece = piece_classes[piece_name](
            x, y, color, self.chessPieceId, self.blockSize
        )
        self.chessPieceId += 1

        # Replace the pawn with the new piece
        self.playerTurn.chessPieces.remove(self.currentPiece)
        self.playerTurn.chessPieces.append(new_piece)

    # Using pygame clock to limit amount of actions
    def getClock(self):
        return clock

    # Function to ensure that all the games events have been processed
    def ensureProcessedEvents(self):
        # Processing pygame events, if any
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
