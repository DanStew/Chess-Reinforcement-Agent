from chess_game_environment import ChessGameAI


class ChessAgent:
    def __init__(self):
        self.n_games = 0
        self.chessPieces = []

    # Function to get the agent's state
    def get_state(self):
        pass

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


# Function to train the chess agents
def train():
    # Making the Agents and the Environment
    player1 = ChessAgent()
    player2 = ChessAgent()
    game = ChessGameAI(player1, player2)

    while True:
        old_state = game.playerTurn.get_state()
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
