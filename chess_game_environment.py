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
        self.blockerLocations = {}  # Initialising this, but implemented elsewhere
        # Defining the directions you would need to check for blockers
        # If white pieces, the values would need to be multiplied by -1 before moving
        self.blockerMovementLocations = {
            "forward": (0, 1),
            "backward": (0, -1),
            "left": (-1, 0),
            "right": (1, 0),
            "forwardRight": (1, 1),
            "forwardLeft": (-1, 1),
            "backwardRight": (1, -1),
            "backwardLeft": (-1, -1),
        }

    # Function to check for the blocker locations from the current piece
    def checkBlockerLocations(self, gamePieces, moveNmb):
        # If the moveNmb hasn't changed from the last time the blockers were calculated, return as blockers remain the same
        if self.blockerLocations["moveNmb"] == moveNmb:
            return
        # Looping through all the directions we want to identify blockers for
        for direction in list(self.blockerLocations.keys())[1:]:
            # Finding out the direction we need to move in
            movementDirection = self.blockerMovementLocations[direction]
            # Multiplying the direction by -1 if piece color is white
            if self.color == "white":
                movementDirection = (
                    movementDirection[0] * -1,
                    movementDirection[1] * -1,
                )
            currentLocation = self.location
            blockerFound = False
            # While we are within the board
            while (
                1 <= currentLocation[0] <= 8
                and 1 <= currentLocation[1] <= 8
                and blockerFound == False
            ):
                # Move in the direction we are aiming to check for blockers
                currentLocation = (
                    currentLocation[0] + movementDirection[0],
                    currentLocation[1] + movementDirection[1],
                )
                # If any gamePiece is at the current postion
                if not all(pPiece.location != currentLocation for pPiece in gamePieces):
                    # Set blockerFound to true and store the blocker location
                    blockerFound = True
                    self.blockerLocations[direction] = currentLocation
            # If no blockers found, set block in that direction to None
            if blockerFound == False:
                self.blockerLocations[direction] = None

    # Function to use the Blocker Locations to define whether a move is blocked or not
    # Returns True or False, as to whether the move is blocked or not
    def checkBlockedMove(self, move_location, direction):
        # If there is no blocker, move can't be blocked
        if self.blockerLocations[direction] == None:
            return False

        # Making move_location and the blocker into easier to use variables
        x, y = move_location
        bx, by = self.blockerLocations[direction]

        # Checking if the blocker interferes with the move
        # Implements the logic to return True or False as to whether piece is blocked or not
        if "forward" in direction:
            return (self.color == "white" and y < by) or (
                self.color == "black" and y > by
            )
        elif "backward" in direction:
            return (self.color == "white" and y > by) or (
                self.color == "black" and y < by
            )
        elif direction == "right":
            return x > bx
        elif direction == "left":
            return x < bx


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
        self.actions = [(0, 1)]
        # Defining the locations of the blockers for the pawn
        self.blockerLocations = {"moveNmb": None, "forward": None}


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
            [(i, 0) for i in range(1, 8)]  # Right
            + [(0, i) for i in range(1, 8)]  # Up
            + [(-i, 0) for i in range(1, 8)]  # Left
            + [(0, -i) for i in range(1, 8)]  # Down
        )
        # Defining the locations of the blockers for the rook
        self.blockerLocations = {
            "moveNmb": None,
            "forward": None,
            "backward": None,
            "left": None,
            "right": None,
        }


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
            (x, y) for x in [-2, -1, 1, 2] for y in [-2, -1, 1, 2] if abs(x) != abs(y)
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
            [(i, i) for i in range(1, 8)]  # Up and Right
            + [(i, -i) for i in range(1, 8)]  # Down and Right
            + [(-i, i) for i in range(1, 8)]  # Up and Left
            + [(-i, -i) for i in range(1, 8)]  # Down and Left
        )
        # Defining the locations of the blockers for the rook
        self.blockerLocations = {
            "moveNmb": None,
            "forwardRight": None,
            "forwardLeft": None,
            "backwardRight": None,
            "backwardLeft": None,
        }


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
            [(i, i) for i in range(1, 8)]
            + [(i, -i) for i in range(1, 8)]
            + [(-i, i) for i in range(1, 8)]
            + [(-i, -i) for i in range(1, 8)]
            + [(i, 0) for i in range(1, 8)]
            + [(0, i) for i in range(1, 8)]
            + [(-i, 0) for i in range(1, 8)]
            + [(0, -i) for i in range(1, 8)]
        )
        # Defining the locations of the blockers for the rook
        self.blockerLocations = {
            "moveNmb": None,
            "forward": None,
            "backward": None,
            "left": None,
            "right": None,
            "forwardRight": None,
            "forwardLeft": None,
            "backwardRight": None,
            "backwardLeft": None,
        }


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
            (x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == 0 and y == 0)
        ]
        # Defining the locations of the blockers for the rook
        self.blockerLocations = {
            "moveNmb": None,
            "forward": None,
            "backward": None,
            "left": None,
            "right": None,
            "forwardRight": None,
            "forwardLeft": None,
            "backwardRight": None,
            "backwardLeft": None,
        }


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
        # Tracking the selectedPieces, possible moves and the highlighted sqaures
        self.currentPiece = None
        self.possibleMoves = []
        self.highlightedSquares = []
        # Initialising the state of the game
        self.reset()

    # Function to reset the environment
    def reset(self):
        # Creating the pieces for each player
        self.generateChessPieces(player1, 1)
        self.generateChessPieces(player2, 2)
        # Initialising whose turn it is to play
        self.playerTurn = player1
        # Keeping track of the moveNmb within the game
        self.moveNmb = 1
        # Displaying the initial chess board
        self._update_ui()

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
        # Storing the old value of self.currentPiece, so we can check if it has changed or not
        old_piece = self.currentPiece
        # Converting the pixel number where the user has pressed into a position on the grid (1,1) --> (8,8)
        (x, y) = (click[0] // self.blockSize + 1, click[1] // self.blockSize + 1)
        # Getting the player's turn pieces
        playerPieces = self.playerTurn.chessPieces
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
            self.identifyPossibleMoves(self.currentPiece, playerPieces)

        # Finding out if the player has pressed any valid move locations
        for location in self.possibleMoves:
            # If the location pressed is a valid move, move to the location
            if location == (x, y):
                self._move(location)

        # Code to update the UI once the action has been made
        self._update_ui()

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
                    # If no blockers, mark move as possible and highlight it
                    self.possibleMoves.append(new_pos)
                    self.highlightedSquares.append(new_pos)
                    self.changeGridSpaceColor(new_pos, HIGHLIGHT)

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
    def _update_ui(self):
        # Resetting the display of the board
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
    def _move(self, action):
        self.currentPiece.location = action  # Moving the piece to the location


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
