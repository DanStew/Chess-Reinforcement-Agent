import pygame
from chess_game_agent import ChessAgent
from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King

# Initialising the PyGame environment
pygame.init()

# Defining the different colours used throughout the game
LIGHT = (240, 217, 181)
DARK = (105, 170, 75)
HIGHLIGHT = (255, 76, 78)
CURRENTHIGHIGHLIGHT = (205, 76, 78)


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
        # Tracking the selectedPieces, possible moves and the highlighted sqaures
        self.currentPiece = None
        self.possibleMoves = []
        self.allPlayer1Moves = []
        self.calculatedAllPlayer1Moves = False
        self.allPlayer2Moves = []
        self.calulcatedAllPlayer2Moves = False
        self.highlightedSquares = []
        # Initialising the piece id for the new game
        self.chessPieceId = 1
        # Creating the pieces for each player
        self.generateChessPieces(player1, 1)
        self.generateChessPieces(player2, 2)
        # Initialising whose turn it is to play
        self.playerTurn = player1
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
            pieceClass(x + 1, baseRow, color, self.chessPieceId + x)
            for x, pieceClass in enumerate(piece_classes)
        ]
        self.chessPieceId += 7
        # Adding a Pawn Piece in every square of the Pawn Row
        chessPieces.extend(
            Pawn(i, pawnRow, color, self.chessPieceId + i) for i in range(1, 9)
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
    def play_step(self, click):
        # Initialising resetGrid value to false, so grid isn't reset every time
        resetGrid = False
        # Storing the old value of self.currentPiece, so we can check if it has changed or not
        old_piece = self.currentPiece
        # Converting the pixel number where the user has pressed into a position on the grid (1,1) --> (8,8)
        (x, y) = (click[0] // self.blockSize + 1, click[1] // self.blockSize + 1)
        # Getting the player's turn pieces
        playerPieces = self.playerTurn.chessPieces
        # Getting the opponents pieces
        opponentPieces = (
            self.player2.chessPieces
            if self.playerTurn == player1
            else self.player1.chessPieces
        )

        # Calculating all the player's possible moves, if it hasn't been calculated already
        if not self.calculatedAllPlayer1Moves:
            if self.playerTurn == player1:
                self.allPlayer1Moves = self.calculateAllPossibleMoves(
                    "player1", playerPieces, True, opponentPieces
                )
            else:
                self.allPlayer2Moves = self.calculateAllPossibleMoves(
                    "player2", playerPieces, True, opponentPieces
                )

        # Finding out if the player has pressed any of their own pieces
        for chessPiece in playerPieces:
            if chessPiece.location == (x, y):
                if self.currentPiece != chessPiece:
                    self.resetBoardDisplay()
                    # Marking the current piece as highlighted
                    self.currentPiece = chessPiece
                    self.changeGridSpaceColor(chessPiece.location, CURRENTHIGHIGHLIGHT)
                    self.highlightedSquares.append(chessPiece.location)
                else:
                    # Deselecting the current piece, and reverting its color
                    self.currentPiece = None
                    self.resetBoardDisplay()
                break

        # If there is a currently selected piece, identify the moves that piece can make
        # This if statement is introduced to only call this when the currentPiece has changed
        if old_piece != self.currentPiece and self.currentPiece != None:
            self.possibleMoves = []  # Resetting possible moves
            allPossibleMoves = (
                self.allPlayer1Moves
                if self.playerTurn == player1
                else self.allPlayer2Moves
            )
            self.getPossibleMoves(self.currentPiece, allPossibleMoves)

        # Finding out if the player has pressed any valid move locations
        for location in self.possibleMoves:
            # If the location pressed is a valid move, move to the location
            if location == (x, y):
                self._move(location, opponentPieces)  # Performing the move
                resetGrid = True

        # Code to update the UI once the action has been made
        self._update_ui(resetGrid)

    # Function to find ALL the possible moves the player could make
    def calculateAllPossibleMoves(
        self, player, playerPieces, checkmateCheck, opponentPieces=None
    ):
        allPossibleMoves = []
        kingLocation = ()  # Location of the king
        king = None  # Will store the users king, when found

        # Looping through every user piece and identifying their moves
        for piece in playerPieces:
            allPossibleMoves += self.identifyPossibleMoves(piece, playerPieces)
            # This is used within checkmate check, if required
            if type(piece) == King:
                kingLocation = piece.location
                king = piece

        # If checkmateCheck, then we need to apply the checking for checkmate
        if checkmateCheck:
            opposingPlayer = "player1" if player != "player1" else "player2"
            kingAttacks = self.identifyAttacksOnLocation(opposingPlayer, kingLocation)

            # If there are any pieces that can attack the king
            if len(kingAttacks) > 0:
                # Iterating over a copy of allPossibleMoves, so we can remove actions without affecting the for loop
                for action in allPossibleMoves[:]:
                    # For every action that involves the king
                    if action[0] == king:
                        # If the king's move still leads to the king attacked, pop it from the list
                        if (
                            len(
                                self.identifyAttacksOnLocation(
                                    opposingPlayer, action[1]
                                )
                            )
                            != 0
                        ):
                            allPossibleMoves.remove(action)
                    # Only applying the blocker checks if there is only one piece attacking the king
                    elif len(kingAttacks) == 1:
                        if not self.blockedMove(
                            opposingPlayer, kingLocation, kingAttacks[0], action[1]
                        ):
                            allPossibleMoves.remove(action)

        if player == "player1":
            self.calculatedAllPlayer1Moves = True
        else:
            self.calculatedAllPlayer2Moves = True

        return allPossibleMoves

    # Function to identify all the moves that attack a specified location (usually used for the king)
    def identifyAttacksOnLocation(self, opposingPlayer, location):

        # If we haven't calculated all the opposing players moves yet, calculate them
        if opposingPlayer == "player1":
            if self.calculatedAllPlayer1Moves == False:
                self.allPlayer1Moves = self.calculateAllPossibleMoves(
                    "player1", player1.chessPieces, False, player2.chessPieces
                )
        else:
            if self.calulcatedAllPlayer2Moves == False:
                self.allPlayer2Moves = self.calculateAllPossibleMoves(
                    "player2", player2.chessPieces, False, player1.chessPieces
                )

        # Going through all the opposing players actions and seeing if any of them meet the kings locations
        actionsToCheck = (
            self.allPlayer1Moves
            if opposingPlayer == "player1"
            else self.allPlayer2Moves
        )

        attackingPieces = []  # Defining list of all pieces directly attacking the king
        for action in actionsToCheck:
            # If the actions location matches the king's location, it means that that piece can attack the king
            if action[1] == location:
                attackingPieces.append(action[0].location)

        return attackingPieces  # Returning all pieces that can attack the king

    def blockedMove(self, opposingPlayer, location, attackerLocation, blockerLocation):
        ax, ay = attackerLocation
        kx, ky = location
        bx, by = blockerLocation

        dx, dy = kx - ax, ky - ay

        # Normalize direction to unit step
        def sign(n):
            return (n > 0) - (n < 0)

        step_x = sign(dx)
        step_y = sign(dy)

        if blockerLocation == attackerLocation:
            return True  # Same square

        # Build path from attacker to target
        cx, cy = ax + step_x, ay + step_y
        while (cx, cy) != (kx, ky):
            # If the blocker location is identified within the path, attack blocked
            if (cx, cy) == (bx, by):
                return True
            cx += step_x
            cy += step_y

        return False

    # Function to change the color of a rectangle at a positon in the chess grid to a specific colour
    def changeGridSpaceColor(self, gridSpace, color):
        rect = pygame.Rect(
            (gridSpace[0] - 1) * self.blockSize,
            (gridSpace[1] - 1) * self.blockSize,
            self.blockSize,
            self.blockSize,
        )

        # Draw filled rectangle
        pygame.draw.rect(self.display, color, rect)

        # Draw black border
        pygame.draw.rect(self.display, (0, 0, 0), rect, width=1)

    # Function to revert all highlighted squares back to default
    def resetBoardDisplay(self):
        # Looping through all the highlighted squares
        for location in self.highlightedSquares:
            # Resetting back to their original color
            newColor = LIGHT if (location[0] + location[1]) % 2 == 0 else DARK
            self.changeGridSpaceColor(location, newColor)
            # Removing the square from highlighted squares
        self.highlightedSquares = []

    # Function to identify the possible moves a piece can make
    def identifyPossibleMoves(self, piece, playerPieces):

        possibleMoves = []
        for action in piece.actions:
            if piece.color == "white":
                # Multiplying the action by -1 as we are moving in the opposite direction, up the board
                action = (action[0] * -1, action[1] * -1)
            new_pos = (piece.location[0] + action[0], piece.location[1] + action[1])
            # Ensuring the (x,y) values are between 1 and 8
            if 1 <= new_pos[0] <= 8 and 1 <= new_pos[1] <= 8:
                # Ensuring that none of the player's pieces are located at the new moves location
                if all(pPiece.location != new_pos for pPiece in playerPieces):
                    # Implement the code to check for blockers here, and reject if necessary
                    # Not implementing checks for Knights, as they can't be blocked
                    if type(piece) != Knight:
                        # Calculating the blocker locations for the current piece
                        piece.checkBlockerLocations(
                            player1.chessPieces + player2.chessPieces, self.moveNmb
                        )
                        # Calculating the direction of the current action
                        tempAction = action
                        # Reverting back the action, so we can determine the correct way the piece is moving
                        if piece.color == "white":
                            tempAction = (tempAction[0] * -1, tempAction[1] * -1)
                        direction = self.getDirectionFromAction(tempAction)
                        # Determining whether the move is blocked or not
                        blocked = piece.checkBlockedMove(new_pos, direction)
                        # If the move is blocked, move to the next action
                        if blocked:
                            continue
                    # If no blockers, add the move to possible moves
                    possibleMoves.append([piece, new_pos])
        return possibleMoves

    # Function to get the current moves that a piece can make, given the piece and all the possible actions the player could make
    def getPossibleMoves(self, piece, allPossibleMoves):
        for move in allPossibleMoves:
            if move[0] == piece:
                self.possibleMoves.append(move[1])
                self.highlightedSquares.append(move[1])
                self.changeGridSpaceColor(move[1], HIGHLIGHT)

    # Function to calculate the direction you're going in, giving the action
    def getDirectionFromAction(self, action):
        direction = ""
        if action[1] > 0:
            direction = "forward"
        elif action[1] < 0:
            direction = "backward"
        if action[0] > 0:
            if direction == "":
                direction = "right"
            else:
                direction += "Right"
        elif action[0] < 0:
            if direction == "":
                direction = "left"
            else:
                direction += "Left"
        return direction

    # Function to update the outputted UI display
    def _update_ui(self, resetGrid):
        # Resetting the display of the board
        if resetGrid:
            self.display.fill((255, 255, 255))
            self.displayInitialBoard()

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
    def _move(self, action, opponentPieces):
        self.currentPiece.location = action  # Moving the piece to the location
        # Resetting some of the environment attributes
        self.currentPiece = None
        self.possibleMoves = []
        self.calculatedAllPlayer1Moves = False
        self.calculatedAllPlayer2Moves = False
        self.highlightedSquares = []
        # Changing whose turn it is to play
        self.playerTurn = player1 if self.playerTurn != player1 else player2
        self.moveNmb += 1

        # Checking whether the move has captured any pieces
        for chessPiece in opponentPieces:
            # If action == chessPiece.location, the piece should be captured
            if action == chessPiece.location:
                # Capturing the piece (taking it off the board)
                self.playerTurn.chessPieces.remove(chessPiece)


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
