import pygame


# Classes to create the Chess Pieces
class ChessPiece:
    def __init__(self, x, y, color, id):
        self.id = id
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
    def checkBlockerLocations(self, gamePieces):
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

    # Function to use the Blocker Locations to define whether a move is blocked or not
    # Returns True or False, as to whether the move is blocked or not
    def checkBlockedMove(self, move_location, direction):

        # If there is no blocker, move can't be blocked
        if self.blockerLocations[direction] == None:
            return False

        # Shouldn't happen but if move location == self.location, quit
        if move_location == self.location:
            return True

        if (
            move_location == self.blockerLocations[direction]
            and type(self) == Pawn
            and direction == "forward"
        ):
            return True

        ax, ay = self.location
        kx, ky = move_location
        bx, by = self.blockerLocations[direction]

        dx, dy = kx - ax, ky - ay

        # Normalize direction to unit step
        def sign(n):
            return (n > 0) - (n < 0)

        step_x = sign(dx)
        step_y = sign(dy)

        # Build path from attacker to target
        cx, cy = ax + step_x, ay + step_y
        while (cx, cy) != (kx, ky):
            # If the blocker location is identified within the path, attack blocked
            if (cx, cy) == (bx, by):
                return True
            cx += step_x
            cy += step_y

        return False

    # Function to remove a blocker location, to simulate that location being attacked
    def checkForBlocker(self, attackLocation):
        # Looping through all the directions we want to identify blockers for
        for direction in list(self.blockerLocations.keys())[1:]:
            if self.blockerLocations[direction] == attackLocation:
                return True

    # Function to get any additional special moves a piece could make
    # This function is overridden for classes which have special moves that they can make
    def getSpecialMoves(self, playerPieces, opponentPieces):
        return []


class Pawn(ChessPiece):
    def __init__(self, x, y, color, id):
        super().__init__(x, y, color, id)
        # Setting the image of the piece, to be displayed to the screen
        self.imageSrc = (
            "./images/pawn.png" if self.color == "white" else "./images/pawnBlack.png"
        )
        self.image = pygame.image.load(self.imageSrc).convert_alpha()
        # Defining the actions a pawn can make
        # NOTE : En Passant isn't included within the initial actions
        self.actions = [(0, 1)]
        # Defining the locations of the blockers for the pawn
        self.blockerLocations = {
            "moveNmb": None,
            "forward": None,
            "forwardRight": None,
            "forwardLeft": None,
        }
        # Defining whether the piece has been moved or not
        self.moved = False
        # Defining the pieces value
        self.value = 1
        # Defining the index of the piece within the piece location tensor
        self.tensor_idx = 0 if self.color == "white" else 6

    # Function to add any special moves for the Pawn
    def getSpecialMoves(self, playerPieces, opponentPieces):
        specialMoves = []

        # Pawn First Move
        if not self.moved:
            specialMoves.append((0, 2))

        # Pawn Captures
        x, y = self.location
        forwardRight = (x + 1, y + 1) if self.color == "black" else (x + 1, y - 1)
        forwardLeft = (x - 1, y + 1) if self.color == "black" else (x - 1, y - 1)
        for piece in opponentPieces:
            if forwardRight == piece.location:
                if self.color == "white":
                    specialMoves.append((-1, 1))
                else:
                    specialMoves.append((1, 1))
            if forwardLeft == piece.location:
                if self.color == "white":
                    specialMoves.append((1, 1))
                else:
                    specialMoves.append((-1, 1))

        return specialMoves


class Knight(ChessPiece):
    def __init__(self, x, y, color, id):
        super().__init__(x, y, color, id)
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
        # Defining the pieces value
        self.value = 3
        # Defining the index of the piece within the piece location tensor
        self.tensor_idx = 1 if self.color == "white" else 7


class Bishop(ChessPiece):
    def __init__(self, x, y, color, id):
        super().__init__(x, y, color, id)
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
        # Defining the pieces value
        self.value = 3
        # Defining the index of the piece within the piece location tensor
        self.tensor_idx = 2 if self.color == "white" else 8


class Rook(ChessPiece):
    def __init__(self, x, y, color, id):
        super().__init__(x, y, color, id)
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
        # Defining whether the piece has been moved or not
        self.moved = False
        # Defining the pieces value
        self.value = 5
        # Defining the index of the piece within the piece location tensor
        self.tensor_idx = 3 if self.color == "white" else 9


class Queen(ChessPiece):
    def __init__(self, x, y, color, id):
        super().__init__(x, y, color, id)
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
        # Defining the pieces value
        self.value = 10
        # Defining the index of the piece within the piece location tensor
        self.tensor_idx = 4 if self.color == "white" else 10


