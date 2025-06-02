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
            return x < bx
        elif direction == "left":
            return x > bx


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
        self.blockerLocations = {"moveNmb": None, "forward": None}


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
