from chess_game_environment import ChessGameAI
from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King
import numpy as np


class ChessAgent:
    def __init__(self):
        self.n_games = 0
        self.chessPieces = []

    # Function to get the agent's state
    def get_state(self, opponent):
        # Calculating all the moves of yourself and your opponent
        opponent_moves = opponent.calculateAllPossibleMoves(
            False, self, self.chessPieces
        )
        # Making a tensor for the position of all the pieces on the board
        piece_position_tensor = self.calculatePiecePositionTensor(
            self.chessPieces + opponent.chessPieces
        )
        # Finding out all the squares which your opponent could attack (8x8 array)
        vulnerable_squares = self.calculateVulnerableSquares(opponent_moves)
        # Making the array into a tensor, so I can combine it with the other tensor
        vulnerable_squares_plane = np.expand_dims(vulnerable_squares, axis=0)

        return np.concatenate([piece_position_tensor, vulnerable_squares_plane], axis=0)

    # Function to get a move from a state
    def get_move(self, state):
        pass

    # Function to append informations to the agent's memory
    def remember(self, old_state, final_move, reward, new_state, checkmate):
        pass

    # Function to train the agent's short memory
    def train_short_memory(self, old_state, final_move, reward, new_state, checkmate):
        pass

    # Function to train the agent's long memory
    def train_long_memory(self):
        pass

    # Function to make the Piece Position Tensor, to describe the position of all the pieces
    def calculatePiecePositionTensor(self, gamePieces):
        piece_position_tensor = np.zeros((12, 8, 8), dtype=np.int16)
        for piece in gamePieces:
            x, y = piece.location
            piece_position_tensor[piece.tensor_idx][y - 1][x - 1] = 1

        return piece_position_tensor

    # Function to make an array for all vulnerable squares
    def calculateVulnerableSquares(self, opponentMoves):
        vulnerableSquares = np.zeros((8, 8), dtype=np.int16)
        for move in opponentMoves:
            x, y = move[1]
            vulnerableSquares[y - 1][x - 1] = 1
        return vulnerableSquares

    # Function to find ALL the possible moves the player could make
    def calculateAllPossibleMoves(self, checkmateCheck, opponent, opponentPieces=None):
        allPossibleMoves = []
        kingLocation = ()  # Location of the king
        king = None  # Will store the users king, when found

        # Looping through every user piece and identifying their moves
        for piece in self.chessPieces:
            allPossibleMoves += self.identifyPossibleMoves(
                piece, self.chessPieces, opponentPieces
            )
            # This is used within checkmate check, if required
            if type(piece) == King:
                kingLocation = piece.location
                king = piece

        # If checkmateCheck, then we need to apply the checking for checkmate
        if checkmateCheck:
            kingAttacks = self.identifyAttacksOnLocation(opponent, kingLocation)

            # If there are any pieces that can attack the king
            if len(kingAttacks) > 0:
                # Iterating over a copy of allPossibleMoves, so we can remove actions without affecting the for loop
                for action in allPossibleMoves[:]:
                    if len(allPossibleMoves) == 0:
                        break
                    # For every action that involves the king
                    if action[0] == king:
                        # If the king's move still leads to the king attacked, pop it from the list
                        if (
                            len(self.identifyAttacksOnLocation(opponent, action[1]))
                            != 0
                        ):
                            allPossibleMoves.remove(action)
                        # Checking whether any of the opponents pieces has the action as a blocker
                        elif self.checkOpponentBlockers(opponentPieces, action[1]):
                            allPossibleMoves.remove(action)
                    # Only applying the blocker checks if there is only one piece attacking the king
                    elif len(kingAttacks) == 1:
                        if not self.blockedMove(
                            kingLocation, kingAttacks[0], action[1]
                        ):
                            allPossibleMoves.remove(action)

        return allPossibleMoves

    # Function to identify the possible moves a piece can make
    def identifyPossibleMoves(self, piece, playerPieces, opponentPieces):
        possibleMoves = []
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

    # Function to identify all the moves that attack a specified location (usually used for the king)
    def identifyAttacksOnLocation(self, opponent, location):
        # Getting a list of all the opponents actions
        actionsToCheck = opponent.calculateAllPossibleMoves(
            False, self, self.chessPieces
        )

        attackingPieces = []  # Defining list of all pieces directly attacking the king
        for action in actionsToCheck:
            # If the actions location matches the king's location, it means that that piece can attack the king
            if action[1] == location:
                attackingPieces.append(action[0].location)

        return attackingPieces  # Returning all pieces that can attack the king

    # Function which checks whether an opponents piece has a location as a blocker, as whether it would be able to attack that location or not
    def checkOpponentBlockers(self, opponentPieces, location):
        # Going through all the opponents pieces
        for piece in opponentPieces:
            # Checking if a blocker exists at the location we are checking for
            blockerExists = piece.checkForBlocker(location)
            if blockerExists:
                # Checking whether any of the piece's moves could reach the location, if the blocker didn't exist
                for move in piece.actions:
                    new_pos = (piece.location[0] + move[0], piece.location[1] + move[1])
                    if new_pos == location:
                        # If it could, return True
                        return True
        return False

    def blockedMove(self, location, attackerLocation, blockerLocation):
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


# Function to train the chess agents
def train():
    # Making the Agents and the Environment
    player1 = ChessAgent()
    player2 = ChessAgent()
    game = ChessGameAI(player1, player2)

    while True:
        opponent = player2 if game.playerTurn == player1 else player1
        old_state = game.playerTurn.get_state(opponent)
        final_move = game.playerTurn.get_move(old_state)
        reward, checkmate, score = game.play_step(final_move)
        new_state = game.playerTurn.get_state()

        # Training the short memory
        game.playerTurn.train_short_memory(
            old_state, final_move, reward, new_state, checkmate
        )

        # Remember this information
        game.playerTurn.remember(old_state, final_move, reward, new_state, checkmate)

        # If the agent has checkmated the opponent
        if checkmate:
            game.reset()
            player1.n_games += 1
            player2.n_games += 1
            game.playerTurn.train_long_memory()


if __name__ == "__main__":
    print("Beginning ChessAgent Program")
    train()