class King(ChessPiece):
    def __init__(self, x, y, color, id):
        super().__init__(x, y, color, id)
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
        # Defining whether the piece has been moved or not
        self.moved = False
        # Defining the pieces value
        self.value = 1000
        # Defining the index of the piece within the piece location tensor
        self.tensor_idx = 5 if self.color == "white" else 11

    # Function to find ALL the possible moves the player could make
    def calculateAllPossibleMoves(self, playerPieces, opponentPieces):
        allPossibleMoves = []

        # Looping through every user piece and identifying their moves
        for piece in playerPieces:
            allPossibleMoves += self.identifyPossibleMoves(
                piece, playerPieces, opponentPieces
            )

        return allPossibleMoves

    # Function to identify the possible moves a piece can make
    def identifyPossibleMoves(self, piece, playerPieces, opponentPieces):
        possibleMoves = []
        if isinstance(piece, King):
            allPieceActions = piece.actions
        else:
            allPieceActions = piece.actions + piece.getSpecialMoves(
                playerPieces, opponentPieces
            )
        for action in allPieceActions:
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
                        piece.checkBlockerLocations(playerPieces + opponentPieces)
                        # Calculating the direction of the current action
                        tempAction = action
                        # Reverting back the action, so we can determine the correct way the piece is moving
                        if piece.color == "white":
                            tempAction = (tempAction[0] * -1, tempAction[1] * -1)
                        direction = piece.getDirectionFromAction(tempAction)
                        # Determining whether the move is blocked or not
                        blocked = piece.checkBlockedMove(new_pos, direction)
                        # If the move is blocked, move to the next action
                        if blocked:
                            continue
                    # If no blockers, add the move to possible moves
                    possibleMoves.append([piece, new_pos])
        return possibleMoves

    # Function to check a specific position and whether it's being attacked or not
    # Function to identify all the moves that attack a specified location (usually used for the king)
    def identifyAttacksOnLocation(self, allActions, location):
        for action in allActions:
            # If the actions location matches the king's location, it means that that piece can attack the king
            if action[1] == location:
                return True
        return False

    # Function to add any special moves for the King
    def getSpecialMoves(self, playerPieces, opponentPieces):
        specialMoves = []

        # If king has already moved, no castling possible
        if self.moved:
            return specialMoves

        # Find all rooks of the same color
        rooks = [
            piece
            for piece in playerPieces
            if isinstance(piece, Rook) and piece.color == self.color
        ]

        # Check for castling conditions
        for rook in rooks:
            if not rook.moved:
                # Determine direction of castling
                if rook.location[0] > self.location[0]:  # Kingside castling
                    if (
                        rook.location[0] == self.location[0] + 3
                    ):  # Standard kingside position
                        # Check if squares between king and rook are empty, on the players side
                        if (self.location[0] + 1, self.location[1]) not in [
                            p.location for p in playerPieces + opponentPieces
                        ] and (self.location[0] + 2, self.location[1]) not in [
                            p.location for p in playerPieces + opponentPieces
                        ]:
                            # Checking whether any of the spaces are being attacked or not
                            opposingActions = self.calculateAllPossibleMoves(
                                opponentPieces, playerPieces
                            )
                            if self.identifyAttacksOnLocation(
                                opposingActions,
                                (self.location[0] + 1, self.location[1]),
                            ) or self.identifyAttacksOnLocation(
                                opposingActions,
                                (self.location[0] + 2, self.location[1]),
                            ):
                                continue
                            if self.color == "white":
                                specialMoves.append((-2, 0))  # Kingside castling move
                            else:
                                specialMoves.append((2, 0))
                else:  # Queenside castling
                    if (
                        rook.location[0] == self.location[0] - 4
                    ):  # Standard queenside position
                        # Check if squares between king and rook are empty
                        if (
                            (self.location[0] - 1, self.location[1])
                            not in [p.location for p in playerPieces + opponentPieces]
                            and (self.location[0] - 2, self.location[1])
                            not in [p.location for p in playerPieces + opponentPieces]
                            and (self.location[0] - 3, self.location[1])
                            not in [p.location for p in playerPieces + opponentPieces]
                        ):
                            opposingActions = self.calculateAllPossibleMoves(
                                opponentPieces, playerPieces
                            )
                            if self.identifyAttacksOnLocation(
                                opposingActions,
                                (self.location[0] - 1, self.location[1]),
                            ) or self.identifyAttacksOnLocation(
                                opposingActions,
                                (self.location[0] - 2, self.location[1]),
                            ):
                                continue
                            if self.color == "white":
                                specialMoves.append((2, 0))  # Queenside castling move
                            else:
                                specialMoves.append((-2, 0))

        return specialMoves
